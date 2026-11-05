---
name: image-search
description: Aggregate image search across Unsplash, Pexels, Pixabay, Wikimedia Commons and Openverse in one call — concurrent multi-source query with unified JSON results (download/preview URLs, dimensions, license, attribution text) and optional top-N download. **TRIGGER when users need:** to compare or combine multiple free stock-photo sources at once, find images without knowing which provider is best, maximize candidate coverage for one query, or mention 聚合搜索/多来源/综合搜索/全网找图. Use the bundled `scripts/image_search.py` — do not hand-write five separate API calls.
---

# Image Search（多来源聚合搜索）

一次调用并发搜索 Unsplash / Pexels / Pixabay / Wikimedia Commons / Openverse，输出统一结构的 JSON（原图/预览 URL、尺寸、许可、署名文本），可选下载混排前 N 张。

## ⚠️ 前置要求

Python 3.10+ 与 `requests`。零配置来源（mediawiki / openverse）无需任何 Key；keyed 来源检测到环境变量才参与搜索，缺失自动跳过（记入 `skipped`，不影响其他来源）：

| 来源 | 环境变量 | 缺失时 |
|------|---------|--------|
| unsplash | `UNSPLASH_ACCESS_KEY` | 跳过 |
| pexels | `PEXELS_API_KEY` | 跳过 |
| pixabay | `PIXABAY_API_KEY` | 跳过 |
| mediawiki | 无需 | 始终可用 |
| openverse | 无需（可选 `OPENVERSE_CLIENT_ID`/`OPENVERSE_CLIENT_SECRET`） | 匿名限流 20次/分 + 200次/天 |

聚合搜索每个来源只发 1 个请求，匿名额度足够单次查询。Openverse 的 access_token 是动态凭据（仅 12h 有效），不要让用户手动配置——配置长期 client 凭据后脚本自动换取，缓存于 `~/.cache/openverse_token.json` 临期内复用，无需人工介入。

---

## 🎯 搜索需求分析（调用前先确认）

信息不完整时，先与用户确认以下要求再执行搜索；用户已给全或明确说"随便找"时直接执行，不要逐项追问。每项都给用户**具体选项**（而非开放式提问），用户可直接选，也可补充自定义要求。

| 要求项 | 是否必问 | 沟通时给出的选项（标注默认） | 落地方式 |
|--------|---------|----------------------------|---------|
| 搜索主题 | ✅ 必要 | 开放式收集；用户给中文时附上英文译法让用户确认（如"雪山湖泊 → snowy mountain lake，可以吗？"） | `query`（无此参数无法调用） |
| 方向 / 宽高比 | 有布局用途时问 | A. 横图（hero/banner）· B. 竖图（手机端/文章）· C. 方形（头像/缩略图）· **D. 不限（默认）** | `--orientation landscape/portrait/square` |
| 许可 / 署名限制 | 商用场景必问 | A. **可接受署名（默认）** · B. 必须免署名（只用 CC0/公有领域及各站免费许可）· C. 商用且需避开 nc/nd 限制 | B 加 `--license-free`（openverse/Commons 过滤，其余来源本就免署名）；C 无参数，筛掉 `license` 含 `nc`/`nd` 的结果 |
| 尺寸下限 | 高清场景问 | A. 宽 ≥1920px（高清/壁纸级）· B. 宽 ≥1200px（网页常规）· **C. 不限（默认）** | 按 `width` / `pixels` 字段筛选 |
| 数量与是否下载 | 可选 | A. **每来源 5 条，仅预览不下载（默认）** · B. 每来源 10 条仅预览 · C. 下载前 N 张到指定目录（N 常用 1–5） | `--per-provider`、`--download N -o DIR` |
| 颜色 / 内容类型 | 可选 | A. **不限（默认）** · B. 指定颜色（黑/白/红/蓝等 8 色）· C. 只要照片 · D. 只要插画 · E. 只要矢量图 | B 用 `--color`（仅 unsplash/pexels）；C–E 用 `--type`（服务端过滤仅 pixabay/openverse，其余来源不区分类型） |

确认后把要求翻译成参数组合：能落参数的落参数（`query` / `--orientation` / `--per-provider` / `--download`），落不了的（许可、尺寸、颜色）在拿到 JSON 后按字段筛选并向用户说明筛选依据。

---

## 🎯 用法

```bash
# 聚合搜索（零配置即可跑），输出 JSON 到 stdout
python scripts/image_search.py "mountain lake" --orientation landscape

# 只搜指定来源，每来源取 8 条
python scripts/image_search.py "office team" --providers pexels,unsplash --per-provider 8

# 搜索并下载混排前 3 张到 ./images/
python scripts/image_search.py "sunset" --download 3 -o images/
```

