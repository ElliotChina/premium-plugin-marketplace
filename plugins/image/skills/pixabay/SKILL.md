---
name: pixabay
description: Search and download free high-quality photos, illustrations, vectors and videos from Pixabay for any project. **TRIGGER when users need:** stock photos, hero images, backgrounds, banners, thumbnails, cover images, illustrations, vectors, stock videos, footage, or mention Pixabay/图片/照片/素材/找图/视频. Use when building websites, apps, presentations, or marketing materials requiring visual content — even if Pixabay isn't explicitly named.
---

# Pixabay Photo Skill

快速搜索和获取免费高质量照片、插画、矢量图与视频，用于网站、应用、演示文稿等项目。

## ⚠️ 前置要求

**检查环境变量（每次使用前必做）：**

```bash
# 快速检查
[ -z "$PIXABAY_API_KEY" ] && echo "❌ 需要配置 Pixabay API Key"
```

**如果未配置，提示用户：**
- 获取 Key: https://pixabay.com/api/docs/ → 登录后即可见（免费注册即得）
- 配置命令: `export PIXABAY_API_KEY=your_key_here`
- API 限制: 100次/60秒（按 Key 计数，超限返回 429）

<details>
<summary>📖 详细配置步骤（点击展开）</summary>

1. 访问 https://pixabay.com/ 并注册/登录
2. 访问 https://pixabay.com/api/docs/ ，页面中"Your API key"处直接显示 Key

**永久配置：**
```bash
# macOS/Linux
echo 'export PIXABAY_API_KEY=your_key' >> ~/.zshrc
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
- **偏好**: 横向/纵向？照片/插画/矢量？色调？数量？

### 2. 搜索图片
根据需求选择合适的 API 调用：

```bash
# 搜索照片（推荐）
curl "https://pixabay.com/api/?key=$PIXABAY_API_KEY&q=mountain&orientation=horizontal&image_type=photo&per_page=10"

# 编辑精选（适合背景/占位符）
curl "https://pixabay.com/api/?key=$PIXABAY_API_KEY&editors_choice=true&orientation=horizontal&per_page=10"
```

**参数选择建议：**
- `orientation`: `horizontal`(横向-适合hero/banner), `vertical`(纵向-适合手机/文章配图)
- `image_type`: `photo`(照片), `illustration`(插画), `vector`(矢量图), `all`(默认)
- `per_page`: 3-200，建议 5-10 张供用户选择
- `category`: `nature`, `people`, `animals`, `food`, `travel`, `backgrounds` 等
- `safesearch`: 面向全年龄内容时开启

### 3. 展示选项
向用户展示搜索结果：
- **图片预览**: 使用 `webformatURL`（640px）或 `previewURL`（150px）
- **推荐用途**: 根据尺寸/方向说明适合场景
- **作者信息**: 用于署名

示例格式：
```
找到 5 张符合条件的图片：

1. 🏔️ 雪山日出 - 6000x4000 横向 照片
   适合: Hero 背景、Banner
   作者: johndoe

2. 🌲 森林小径 - 4000x6000 纵向 照片
   适合: 文章配图、手机壁纸
   作者: janesmith
```

### 4. 集成图片
⚠️ **返回的 URL 仅 24 小时有效，禁止永久 hotlinking。**
正确做法是下载图片到用户项目/自有服务器后引用本地路径：

```bash
# 下载到本地（largeImageURL 最大 1280px；原图/1920px URL 需官方审批才能访问）
curl -L -o mountain.jpg "$LARGE_IMAGE_URL"
```

然后在代码中引用本地文件：
```html
<img src="/assets/images/mountain.jpg" alt="作者 johndoe on Pixabay" loading="lazy">
```

### 5. 提醒规则
首次使用时告知用户：
- ✅ 展示搜索结果时需说明图片来自 Pixabay（API 免费使用的唯一要求）
- ✅ 返回的 URL 仅 24 小时有效，长期使用必须下载到本地
- ✅ API 响应需缓存 24 小时，不要高频重复请求

---

## ⚡ 核心规则（必读）

**违反这些规则将导致 API 使用条款问题：**

### 1. 认证方式：query 参数 ⚠️
API Key 通过 `key` **查询参数**传递，**不是**请求头：

```bash
✅ 正确: curl "https://pixabay.com/api/?key=$PIXABAY_API_KEY&q=mountain"
❌ 错误: -H "Authorization: $PIXABAY_API_KEY"  （header 方式无效）
```

### 2. 禁止永久 Hotlinking ⚠️
返回的 URL 仅 24 小时有效，仅允许临时展示。
长期使用（网页/应用中引用）**必须下载图片到自己的服务器**：

```html
✅ <img src="/assets/images/local-saved.jpg">   （下载后本地引用）
⚠️ <img src="https://pixabay.com/get/xxx_640.jpg">  （仅限 24h 内临时展示）
```

### 3. 来源标注（API 免费使用的唯一要求）
展示搜索结果时说明图片来自 Pixabay，建议附作者与原图链接：

```html
<div class="credit">
  Image by <a href="{userURL 或 pageURL}">{user}</a> on <a href="https://pixabay.com/">Pixabay</a>
