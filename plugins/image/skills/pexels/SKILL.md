---
name: pexels
description: Search and download free high-quality photos and videos from Pexels for any project. **TRIGGER when users need:** stock photos, hero images, backgrounds, banners, thumbnails, cover images, stock videos, footage, or mention Pexels/图片/照片/素材/找图/视频. Use when building websites, apps, presentations, or marketing materials requiring visual content — even if Pexels isn't explicitly named.
disable-model-invocation: true
---

# Pexels Photo Skill

快速搜索和获取免费高质量照片与视频，用于网站、应用、演示文稿等项目。

## ⚠️ 前置要求

**检查环境变量（每次使用前必做）：**

```bash
# 快速检查
[ -z "$PEXELS_API_KEY" ] && echo "❌ 需要配置 Pexels API Key"
```

**如果未配置，提示用户：**
- 获取 Key: https://www.pexels.com/api/ → 注册/登录 → 复制 API Key（即时发放）
- 配置命令: `export PEXELS_API_KEY=your_key_here`
- API 限制: 默认 200次/小时、20000次/月（可发邮件申请提高额度，需证明已提供署名）

<details>
<summary>📖 详细配置步骤（点击展开）</summary>

1. 访问 https://www.pexels.com/api/
2. 注册/登录 Pexels 账号
3. 填写用途说明后即可获得 API Key（无需审核）

**永久配置：**
```bash
# macOS/Linux
echo 'export PEXELS_API_KEY=your_key' >> ~/.zshrc
source ~/.zshrc

# Windows - 通过"系统属性 → 环境变量"添加
```

</details>

---

## 🎯 工作流程

当用户请求图片时，按以下步骤执行：

### 1. 理解需求
询问用户（如果信息不完整）：
- **用途**: hero背景？产品图？文章配图？头像？
- **主题**: 关键词或具体描述
- **偏好**: 横向/纵向？色调？数量？

### 2. 搜索照片
根据需求选择合适的 API 调用：

```bash
# 搜索特定主题（推荐）
curl "https://api.pexels.com/v1/search?query=mountain&orientation=landscape&per_page=5" \
  -H "Authorization: $PEXELS_API_KEY"

# 精选照片（编辑精选，每小时更新，适合背景/占位符）
curl "https://api.pexels.com/v1/curated?per_page=5" \
  -H "Authorization: $PEXELS_API_KEY"
```

**参数选择建议：**
- `orientation`: `landscape`(横向-适合hero/banner), `portrait`(纵向-适合手机/文章配图), `square`(方形-适合头像/缩略图)
- `size`: `large`(24MP), `medium`(12MP), `small`(4MP)
- `per_page`: 建议 5-10 张供用户选择（最大 80）
- `locale`: 28 种语言环境（如 `en-US`），影响搜索相关性

### 3. 展示选项
向用户展示搜索结果：
- **图片预览**: 使用 `src.medium` 或 `src.small`
- **推荐用途**: 根据尺寸/方向说明适合场景
- **摄影师信息**: 用于署名

示例格式：
```
找到 5 张符合条件的图片：

1. 🏔️ 雪山日出 - 6000x4000 横向
   适合: Hero 背景、Banner
   摄影师: John Doe

2. 🌲 森林小径 - 4000x6000 纵向
   适合: 文章配图、手机壁纸
   摄影师: Jane Smith
```

### 4. 集成代码
根据用户技术栈提供代码（见下方代码示例）：
- HTML + 响应式图片
- React/Vue 组件
- 纯 URL（CSS background-image）

### 5. 提醒规则
首次使用时告知用户：
- ✅ 需要在显著位置链接到 Pexels（API 使用要求）
- ✅ 建议为摄影师署名（"Photo by 摄影师 on Pexels" 并链接到照片页）
- ✅ 不可将 Pexels 内容做成壁纸类应用（API 条款禁止）

---

## ⚡ 核心规则（必读）

**违反这些规则将导致 API 使用条款问题：**

### 1. 认证方式：裸 Key ⚠️
`Authorization` 头直接放 API Key，**不加**任何前缀：

```bash
✅ 正确: -H "Authorization: $PEXELS_API_KEY"
❌ 错误: -H "Authorization: Bearer $PEXELS_API_KEY"  （多余前缀）
❌ 错误: -H "Authorization: Client-ID $PEXELS_API_KEY"  （多余的 Client-ID 前缀）
```

### 2. Hotlinking（直接链接）
**直接使用返回的 URL**（`images.pexels.com` CDN），不要下载后重新托管：

