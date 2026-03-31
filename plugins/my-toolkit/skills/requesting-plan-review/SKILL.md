---
name: requesting-plan-review
description: >
  Use after writing an implementation plan to dispatch review agents.
  Verifies the plan is complete, matches the spec, and has proper task decomposition.
  Dispatch after the plan document is written and saved.
---

# Requesting Plan Review

Dispatch my-toolkit:plan-reviewer subagent to catch task gaps and ordering issues before coding begins. The reviewer gets precisely crafted context — the plan file path and spec reference — never your session's history. This keeps the reviewer focused on the plan quality, not your thought process, and preserves your own context for continued work.

**Core principle:** A bad plan wastes far more time than a good review saves.

## When to Request Review

**Mandatory:**
- After the implementation plan is written and saved
- Before starting code implementation

**Optional but valuable:**
- After significant changes to an existing plan
- When the plan is complex (5+ interdependent tasks)

## How to Request

**1. Dispatch plan-reviewer subagent:**

Use Agent tool with my-toolkit:plan-reviewer type, fill template at `plan-reviewer.md`

Before dispatching, replace all `{placeholders}` with actual values:

- `{PLAN_FILE_PATH}` — Saved plan document path
- `{SPEC_FILE_PATH}` — Spec document path (for cross-referencing)

**2. Act on feedback:**
- Fix missing tasks immediately
- Resolve dependency issues before implementation
- Remove placeholders (TBD, TODO, "add appropriate error handling", etc.)
- Reject over-engineering suggestions from reviewer

## Example

```
[Just finished writing implementation plan]

You: Let me request plan review before proceeding.

[Dispatch my-toolkit:plan-reviewer subagent]
  PLAN_FILE_PATH: docs/plans/user-auth-plan.md
  SPEC_FILE_PATH: docs/specs/user-auth-spec.md

[Subagent returns]:
  Issues:
    Critical: Task 3 references UserService not defined in any prior task
    Important: Step 2.4 says "add error handling" without specifying what errors
    Important: No test step for Task 5 (API endpoint)
    Minor: Task 4 and Task 6 could run in parallel
  Assessment: Issues Found — missing definitions and vague steps

You: [Fix missing UserService definition in Task 2]
[Replace "add error handling" with specific error cases]
[Add test step to Task 5]
```

## Integration with Workflows

**New Feature Workflow:**
- Review after the plan is written and saved
- Dispatch 3 concurrent agents for broader coverage
- Merge results using receiving-plan-review skill
- Fix before starting implementation

**Executing Plans:**
- Re-review after significant plan changes
- Catch compounding issues before they cascade into code

**Ad-Hoc Planning:**
- Review when plan complexity is high
- Review when unsure about task ordering

## Red Flags

**Never:**
- Skip review because "the plan is straightforward"
- Ignore Critical issues (missing tasks, placeholders)
- Proceed with unfixed Important issues (vague steps, missing tests)
- Accept over-engineering suggestions without evaluating against spec

**If reviewer is wrong:**
- Push back with specific reasoning (quote the plan section that proves it works)
- Check if plan description was unclear — if so, improve it
- Move on if the issue is a misunderstanding, but note it

See template at: requesting-plan-review/plan-reviewer.md
