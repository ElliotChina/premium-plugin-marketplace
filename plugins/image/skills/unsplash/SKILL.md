---
name: unsplash
description: Search and download free high-quality photos from Unsplash for any project. **TRIGGER when users need:** stock photos, hero images, backgrounds, banners, thumbnails, cover images, or mention Unsplash/图片/照片/素材/找图. Use when building websites, apps, presentations, or marketing materials requiring visual content — even if Unsplash isn't explicitly named.
---

# Unsplash Photo Skill

快速搜索和获取免费高质量照片，用于网站、应用、演示文稿等项目。

## ⚠️ 前置要求

**检查环境变量（每次使用前必做）：**

```bash
# 快速检查
[ -z "$UNSPLASH_ACCESS_KEY" ] && echo "❌ 需要配置 Unsplash Access Key"
```

**如果未配置，提示用户：**
- 获取 Key: https://unsplash.com/developers → 创建应用 → 复制 Access Key
- 配置命令: `export UNSPLASH_ACCESS_KEY=your_key_here`
- API 限制: Demo 50次/小时, Production 5000次/小时

<details>
<summary>📖 详细配置步骤（点击展开）</summary>

1. 访问 https://unsplash.com/developers
2. 登录/注册 Unsplash 账号
3. 创建新应用（Application）
4. 复制 **Access Key**（不是 Secret Key）

**永久配置：**
```bash
# macOS/Linux
echo 'export UNSPLASH_ACCESS_KEY=your_key' >> ~/.zshrc
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
curl "https://api.unsplash.com/search/photos?query=mountain&orientation=landscape&per_page=5" \
  -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY"

# 随机照片（适合背景/占位符）
curl "https://api.unsplash.com/photos/random?query=nature&orientation=landscape&count=3" \
  -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY"
```

**参数选择建议：**
- `orientation`: `landscape`(横向-适合hero/banner), `portrait`(纵向-适合手机/文章配图), `squarish`(方形-适合头像/缩略图)
- `color`: `blue/red/green/black_and_white` 等
- `per_page`: 建议 5-10 张供用户选择

### 3. 展示选项
向用户展示搜索结果：
- **图片预览**: 使用 `urls.small` 或 `urls.thumb`
- **推荐用途**: 根据尺寸/方向说明适合场景
- **摄影师信息**: 用于署名

示例格式：
```
找到 5 张符合条件的图片：

1. 🏔️ 雪山日出 - 6000x4000 横向
   适合: Hero 背景、Banner
   摄影师: John Doe (@johndoe)
   
2. 🌲 森林小径 - 4000x6000 纵向
   适合: 文章配图、手机壁纸
   摄影师: Jane Smith (@janesmith)
```

### 4. 集成代码
根据用户技术栈提供代码（见下方代码示例）：
- HTML + 响应式图片
- React/Vue 组件
- 纯 URL（CSS background-image）

### 5. 提醒规则
首次使用时告知用户：
- ✅ 必须保留 URL 中的 `ixid` 参数
- ✅ 建议为摄影师署名
- ✅ 直接使用 Unsplash URL，不要重新托管

---

## ⚡ 核心规则（必读）

**违反这些规则将导致 API 使用条款问题：**

### 1. 保留 ixid 参数 ⚠️
API 返回的 URL 包含 `ixid`，**必须保留**：

```
✅ 正确: https://images.unsplash.com/photo-xxx?ixid=abc123&w=800
❌ 错误: https://images.unsplash.com/photo-xxx?w=800  （移除了 ixid）
```

### 2. Hotlinking（直接链接）
**必须**直接使用返回的 URL，**不要**下载后重新托管：

```html
✅ <img src="https://images.unsplash.com/photo-xxx?w=800">
❌ <img src="https://your-cdn.com/saved-image.jpg">
```

### 3. 摄影师署名（强烈推荐）
```html
Photo by <a href="https://unsplash.com/@username?utm_source=your_app&utm_medium=referral">
  Photographer Name
</a> on <a href="https://unsplash.com?utm_source=your_app&utm_medium=referral">Unsplash</a>
```

---