```html
✅ <img src="https://images.pexels.com/photos/xxx/pexels-photo-xxx.jpeg?auto=compress&cs=tinysrgb&w=800">
❌ <img src="https://your-cdn.com/saved-image.jpg">
```

### 3. Pexels 署名（API 使用要求）
每次使用 API 获取的内容需在显著位置提供指向 Pexels 的链接（文字链接或官方 logo），并尽可能署名摄影师：

```html
<div class="credit">
  <a href="https://www.pexels.com">Pexels</a> ·
  Photo by <a href="{photographer_url}">{photographer}</a>
  on <a href="{url}">Pexels</a>
</div>
```

### 4. 禁止用途
不可将 Pexels 内容作为壁纸应用（wallpaper app）提供——这是 API 条款明确禁止的"复制 Pexels 核心功能"行为。

---

## 📚 核心 API 端点

### 搜索照片 `/v1/search` （最常用）

```bash
GET https://api.pexels.com/v1/search?query={关键词}&orientation={方向}&per_page={数量}
Authorization: YOUR_API_KEY
```

**常用参数：**
- `query` (必填): 搜索关键词，如 `mountain`, `office`, `food`
- `orientation`: `landscape`(横向), `portrait`(纵向), `square`(方形) ⚠️ 是 `square` 不是 `squarish`
- `per_page`: 每页数量（1-80，默认 15），建议 5-10
- `size`: 最小尺寸过滤 - `large`(24MP)/`medium`(12MP)/`small`(4MP)
- `color`: 颜色过滤，支持颜色名（`red`, `blue`, `black` 等）或 hex 码（如 `#ffffff`）
- `locale`: 语言环境（如 `en-US`, `ja-JP`），共 28 种
- `page`: 页码（默认 1）

**返回数据结构：**
```json
{
  "page": 1,
  "per_page": 15,
  "total_results": 1000,
  "next_page": "https://api.pexels.com/v1/search?query=mountain&page=2",
  "photos": [{
    "id": 123456,
    "width": 6000,
    "height": 4000,
    "url": "https://www.pexels.com/photo/xxx-123456/",
    "photographer": "Photographer Name",
    "photographer_url": "https://www.pexels.com/@photographer",
    "avg_color": "#6E6259",
    "alt": "照片描述文本",
    "src": {
      "original": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg",
      "large2x": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940",
      "large": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
      "medium": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&h=350",
      "small": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&h=130",
      "portrait": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=1200&w=800",
      "landscape": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&fit=crop&h=627&w=1200",
      "tiny": "https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&dpr=1&fit=crop&h=200&w=280"
    }
  }]
}
```

### 精选照片 `/v1/curated`

```bash
GET https://api.pexels.com/v1/curated?per_page={数量}&page={页码}
Authorization: YOUR_API_KEY
```

编辑实时精选（至少每小时更新），适合背景图、占位符场景。参数仅 `per_page` 和 `page`。

### 单张照片 `/v1/photos/:id`

根据 ID 获取照片详情：

```bash
GET https://api.pexels.com/v1/photos/123456
Authorization: YOUR_API_KEY
```

---

## 🎬 视频搜索

认证方式与限额同照片（裸 Key header，200次/小时）。⚠️ 旧路径 `https://api.pexels.com/videos/` 已弃用，统一用 `/v1/videos/` 前缀。

### 搜索视频 `/v1/videos/search`

```bash
GET https://api.pexels.com/v1/videos/search?query={关键词}&orientation={方向}&per_page={数量}
Authorization: YOUR_API_KEY
```

**常用参数：**
- `query` (必填): 搜索关键词
- `orientation`: `landscape`/`portrait`/`square`
- `size`: 最小分辨率过滤 - `large`(4K)/`medium`(Full HD)/`small`(HD)
- `locale` / `page` / `per_page`: 同照片搜索（per_page 默认 15，最大 80）

**热门视频 `/v1/videos/popular`** 参数不同：`min_width`, `min_height`, `min_duration`, `max_duration`, `page`, `per_page`。

**按 ID 获取 `/v1/videos/videos/:id`**：返回单个视频对象。

**返回数据结构（`videos` 数组）：**
```json
{
  "page": 1,
  "per_page": 15,
  "total_results": 500,
  "videos": [{
    "id": 123456,
    "width": 3840,
    "height": 2160,
    "url": "https://www.pexels.com/video/xxx-123456/",
    "image": "https://images.pexels.com/videos/123456/xxx.jpg?auto=compress&cs=tinysrgb&fit=crop&h=630&w=1200",
    "duration": 15,
    "user": { "id": 789, "name": "Videographer Name", "url": "https://www.pexels.com/@videographer" },
    "video_files": [{
      "id": 654321,
      "quality": "hd",
      "file_type": "video/mp4",
      "width": 1920,
      "height": 1080,
      "fps": 30.0,
      "link": "https://videos.pexels.com/video-files/123456/xxx.mp4"
    }],
    "video_pictures": [{ "id": 1, "picture": "https://images.pexels.com/videos/123456/xxx-frame.jpg", "nr": 0 }]
  }]
}
```

