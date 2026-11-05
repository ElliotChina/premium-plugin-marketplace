---
name: openverse
description: Search and download openly-licensed images aggregated by Openverse (Flickr, Wikimedia Commons, museum collections) via the Openverse REST API. **TRIGGER when users need:** openly-licensed / CC-licensed / public domain stock photos, artwork, illustrations, historical imagery, or mention Openverse/开放许可/CC 图片/公有领域/素材/找图. Use when building websites, apps, presentations, or documents requiring freely-usable visual content with per-image license metadata — even if Openverse isn't explicitly named.
---

# Openverse Image Skill

通过 Openverse REST API 搜索开放许可图片。Openverse 聚合 Flickr、Wikimedia Commons、博物馆馆藏（Smithsonian 等）多个来源的 CC 授权与公有领域作品，每条结果自带许可元数据与署名文本。

## ⚠️ 前置要求

**无需 API Key** —— 匿名即可搜索，零配置。

**匿名限流（响应头实测）：**
- `anon_burst`: **20 次/分钟**
- `anon_sustained`: **200 次/天**
- 额度很紧，务必落实结果缓存，循环里控制请求次数

**可选注册提升额度**（无需网页注册，纯 API 调用）：
```bash
# 1. 注册应用，得到 client_id / client_secret
curl -X POST "https://api.openverse.org/v1/auth_tokens/register/" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-project", "description": "image search for my app", "email": "me@example.com"}'

# 2. 换取 access_token
curl -X POST "https://api.openverse.org/v1/auth_tokens/token/" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&grant_type=client_credentials"

# 3. 带 Bearer token 请求（额度显著提升）
curl "https://api.openverse.org/v1/images/?q=mountain" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

⚠️ 注册实测注意：
- 注册后 Openverse 发验证邮件，**点击验证链接前额度不提升**（token 可用但仍走匿名额度，`GET /v1/rate_limit/` 返回 `verified: false`）
- `access_token` 仅 **12 小时有效**（`expires_in: 43200`），过期后用长期有效的 client_id/secret 重新调 `/v1/auth_tokens/token/` 刷新；不要把 token 当长期凭据

配置了 token 时用环境变量 `OPENVERSE_ACCESS_TOKEN`；未配置则匿名调用。

---

## 🎯 核心概念

### 聚合索引，图片存在源站
Openverse 是**元数据索引**，不是图床。每条结果的 `url` 指向源站（Flickr、Wikimedia 等）的原图，`thumbnail` 是 Openverse 代理的小图。

### 每个结果自带许可与署名 ⚠️
- `license` + `license_version` + `license_url`：该图的 CC 许可（`by` / `by-sa` / `cc0` / `pdm` 公有领域标记等）
- `attribution`：**API 直接生成好的合法署名文本**（英文），如
  `"Mountains" by Kamil Porembiński is licensed under CC BY-SA 2.0...`
  直接展示/落库即可，无需自己拼接
- CC BY / CC BY-SA 图片必须按 `attribution` 署名；`cc0` / `pdm`（公有领域）无强制署名义务

---

## 🎯 工作流程

### 1. 理解需求
询问用户（如果信息不完整）：
- **主题**: 关键词或具体描述
- **许可要求**: 必须免署名（只用 `cc0,pdm`）？还是允许 CC BY 系（需署名）？
- **偏好**: 宽高比 / 尺寸 / 类别（照片、插画、艺术品）？

### 2. 搜索图片

```bash
curl "https://api.openverse.org/v1/images/?q=mountain%20lake&license=cc0,pdm,by&size=large&aspect_ratio=wide&page_size=10" \
  -H "User-Agent: my-project/1.0" -H "Accept: application/json"
