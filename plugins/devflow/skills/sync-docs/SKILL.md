---
name: sync-docs
argument-hint: "[文档类型或文件名]"
description: >
  This skill should be used when the user runs "/devflow:sync-docs" to update project documentation.
  Covers README updates, API documentation, changelogs, and other project documentation.
---

# Docs - 更新文档

结构化的文档更新流程，保持项目文档与代码同步。

## 触发方式

用户执行 `/devflow:sync-docs` 命令时激活。传入需要更新的文档类型或文件名作为参数。

## 工作流程

### 1. 确定文档范围

根据用户需求确定更新范围：

- README.md：项目说明、使用指南
- CLAUDE.md：项目配置指令和开发规范
- API 文档：接口说明、参数描述
- CHANGELOG.md：版本变更记录
- 架构文档：系统设计、模块说明
- 配置文档：环境变量、部署说明
- PRD / 需求文档：产品需求说明
- 原型设计文档：UI/UX 设计说明

> **注意**：PRD、需求文档、原型设计文档等设计类文档涉及产品决策，修改前**必须与用户确认**，不可自行变更内容。

### 2. 收集信息

收集文档更新所需的上下文：

- 读取现有文档内容
- 通过 git log / git diff 了解最近的代码变更
- 读取相关的源代码和配置文件
- 了解文档的目标读者

### 3. 更新文档

遵循以下原则：

- 基于事实，反映代码的实际行为
- 语言简洁清晰，避免冗余描述
- 保持与现有文档风格一致
- 中英文与项目现有风格保持一致
- 不添加未实现功能的文档

### 4. 审查

更新完成后检查：

- 文档是否准确反映当前代码状态
- 示例代码是否可运行
- 链接和引用是否有效
- 格式是否统一规范

### 5. 总结

简要说明更新了哪些文档和主要变更内容。

## 注意事项

- 先读现有文档再修改，保持风格一致
- 不创建不必要的文档文件
- 不为未实现的功能写文档
- 遵循用户 CLAUDE.md 中的开发原则