**参数：**

| 参数 | 说明 |
|------|------|
| `query` | 搜索关键词（英文命中率高） |
| `--providers` | 逗号分隔来源列表；默认全部可用来源 |
| `--orientation` | `any`（默认）/ `landscape` / `portrait` / `square`；各来源自动映射（Commons 不支持时按宽高事后过滤） |
| `--type` | `photo` / `illustration` / `vector`；服务端过滤仅 pixabay（`image_type`）与 openverse（`category`，无 vector 分类）支持，其余来源不区分类型（unsplash/pexels 为纯照片站） |
| `--color` | `black`/`white`/`yellow`/`orange`/`red`/`purple`/`green`/`blue`；仅 unsplash/pexels 支持（`purple` 自动映射为 pexels 的 `violet`） |
| `--license-free` | 仅保留免强制署名结果：openverse 服务端过滤 CC0/公有领域，Commons 结果后筛（许可未知即排除），unsplash/pexels/pixabay 本就免强制署名 |
| `--per-provider` | 每来源结果数（默认 5）⚠️ pixabay 要求 ≥3，openverse 匿名上限 20 |
| `--download N` | 下载混排前 N 张到 `-o` 目录，文件名 `{排名}_{来源}_{id}.{扩展名}` |
| `-o` | 下载目录（默认 `./images`） |

---

## 📊 输出结构

stdout 输出一个 JSON 对象：

```json
{
  "query": "mountain lake",
  "providers_used": ["mediawiki", "openverse", "unsplash", "pexels", "pixabay"],
  "errors": {},           // {来源: 错误信息}，单来源失败不影响其他
  "skipped": {},          // {来源: "缺少环境变量 XXX"}
  "total": 15,
  "results": { ... },     // 按来源分组，保留各来源自身相关度排序
  "merged": [ ... ],      // 各来源轮流交错的混排（跨源 URL 去重）
  "downloaded": [ ... ]   // 仅 --download 时出现；失败条目为 {rank, provider, file: null, error}，成功条目含 file/page_url/license/attribution
}
```

每条结果统一字段：

| 字段 | 说明 |
|------|------|
| `url` | 原图下载地址（openverse 原图可为空，已自动回退代理预览） |
| `preview` | 预览/缩略图地址（给用户展示用） |
| `width` / `height` / `pixels` | 尺寸与像素数 |
| `page_url` | 源页面（署名链接指向这里） |
| `license` | 许可名称 |
| `attribution` | 建议署名文本 |
| `attribution_required` | `true` 时必须展示署名（CC BY 系许可） |

**两组结果的用法：** 挑"每个来源最好的"看 `merged` 头部；按相关度深挖某一来源看 `results.<provider>`。

---

## ⚡ 核心规则（必读）

### 1. 优先用本脚本，不要手写五份 API 调用
并发、认证差异、orientation 映射、跨源去重、统一字段都由脚本处理。仅当需要脚本未覆盖的细粒度参数（如 Pexels 颜色过滤、Pixabay 视频）时，才直接调用该来源 API。

### 2. 按许可展示署名
- `attribution_required: true`（CC BY 系 / 来源站条款要求）：展示 `attribution` 文本并链接 `page_url`
- `false`（Unsplash / Pexels / Pixabay / CC0 / 公有领域）：署名可选，但建议保留摄影师署名
- Openverse 结果可能含 `by-nc-sa` 等非商用许可，商用前确认 `license` 字段
- Pixabay `url` 是 1280px 版本；需要更高分辨率从 `page_url` 手动获取

### 3. 单来源失败是常态
任何来源 429/超时/Key 失效都只记入 `errors`，不中断整体。若该来源的结果是关键需求，稍后单独重试该来源。

### 4. 结果不落盘即失效
`url` 指向源站或 CDN。要长期使用就用 `--download` 落地本地文件，署名信息以 `downloaded` 数组为准随文件保存。

---

## ✅ 最佳实践清单

- [ ] 零配置即可用；keyed 来源缺 Key 先检查 `skipped` 字段并提示用户配置
- [ ] 关键词用英文；中文关键词各来源命中率显著下降
- [ ] `--download` 前先看 `merged` / `preview` 确认候选，避免下载不需要的原图
- [ ] 展示给用户时用 `preview` URL（小图快），交付/集成用 `url`（原图）
- [ ] `attribution_required: true` 的图必须带署名，商用注意 `nc`/`nd` 限制
- [ ] 本脚本只搜图片；视频搜索不在覆盖范围
