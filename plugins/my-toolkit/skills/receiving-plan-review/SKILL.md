---
name: receiving-plan-review
user-invocable: false
description: >
  Use when receiving implementation plan review feedback from multiple agents, before applying changes.
  Merge deduplicated results, verify against the spec, then apply unified fixes to the plan.
  Requires technical rigor and verification, not blind acceptance of all suggestions.
---

# Receiving Plan Review

## Overview

Plan review requires technical evaluation, not blind acceptance. Multiple agents provide overlapping coverage — their feedback must be merged, verified against the spec, and applied surgically.

**Core principle:** Merge first, verify against spec, then fix the plan. Produce one coherent plan, not three stitched together.

## The Response Pattern

```
WHEN all 3 plan-reviewer agents complete:

1. MERGE: Collect all issues, deduplicate, identify consensus (2+ agents found same issue)
2. VERIFY: Cross-check each unique issue against the spec and actual plan
3. EVALUATE: Is this a real gap, misunderstanding, or over-engineering suggestion?
4. RANK: Consensus issues first, then Critical → Important → Minor
5. FIX: Fix the plan file directly, one category at a time
```

## Forbidden Responses

**NEVER:**
- Accept all feedback without verification
- Apply three sets of fixes independently
- Fix issues out of dependency order
- Keep placeholders because "reviewer didn't mention them"

**INSTEAD:**
- Merge and deduplicate first
- Verify each issue against actual spec content
- Fix in priority order with post-fix verification
- Reject over-engineering with reasoning

## Consensus Detection

- **2+ agents found same issue** → High confidence, likely a real problem
- **Only 1 agent found issue** → Verify before acting (possible false positive)

**Deduplication:**
- Different tasks with same root cause → merge into one issue
- Overlapping issues in same task → merge into single fix

## Handling Unclear Feedback

```
IF any issue is unclear or ambiguous:
  STOP - do not apply fixes yet
  Cross-reference against spec and plan
  If still unclear, flag for user decision

WHY: Issues may be related. Partial fixes = broken plan.
```

**Example:**
```
Agent 1: "Task 3 missing error handling"
Agent 2: "Task 3 step 2 should handle network timeout"
Agent 3: "Task 3 needs retry logic"

Your evaluation:
  Root cause: All agents flagged Task 3's error handling
  Merge: Task 3 needs specific error handling (network timeout + retry)
  Action: Add concrete steps with actual error handling code
```

## Issue Type Handling

### Placeholders and TBD (Critical)
- Replace with actual content (code, commands, or specific details)
- If content cannot be determined, escalate to user rather than keeping placeholder

### Missing Tasks for Spec Requirements (Critical)
- Add task at correct dependency position
- Include full step structure (test → run → implement → run → commit)
- Verify new task doesn't break existing dependency chain

### Vague or Non-Executable Steps (Important)
- Replace descriptions with actual code blocks and commands
- Ensure each step can be executed independently

### Missing Test Steps (Important)
- Add the cycle: failing test → run → implement → run → commit
- Include actual test code, not "write tests for the above"

### Dependency Issues (Important)
- Fix ordering to match actual dependencies
- Mark independent tasks as parallelizable
- Verify no circular dependencies after changes

### Over-Engineering Suggestions
- Evaluate: Does the spec require this?
- Not in spec: Skip
- "Nice to have" but significantly adds scope: Document but don't add

### False Positives
- Skip with brief reasoning
- Check if plan description was unclear — if so, improve wording

## Fix Order

```
For verified, deduplicated issues:
  1. Placeholders, TBD, incomplete steps (Critical)
  2. Missing tasks for spec requirements (Critical)
  3. Steps without executable code/commands (Important)
  4. Missing test steps (Important)
  5. Dependency ordering issues (Important)
  6. Task description clarity (Minor)
```

## Post-Fix Verification

After applying all fixes:
- Every spec requirement maps to at least one task
- No remaining placeholders
- All referenced types/functions defined in prior tasks
- No circular dependencies in task ordering
- All fixes are internally consistent

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting all feedback blindly | Verify each issue against spec |
| Fixing issues independently | Merge first, fix once |
| Wrong priority order | Critical (blockers) first, then Important, then Minor |
| Breaking dependency chain | Verify ordering after each fix |
| Adding over-engineering | Only add what spec requires |
| Ignoring consensus issues | 2+ agents agree = high priority |

## When To Push Back

Push back when:
- Suggestion adds tasks beyond spec scope (YAGNI)
- Reviewer misunderstood the plan context
- Suggestion would break existing dependency chain
- Issue is a false positive (plan already addresses it)

**How to push back:**
- Use technical reasoning, quote the relevant plan section
- Reference the spec requirement being addressed
- Skip false positives with brief reasoning
