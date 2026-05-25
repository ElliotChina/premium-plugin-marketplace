# web-design-guidelines

来源：[vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines)

## 文件结构

```text
web-design-guidelines/
├── SKILL.md    Skill 定义文件
└── README.md   本文件
```

## 同步更新

从源仓库拉取最新内容：

```bash
# 1. 拉取 SKILL.md
curl -s "https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/web-design-guidelines/SKILL.md" \
  -o plugins/frontend-web/skills/web-design-guidelines/SKILL.md

# 2. 检查是否有新增文件
curl -s "https://api.github.com/repos/vercel-labs/agent-skills/contents/skills/web-design-guidelines" \
  | jq -r '.[].name'
```

同步后检查版本号（SKILL.md frontmatter 中的 `version` 字段）和文件列表是否有变化。
