---
name: requesting-spec-review
description: >
  Use after writing a spec document (design doc) to dispatch review agents.
  Verifies the spec is complete, consistent, and ready for implementation planning.
  Dispatch after the spec document is written and saved.
---

# Requesting Spec Review

Dispatch my-toolkit:spec-reviewer subagent to catch document defects before they cascade into implementation plans and code. The reviewer gets precisely crafted context — the spec file path, original request, and project context — never your session's history. This keeps the reviewer focused on the spec quality, not your thought process, and preserves your own context for continued work.

**Core principle:** Wrong spec = wrong plan = wrong code. Fix at the source.

## When to Request Review

**Mandatory:**
- After the spec document is written and saved
- Before calling implementation plan writing

**Optional but valuable:**
- After significant design decision changes to an existing spec
- When the spec covers a complex domain with many edge cases

## How to Request

**1. Dispatch spec-reviewer subagent:**

Use Task tool with my-toolkit:spec-reviewer type, fill template at `spec-reviewer.md`

Before dispatching, replace all `{placeholders}` with actual values:

- `{SPEC_FILE_PATH}` — Saved spec document path
- `{ORIGINAL_REQUEST}` — User's original feature description
- `{PROJECT_CONTEXT}` — Key project architecture info (framework, conventions, constraints)

**2. Act on feedback:**
- Fix gaps and contradictions directly in the spec
- Resolve ambiguities by choosing one interpretation and making it explicit
- Remove unrequested features (YAGNI violations)
- Present changes to user for confirmation

## Example

```
[Just finished writing spec document]

You: Let me request spec review before planning.

[Dispatch my-toolkit:spec-reviewer subagent]
  SPEC_FILE_PATH: docs/specs/notification-spec.md
  ORIGINAL_REQUEST: "Add email notifications for order status changes"
  PROJECT_CONTEXT: "Next.js 14 App Router, PostgreSQL, Resend for email"

[Subagent returns]:
  Issues:
    Critical: Section "Error Handling" contains only TBD placeholder
    Important: "batch notifications" feature mentioned in Section 3 but not in original request
    Important: Section 2.4 "rate limiting" is ambiguous — per-user or global?
    Minor: Terminology inconsistency — "notification" vs "alert" used interchangeably
  Assessment: Issues Found — placeholder and scope creep need fixing

You: [Fill in error handling section with actual requirements]
[Remove batch notifications — not requested]
[Clarify rate limiting as per-user with 100/hr limit]
```

## Integration with Workflows

**New Feature Workflow:**
- Review after the spec is written and saved
- Dispatch 3 concurrent agents for broader coverage
- Merge results using receiving-spec-review skill
- Fix before writing the implementation plan

**Spec Revisions:**
- Re-review after significant design changes
- Ensure changes don't introduce new contradictions

**Ad-Hoc Specs:**
- Review when the spec covers unfamiliar domain
- Review when requirements seem unclear

## Red Flags

**Never:**
- Skip review because "the spec seems complete"
- Ignore Critical issues (placeholders, contradictions)
- Proceed with unfixed Important issues (ambiguities, scope creep)
- Accept YAGNI suggestions without evaluating against user intent

**If reviewer is wrong:**
- Push back with specific reasoning (quote the spec section that proves consistency)
- Check if spec description was unclear — if so, improve wording
- Move on if the issue is a misunderstanding, but note it

See template at: requesting-spec-review/spec-reviewer.md
