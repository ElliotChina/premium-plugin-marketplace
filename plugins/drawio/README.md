# drawio

Draw.io 图表生成插件。通过自然语言描述生成、编辑与校验 `.drawio` 图表文件，生成的文件可直接在 [draw.io](https://www.drawio.com/) 网页版 / 桌面版或 VS Code（`hediet.vscode-drawio` 扩展）中打开编辑。

## 技能

### draw-io-diagram-generator

| 图表类型 | 模板 |
|---|---|
| 流程图 | `assets/templates/flowchart.drawio` |
| 系统架构图 | `assets/templates/architecture.drawio` |
| 时序图 | `assets/templates/sequence.drawio` |
| ER 图 | `assets/templates/er-diagram.drawio` |
| UML 类图 | `assets/templates/uml-class.drawio` |
| 网络拓扑 / BPMN / 思维导图 | 使用形状库或手动布局 |

内置资源：

- `references/`：mxGraph XML schema、样式键目录、形状库完整参考
- `scripts/validate-drawio.py`：`.drawio` 文件 XML 结构校验器
- `scripts/add-shape.py`：向现有图表安全添加形状的 CLI

## 使用示例

```text
画一个用户下单的流程图，保存为 order-flow.drawio
生成一个三层电商系统架构图
把这个 ER 图补充 users 表和 orders 表的关系
```

## 来源

技能来自 [github/awesome-copilot](https://github.com/github/awesome-copilot)，由 CI 工作流定时同步（见 [.github/sync-skills-mapping.json](../../.github/sync-skills-mapping.json)）。
