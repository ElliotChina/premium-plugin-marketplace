# premium-plugin-marketplace

个人精选的 Claude Code 插件市场。插件清单、结构与安装方式见 [README.md](README.md)；本地维护的插件在 `plugins/` 下。

## 插件维护规则

- **版本号强制升级**：插件内容有任何修改（技能增删、脚本、README、配置），提交前必须升级 `plugins/<name>/.claude-plugin/plugin.json` 的 `version`——功能变更进位次版本号（0.x 段允许含破坏性变更），纯笔误修正进位修订号。不升级的后果：用户侧 `/plugin update` 比对版本号，检测不到任何内容更新。
- **文档与配置联动检查**：改完插件后，提交前核查以下文件是否需要同步更新：
  - 插件自身 `README.md` 与 `plugin.json` 的 description / keywords
  - 根 `README.md`（插件清单、计数、目录结构树）
  - `.claude-plugin/marketplace.json` 对应条目的 description / keywords
  - 涉及外部上游技能的增删时：`.github/sync-skills-mapping.json`（失效条目会导致同步报错或复活已删文件）与 `recommended-external-plugins.md` 的技能引用表

## 其他约定

- 外部技能副本由 CI 工作流（`sync-external-skills.yml`）按映射表定时同步；自研技能不登记映射表
- 三处描述必须一致：`plugin.json` ↔ `marketplace.json` 条目 ↔ 插件 `README.md`
