# devflow

Elliot 的个人工具箱插件，包含日常开发中常用的命令。

> 新功能开发、问题诊断修复、代码/Spec/Plan 审查已迁移到 [superpowers-plus](../superpowers-plus/) 插件。
> Unsplash 图片搜索已迁移到 [image](../image/) 插件。
> Reveal.js 幻灯片制作已迁移到 [slide](../slide/) 插件。

## 命令列表

| 命令 | 用途 |
|------|------|
| `/devflow:project-config` | 项目配置 |
| `/devflow:test` | 功能测试 |
| `/devflow:sync-docs` | 更新文档 |
| `/devflow:prd` | 写需求文档 |
| `/devflow:ui` | 原型/UI 设计 |
| `/devflow:pencil-design` | Pencil MCP UI 设计 |

## 安装

```bash
claude plugin add /path/to/devflow
```

## 使用

在 Claude Code 中直接输入命令即可，例如：

```
/devflow:prd 用户登录功能需求
/devflow:test 登录功能测试
```

## 许可证

MIT License
