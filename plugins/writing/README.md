# writing

中文写作技能集,内嵌两个上游 Skill:

| Skill | 用途 | 上游 |
|-------|------|------|
| humanizer-zh | 编辑已有中文文本中的空话、重复及模板化表达,保留事实、确定程度和作者声音 | [op7418/humanizer-zh](https://github.com/op7418/humanizer-zh) |
| human-writing | 活人感中文创作与改稿,覆盖知乎、公众号、小说等文体,成稿硬禁翻案腔、破折号与黑话 | [KKKKhazix/human-writing](https://github.com/KKKKhazix/human-writing) |

## 从上游更新

两个 Skill 为上游仓库的副本,由 GitHub Actions 自动同步:`.github/workflows/sync-external-skills.yml` 每周一检查 `.github/sync-skills-mapping.json` 中登记的上游仓库,有变更时自动开 PR 递增版本并合并。也可在 Actions 页面手动触发 Sync External Skills。

## 许可

两个上游 Skill 均为 MIT,其 LICENSE 随副本保留在各自目录中。
