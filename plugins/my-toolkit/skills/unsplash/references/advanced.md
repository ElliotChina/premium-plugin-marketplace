# Unsplash 高级功能

## BlurHash 占位符

API 返回 `blur_hash` 字段，用于生成模糊占位符，提升加载体验。

### JavaScript 实现

```javascript
import { decode } from 'blurhash';

// 解码 blur_hash 为像素数据
const pixels = decode(photo.blur_hash, 32, 32);

// 绘制到 canvas 作为占位符
const canvas = document.createElement('canvas');
canvas.width = 32;
canvas.height = 32;
const ctx = canvas.getContext('2d');
const imageData = ctx.createImageData(32, 32);
imageData.data.set(pixels);
ctx.putImageData(imageData, 0, 0);

// 使用 canvas.toDataURL() 作为占位符 src
const placeholder = canvas.toDataURL();
```

### 使用场景

```html
<!-- 1. 先显示模糊占位符 -->
<img src="data:image/png;base64,..." style="filter: blur(10px);">

<!-- 2. 图片加载后替换 -->
<img src="https://images.unsplash.com/photo-xxx?w=800" loading="lazy" onload="this.style.opacity=1">
```

---

## 完整 API 端点参考

### 照片列表 `/photos`

获取最新或热门照片。

**参数：**
- `order_by`: `latest`/`oldest`/`popular`
- `per_page`: 每页数量（最大30）
- `page`: 页码

```bash
curl "https://api.unsplash.com/photos?order_by=popular&per_page=30" \
  -H "Authorization: Client-ID YOUR_KEY"
```

### 单张照片 `/photos/:id`

根据 ID 获取照片详情。

```bash
curl "https://api.unsplash.com/photos/abc123" \
  -H "Authorization: Client-ID YOUR_KEY"
```

### 用户照片 `/users/:username/photos`

获取特定用户的照片。

**参数：**
- `username`: 用户名
- `per_page`: 每页数量
- `order_by`: `latest`/`oldest`/`popular`

```bash
curl "https://api.unsplash.com/users/photographer/photos?per_page=10" \
  -H "Authorization: Client-ID YOUR_KEY"
```

### 下载跟踪 `/photos/:id/download`

**重要：** 当用户实际下载图片时必须调用此端点（API 使用要求）。

```bash
curl "https://api.unsplash.com/photos/abc123/download" \
  -H "Authorization: Client-ID YOUR_KEY"
```

---

## 图片 URL 高级处理

### 完整参数列表

| 参数 | 说明 | 示例 |
|-----|------|-----|
| `w` | 宽度(px) | `w=800` |
| `h` | 高度(px) | `h=600` |
| `fit` | 适配模式 | `crop`/`clamp`/`scale` |
| `fm` | 格式 | `webp`/`jpg`/`png` |
| `q` | 质量(1-100) | `q=85` |
| `dpr` | 设备像素比 | `dpr=2` |
| `auto` | 自动优化 | `auto=format` |
| `crop` | 裁剪模式 | `crop=faces`/`crop=edges` |
| `crop-h` / `crop-w` | 裁剪区域 | `crop-h=800` |
| `crop-x` / `crop-y` | 裁剪起点 | `crop-x=100` |

### 适配模式详解

- **crop**: 裁剪以填充指定尺寸
- **clamp**: 保持比例，添加边框
- **scale**: 缩放以适应尺寸（可能变形）

### 高级示例

```bash
# 1. 人脸优先裁剪
https://images.unsplash.com/photo-xxx?ixid=abc&w=400&h=400&fit=crop&crop=faces

# 2. 高 DPI 设备优化
https://images.unsplash.com/photo-xxx?ixid=abc&w=800&dpr=2&fm=webp

# 3. 渐进式加载（低质量占位符）
https://images.unsplash.com/photo-xxx?ixid=abc&w=800&q=30  # 低质量
https://images.unsplash.com/photo-xxx?ixid=abc&w=800&q=85  # 高质量

# 4. 特定区域裁剪
https://images.unsplash.com/photo-xxx?ixid=abc&crop-x=100&crop-y=50&crop-w=800&crop-h=600
```

---

## 错误处理详细指南

### 状态码说明

| 状态码 | 原因 | 解决方案 |
|-------|------|---------|
| 401 | Access Key 无效 | 检查 Key 是否正确复制，没有多余空格 |
| 403 | 超过速率限制 | Demo: 50次/小时, Production: 5000次/小时。等待重置或申请 Production API |
| 404 | 照片不存在 | 照片可能已被删除，检查 ID 是否正确 |
| 422 | 参数错误 | 检查参数格式，如 `orientation` 拼写、`per_page` 范围等 |
| 500 | 服务器错误 | Unsplash 服务问题，稍后重试 |
| 503 | 服务不可用 | 维护中，等待恢复 |

