# image

Unsplash / Pexels / Pixabay / MediaWiki 图片与视频搜索下载插件，快速获取高质量免费素材用于项目开发。

> 从 [devflow](../devflow/) 插件迁移而来。

## 命令列表

| 命令 | 用途 |
|------|------|
| `/image:unsplash` | Unsplash 图片搜索下载 |
| `/image:pexels` | Pexels 图片/视频搜索下载 |
| `/image:pixabay` | Pixabay 图片/插画/矢量图/视频搜索下载 |
| `/image:mediawiki` | MediaWiki（Wikimedia Commons 等）自由许可图片搜索下载 |

## 安装

```bash
claude plugin add /path/to/image
```

## 环境变量

| 技能 | 环境变量 | 获取方式 |
|------|---------|---------|
| unsplash | `UNSPLASH_ACCESS_KEY` | https://unsplash.com/developers 创建应用 |
| pexels | `PEXELS_API_KEY` | https://www.pexels.com/api/ 注册即得（照片与视频共用） |
| pixabay | `PIXABAY_API_KEY` | https://pixabay.com/api/docs/ 登录后页面可见（图片与视频共用） |
| mediawiki | 无需 API Key | 公开 API 匿名可用，请求需携带自定义 User-Agent |

## 许可证

MIT License
