---
name: mediawiki
description: Search and download freely-licensed images from MediaWiki wikis (Wikimedia Commons, Wikipedia) via the Action API. **TRIGGER when users need:** freely-licensed stock photos, public domain images, historical photos, maps, diagrams, technical illustrations, or mention MediaWiki/Wikipedia/Wikimedia/Commons/维基/百科/素材/找图. Use when building websites, apps, presentations, or documents requiring freely-usable visual content — even if MediaWiki isn't explicitly named.
---

# MediaWiki Image Skill

通过 MediaWiki Action API 搜索和获取自由许可图片（照片、地图、图表、历史影像等），主要用于 Wikimedia Commons 等公开 wiki。

## ⚠️ 前置要求

**无需 API Key** —— MediaWiki Action API 公开可读，匿名即可调用。

**但需遵守 Wikimedia API 礼仪：**
- 请求携带**有意义的 `User-Agent`**（含联系方式），Wikimedia 会封禁无 UA 或泛用 UA 的客户端
- 高频使用建议缓存响应，避免并发大量请求

```bash
# 请求示例必须带 User-Agent
curl "https://commons.wikimedia.org/w/api.php?action=query&format=json&..." \
  -H "User-Agent: my-project/1.0 (https://example.com; contact@example.com)"
```

---

## 🎯 核心概念

### 端点 = 各 wiki 自己的 api.php
没有统一 API 域名，每个 MediaWiki 站点有独立端点：

| Wiki | 端点 | 说明 |
|------|------|------|
| Wikimedia Commons | `https://commons.wikimedia.org/w/api.php` | **图片素材首选**，收录自由许可媒体 |
| 英文 Wikipedia | `https://en.wikipedia.org/w/api.php` | 仅本 wiki 本地上传的文件 |
| 中文 Wikipedia | `https://zh.wikipedia.org/w/api.php` | 同上 |
| 自建 wiki | `https://你的域名/w/api.php` | 任意 MediaWiki 站点 |

> Wikipedia 页面上引用的很多文件实际托管在 Commons。仅对 Commons 调 API 即可覆盖绝大多数素材；对其他 wiki 查不到 Commons 文件是正常现象。

### 每个文件有自己的许可 ⚠️
Commons 收录 CC0 / 公有领域（PD）/ CC BY / CC BY-SA 等多种许可的文件。
**使用前必须查询该文件的许可（`extmetadata` 的 `LicenseShortName`），并按许可要求署名**：
- `CC0` / `PD`（公有领域）: 可自由使用，署名非强制
- `CC BY` / `CC BY-SA`: **必须署名**（作者 + 许可链接），CC BY-SA 还要求衍生作品同许可共享
- `Fair use` 类（Wikipedia 本地文件常见）: **仅限百科式合理使用，不可用于一般项目**

---

## 🎯 工作流程

### 1. 理解需求
询问用户（如果信息不完整）：
- **用途**: 文章配图？技术图表？历史照片？地图？
- **主题**: 关键词或具体描述
- **wiki**: 默认用 Commons；用户指定 wiki 时换端点
- **许可要求**: 是否必须 CC0/PD（可商用无署名义务）？

### 2. 搜索文件
`list=search` + **`srnamespace=6`**（6 = File 文件命名空间，默认 0 只搜条目）：

```bash
curl "https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&list=search&srsearch=mountain%20landscape&srnamespace=6&srlimit=10" \
  -H "User-Agent: my-project/1.0 (contact@example.com)"
```

**常用参数：**
- `srsearch` (必填): 搜索词，支持 CirrusSearch 语法（如 `filemime:image/jpeg` 过滤格式、`-word` 排除）
- `srnamespace`: `6`（File）⚠️ 不指定则默认搜条目命名空间，搜不到图片
- `srlimit`: 1-500（默认 10），建议 5-10
- `sroffset`: 翻页偏移（配合响应中的 `continue.sroffset`）
- `srsort`: `relevance`(默认)/`last_edit_desc`/`random` 等