</div>
```

### 4. 缓存与请求频率
- API 响应**必须缓存 24 小时**，同一查询勿反复请求
- 限流 100次/60秒，按 Key 计数（非按 IP）
- API 面向真实人类使用，禁止高频自动化查询和系统性批量下载

---

## 📚 核心 API 端点

### 搜索图片 `https://pixabay.com/api/` （唯一端点，含单图查询）

```bash
GET https://pixabay.com/api/?key={KEY}&q={关键词}&orientation={方向}&per_page={数量}
```

**常用参数：**
- `key` (必填): API Key
- `q`: 搜索关键词（URL 编码，≤100 字符），省略则返回全部图片
- `lang`: ISO 639-1 语言代码（如 `en`, `de`, `zh`），默认 `en`
- `id`: 按 ID 获取单张图片（等同"详情"端点，Pixabay 无独立的 `/photos/:id` 路径）
- `image_type`: `all`(默认)/`photo`/`illustration`/`vector`
- `orientation`: `all`(默认)/`horizontal`/`vertical`
- `category`: 如 `backgrounds`, `nature`, `people`, `animals`, `food`, `travel`
- `min_width` / `min_height`: 最小尺寸过滤（默认 0）
- `colors`: 逗号分隔 - `grayscale`, `transparent`, `red`, `blue`, `white` 等
- `editors_choice`: 编辑精选，`true`/`false`（默认 false）
- `safesearch`: 全年龄内容过滤（默认 false）
- `order`: `popular`(默认)/`latest`
- `page`: 页码（默认 1）
- `per_page`: 每页数量（**3-200**，默认 20）

**返回数据结构：**
```json
{
  "total": 10000,
  "totalHits": 500,
  "hits": [{
    "id": 123456,
    "pageURL": "https://pixabay.com/photos/mountain-123456/",
    "type": "photo",
    "tags": "mountain, landscape, snow",
    "previewURL": "https://cdn.pixabay.com/photo/xxx_150.jpg",
    "previewWidth": 150,
    "previewHeight": 100,
    "webformatURL": "https://cdn.pixabay.com/photo/xxx_640.jpg",
    "webformatWidth": 640,
    "webformatHeight": 427,
    "largeImageURL": "https://cdn.pixabay.com/photo/xxx_1280.jpg",
    "imageWidth": 6000,
    "imageHeight": 4000,
    "imageSize": 4500000,
    "views": 100000,
    "downloads": 50000,
    "likes": 2000,
    "user_id": 789,
    "user": "johndoe",
    "userImageURL": "https://cdn.pixabay.com/user/xxx_250.jpg"
  }]
}
```

> `totalHits` 上限 500（即使 `total` 更大）。`fullHDURL`（1920px）与 `imageURL`（原图）仅官方审批的完整 API 权限可见，普通 Key 拿到的最大尺寸是 `largeImageURL`（1280px）。

### 搜索视频 `https://pixabay.com/api/videos/`

认证方式同图片（`key` query 参数），共享同一限流额度（100次/60秒）：

```bash
GET https://pixabay.com/api/videos/?key={KEY}&q={关键词}&video_type=footage&per_page=10
```

**常用参数：**
- `q`, `lang`, `id`, `category`, `min_width`/`min_height`, `editors_choice`, `safesearch`, `order`, `page`, `per_page`: 同图片搜索
- `video_type`: `all`(默认)/`animation`(动画)/`film`(影片)/`footage`(实拍素材)

**返回数据结构（`hits` 数组）：**
```json
{
  "total": 5000,
  "totalHits": 500,
  "hits": [{
    "id": 654321,
    "pageURL": "https://pixabay.com/videos/ocean-waves-654321/",
    "type": "footage",
    "tags": "ocean, waves, sea",
    "duration": 12,
    "views": 50000,
    "downloads": 8000,
    "likes": 300,
    "user": "videomaker",
    "user_id": 456,
    "userURL": "https://pixabay.com/users/videomaker-456/",
    "videos": {
      "large":  { "url": "https://cdn.pixabay.com/video/xxx_large.mp4", "width": 3840, "height": 2160, "size": 45000000 },
      "medium": { "url": "https://cdn.pixabay.com/video/xxx_medium.mp4", "width": 1920, "height": 1080, "size": 12000000 },
      "small":  { "url": "https://cdn.pixabay.com/video/xxx_small.mp4", "width": 1280, "height": 720, "size": 5000000 },
      "tiny":   { "url": "https://cdn.pixabay.com/video/xxx_tiny.mp4", "width": 960, "height": 540, "size": 2000000 }
    }
  }]
}
```

