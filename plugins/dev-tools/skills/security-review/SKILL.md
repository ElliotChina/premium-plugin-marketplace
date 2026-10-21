---
name: security-review
description: 安全审查技能。This skill should be used when the user asks to "security review", "安全审查", "检查安全漏洞", "check for vulnerabilities", "review security of the changes", "audit this branch for security issues", or wants a security-focused review of pending changes on the current branch. Completes a high-confidence security review of the pending changes, reporting only exploitable vulnerabilities with concrete attack paths.
allowed-tools: Bash(git diff:*), Bash(git log:*), Bash(git status:*), Bash(git show:*), Read, Glob, Grep
---

# Security Review

以资深安全工程师的视角，对当前分支的待提交改动做一次聚焦的安全审查。只报告**高置信度**、有真实利用可能的安全漏洞——这不是一次通用代码评审，只关注本次改动新引入的安全问题，不评论已存在的安全隐患。

## 收集上下文

先运行以下命令收集评审输入：

```bash
git status
git diff --name-only origin/HEAD...   # 无 origin/HEAD 时用 main...HEAD
git log --no-decorate origin/HEAD...
git diff origin/HEAD...
```

以上完整 diff 即本次评审对象。

## 目标

找出有真实利用潜力的**高置信度**安全漏洞。硬性要求：

1. **最小化误报**：只标记对实际可利用性有 **>80% 置信度**的问题。
2. **避免噪音**：跳过理论性问题、风格问题、低影响发现。
3. **聚焦影响**：优先报告可能导致未授权访问、数据泄露或系统沦陷的漏洞。
4. **排除项**：不报拒绝服务（DoS）、磁盘上存储的 secrets（由其他流程管理）、限流/资源耗尽问题。
5. 仅可从内网利用的问题仍可评为 HIGH——按影响评级，不按可达距离。

## 安全类别

逐类检查 diff：

**输入验证**
- SQL 注入（未净化的用户输入拼接查询）
- 命令注入（系统调用 / 子进程）
- XXE（XML 解析）、模板注入、NoSQL 注入
- 路径穿越（文件操作）

**认证与授权**
- 认证绕过逻辑、权限提升路径
- 会话管理缺陷、JWT 漏洞
- 授权逻辑绕过

**加密与密钥管理**
- 硬编码 API key / 密码 / token
- 弱加密算法或实现、密钥存储不当
- 加密随机数问题、证书校验绕过

**注入与代码执行**
- 反序列化 RCE、Pickle 注入、YAML 反序列化漏洞
- eval 注入、XSS（反射型 / 存储型 / DOM 型）

**数据暴露**
- 敏感数据写入日志或存储、PII 处理违规
- API 端点数据泄漏、调试信息暴露

## 分析方法论

- **Phase 1 — 仓库上下文研究**（用文件搜索工具）：识别项目已有的安全框架与库、既有的安全编码模式、现有的净化/校验模式；理解项目的安全模型与威胁模型。
- **Phase 2 — 对比分析**：将新改动与既有安全模式对比，找出对既有安全实践的偏离、不一致的安全实现、引入新攻击面的代码。
- **Phase 3 — 漏洞评估**：逐个检查修改文件的安全含义；追踪从用户输入到敏感操作的数据流；找出不安全跨越权限边界的位置；识别注入点与不安全反序列化。

## 执行步骤

1. **找一个子任务识别漏洞**（`Explore` 或 `general-purpose`，只读）：先探索代码库理解上下文，再分析 diff 的安全含义。子任务 prompt 中包含上述目标、类别与方法论全文。
2. **对第 1 步找到的每个漏洞，并行启动子任务做误报过滤**：每个子任务的 prompt 中包含 **`references/false-positive-filtering.md`** 的全部内容，要求读取代码判定真伪（不运行命令、不写文件），并给出 1–10 置信度分。
3. **过滤**：丢弃置信度低于 **8** 的漏洞。

## 输出格式

最终回复只包含 markdown 报告，不含其他内容。每条发现包含文件、行号、severity、category（如 `sql_injection`、`xss`）、description、exploit scenario、fix recommendation：

```markdown
# Vuln 1: XSS: `foo.py:42`

* Severity: High
* Description: `username` 参数的用户输入未转义直接插入 HTML，导致反射型 XSS
* Exploit Scenario: 攻击者构造 /bar?q=<script>alert(document.cookie)</script> 在受害者浏览器执行 JS，劫持会话
* Recommendation: 对所有渲染进 HTML 的用户输入启用自动转义或显式 escape
```

**Severity 分级：**
- **HIGH**：可直接利用，导致 RCE、数据泄露或认证绕过
- **MEDIUM**：需要特定条件但影响显著
- **LOW**：纵深防御类或影响较低的漏洞

**置信度标准（子任务评分用）：**
- 0.9–1.0：确认存在可利用路径，尽可能已验证
- 0.8–0.9：明确的漏洞模式，有已知利用方法
- 0.7–0.8：可疑模式，需要特定条件才能利用
- 低于 0.7：不报（过于投机）

最后提醒：只报 HIGH 和 MEDIUM。宁可漏掉几个理论问题，也不要用误报淹没报告——每条发现都应该是安全工程师会在 PR 评审中有把握提出的问题。