```

**常用参数：**

| 参数 | 说明 |
|------|------|
| `q` | 搜索词（≤200 字符） |
| `license` | 逗号分隔许可过滤：`by`, `by-sa`, `by-nc`, `by-nc-nd`, `by-nc-sa`, `by-nd`, `cc0`, `pdm`。免署名档用 `cc0,pdm` |
| `license_type` | `all` / `all-cc` / `commercial` / `modification`。⚠️ 匿名实测可返回 HTTP 500，**优先用 `license` 精确枚举** |
| `size` | `large` / `medium` / `small`（逗号分隔） |
| `aspect_ratio` | `wide`(横) / `tall`(竖) / `square`(方) |
| `category` | `photograph` / `illustration` / `digitized_artwork` |
| `extension` | 文件扩展名过滤，如 `jpg`, `png` |
| `source` / `excluded_source` | 数据源过滤（源列表见 `/v1/images/stats/`），如 `flickr`, `wikimedia` |
| `tags` / `title` / `creator` | 仅按标签/标题/作者搜（`tags`/`title` 与 `q` 互斥；`q` 存在时 `creator` 被忽略） |
| `page_size` | 每页数量（默认 20） |
| `page` | 页码（匿名页数受限） |
| `filter_dead` | 过滤 404 死链（默认 true） |
| `mature` | 是否含敏感内容（默认 false） |

**响应结构：**
```json
{
  "result_count": 240,
  "page_count": 120,
  "page_size": 2,
  "page": 1,
  "results": [{
    "id": "f561777d-24ea-483f-9cf8-f17aa1fd6aa3",
    "title": "Mountains",
    "url": "https://live.staticflickr.com/7539/16129656628_ddd1db38c2_b.jpg",
    "thumbnail": "https://api.openverse.org/v1/images/f561.../thumb/",
    "foreign_landing_url": "https://www.flickr.com/photos/.../16129656628",
    "creator": "Kamil Porembiński",
    "creator_url": "https://www.flickr.com/photos/.../",
    "license": "by-sa",
    "license_version": "2.0",
    "license_url": "https://creativecommons.org/licenses/by-sa/2.0/",
    "provider": "flickr",
    "source": "flickr",
    "attribution": "\"Mountains\" by Kamil Porembiński is licensed under CC BY-SA 2.0...",
    "width": 1024, "height": 683,
    "filetype": "jpg", "filesize": null,
    "category": null,
    "tags": [{"name": "iceland", "accuracy": null}],
    "detail_url": "https://api.openverse.org/v1/images/f561.../",
    "related_url": "https://api.openverse.org/v1/images/f561.../related/"
  }]
}
```

### 3. 展示选项
```
找到 5 张符合条件的图片：

1. 🏔️ Mountains - 1024x683 JPEG
   许可: CC BY-SA 2.0（需署名）
   作者: Kamil Porembiński（Flickr）
   源页面: https://www.flickr.com/photos/.../16129656628

2. 🖼️ Sunrise over peaks - 2000x1200 JPEG
   许可: CC0（免署名）
```

### 4. 下载与署名
- 下载用 `url`（原图，存源站）；列表预览用 `thumbnail`（Openverse 代理）
- CC BY / CC BY-SA 图直接引用返回的 `attribution` 文本署名，链接到 `foreign_landing_url` 与 `license_url`
- 下载到本地长期使用，详见下方「核心规则」

---

## ⚡ 核心规则（必读）

### 1. 限流额度紧，必须缓存 ⚠️
匿名 20 次/分钟 + 200 次/天。超限返回 **429**。做法：
- 同一查询结果缓存复用，不要循环翻页抓全量
- 批量找图时一次 `page_size=20` 拿足候选，本地筛选
- 需要高频调用就让用户注册 token（`OPENVERSE_ACCESS_TOKEN`），并轮询 `GET /v1/rate_limit/` 自查余量：

```json
{"requests_this_minute": 3, "requests_today": 45, "rate_limit_model": "standard", "verified": false}
```

### 2. 按许可署名 ⚠️
每张图许可不同，以响应的 `license` 字段为准：
- `cc0` / `pdm`（公有领域）: 无强制署名义务
- `by` / `by-sa` 等: **必须署名**——直接用 API 返回的 `attribution` 文本，附 `foreign_landing_url`（作品页）与 `license_url`（许可条款）
- 含 `nc`（非商业）/ `nd`(禁止衍生) 的许可对商用有额外限制，选图前确认用户用途

### 3. url 可能为空，thumbnail 代理不稳定
- `url`（原图）可为 `null`：此时回退用 `thumbnail`
- Openverse 的 `thumbnail` 代理链路偶发不可用；Wikimedia 来源的图可改用稳定的 Special:Redirect 构造预览：
  `https://commons.wikimedia.org/wiki/Special:Redirect/file/{文件名}?width=1024`