**video_files 说明：**
- 数组含同一视频的多种分辨率（4K→SD）与格式（mp4 / hls m3u8）
- `quality`: `hd`/`sd`，4K 大文件也标 `hd`；hls 变体的 `width`/`height` 为 null
- 选择建议: 网页背景用 1080p (`video/mp4`)，`file_type` 过滤格式，`fps` 确认帧率
- `image` 字段是视频封面截图，可直接用作海报帧
- 热链接 `link` 与照片规则相同：直接使用返回 URL，不要重新托管

### Python: 搜索视频

```python
import os, requests

def search_videos(query: str, orientation: str = 'landscape', per_page: int = 5) -> list:
    """搜索 Pexels 视频，返回每个视频最佳的 1080p mp4 文件"""
    res = requests.get(
        'https://api.pexels.com/v1/videos/search',
        params={'query': query, 'orientation': orientation, 'per_page': per_page},
        headers={'Authorization': os.environ['PEXELS_API_KEY']}  # 裸 Key，无前缀
    )
    results = []
    for video in res.json()['videos']:
        files = [f for f in video['video_files'] if f['file_type'] == 'video/mp4']
        # 按 1080p 优先、面积最接近原则选文件
        best = min(files, key=lambda f: abs(f['width'] * f['height'] - 1920 * 1080), default=None)
        results.append({
            'duration': video['duration'],       # 秒
            'poster': video['image'],            # 封面截图 URL
            'link': best['link'] if best else None,
            'videographer': video['user']['name']
        })
    return results
```

---

## 🖼️ 图片 URL 处理

### 尺寸选择

| 变体 | 尺寸 | 用途 |
|-----|------|------|
| `tiny` | 280x200 裁剪 | 缩略图、占位符 |
| `small` | 高 130px | 列表项、小图 |
| `medium` | 高 350px | 卡片图 |
| `large` | 940x650 | **网页默认选择** |
| `large2x` | 940x650 @2x | 高 DPI 屏幕 |
| `portrait` | 800x1200 裁剪 | 纵向固定比例 |
| `landscape` | 1200x627 裁剪 | 横向固定比例（OG 图等） |
| `original` | 原始分辨率 | 全屏展示、下载 |

### 动态调整（CDN 参数）

返回的 `src` URL 均带 `auto=compress&cs=tinysrgb`，可在其基础上追加参数自定义尺寸：

```bash
# 原始 src URL 已含压缩参数，追加 & 即可
https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&w=800&h=600&fit=crop
```

**常用参数：**
- `w` / `h`: 宽度/高度 (px)
- `fit`: `crop`(裁剪填充) / 不指定则按宽高比缩放
- `dpr`: 设备像素比（如 `dpr=2`）
- `auto=compress&cs=tinysrgb`: 压缩与色彩空间优化（URL 已默认携带，保留即可）

### avg_color 占位符

每张照片返回 `avg_color`（hex），可直接作为图片加载前的背景占位色，无需额外计算：

```html
<div style="background:#6E6259">
  <img src="..." loading="lazy" onload="this.parentElement.style.background='transparent'">
</div>
```

---

## 💻 常用场景代码

### TypeScript: 搜索照片

```typescript
interface PexelsPhoto {
  id: number;
  width: number;
  height: number;
  url: string;              // Pexels 照片页（署名链接用）
  photographer: string;
  photographer_url: string;
  avg_color: string;
  alt: string;
  src: { original: string; large2x: string; large: string; medium: string; small: string; portrait: string; landscape: string; tiny: string; };
}

async function searchPhotos(
  query: string,
  options: { orientation?: 'landscape' | 'portrait' | 'square'; perPage?: number; size?: 'large' | 'medium' | 'small'; color?: string; } = {}
): Promise<{ total_results: number; photos: PexelsPhoto[] }> {
  const params = new URLSearchParams({
    query,
    per_page: String(options.perPage ?? 10),
    ...(options.orientation && { orientation: options.orientation }),
    ...(options.size && { size: options.size }),
    ...(options.color && { color: options.color }),
  });

  const res = await fetch(`https://api.pexels.com/v1/search?${params}`, {
    headers: { Authorization: process.env.PEXELS_API_KEY! },  // 裸 Key，无前缀
  });
  return res.json();
}