**响应结构（formatversion=2 时 pages 为数组）：**
```json
{
  "continue": { "sroffset": 10, "continue": "-||" },
  "query": {
    "searchinfo": { "totalhits": 5000 },
    "search": [
      { "ns": 6, "title": "File:Mont Blanc.jpg", "pageid": 123456,
        "size": 196026, "wordcount": 100,
        "snippet": "...<span class=\"searchmatch\">mountain</span>...",
        "timestamp": "2020-01-01T00:00:00Z" }
    ]
  }
}
```

### 3. 查询文件信息（URL / 尺寸 / 许可）
用 `prop=imageinfo` 按 `titles=File:文件名` 获取图片 URL 与许可元数据：

```bash
curl "https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&prop=imageinfo&titles=File:Mont%20Blanc.jpg&iiprop=url%7Csize%7Cmime%7Cextmetadata&iiurlwidth=800" \
  -H "User-Agent: my-project/1.0 (contact@example.com)"
```

**关键参数：**
- `iiprop`: `url`(原图 URL + 描述页), `size`(字节/宽/高), `mime`, `extmetadata`(许可/作者/描述), `canonicaltitle`, `timestamp`
- `iiurlwidth`: 同时返回该宽度缩略图（`thumburl`/`thumbwidth`/`thumbheight`）⚠️ 实际返回宽度可能等于或大于请求值（预生成尺寸列表）
- `iiextmetadatafilter`: 只取需要的元数据键（`extmetadata` 是高开销属性，务必过滤）：`LicenseShortName|Artist|ImageDescription|Credit|DateTimeOriginal`
- `iilimit`: 文件修订历史条数（默认 1 = 仅最新版）

**响应结构：**
```json
{
  "query": {
    "pages": [{
      "pageid": 123456, "ns": 6, "title": "File:Mont Blanc.jpg",
      "imagerepository": "local",
      "imageinfo": [{
        "thumburl": "https://upload.wikimedia.org/.../800px-Mont_Blanc.jpg",
        "thumbwidth": 800, "thumbheight": 533,
        "url": "https://upload.wikimedia.org/.../Mont_Blanc.jpg",
        "descriptionurl": "https://commons.wikimedia.org/wiki/File:Mont_Blanc.jpg",
        "width": 4000, "height": 2667, "size": 3500000, "mime": "image/jpeg",
        "extmetadata": {
          "LicenseShortName": { "value": "CC BY-SA 4.0" },
          "Artist": { "value": "<a href=\"...\">John Doe</a>" },
          "ImageDescription": { "value": "Mont Blanc at sunrise" },
          "DateTimeOriginal": { "value": "2020-06-15" }
        }
      }]
    }]
  }
}
```

### 4. 展示选项
向用户展示搜索结果（含许可，供决策）：

```
找到 5 张符合条件的图片：

1. 🏔️ Mont Blanc.jpg - 4000x2667 JPEG (3.4MB)
   许可: CC BY-SA 4.0（需署名）
   作者: John Doe
   描述页: https://commons.wikimedia.org/wiki/File:Mont_Blanc.jpg

2. 🗺️ Alps_map.png - 2000x1500 PNG
   许可: CC0（自由使用）
```

### 5. 集成与署名
- 网页展示用 `thumburl`（如 800px），需要大图/下载用 `url`（原图）
- **按许可署名**，格式：`图片作者，via Wikimedia Commons，CC BY-SA 4.0`（附 `descriptionurl` 与许可链接）
- 搜索与选图可合并为一步：`generator=search&gsrsearch=...&gsrnamespace=6&prop=imageinfo&iiprop=url|size|mime|extmetadata`（一次请求返回搜索结果并附图片信息，`gsrlimit` 控制数量）

---

## ⚡ 核心规则（必读）

### 1. 携带有意义的 User-Agent
匿名请求也必须带 UA，格式 `项目名/版本 (联系方式)`。缺失或泛用 UA（如默认 curl UA）可能被 Wikimedia 拒绝或封禁：

```bash
✅ -H "User-Agent: my-project/1.0 (https://example.com; contact@example.com)"
❌ 不带 User-Agent / 只有 "curl/8.0"
```