**视频尺寸说明：**
- `large` (~4K) 部分视频才有；`medium` (~1080p) / `small` (~720p) / `tiny` (~960x540) **所有视频都提供**，优先从 `medium` 开始取
- 每档含 `url` / `width` / `height` / `size`（字节数），可按体积预判下载量
- ⚠️ 与图片相同：禁止永久 hotlinking。视频允许嵌入播放器，但仍**推荐自托管**——下载到本地使用；下载时在 URL 后加 `&download=1` 触发浏览器下载

### Python: 搜索并下载视频到本地

```python
import os, pathlib, requests

def search_and_download_videos(query: str, dest_dir: str = 'assets/videos',
                               video_type: str = 'footage', per_page: int = 3) -> list:
    """搜索 Pixabay 视频并下载 1080p 版本到本地

    ⚠️ 视频同样禁止永久 hotlinking（推荐自托管），下载到本地使用
    """
    res = requests.get('https://pixabay.com/api/videos/', params={
        'key': os.environ['PIXABAY_API_KEY'],  # ⚠️ query 参数认证，非 header
        'q': query, 'video_type': video_type, 'per_page': per_page,
    })
    saved = []
    for hit in res.json()['hits']:
        rendition = hit['videos'].get('medium') or hit['videos'].get('small')  # medium 不一定有，逐级回退
        if not rendition:
            continue
        path = pathlib.Path(dest_dir) / f"{hit['id']}.mp4"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(requests.get(rendition['url'], stream=True).content)
        saved.append({'file': str(path), 'duration': hit['duration'], 'user': hit['user']})
    return saved

# 使用示例
for item in search_and_download_videos('ocean waves'):
    print(item['file'], '-', f"{item['duration']}秒, 作者 {item['user']} on Pixabay")
```

---

## 🖼️ 图片 URL 处理

### 尺寸选择

| 字段 | 最大尺寸 | 用途 |
|-----|---------|------|
| `previewURL` | 150px | 缩略图、占位符 |
| `webformatURL` | 640px (`_640`) | 列表项、卡片图、**网页默认选择** |
| `largeImageURL` | 1280px (`_1280`) | Hero/Banner、本地下载首选 |
| `fullHDURL` | 1920px | ⚠️ 需官方审批权限 |
| `imageURL` | 原始 | ⚠️ 需官方审批权限 |

### 动态调整（改文件名后缀）

`webformatURL` 中的 `_640` 后缀可替换来获取其他尺寸：

```bash
# 原始: https://cdn.pixabay.com/photo/xxx_640.jpg

# 换成其他高度（宽度按比例缩放）
https://cdn.pixabay.com/photo/xxx_180.jpg   # 高 180px
https://cdn.pixabay.com/photo/xxx_340.jpg   # 高 340px
https://cdn.pixabay.com/photo/xxx_960.jpg   # 最大 960x720
https://cdn.pixabay.com/photo/xxx_1280.jpg  # 最大 1280px（等同 largeImageURL）
```

---

## 💻 常用场景代码

### TypeScript: 搜索图片

```typescript
interface PixabayImage {
  id: number;
  pageURL: string;
  tags: string;
  previewURL: string;
  webformatURL: string;
  webformatWidth: number;
  webformatHeight: number;
  largeImageURL: string;
  imageWidth: number;
  imageHeight: number;
  user: string;
  user_id: number;
}

async function searchImages(
  q: string,
  options: { orientation?: 'horizontal' | 'vertical'; imageType?: 'photo' | 'illustration' | 'vector'; perPage?: number; category?: string; editorsChoice?: boolean; safeSearch?: boolean; } = {}
): Promise<{ total: number; totalHits: number; hits: PixabayImage[] }> {
  const params = new URLSearchParams({
    key: process.env.PIXABAY_API_KEY!,          // ⚠️ query 参数认证，非 header
    q,
    per_page: String(options.perPage ?? 10),
    ...(options.orientation && { orientation: options.orientation }),
    ...(options.imageType && { image_type: options.imageType }),
    ...(options.category && { category: options.category }),
    ...(options.editorsChoice && { editors_choice: 'true' }),
    ...(options.safeSearch && { safesearch: 'true' }),
  });

  const res = await fetch(`https://pixabay.com/api/?${params}`);
  return res.json();
}