// 使用示例
const { photos } = await searchPhotos('mountain', { orientation: 'landscape', perPage: 5 });
photos.forEach(p => {
  console.log(p.src.large);       // 网页用图片 URL
  console.log(p.photographer);    // 摄影师（建议署名）
  console.log(p.avg_color);       // 加载占位色
});
```

### Python: 获取精选照片

```python
import os, requests

def get_curated_photos(per_page: int = 5) -> list:
    """获取编辑精选照片（每小时更新，适合背景/占位符）"""
    res = requests.get(
        'https://api.pexels.com/v1/curated',
        params={'per_page': per_page},
        headers={'Authorization': os.environ['PEXELS_API_KEY']}  # 裸 Key，无前缀
    )
    return res.json()['photos']

# 使用示例
photos = get_curated_photos(3)
print(photos[0]['src']['large'])          # 网页用图片 URL
print(photos[0]['photographer'])          # 摄影师（建议署名）
print(photos[0]['avg_color'])             # 加载占位色
```

### 生成带署名的 HTML

```python
def generate_img_html(photo: dict, width: int = 800) -> str:
    """生成带 Pexels 署名的图片 HTML

    ⚠️ 基于原始 URL 追加 CDN 参数（& 开头），保留 auto=compress&cs=tinysrgb
    """
    url = f"{photo['src']['original']}?auto=compress&cs=tinysrgb&w={width}"

    return f'''<img src="{url}" alt="{photo.get('alt', '')}" loading="lazy" style="background:{photo['avg_color']}">
<div class="credit">Photo by <a href="{photo['photographer_url']}">{photo['photographer']}</a>
on <a href="{photo['url']}">Pexels</a></div>'''
```

### HTML: 响应式图片

```html
<img
  src="https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&w=800"
  srcset="
    https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&w=400 400w,
    https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&w=800 800w,
    https://images.pexels.com/photos/123456/pexels-photo-123456.jpeg?auto=compress&cs=tinysrgb&w=1200 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Photo by Photographer on Pexels"
  loading="lazy"
>
```

---

## ❌ 错误处理

| 状态码 | 原因 | 解决方案 |
|-------|------|---------|
| 400 | 缺少必需参数 | 检查 `query` 等必填参数 |
| 401 | API Key 无效 | 检查 Key 是否正确复制（裸 Key，无前缀） |
| 403 | Key 被禁用 | 检查账户状态 |
| 429 | 超过速率限制 | 200次/小时、20000次/月，客户端自行计数 |

剩余额度可通过响应头查询（**仅在 2xx 响应中出现**，429 响应没有额度头，需客户端自行计数）：
- `X-Ratelimit-Limit`: 总额度
- `X-Ratelimit-Remaining`: 剩余请求数
- `X-Ratelimit-Reset`: 重置时间（UNIX 时间戳）

```python
def handle_pexels_error(status: int) -> str:
    errors = {
        400: '缺少必需参数：检查 query 等必填参数',
        401: '认证失败：检查 PEXELS_API_KEY（裸 Key，无 Bearer/Client-ID 前缀）',
        403: 'Key 被禁用：检查 Pexels 账户状态',
        429: '速率限制：200次/小时，请等待后重试（429 响应无额度头，需客户端计数）'
    }
    return errors.get(status, f'未知错误: {status}')
```

---

## ✅ 最佳实践清单

**执行前检查：**
- [ ] **配置检查** - 验证 `PEXELS_API_KEY` 环境变量已设置

**必须遵守：**
- [ ] **认证用裸 Key** - `Authorization: KEY`，不加 `Bearer`/`Client-ID` 前缀
- [ ] **Hotlinking** - 直接使用 `images.pexels.com` 返回的 URL，不要重新托管
- [ ] **Pexels 署名** - 显著位置链接到 Pexels，摄影师署名（`photographer_url` + `url` 字段）
- [ ] **禁止壁纸应用** - 不可将内容做成 wallpaper app

**强烈推荐：**
- [ ] 选择合适尺寸（`large`/`medium`/`small`），高 DPI 用 `large2x`
- [ ] 使用 `avg_color` 作为加载占位背景色
- [ ] 使用 `loading="lazy"` 实现懒加载
- [ ] 429 时客户端自行计数限流（该响应无额度头）
- [ ] 视频：照片与视频共用同一限额，搜索时按需选择端点（`/v1/search` vs `/v1/videos/search`）