- 生产环境把图下载到自有存储，不长期依赖 Openverse 代理

### 4. 请求带 User-Agent
请求携带自定义 `User-Agent` 与 `Accept: application/json`。

---

## 💻 常用场景代码

### TypeScript: 搜索图片

```typescript
interface OpenverseImage {
  id: string;
  title: string | null;
  url: string | null;               // ⚠️ 可为 null，回退 thumbnail
  thumbnail: string;
  foreign_landing_url: string | null;
  creator: string | null;
  license: string;                  // 'by' | 'by-sa' | 'cc0' | 'pdm' | ...
  license_version: string | null;
  license_url: string | null;
  attribution: string | null;       // 现成的合法署名文本（英文）
  source: string | null;
  width: number | null;
  height: number | null;
  filetype: string | null;
  tags: Array<{ name: string }>;
}

interface SearchOptions {
  license?: string;        // 如 'cc0,pdm,by'
  size?: 'large' | 'medium' | 'small';
  aspectRatio?: 'wide' | 'tall' | 'square';
  category?: 'photograph' | 'illustration' | 'digitized_artwork';
  pageSize?: number;
}

async function searchOpenverseImages(q: string, opts: SearchOptions = {}): Promise<OpenverseImage[]> {
  const headers: Record<string, string> = {
    'User-Agent': 'my-project/1.0',
    'Accept': 'application/json',
  };
  if (process.env.OPENVERSE_ACCESS_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.OPENVERSE_ACCESS_TOKEN}`;
  }
  const params = new URLSearchParams({
    q,
    page_size: String(opts.pageSize ?? 10),
    ...(opts.license && { license: opts.license }),
    ...(opts.size && { size: opts.size }),
    ...(opts.aspectRatio && { aspect_ratio: opts.aspectRatio }),
    ...(opts.category && { category: opts.category }),
  });
  const res = await fetch(`https://api.openverse.org/v1/images/?${params}`, { headers });
  if (res.status === 429) throw new Error('限流：匿名 20次/分钟、200次/天，缓存结果或注册 token');
  const data = await res.json();
  return data.results as OpenverseImage[];
}

// 使用示例：免署名档大图
const images = await searchOpenverseImages('mountain lake', {
  license: 'cc0,pdm', size: 'large', aspectRatio: 'wide',
});
for (const img of images) {
  console.log(img.url ?? img.thumbnail);  // 下载地址（url 可能为 null）
  console.log(img.attribution);           // 署名文本（cc0/pdm 可省略）
}
```

### Python: 搜索并下载到本地

```python
import os, pathlib, requests

UA = {'User-Agent': 'my-project/1.0', 'Accept': 'application/json'}