### 2. 许可合规 ⚠️
每个文件的许可不同，使用前查 `extmetadata.LicenseShortName`：
- CC BY / CC BY-SA：必须署名作者与许可；CC BY-SA 衍生作品需同许可共享
- Fair use 文件：不可用于一般项目
- 署名格式：`"文件名" by 作者, via Wikimedia Commons, 许可名`，链接到 `descriptionurl`
- `Artist` 等字段值是 HTML，嵌入页面前需清理（strip 标签或白名单过滤）

### 3. 缓存与礼貌使用
Wikimedia 期望客户端缓存响应、避免高频并发。无硬性速率数字，但滥用会触发临时封禁；高频场景考虑申请 `api-highlimits` 权限账号。

### 4. 缩略图宽度取整
`iiurlwidth` 请求的缩略图实际宽度**可能大于请求值**（服务端从预生成尺寸中选取），布局上不要假设 `thumbwidth === iiurlwidth`，按返回的 `thumbwidth` 处理。

---

## 💻 常用场景代码

### TypeScript: 搜索并获取图片信息（合并查询）

```typescript
interface CommonsImage {
  title: string;
  imageinfo: Array<{
    url: string;              // 原图
    thumburl?: string;        // iiurlwidth 请求的缩略图
    thumbwidth?: number;      // ⚠️ 可能大于请求宽度
    descriptionurl: string;   // 文件页（署名链接用）
    width: number; height: number; size: number; mime: string;
    extmetadata: Record<string, { value: string }>;  // value 是 HTML，需清理
  }>;
}

async function searchCommonsImages(query: string, thumbWidth = 800, limit = 5): Promise<CommonsImage[]> {
  const params = new URLSearchParams({
    action: 'query', format: 'json', formatversion: '2',
    generator: 'search',                     // 搜索结果直接作为 imageinfo 的输入
    gsrsearch: query,
    gsrnamespace: '6',                       // 6 = File 命名空间
    gsrlimit: String(limit),
    prop: 'imageinfo',
    iiprop: 'url|size|mime|extmetadata',
    iiurlwidth: String(thumbWidth),
    iiextmetadatafilter: 'LicenseShortName|Artist|ImageDescription|DateTimeOriginal',
  });
  const res = await fetch(`https://commons.wikimedia.org/w/api.php?${params}`, {
    headers: { 'User-Agent': 'my-project/1.0 (https://example.com; contact@example.com)' },
  });
  const data = await res.json();
  return (data.query?.pages ?? []) as CommonsImage[];
}

// 使用示例
const images = await searchCommonsImages('mountain landscape filemime:image/jpeg');
for (const img of images) {
  const info = img.imageinfo[0];
  console.log(info.thumburl ?? info.url);     // 展示用缩略图
  console.log(info.extmetadata.LicenseShortName?.value);  // 许可（署名依据）
}
```

### Python: 获取单文件信息并下载

```python
import requests

UA = {'User-Agent': 'my-project/1.0 (https://example.com; contact@example.com)'}

def get_file_info(file_title: str, thumb_width: int = 800) -> dict:
    """查询 Commons 文件的 URL、尺寸与许可

    file_title 形如 'File:Mont Blanc.jpg'
    """
    res = requests.get('https://commons.wikimedia.org/w/api.php', params={
        'action': 'query', 'format': 'json', 'formatversion': '2',
        'prop': 'imageinfo', 'titles': file_title,
        'iiprop': 'url|size|mime|extmetadata', 'iiurlwidth': thumb_width,
        'iiextmetadatafilter': 'LicenseShortName|Artist|ImageDescription',
    }, headers=UA)
    page = res.json()['query']['pages'][0]
    return page['imageinfo'][0]  # 含 url/thumburl/width/height/mime/extmetadata

# 使用示例
info = get_file_info('File:Mont Blanc.jpg')
license = info['extmetadata']['LicenseShortName']['value']   # 如 'CC BY-SA 4.0'
print(license, '-', info['url'])                             # 原图 URL
print(info['descriptionurl'])                                # 文件页（署名链接）