// 使用示例
const { hits } = await searchImages('mountain', { orientation: 'horizontal', imageType: 'photo', perPage: 5 });
for (const img of hits) {
  console.log(img.largeImageURL);  // 1280px，下载后本地引用（URL 仅 24h 有效）
  console.log(img.user);           // 作者（建议署名）
}
```

### Python: 搜索并下载到本地

```python
import os, pathlib, requests

def search_and_download(query: str, dest_dir: str = 'assets/images',
                        orientation: str = 'horizontal', per_page: int = 5) -> list:
    """搜索 Pixabay 并下载图片到本地

    ⚠️ Pixabay 禁止永久 hotlinking（URL 仅 24h 有效），必须下载到本地使用
    """
    res = requests.get('https://pixabay.com/api/', params={
        'key': os.environ['PIXABAY_API_KEY'],  # ⚠️ query 参数认证，非 header
        'q': query, 'orientation': orientation, 'image_type': 'photo',
        'per_page': per_page,
    })
    saved = []
    for hit in res.json()['hits']:
        path = pathlib.Path(dest_dir) / f"{hit['id']}.jpg"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(requests.get(hit['largeImageURL']).content)  # 1280px 最大可用尺寸
        saved.append({'file': str(path), 'user': hit['user'], 'pageURL': hit['pageURL']})
    return saved

# 使用示例
for item in search_and_download('mountain'):
    print(item['file'], '-', f"作者 {item['user']} on Pixabay")  # 建议署名
```

### 生成带署名的 HTML

```python
def generate_img_html(hit: dict, local_path: str) -> str:
    """生成带 Pixabay 署名的图片 HTML（引用本地下载的文件）"""
    return f'''<img src="{local_path}" alt="{hit['tags']}" loading="lazy">
<div class="credit">Image by <a href="{hit['pageURL']}">{hit['user']}</a>
on <a href="https://pixabay.com/">Pixabay</a></div>'''
```

### HTML: 响应式图片（本地文件 + srcset）

```html
<!-- 下载时同时取 _640 和 _1280 两个尺寸 -->
<img
  src="/assets/images/photo-123456_1280.jpg"
  srcset="
    /assets/images/photo-123456_640.jpg 640w,
    /assets/images/photo-123456_1280.jpg 1280w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Image by johndoe on Pixabay"
  loading="lazy"
>
```

---

## ❌ 错误处理

| 状态码 | 原因 | 解决方案 |
|-------|------|---------|
| 400 | 缺少 `key` 参数 | 检查 URL 是否携带 `key=$PIXABAY_API_KEY` |
| 401 | API Key 无效 | 检查 Key 是否正确复制 |
| 404 | 图片不存在 | 检查 `id` 是否正确 |
| 429 | 超过速率限制 | 100次/60秒，等待后重试并落实 24h 缓存 |

剩余额度可通过响应头查询：`X-Ratelimit-Limit`（总额度）、`X-Ratelimit-Remaining`（剩余请求数）、`X-Ratelimit-Reset`（重置时间）。

```python
def handle_pixabay_error(status: int) -> str:
    errors = {
        400: '缺少 key 参数：检查 URL 是否携带 key=$PIXABAY_API_KEY',
        401: '认证失败：检查 PIXABAY_API_KEY',
        404: '资源不存在：检查图片 id',
        429: '速率限制：100次/60秒，等待后重试'
    }
    return errors.get(status, f'未知错误: {status}')
```

---

## ✅ 最佳实践清单

**执行前检查：**
- [ ] **配置检查** - 验证 `PIXABAY_API_KEY` 环境变量已设置

**必须遵守：**
- [ ] **认证走 query 参数** - `?key=$PIXABAY_API_KEY`，非 Authorization header
- [ ] **下载到本地使用** - URL 仅 24h 有效，禁止永久 hotlinking
- [ ] **24h 缓存响应** - 同一查询勿反复请求
- [ ] **来源标注** - 展示结果时说明来自 Pixabay，附作者署名

**强烈推荐：**
- [ ] 选择合适尺寸（`webformatURL` 640px / `largeImageURL` 1280px）
- [ ] 用 `image_type=photo` 过滤照片，需要插画/矢量时切换 `illustration`/`vector`
- [ ] 用 `views`/`downloads`/`likes` 评估图片热度
- [ ] 使用 `loading="lazy"` 实现懒加载
- [ ] 视频：用 `video_type` 过滤素材类型，从 `medium`（1080p）档取流，避免不必要的 4K 下载
