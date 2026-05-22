# superpowers-plus

superpowers 插件扩展，提供代码、Spec 和 Plan 的并发多 agent 审查能力。

## 命令列表

| 命令 | 用途 |
|------|------|
| `/superpowers-plus:dev` | 新功能开发（需求→设计→实现→验证全流程） |
| `/superpowers-plus:fix` | 问题诊断修复 & 功能调试 |
| `/superpowers-plus:code-review` | 代码审查（并发多 agent） |
| `/superpowers-plus:spec-review` | Spec 文档审查（并发多 agent） |
| `/superpowers-plus:plan-review` | 实现计划审查（并发多 agent） |

## 审查流程

每个审查命令遵循相同的核心模式：

1. **派发** — 按并发数（默认 3）派发独立审查 agent
2. **合并去重** — 收集所有问题，识别共识（2+ agent 标记同一问题）
3. **验证** — 将每个问题与实际内容交叉比对，排除误报
4. **修复** — 按优先级（Critical → Important → Minor）直接修复文件

并发数为 1 时跳过合并去重，直接根据单个 agent 反馈修复。

## 安装

```bash
claude plugin add /path/to/superpowers-plus
```

## 使用

```
/superpowers-plus:dev 用户登录功能
/superpowers-plus:code-review src/auth/
/superpowers-plus:spec-review docs/specs/notification-spec.md
/superpowers-plus:plan-review docs/plans/auth-plan.md
/superpowers-plus:fix 页面加载时报 500 错误
```

## 依赖

- [superpowers](../superpowers/) 插件提供基础能力（worktree 管理、调试、验证等）

## 许可证

MIT License