# 下载原图（自由许可文件可下载使用，按许可署名）
content = requests.get(info['url'], headers=UA).content
```

### 生成带署名的 HTML

```python
import re

def strip_html(s: str) -> str:
    """extmetadata 值是 HTML（如 Artist 含 <a>），嵌入前清理"""
    return re.sub(r'<[^>]+>', '', s)

def generate_img_html(info: dict, alt: str = '') -> str:
    """生成带许可署名的图片 HTML

    ⚠️ CC BY / CC BY-SA 必须署名作者与许可（LicenseShortName）
    """
    meta = info['extmetadata']
    artist = strip_html(meta.get('Artist', {}).get('value', 'Unknown'))
    license_name = meta.get('LicenseShortName', {}).get('value', '')
    src = info.get('thumburl') or info['url']   # 网页展示优先缩略图

    return f'''<figure>
  <img src="{src}" alt="{alt}" loading="lazy">
  <figcaption>{alt} — {artist},
    via <a href="{info['descriptionurl']}">Wikimedia Commons</a>,
    {license_name}</figcaption>
</figure>'''
```

### HTML: 响应式图片（多档缩略图 URL）

```html
<!-- MediaWiki 缩略图按 URL 路径中的宽度前缀区分（800px/1280px 等），
     可自行构造多档 srcset，或对每档调一次 iiurlwidth -->
<img
  src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/xxx.jpg/800px-xxx.jpg"
  srcset="
    https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/xxx.jpg/400px-xxx.jpg 400w,
    https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/xxx.jpg/800px-xxx.jpg 800w,
    https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/xxx.jpg/1280px-xxx.jpg 1280w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="描述 — 作者, via Wikimedia Commons, CC BY-SA 4.0"
  loading="lazy"
>
```

---

## ❌ 错误处理

| 现象 | 原因 | 解决方案 |
|------|------|---------|
| `error.code: "nosrsearch"` | 缺少 `srsearch` | 补全搜索词 |
| `warning` 提示 unrecognized 参数 | 参数名拼错（注意 `gsr` 前缀用于 generator 版本） | 对照参数表检查 |
| 空的 `query.pages` | 文件不存在，或该 wiki 没有 Commons 的共享文件 | 检查 `titles` 拼写；对 Commons 端点重试 |
| HTTP 403 / UA 相关提示 | User-Agent 缺失或泛用 | 补充有意义 UA（含联系方式） |
| 搜索结果都是条目不是文件 | `srnamespace` 未设为 6 | 加 `srnamespace=6` |

```python
def handle_mediawiki_error(data: dict) -> str:
    """MediaWiki 错误在 200 响应体内返回，需检查 error 字段"""
    if 'error' in data:
        return f"{data['error']['code']}: {data['error']['info']}"
    return ''
```

---

## ✅ 最佳实践清单

**执行前检查：**
- [ ] **端点选择** - 图片素材优先用 Commons 端点（`commons.wikimedia.org/w/api.php`）
- [ ] **User-Agent** - 每个请求携带 `项目名/版本 (联系方式)`

**必须遵守：**
- [ ] **查许可** - `extmetadata.LicenseShortName`，CC BY/CC BY-SA 按条款署名，Fair use 不用于一般项目
- [ ] **清理 HTML** - `extmetadata` 各字段值是 HTML，嵌入前 strip
- [ ] **缓存响应** - 礼貌使用，避免高频重复请求

**强烈推荐：**
- [ ] **搜索带 `srnamespace=6`** - 否则搜的是条目不是文件；或直接用 `generator=search` 合并查询
- [ ] 网页展示用 `iiurlwidth` 缩略图，按需取原图
- [ ] 用 `iiextmetadatafilter` 只取需要的元数据键（`extmetadata` 高开销）
- [ ] 用 CirrusSearch 语法精确过滤：`filemime:image/png`、`-排除词`、`intitle:标题`
- [ ] 使用 `formatversion=2`（`pages` 为数组，遍历更方便）
