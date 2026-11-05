#!/usr/bin/env python3
"""多来源图片聚合搜索 CLI。

一次并发搜索 Unsplash / Pexels / Pixabay / Wikimedia Commons / Openverse，
输出统一结构的 JSON 结果（含原图/预览 URL、尺寸、许可与署名信息），
可选按混排排名下载前 N 张到本地。

零配置来源（mediawiki / openverse）无需任何 Key；keyed 来源
（unsplash / pexels / pixabay）检测到对应环境变量才参与搜索，
缺失时记入 errors 并跳过，不会导致整体失败。

Examples:
    # 聚合搜索（零配置即可跑）
    python scripts/image_search.py "mountain lake" --orientation landscape

    # 只搜指定来源，每个来源取 8 条
    python scripts/image_search.py "office team" --providers pexels,unsplash --per-provider 8

    # 搜索并下载混排前 3 张
    python scripts/image_search.py "sunset" --download 3 -o images/
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
TIMEOUT = 30

KEYED_PROVIDERS = ("unsplash", "pexels", "pixabay")
ZERO_CONFIG_PROVIDERS = ("mediawiki", "openverse")
ALL_PROVIDERS = ZERO_CONFIG_PROVIDERS + KEYED_PROVIDERS

ORIENT_MAP = {
    # provider: {统一取值: provider 自己的取值}
    "unsplash": {"landscape": "landscape", "portrait": "portrait", "square": "squarish"},
    "pexels": {"landscape": "landscape", "portrait": "portrait", "square": "square"},
    "openverse": {"landscape": "wide", "portrait": "tall", "square": "square"},
}


def _get(url: str, params: dict | None = None, headers: dict | None = None) -> dict:
    resp = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _strip_html(text: str | None) -> str:
    """Wikimedia extmetadata 的 Artist/许可字段常含内联 HTML 链接，剥掉标签留纯文本。"""
    if not text:
        return ""
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


def _item(
    provider: str,
    *,
    id: str,
    title: str = "",
    author: str = "",
    width: int | None = None,
    height: int | None = None,
    url: str = "",
    preview: str = "",
    page_url: str = "",
    license: str = "",
    attribution: str = "",
    attribution_required: bool = False,
) -> dict:
    return {
        "provider": provider,
        "id": str(id),
        "title": title,
        "author": author,
        "width": width,
        "height": height,
        "pixels": (width or 0) * (height or 0) or None,
        "url": url,
        "preview": preview,
        "page_url": page_url,
        "license": license,
        "attribution": attribution,
        "attribution_required": attribution_required,
    }


# ---------------------------------------------------------------------------
# 各来源搜索（每个函数返回统一结构的 list[dict]）
# ---------------------------------------------------------------------------


def search_unsplash(query: str, per_provider: int, orientation: str) -> list[dict]:
    key = os.environ["UNSPLASH_ACCESS_KEY"]
    data = _get(
        "https://api.unsplash.com/search/photos",
        params={
            "query": query,
            "per_page": per_provider,
            **({"orientation": ORIENT_MAP["unsplash"][orientation]} if orientation in ORIENT_MAP["unsplash"] else {}),
        },
        headers={"Authorization": f"Client-ID {key}", "Accept-Version": "v1"},
    )
    return [
        _item(
            "unsplash",
            id=p["id"],
            title=p.get("alt_description") or p.get("description") or "",
            author=p.get("user", {}).get("name", ""),
            width=p.get("width"),
            height=p.get("height"),
            url=p.get("urls", {}).get("raw", ""),
            preview=p.get("urls", {}).get("small", ""),
            page_url=p.get("links", {}).get("html", ""),
            license="Unsplash License",
            attribution=f"Photo by {p.get('user', {}).get('name', '')} on Unsplash",
        )
        for p in data.get("results", [])
    ]


def search_pexels(query: str, per_provider: int, orientation: str) -> list[dict]:
    key = os.environ["PEXELS_API_KEY"]
    data = _get(
        "https://api.pexels.com/v1/search",
        params={
            "query": query,
            "per_page": per_provider,
            **({"orientation": orientation} if orientation in ORIENT_MAP["pexels"] else {}),
        },
        # Pexels 认证是裸 Key，无 Bearer/Client-ID 前缀
        headers={"Authorization": key},
    )
    return [
        _item(
            "pexels",
            id=p["id"],
            title=p.get("alt", ""),
            author=p.get("photographer", ""),
            width=p.get("width"),
            height=p.get("height"),
            url=p.get("src", {}).get("original", ""),
            preview=p.get("src", {}).get("medium", ""),
            page_url=p.get("url", ""),
            license="Pexels License",
            attribution=f"Photo by {p.get('photographer', '')} on Pexels",
        )
        for p in data.get("photos", [])
    ]


def search_pixabay(query: str, per_provider: int, orientation: str) -> list[dict]:
    key = os.environ["PIXABAY_API_KEY"]
    # Pixabay 无 orientation 参数，用横向要求的常见最小宽高近似过滤
    params = {
        "key": key,
        "q": query,
        "image_type": "photo",
        "per_page": per_provider,
        "safesearch": "true",
    }
    if orientation == "landscape":
        params["min_width"] = 960
    elif orientation == "portrait":
        params["min_height"] = 960
    data = _get("https://pixabay.com/api/", params=params)
    return [
        _item(
            "pixabay",
            id=p["id"],
            title=p.get("tags", ""),
            author=p.get("user", ""),
            width=p.get("imageWidth"),
            height=p.get("imageHeight"),
            url=p.get("largeImageURL", ""),
            preview=p.get("webformatURL", ""),
            page_url=p.get("pageURL", ""),
            license="Pixabay Content License",
            attribution=f"Image by {p.get('user', '')} on Pixabay",
        )
        for p in data.get("hits", [])
    ]


def search_mediawiki(query: str, per_provider: int, orientation: str) -> list[dict]:
    headers = {"User-Agent": USER_AGENT}
    data = _get(
        "https://commons.wikimedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "formatversion": 2,
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,  # File 命名空间
            "gsrlimit": per_provider,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "iiurlwidth": 1024,
            "iiextmetadatafilter": "LicenseShortName|Artist",
        },
        headers=headers,
    )
    items = []
    for page in data.get("query", {}).get("pages", []):
        info = (page.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        if mime and not mime.startswith("image/"):
            continue
        meta = info.get("extmetadata", {})
        license_name = _strip_html((meta.get("LicenseShortName") or {}).get("value"))
        license_lower = license_name.lower()
        # 许可未知时按需署名处理（保守默认），CC0/公有领域才免署名
        attribution_required = (
            not license_name or license_lower.startswith(("cc by", "attribution"))
        )
        author = _strip_html((meta.get("Artist") or {}).get("value"))
        items.append(
            _item(
                "mediawiki",
                id=page.get("pageid", ""),
                title=page.get("title", "").removeprefix("File:"),
                author=author,
                width=info.get("width"),
                height=info.get("height"),
                url=info.get("url", ""),
                preview=info.get("thumburl", ""),
                page_url=info.get("descriptionurl", ""),
                license=license_name or "见源页面",
                attribution=f"{author}，via Wikimedia Commons，{license_name}".strip("，"),
                attribution_required=attribution_required,
            )
        )
    # Commons 搜索 API 无 orientation 参数，按宽高事后过滤
    if orientation == "landscape":
        items = [i for i in items if (i["width"] or 0) >= (i["height"] or 1)]
    elif orientation == "portrait":
        items = [i for i in items if (i["height"] or 0) >= (i["width"] or 1)]
    return items


# access_token 仅 12h 有效（动态凭据），缓存于该文件避免每次运行重复换取；
# 格式 {"access_token", "expires_at"}，与 openverse 技能的刷新脚本共用同一缓存
OPENVERSE_TOKEN_CACHE = Path.home() / ".cache" / "openverse_token.json"
OPENVERSE_TOKEN_BUFFER = 300   # 提前 5 分钟视为过期
OPENVERSE_TOKEN_URL = "https://api.openverse.org/v1/auth_tokens/token/"
OPENVERSE_TOKEN_VALIDITY = 43200  # API 返回 expires_in=43200（12h），响应缺失时兜底


def _openverse_token() -> str:
    """取 Openverse Bearer token：缓存未过期直接用；临期或缺失时用长期
    client 凭据（OPENVERSE_CLIENT_ID/SECRET）换取并写回缓存。环境已有的
    OPENVERSE_ACCESS_TOKEN 优先。换取失败降级匿名（返回空串），不中断搜索。"""
    token = os.environ.get("OPENVERSE_ACCESS_TOKEN", "")
    if not token:
        try:
            data = json.loads(OPENVERSE_TOKEN_CACHE.read_text())
            token = data.get("access_token", "")
            expires_at = data.get("expires_at", 0)
        except Exception:
            token, expires_at = "", 0
        if token and time.time() < expires_at - OPENVERSE_TOKEN_BUFFER:
            return token
        token = ""  # 过期缓存不可再信，丢弃后尝试重新换取
    else:
        return token
    client_id = os.environ.get("OPENVERSE_CLIENT_ID")
    client_secret = os.environ.get("OPENVERSE_CLIENT_SECRET")
    if not (client_id and client_secret):
        return ""
    try:
        resp = requests.post(
            OPENVERSE_TOKEN_URL,
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "client_credentials",
            },
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        token = resp.json().get("access_token", "")
    except requests.RequestException as exc:
        print(f"  [warn] Openverse token 换取失败，降级匿名: {exc}", file=sys.stderr)
        return ""
    if token:
        try:
            expires_at = int(time.time() + resp.json().get("expires_in", OPENVERSE_TOKEN_VALIDITY))
            OPENVERSE_TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
            OPENVERSE_TOKEN_CACHE.write_text(json.dumps({"access_token": token, "expires_at": expires_at}))
            OPENVERSE_TOKEN_CACHE.chmod(0o600)
        except OSError as exc:
            print(f"  [warn] Openverse token 缓存写入失败: {exc}", file=sys.stderr)
    return token


def search_openverse(query: str, per_provider: int, orientation: str) -> list[dict]:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    token = _openverse_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = _get(
        "https://api.openverse.org/v1/images/",
        params={
            "q": query,
            "page_size": per_provider,
            **({"aspect_ratio": ORIENT_MAP["openverse"][orientation]} if orientation in ORIENT_MAP["openverse"] else {}),
        },
        headers=headers,
    )
    items = []
    for p in data.get("results", []):
        license_name = " ".join(
            part for part in (p.get("license", ""), p.get("license_version") or "") if part
        )
        no_attribution = p.get("license") in ("cc0", "pdm")
        url = p.get("url") or p.get("thumbnail") or ""  # 原图 url 可能为 null，回退代理预览
        items.append(
            _item(
                "openverse",
                id=p.get("id", ""),
                title=p.get("title") or "",
                author=p.get("creator") or "",
                width=p.get("width"),
                height=p.get("height"),
                url=url,
                preview=p.get("thumbnail") or "",
                page_url=p.get("foreign_landing_url") or "",
                license=license_name,
                attribution=p.get("attribution") or "",
                attribution_required=not no_attribution,
            )
        )
    return items


SEARCHERS = {
    "unsplash": search_unsplash,
    "pexels": search_pexels,
    "pixabay": search_pixabay,
    "mediawiki": search_mediawiki,
    "openverse": search_openverse,
}


# ---------------------------------------------------------------------------
# 聚合、混排与下载
# ---------------------------------------------------------------------------


def resolve_providers(requested: str | None) -> tuple[list[str], dict[str, str]]:
    """解析实际参与搜索的来源；keyed 来源缺环境变量时记入 skipped。"""
    wanted = list(ALL_PROVIDERS) if not requested else [p.strip() for p in requested.split(",") if p.strip()]
    unknown = [p for p in wanted if p not in ALL_PROVIDERS]
    if unknown:
        raise SystemExit(f"未知来源: {', '.join(unknown)}（可选: {', '.join(ALL_PROVIDERS)}）")
    env_names = {
        "unsplash": "UNSPLASH_ACCESS_KEY",
        "pexels": "PEXELS_API_KEY",
        "pixabay": "PIXABAY_API_KEY",
    }
    skipped: dict[str, str] = {}
    providers = []
    for p in wanted:
        env = env_names.get(p)
        if env and not os.environ.get(env):
            skipped[p] = f"缺少环境变量 {env}"
            continue
        providers.append(p)
    return providers, skipped


def merge_round_robin(groups: dict[str, list[dict]]) -> list[dict]:
    """各来源按自身相关度序轮流交错，保证混排头部覆盖每个来源。"""
    merged: list[dict] = []
    seen_urls: set[str] = set()
    for i in range(max((len(g) for g in groups.values()), default=0)):
        for provider in groups:
            if i >= len(groups[provider]):
                continue
            item = groups[provider][i]
            key = (item["url"] or item["preview"]).split("?", 1)[0]
            if key and key in seen_urls:
                continue  # Wikimedia Commons 图片常同时出现在 mediawiki 与 openverse
            seen_urls.add(key)
            merged.append(item)
    return merged


def download_items(items: list[dict], output_dir: Path, limit: int) -> list[dict]:
    """下载混排前 limit 张，返回下载清单（含本地路径与失败原因）。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    downloaded = []
    for rank, item in enumerate(items[:limit], start=1):
        url = item["url"] or item["preview"]
        if not url:
            continue
        ext = Path(urlparse(url).path).suffix.lower() or ".jpg"
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"):
            ext = ".jpg"
        path = output_dir / f"{rank:02d}_{item['provider']}_{item['id']}{ext}"
        try:
            resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
            resp.raise_for_status()
            path.write_bytes(resp.content)
            downloaded.append({"rank": rank, "provider": item["provider"], "file": str(path),
                               "page_url": item["page_url"], "license": item["license"],
                               "attribution": item["attribution"]})
            print(f"  [OK] {path.name}  <- {item['provider']}", file=sys.stderr)
        except requests.RequestException as exc:
            downloaded.append({"rank": rank, "provider": item["provider"], "file": None,
                               "error": str(exc)})
            print(f"  [FAIL] #{rank} {item['provider']}: {exc}", file=sys.stderr)
    return downloaded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="多来源图片聚合搜索（Unsplash/Pexels/Pixabay/Wikimedia Commons/Openverse）",
    )
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument(
        "--providers",
        default=None,
        help=f"逗号分隔的来源列表（默认: 全部可用来源，可选 {','.join(ALL_PROVIDERS)}）",
    )
    parser.add_argument("--orientation", choices=("any", "landscape", "portrait", "square"), default="any")
    parser.add_argument("--per-provider", type=int, default=5, help="每个来源取多少条（默认 5）")
    parser.add_argument("--download", type=int, default=0, metavar="N", help="下载混排前 N 张到 -o 目录")
    parser.add_argument("-o", "--output", default="images", help="下载目录（默认 ./images）")
    args = parser.parse_args(argv)

    providers, skipped = resolve_providers(args.providers)
    if not providers:
        print("没有可用的搜索来源。配置以下环境变量之一以启用 keyed 来源：", file=sys.stderr)
        for p, reason in skipped.items():
            print(f"  {p}: {reason}", file=sys.stderr)
        return 1
    for p, reason in skipped.items():
        print(f"  [skip] {p}: {reason}", file=sys.stderr)
    print(f"搜索来源: {', '.join(providers)}", file=sys.stderr)

    orientation = "" if args.orientation == "any" else args.orientation
    groups: dict[str, list[dict]] = {}
    errors: dict[str, str] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(providers)) as pool:
        futures = {
            p: pool.submit(SEARCHERS[p], args.query, args.per_provider, orientation)
            for p in providers
        }
        for p, fut in futures.items():
            try:
                # 搜索成功（含被 orientation 过滤为空）也进 groups，保证该来源可见
                groups[p] = fut.result()
            except Exception as exc:
                # Pixabay 的 key 走 URL query 参数，异常字符串会带出完整 URL，先脱敏
                message = re.sub(r"key=[^&\s]+", "key=***", str(exc))
                errors[p] = message
                print(f"  [error] {p}: {message}", file=sys.stderr)

    merged = merge_round_robin(groups)
    result = {
        "query": args.query,
        "providers_used": list(groups),
        "errors": errors,
        "skipped": skipped,
        "total": len(merged),
        "results": groups,   # 按来源分组，保留各来源自身相关度排序
        "merged": merged,    # 各来源轮流交错的混排（跨源 url 去重）
    }

    if args.download > 0:
        result["downloaded"] = download_items(merged, Path(args.output), args.download)

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    print()
    return 0 if (groups or not errors) else 1


if __name__ == "__main__":
    raise SystemExit(main())