### 完整错误处理代码

```python
import requests
import os

def call_unsplash_api(endpoint, params=None):
    """调用 Unsplash API 并处理错误"""
    try:
        res = requests.get(
            f'https://api.unsplash.com{endpoint}',
            params=params or {},
            headers={'Authorization': f"Client-ID {os.environ['UNSPLASH_ACCESS_KEY']}"}
        )

        if res.status_code == 200:
            return res.json()
        elif res.status_code == 401:
            raise Exception('认证失败：检查 UNSPLASH_ACCESS_KEY 是否正确')
        elif res.status_code == 403:
            raise Exception('速率限制：请等待后重试（Demo: 50次/小时）')
        elif res.status_code == 404:
            raise Exception('资源不存在：照片可能已被删除')
        elif res.status_code == 422:
            errors = res.json().get('errors', [])
            raise Exception(f'参数错误: {", ".join(errors)}')
        else:
            raise Exception(f'未知错误: {res.status_code}')

    except requests.exceptions.RequestException as e:
        raise Exception(f'网络错误: {e}')
```

---

## 性能优化建议

### 1. 响应式图片最佳实践

```html
<picture>
  <!-- WebP 格式（现代浏览器）-->
  <source
    type="image/webp"
    srcset="
      https://images.unsplash.com/photo-xxx?ixid=abc&w=400&fm=webp&q=80 400w,
      https://images.unsplash.com/photo-xxx?ixid=abc&w=800&fm=webp&q=85 800w,
      https://images.unsplash.com/photo-xxx?ixid=abc&w=1200&fm=webp&q=85 1200w
    "
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
  >

  <!-- JPEG 回退 -->
  <img
    src="https://images.unsplash.com/photo-xxx?ixid=abc&w=800&fm=jpg&q=85"
    srcset="
      https://images.unsplash.com/photo-xxx?ixid=abc&w=400&fm=jpg&q=80 400w,
      https://images.unsplash.com/photo-xxx?ixid=abc&w=800&fm=jpg&q=85 800w,
      https://images.unsplash.com/photo-xxx?ixid=abc&w=1200&fm=jpg&q=85 1200w
    "
    sizes="(max-width: 600px) 400px, (max-width: 1200px) 800px, 1200px"
    alt="Photo by Photographer on Unsplash"
    loading="lazy"
    decoding="async"
  >
</picture>
```

### 2. 缓存策略

```python
import time
from functools import lru_cache

# 内存缓存（适合小规模应用）
@lru_cache(maxsize=100)
def search_photos_cached(query, orientation='landscape', ttl_hash=None):
    """带缓存的搜索，5分钟过期"""
    # ttl_hash 用于实现过期时间
    return search_photos(query, orientation)

def get_ttl_hash(seconds=300):
    """生成 TTL hash 用于缓存过期"""
    return round(time.time() / seconds)

# 使用
results = search_photos_cached('mountain', 'landscape', get_ttl_hash())
```

### 3. 预加载关键图片

```html
<!-- 预加载 hero 背景图 -->
<link rel="preload" as="image"
  href="https://images.unsplash.com/photo-xxx?ixid=abc&w=1920&fm=webp"
  imagesrcset="
    https://images.unsplash.com/photo-xxx?ixid=abc&w=800&fm=webp 800w,
    https://images.unsplash.com/photo-xxx?ixid=abc&w=1920&fm=webp 1920w
  "
  imagesizes="100vw"
>
```

---

## 常见问题

### Q: 可以下载图片后上传到自己的 CDN 吗？
A: **不可以**。Unsplash 要求直接使用返回的 URL（Hotlinking），这确保了摄影师能获得准确的使用统计。

### Q: 必须为摄影师署名吗？
A: **强烈推荐但不强制**。Unsplash 许可证允许免费使用无需署名，但署名是对摄影师的尊重。

### Q: ixid 参数可以移除吗？
A: **绝对不可以**。`ixid` 是 API 使用条款要求，用于追踪应用使用情况。移除将违反条款。

### Q: Demo API 的 50 次/小时够用吗？
A: 对于个人项目通常足够。如果是生产环境或高流量应用，建议申请 Production API（5000 次/小时）。

### Q: 如何申请 Production API？
A. 访问 https://unsplash.com/oauth/applications，点击你的应用，申请 Production 级别。通常需要说明使用场景。

---

## 参考资源

- [Unsplash API 官方文档](https://unsplash.com/documentation)
- [获取 Access Key](https://unsplash.com/developers)
- [Imgix 图片处理文档](https://docs.imgix.com/)
- [BlurHash 官网](https://blurha.sh/)
- [Unsplash 许可证](https://unsplash.com/license)