## 📚 核心 API 端点

### 搜索照片 `/search/photos` （最常用）

```bash
GET https://api.unsplash.com/search/photos?query={关键词}&orientation={方向}&per_page={数量}
Authorization: Client-ID YOUR_ACCESS_KEY
```

**常用参数：**
- `query` (必填): 搜索关键词，如 `mountain`, `office`, `food`
- `orientation`: `landscape`(横向), `portrait`(纵向), `squarish`(方形)
- `per_page`: 每页数量（1-30），建议 5-10
- `color`: 颜色过滤 - `blue`, `red`, `green`, `black_and_white` 等
- `order_by`: `relevant`(相关度，默认), `latest`(最新)

**返回数据结构：**
```json
{
  "total": 1000,
  "results": [{
    "id": "abc123",
    "urls": {
      "raw": "https://images.unsplash.com/photo-xxx?ixid=xyz",
      "regular": "https://images.unsplash.com/photo-xxx?ixid=xyz&w=1080",
      "small": "https://images.unsplash.com/photo-xxx?ixid=xyz&w=400"
    },
    "user": {
      "name": "Photographer Name",
      "username": "username"
    },
    "width": 6000,
    "height": 4000
  }]
}
```

### 随机照片 `/photos/random`

```bash
GET https://api.unsplash.com/photos/random?query={关键词}&count={数量}
Authorization: Client-ID YOUR_ACCESS_KEY
```

适合背景图、占位符场景。

**参数：**
- `query`: 可选，过滤主题
- `orientation`: 方向过滤
- `count`: 数量（1-30）

---

## 🖼️ 图片 URL 处理

### 尺寸选择

| 变体 | 尺寸 | 用途 |
|-----|------|------|
| `thumb` | 200px | 缩略图、占位符 |
| `small` | 400px | 列表项、小图 |
| `regular` | 1080px | **网页默认选择** |
| `full` | 原始(压缩) | 全屏展示、下载 |
| `raw` | 原始 | 自定义尺寸处理 |

### 动态调整（在 raw URL 上追加参数）

```bash
# 原始: https://images.unsplash.com/photo-abc?ixid=xyz123

# 自定义尺寸和格式（用 & 追加参数）
https://images.unsplash.com/photo-abc?ixid=xyz123&w=800&h=600&fit=crop&fm=webp&q=85
```

**常用参数：**
- `w` / `h`: 宽度/高度 (px)
- `fit`: `crop`(裁剪), `clamp`(填充), `scale`(缩放)
- `fm`: 格式 - `webp`, `jpg`, `png`
- `q`: 质量 (1-100)，建议 80-85
- `auto=format`: 自动选择最佳格式

---

## 💻 常用场景代码

### TypeScript: 搜索照片

```typescript
interface UnsplashPhoto {
  id: string;
  urls: { raw: string; full: string; regular: string; small: string; thumb: string; };
  user: { name: string; username: string; };
  description: string | null;
  width: number;
  height: number;
  color: string;
  blur_hash: string;
}

async function searchPhotos(
  query: string,
  options: { orientation?: 'landscape' | 'portrait' | 'squarish'; perPage?: number; color?: string; } = {}
): Promise<{ total: number; results: UnsplashPhoto[] }> {
  const params = new URLSearchParams({
    query,
    per_page: String(options.perPage ?? 10),
    ...(options.orientation && { orientation: options.orientation }),
    ...(options.color && { color: options.color }),
  });

  const res = await fetch(`https://api.unsplash.com/search/photos?${params}`, {
    headers: { Authorization: `Client-ID ${process.env.UNSPLASH_ACCESS_KEY}` },
  });
  return res.json();
}

// 使用示例
const { results } = await searchPhotos('mountain', { orientation: 'landscape', perPage: 5 });
results.forEach(p => {
  // ⚠️ 重要：使用图片 URL 时保留其中的 ixid 参数（如有）
  console.log(p.urls.regular); // 已包含 ixid
});
```

### Python: 获取随机照片

```python
import os, requests

