# image

Unsplash / Pexels / Pixabay / MediaWiki / Openverse 图片与视频搜索下载插件，支持五来源聚合搜索，快速获取高质量免费素材用于项目开发。

## 命令列表

| 命令 | 用途 |
|------|------|
| `/image:image-search` | 五来源聚合搜索：一次并发查询 Unsplash/Pexels/Pixabay/Wikimedia Commons/Openverse，统一 JSON 输出，可下载前 N 张 |
| `/image:unsplash` | Unsplash 图片搜索下载 |
| `/image:pexels` | Pexels 图片/视频搜索下载 |
| `/image:pixabay` | Pixabay 图片/插画/矢量图/视频搜索下载 |
| `/image:mediawiki` | MediaWiki（Wikimedia Commons 等）自由许可图片搜索下载 |
| `/image:openverse` | Openverse 开放许可图片聚合搜索下载（Flickr/Wikimedia/博物馆馆藏） |

## 安装

从本市场安装：

```bash
claude marketplace add https://github.com/ElliotChina/premium-plugin-marketplace
```

然后在 Claude Code 中执行：

```
/plugin install image@premium-plugin-marketplace
```

## 调用方式

- `image-search`：支持 agent 自动触发，也可手动调用
- 其余技能（unsplash / pexels / pixabay / mediawiki / openverse）：仅限用户手动调用（如 `/image:pexels`），agent 不会自动触发

## 环境变量

| 技能 | 环境变量 | 获取方式 |
|------|---------|---------|
| image-search | 同下（复用各来源 Key，零配置来源可直接用） | 聚合脚本按可用 Key 自动选择参与搜索的来源 |
| unsplash | `UNSPLASH_ACCESS_KEY` | https://unsplash.com/developers 创建应用 |
| pexels | `PEXELS_API_KEY` | https://www.pexels.com/api/ 注册即得（照片与视频共用） |
| pixabay | `PIXABAY_API_KEY` | https://pixabay.com/api/docs/ 登录后页面可见（图片与视频共用） |
| mediawiki | 无需 API Key | 公开 API 匿名可用，请求需携带自定义 User-Agent |
| openverse | 无需（可选 `OPENVERSE_CLIENT_ID`/`OPENVERSE_CLIENT_SECRET`） | 匿名 20次/分 + 200次/天；注册 https://api.openverse.org/v1/auth_tokens/register/ 并完成邮箱验证后提升额度，token 由技能脚本自动刷新 |

## 各来源官方 API 文档

| 来源 | 文档 |
|------|------|
| Unsplash | https://unsplash.com/documentation |
| Pexels | https://www.pexels.com/api/documentation/ |
| Pixabay | https://pixabay.com/api/docs/ |
| Wikimedia Commons (MediaWiki API) | https://www.mediawiki.org/wiki/API:Main_page |
| Openverse | https://api.openverse.org/v1/ |

聚合脚本未暴露的细粒度参数（颜色过滤、内容类型、许可枚举等）可查阅上述文档后直连 API 使用。

## 许可证

MIT License
