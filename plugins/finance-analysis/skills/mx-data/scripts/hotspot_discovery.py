"""
OpenClaw stock_market_hotspot_discovery skill runtime.

This module is intentionally self-contained:
- No hard-coded user identity.
- Runtime defaults are defined in-code.
"""

import argparse
import asyncio
import json
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error as urllib_error
from urllib import request as urllib_request

_SCRIPTS_DIR = str(Path(__file__).resolve().parent)
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

from auth import ensure_auth, AUTH_OK, AUTH_NEED_USER, AUTH_ERROR

EM_BASE_URL = "https://ai-saas.eastmoney.com".rstrip("/")
EM_API_KEY_PLACEHOLDER = "{em" + "_api_key}"
EM_API_KEY = os.environ.get("EM_API_KEY", "").strip()

if EM_API_KEY and EM_API_KEY != EM_API_KEY_PLACEHOLDER:
    os.environ.setdefault("EM_API_KEY", EM_API_KEY)

AUTH_API_KEY_URL_FALLBACK = f"{EM_BASE_URL}/mxClaw"
DEFAULT_OUTPUT_DIR = Path.cwd() / "miaoxiang" / "stock_market_hotspot_discovery"
TIMEOUT_SECONDS = 60
HOTSPOT_DISCOVERY_URL = f"{EM_BASE_URL}/proxy/app-robo-advisor-api/assistant/hotspot-discovery"


def _load_em_api_key() -> str:
    """Load EM_API_KEY from the environment, built-in replacement, then ~/.mx-skills/em_api_key."""
    env_value = (os.environ.get("EM_API_KEY") or "").strip()
    if env_value:
        return env_value
    if EM_API_KEY and EM_API_KEY != EM_API_KEY_PLACEHOLDER:
        return EM_API_KEY
    key_path = Path.home() / ".mx-skills" / "em_api_key"
    if key_path.exists():
        return key_path.read_text(encoding="utf-8").strip()
    return ""


class _AuthRevoked(Exception):
    """EM_API_KEY was rejected by the service."""


def _clear_em_api_key_file() -> None:
    try:
        (Path.home() / ".mx-skills" / "em_api_key").unlink(missing_ok=True)
    except OSError:
        pass


def _handle_auth_revoked(reason: str, result: Dict[str, Any]) -> Dict[str, Any]:
    result.pop("remember_api_key", None)
    result.pop("api_key", None)
    _clear_em_api_key_file()
    env_key = os.environ.pop("EM_API_KEY", None)
    try:
        reauth = ensure_auth()
    finally:
        if env_key is not None:
            os.environ["EM_API_KEY"] = env_key
    if reauth["status"] == AUTH_NEED_USER:
        result["need_auth"] = True
        result["authUrl"] = reauth["auth_url"]
        result["apiKeyUrl"] = reauth["api_key_url"]
        result["auth_message"] = (
            "EM_API_KEY was revoked ({0}); a fresh authorization URL was created. "
            "Authorize and resend the original prompt.".format(reason)
        )
        if env_key and env_key.strip():
            result["auth_message"] += (
                " The EM_API_KEY environment variable still contains the revoked key; clear it first."
            )
    elif reauth["status"] == AUTH_OK:
        result["error"] = (
            "EM_API_KEY was rejected by the service, but the EM_API_KEY environment "
            "variable is still set. Clear it and resend the original prompt to reauthorize."
        )
    else:
        result["error"] = "Failed to create a fresh authorization URL: {0}".format(
            reauth.get("message", "unknown authorization error")
        )
    return result