def get_random_photo(query: str = 'nature', orientation: str = 'landscape') -> dict:
    """获取一张随机照片
    
    ⚠️ 使用返回的 URL 时必须保留 ixid 参数（API 使用条款要求）
    """
    res = requests.get(
        'https://api.unsplash.com/photos/random',
        params={'query': query, 'orientation': orientation, 'count': 1},
        headers={'Authorization': f"Client-ID {os.environ['UNSPLASH_ACCESS_KEY']}"}
    )
    data = res.json()
    return data[0] if isinstance(data, list) else data

# 使用示例
photo = get_random_photo('landscape')
# ⚠️ urls.raw 中的 ixid 参数必须保留，添加自定义参数时使用 & 追加
url = photo['urls']['raw'] + '&w=800&fm=webp&q=85'  # 正确：用 & 追加
print(photo['urls']['regular'])  # 图片 URL（已包含 ixid）
print(photo['user']['name'])     # 摄影师（建议署名）
```

### 生成带署名的 HTML

```python
def generate_img_html(photo: dict, width: int = 800, app_name: str = 'my_app') -> str:
    """生成带署名的图片 HTML
    
    ⚠️ 关键：raw URL 已包含 ixid 参数，使用 & 追加自定义参数
    """
    # 正确：保留 raw URL 中的 ixid，用 & 追加参数
    url = f"{photo['urls']['raw']}&w={width}&q=85&auto=format"
    
    user_url = f"https://unsplash.com/@{photo['user']['username']}?utm_source={app_name}&utm_medium=referral"
    
    return f'''<img src="{url}" alt="{photo.get('alt_description', '')}" loading="lazy">
<div class="credit">Photo by <a href="{user_url}">{photo['user']['name']}</a></div>'''
```

### HTML: 响应式图片

```html
<img
  src="https://images.unsplash.com/photo-xxx?ixid=abc&w=800&h=600&fit=crop&q=85"
  srcset="
    https://images.unsplash.com/photo-xxx?ixid=abc&w=400&h=300&fit=crop&q=80 400w,
    https://images.unsplash.com/photo-xxx?ixid=abc&w=800&h=600&fit=crop&q=85 800w,
    https://images.unsplash.com/photo-xxx?ixid=abc&w=1200&h=900&fit=crop&q=85 1200w
  "
  sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  alt="Photo by Photographer on Unsplash"
  loading="lazy"
>
```

---

## ❌ 错误处理

| 状态码 | 原因 | 解决方案 |
|-------|------|---------|
| 401 | Access Key 无效 | 检查 Key 是否正确复制 |
| 403 | 超过速率限制 | Demo: 50次/小时, Production: 5000次/小时 |
| 404 | 照片不存在 | 检查 ID 是否正确 |
| 422 | 参数错误 | 检查参数格式 |

```python
def handle_unsplash_error(status: int) -> str:
    errors = {
        401: '认证失败：检查 UNSPLASH_ACCESS_KEY',
        403: '速率限制：请等待后重试',
        404: '资源不存在',
        422: '参数错误：检查请求参数'
    }
    return errors.get(status, f'未知错误: {status}')
```

---

## ✅ 最佳实践清单

**执行前检查：**
- [ ] **配置检查** - 验证 `UNSPLASH_ACCESS_KEY` 环境变量已设置

**必须遵守：**
- [ ] **保留 ixid 参数** - URL 中的 `ixid` 是 API 使用条款要求
- [ ] **Hotlinking** - 直接使用返回的 URL，不要重新托管

**强烈推荐：**
- [ ] 添加摄影师署名（使用 `utm_source` 和 `utm_medium` 参数）
- [ ] 选择合适尺寸（`regular`/`small`/`thumb`）
- [ ] 使用 `loading="lazy"` 实现懒加载

**高级功能（见 references/advanced.md）：**
- [ ] BlurHash 占位符
- [ ] 响应式图片优化
- [ ] 缓存策略
- [ ] 完整 API 端点参考

---

## 📖 参考资源

- [Unsplash API 文档](https://unsplash.com/documentation)
- [获取 Access Key](https://unsplash.com/developers)
- [高级功能参考](references/advanced.md) - BlurHash、性能优化、完整 API 端点