def search_and_download(query: str, dest_dir: str = 'assets/images',
                        license_list: str = 'cc0,pdm,by,by-sa', page_size: int = 10) -> list:
    """搜索 Openverse 并下载原图到本地

    license_list 建议显式枚举（license_type 参数匿名下不稳定，可能 500）
    """
    headers = dict(UA)
    token = os.environ.get('OPENVERSE_ACCESS_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'

    res = requests.get('https://api.openverse.org/v1/images/', params={
        'q': query, 'license': license_list, 'size': 'large', 'page_size': page_size,
    }, headers=headers)
    if res.status_code == 429:
        raise RuntimeError('Openverse 限流（匿名 20/min + 200/day）：缓存结果或注册 token')
    res.raise_for_status()

    saved = []
    for item in res.json()['results']:
        download_url = item.get('url') or item.get('thumbnail')  # url 可能为空
        if not download_url:
            continue
        ext = item.get('filetype') or 'jpg'
        path = pathlib.Path(dest_dir) / f"{item['id']}.{ext}"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(requests.get(download_url, headers=UA, timeout=30).content)
        saved.append({
            'file': str(path),
            'license': f"{item['license']} {item.get('license_version') or ''}".strip(),
            'attribution': item.get('attribution'),   # 现成署名文本
            'landing_url': item.get('foreign_landing_url'),
        })
    return saved

# 使用示例
for item in search_and_download('mountain lake'):
    print(item['file'], '-', item['license'])
    if item['attribution']:
        print('  署名:', item['attribution'])
```

### 生成带署名的 HTML

```python
def generate_img_html(item: dict, local_path: str) -> str:
    """生成带许可署名的图片 HTML（引用本地下载的文件）

    ⚠️ CC BY 系许可必须展示 attribution；cc0/pdm 可省略
    """
    landing = item.get('foreign_landing_url') or item.get('detail_url')
    license_url = item.get('license_url') or ''
    attribution = item.get('attribution') or item.get('title') or ''

    credit = ''
    if item.get('license') not in ('cc0', 'pdm'):
        credit = f'<figcaption>{attribution} <a href="{license_url}">License</a></figcaption>'

    return f'''<figure>
  <img src="{local_path}" alt="{item.get('title') or ''}" loading="lazy">
  {credit}
</figure>'''
```

### 查询剩余额度

```python
def check_rate_limit(token: str | None = None) -> dict:
    """查询当前额度余量（匿名/认证皆可调用）"""
    headers = dict(UA)
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return requests.get('https://api.openverse.org/v1/rate_limit/', headers=headers).json()
    # {'requests_this_minute': 3, 'requests_today': 45,
    #  'rate_limit_model': 'standard', 'verified': False}
```

---

## ❌ 错误处理

| 状态码 | 原因 | 解决方案 |
|-------|------|---------|
| 400 | 参数非法（如 `license` 传了不存在的值） | 对照参数表检查 |
| 401 | Bearer token 无效/过期 | 重新调 `/v1/auth_tokens/token/` 换 token |
| 429 | 超过限流（匿名 20次/分 + 200次/天） | 缓存结果、控制请求频率，或注册 token |
| 500 | 服务端错误（实测 `license_type` 参数匿名下可触发） | 改用 `license` 参数精确枚举；仍失败则稍后重试 |

```python
def handle_openverse_error(status: int) -> str:
    errors = {
        400: '参数非法：检查 license/size/aspect_ratio 取值',
        401: 'token 无效：重新获取 access_token',
        429: '限流：匿名 20次/分钟 + 200次/天，缓存结果或注册 token',
        500: '服务端错误：避开 license_type，用 license 精确枚举，稍后重试',
    }
    return errors.get(status, f'未知错误: {status}')
```

---

## ✅ 最佳实践清单

**执行前检查：**
- [ ] **无需 Key 即可用**；高频场景先注册 token（`OPENVERSE_ACCESS_TOKEN`）
- [ ] **请求带 User-Agent** 与 `Accept: application/json`

**必须遵守：**
- [ ] **结果缓存** - 匿名额度 20次/分钟 + 200次/天，429 风险高
- [ ] **按许可署名** - 用响应的 `attribution` 文本；含 `nc`/`nd` 的许可注意商用与衍生限制
- [ ] **下载到本地** - 原图存源站、`thumbnail` 是代理链路，生产环境自托管
- [ ] `url` 为空时回退 `thumbnail`，都空则跳过该结果

**强烈推荐：**
- [ ] 用 `license` 参数精确枚举（`cc0,pdm` 免署名档 / 加 `by,by-sa` 开署名档），避免 `license_type`
- [ ] 一次 `page_size=20` 拿足候选本地筛选，减少翻页请求
- [ ] 按 `size=large` + `aspect_ratio` 缩小结果集
- [ ] 需要时轮询 `GET /v1/rate_limit/` 自查余量