def _extract_error_message(body: str) -> str:
    body = (body or "").strip()
    if not body:
        return ""
    try:
        data = json.loads(body)
    except Exception:
        return body[:200]
    if isinstance(data, dict):
        for key in ("msg", "message", "error", "stack"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return body[:200]


def _extract_content(raw: Dict[str, Any]) -> str:
    """
    Extract readable report content from API response.
    Supports:
    - data.displayData as str
    - data.displayData as list/dict
    - fallback to common textual fields
    """
    if not isinstance(raw, dict):
        return ""

    data = raw.get("data")
    if isinstance(data, dict):
        display_data = data.get("displayData")
        if isinstance(display_data, str) and display_data.strip():
            return display_data.strip()
        if isinstance(display_data, (list, dict)):
            return json.dumps(display_data, ensure_ascii=False, indent=2)

        for key in ("content", "answer", "summary"):
            value = data.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, (list, dict)):
                return json.dumps(value, ensure_ascii=False, indent=2)

    for key in ("displayData", "content", "answer", "summary"):
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, (list, dict)):
            return json.dumps(value, ensure_ascii=False, indent=2)

    return json.dumps(raw, ensure_ascii=False, indent=2)


def _has_valid_display_data(raw: Dict[str, Any]) -> bool:
    """
    Determine whether API response contains a valid report body.
    Used to avoid saving md files for unsupported/failed scenarios.
    """
    if not isinstance(raw, dict):
        return False

    code = raw.get("code")
    if code is not None and code != 200:
        return False

    status = raw.get("status")
    if isinstance(status, int) and status < 0:
        return False

    data = raw.get("data")
    if not isinstance(data, dict):
        return False

    display_data = data.get("displayData")
    if isinstance(display_data, str):
        return bool(display_data.strip())
    if isinstance(display_data, list):
        return len(display_data) > 0
    if isinstance(display_data, dict):
        return len(display_data) > 0

    return False


def _safe_id(value: Any) -> str:
    text = str(value).strip() if value is not None else ""
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", text or uuid.uuid4().hex)


def _save_source_trace_list(data: Dict[str, Any]) -> str:
    out_dir = Path.cwd() / "miaoxiang"
    out_dir.mkdir(parents=True, exist_ok=True)
    article_id = _safe_id(data.get("articleId"))
    path = out_dir / "sourceTrace_{0}.json".format(article_id)
    path.write_text(json.dumps(data.get("sourceTraceList"), ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _http_call_hotspot_discovery(question: str, api_key: str) -> Dict[str, Any]:
    payload = {"question": question, "needSourceTrace": True}
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib_request.Request(
        url=HOTSPOT_DISCOVERY_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "em_api_key": api_key,
        },
    )

    try:
        with urllib_request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw_body = resp.read().decode("utf-8", errors="replace")
    except urllib_error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        if exc.code in (401, 403):
            raise _AuthRevoked("HTTP {0}: {1}".format(exc.code, _extract_error_message(err_body) or err_body[:100]))
        message = _extract_error_message(err_body) or "http status {0}".format(exc.code)
        raise RuntimeError("Hotspot discovery API request failed: {0}".format(message))
    except urllib_error.URLError as exc:
        raise RuntimeError("Hotspot discovery API request failed: {0}".format(exc.reason))

    try:
        parsed = json.loads(raw_body)
    except json.JSONDecodeError:
        raise RuntimeError("Hotspot discovery API returned invalid JSON response.")

    if isinstance(parsed, dict):
        code = parsed.get("code")
        status = parsed.get("status")
        if code in (401, "401", 403, "403") or status in (401, "401", 403, "403"):
            raise _AuthRevoked("business auth rejected: code={0}, status={1}".format(code, status))
        return parsed
    return {"data": parsed}


async def discover_hotspot(
    question: str,
    output_dir: Optional[Path] = None,
    save_to_file: bool = True,
) -> Dict[str, Any]:
    question = (question or "").strip()
    if not question:
        return {
            "question": "",
            "content": "",
            "output_path": None,
            "raw": None,
            "source_trace_path": None,
            "error": "question is empty",
        }

    out_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)

    result = {
        "question": question,
        "content": "",
        "output_path": None,
        "raw": None,
        "source_trace_path": None,
    }

    auth = ensure_auth()
    if auth["status"] == AUTH_NEED_USER:
        result["need_auth"] = True
        result["authUrl"] = auth["auth_url"]
        result["apiKeyUrl"] = auth["api_key_url"]
        result["auth_message"] = (
            "Authorization is required. Prefer the QR URL; use apiKeyUrl as a backup. "
            "After authorization, resend the original prompt."
        )
        return result
    if auth["status"] == AUTH_ERROR:
        result["error"] = auth.get("message", "Authorization failed")
        return result

    newly_obtained_key = auth.get("api_key") if auth.get("newly_obtained") else None
    if newly_obtained_key:
        result["remember_api_key"] = True
        result["api_key"] = newly_obtained_key

    api_key = newly_obtained_key or _load_em_api_key()
    if not api_key:
        result["error"] = "EM_API_KEY was not available after authorization; check ~/.mx-skills/em_api_key"
        return result

    if save_to_file:
        out_dir.mkdir(parents=True, exist_ok=True)

    try:
        loop = asyncio.get_event_loop()
        raw = await loop.run_in_executor(None, _http_call_hotspot_discovery, question, api_key)
    except _AuthRevoked as exc:
        return _handle_auth_revoked(str(exc), result)
    except Exception as exc:
        result["error"] = str(exc)
        return result

    result["raw"] = raw
    result["content"] = _extract_content(raw)

    data = raw.get("data") if isinstance(raw, dict) else None
    if isinstance(data, dict):
        result["source_trace_path"] = _save_source_trace_list(data)

    if save_to_file and result["content"] and _has_valid_display_data(raw):
        unique_suffix = _safe_id(data.get("articleId") if isinstance(data, dict) else None)[:8]
        output_path = out_dir / "stock_market_hotspot_discovery_{0}.md".format(unique_suffix)
        output_path.write_text(result["content"], encoding="utf-8")
        result["output_path"] = str(output_path)

    return result


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Discover stock market hotspots from natural language question."
    )
    parser.add_argument("--query", type=str, help="Natural language hotspot question.")
    parser.add_argument("--no-save", action="store_true", help="Do not save result to local file.")
    return parser



