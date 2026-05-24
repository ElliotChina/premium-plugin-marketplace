# playwright-expert

来源：[Jeffallan/claude-skills](https://github.com/Jeffallan/claude-skills/tree/main/skills/playwright-expert)

## 文件结构

```text
playwright-expert/
├── SKILL.md                          Skill 定义文件
├── README.md                         本文件
└── references/
    ├── api-mocking.md                API Mock 指南
    ├── configuration.md              Playwright 配置
    ├── debugging-flaky.md            Flaky 测试调试
    ├── page-object-model.md          Page Object Model 模式
    └── selectors-locators.md         选择器与定位器
```

## 同步更新

从源仓库拉取最新内容：

```bash
# 1. 查看 SKILL.md
curl -s "https://raw.githubusercontent.com/Jeffallan/claude-skills/main/skills/playwright-expert/SKILL.md" \
  -o plugins/devflow/skills/playwright-expert/SKILL.md

# 2. 拉取所有 reference 文件
for file in api-mocking configuration debugging-flaky page-object-model selectors-locators; do
  curl -s "https://raw.githubusercontent.com/Jeffallan/claude-skills/main/skills/playwright-expert/references/${file}.md" \
    -o "plugins/devflow/skills/playwright-expert/references/${file}.md"
done

# 3. 检查是否有新增文件
curl -s "https://api.github.com/repos/Jeffallan/claude-skills/contents/skills/playwright-expert/references" \
  | jq -r '.[].name'
```

同步后检查版本号（SKILL.md frontmatter 中的 `version` 字段）和文件列表是否有变化。
