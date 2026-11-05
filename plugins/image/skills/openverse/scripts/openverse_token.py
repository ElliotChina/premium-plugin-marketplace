#!/usr/bin/env python
"""Openverse access token 获取与自动刷新。

读取 OPENVERSE_CLIENT_ID / OPENVERSE_CLIENT_SECRET 环境变量，token 缓存于
~/.cache/openverse_token.json，临期或缺失时自动用 client 凭据换取新 token。
stdout 仅输出 token，可直接用于 shell 替换：
    export OPENVERSE_ACCESS_TOKEN="$(python scripts/openverse_token.py)"

注册 client 凭据（一次性）:
    curl -X POST https://api.openverse.org/v1/auth_tokens/register/ \\
      -H "Content-Type: application/json" \\
      -d '{"name": "my-project", "description": "用途", "email": "you@example.com"}'
"""
import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request

CACHE = pathlib.Path.home() / ".cache" / "openverse_token.json"
BUFFER = 300          # 提前 5 分钟视为过期
DEFAULT_VALIDITY = 43200  # API 返回 expires_in=43200（12 小时），响应缺失时兜底
TOKEN_URL = "https://api.openverse.org/v1/auth_tokens/token/"


def load_cached():
    """返回 (token, expires_at)，缓存损坏视为不存在。"""
    try:
        data = json.loads(CACHE.read_text())
        return data["access_token"], data["expires_at"]
    except Exception:
        return None, 0


def refresh(client_id: str, client_secret: str) -> str:
    body = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }).encode()
    # Openverse 拦截默认 UA（Python-urllib/3.x 返回 403），必须带自定义 User-Agent
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST", headers={
        "User-Agent": "openverse-token-refresh/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"Openverse token 刷新失败: {e}", file=sys.stderr)
        sys.exit(1)
    token = data.get("access_token")
    if not token:
        print(f"Openverse token 刷新失败: {data}", file=sys.stderr)
        sys.exit(1)
    expires_at = int(time.time() + data.get("expires_in", DEFAULT_VALIDITY))
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps({"access_token": token, "expires_at": expires_at}))
    CACHE.chmod(0o600)
    return token


def main() -> None:
    token, expires_at = load_cached()
    if token and time.time() < expires_at - BUFFER:
        print(token)
        return
    client_id = os.environ.get("OPENVERSE_CLIENT_ID")
    client_secret = os.environ.get("OPENVERSE_CLIENT_SECRET")
    if not client_id or not client_secret:
        print(
            "需配置 OPENVERSE_CLIENT_ID / OPENVERSE_CLIENT_SECRET（匿名额度足够时可不配置，"
            "见 SKILL.md 注册流程）",
            file=sys.stderr,
        )
        sys.exit(1)
    print(refresh(client_id, client_secret))


if __name__ == "__main__":
    main()