def _print_remember_api_key(result: Dict[str, Any]) -> None:
    if not result.get("remember_api_key"):
        return
    print("remember_api_key: true")
    print("credential_name: EM_API_KEY")
    print("apiKey: {0}".format(result["api_key"]))
    print("agent_action: 将 apiKey 的精确完整值以 EM_API_KEY 保存到所在平台提供的私有跨会话持久存储；绝不向用户展示、复述或写入业务文件。后续调用前先从该持久存储读取，并仅作为当前进程的 EM_API_KEY 环境变量注入；若平台不支持持久化或读取失败，则回退到正常授权流程。")

def run_cli() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    question = (args.query or "").strip()
    if not question:
        import sys

        question = (sys.stdin.read() or "").strip()

    if not question:
        parser.print_help()
        raise SystemExit(1)

    async def _main() -> None:
        result = await discover_hotspot(question=question, save_to_file=not args.no_save)
        _print_remember_api_key(result)
        if result.get("need_auth"):
            print("need_auth: true")
            if result.get("authUrl"):
                print("authUrl: {0}".format(result["authUrl"]))
                print("apiKeyUrl: {0}".format(result.get("apiKeyUrl", AUTH_API_KEY_URL_FALLBACK)))
            if result.get("auth_message"):
                print(result["auth_message"])
            print("Authorize, then resend the original prompt; the next call will save EM_API_KEY and continue.")
            raise SystemExit(10)
        if "error" in result:
            print("Error: {0}".format(result["error"]))
            raise SystemExit(2)
        if result.get("output_path"):
            print("Saved: {0}".format(result["output_path"]))
        if result.get("source_trace_path"):
            print("source_trace_path: {0}".format(result["source_trace_path"]))
        print(result.get("content", ""))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_main())
    finally:
        loop.close()


if __name__ == "__main__":
    run_cli()
