# devops

DevOps 技能插件（技能源自 [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)，MIT）。

## 技能

### ci-cd-and-automation

CI/CD 流水线自动化：搭建或修改构建部署流水线时使用。覆盖质量门禁管线（lint → typecheck → test → build）、GitHub Actions 配置模板（含数据库集成测试与 E2E）、CI 失败回喂 agent 的模式、部署策略（预览部署、特性开关、分阶段发布、回滚预案）、环境管理、Dependabot/Renovate 自动化、build cop 角色与 CI 优化。

### shipping-and-launch

生产发布与上线：准备部署到生产时使用。发布前检查清单、监控搭设、分阶段发布计划与回滚策略。

### observability-and-instrumentation

可观测性与插桩：为生产行为埋点，让问题可诊断。覆盖日志、指标、追踪、告警的添加时机与做法——任何跑在生产上的功能都应有"它正常工作"的证据。

## 参考文件

技能内引用的发布前检查清单位于 `references/`（definition-of-done、security、performance、accessibility、observability 五份），SKILL.md 以 `../../references/` 相对路径按需引用。

## 安装

```bash
claude plugin install devops@premium-plugin-marketplace
```
