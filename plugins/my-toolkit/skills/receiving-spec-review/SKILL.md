---
name: receiving-spec-review
description: >
  Use when receiving spec review feedback from multiple agents, before applying changes.
  Merge deduplicated results, verify against the original spec and user intent,
  then apply unified fixes. Requires technical rigor and verification, not blind acceptance.
---

# Receiving Spec Review

## Overview

Spec review requires technical evaluation, not blind acceptance. Multiple agents provide overlapping coverage — their feedback must be merged, verified against the original user request, and applied surgically.

**Core principle:** Merge first, verify against user intent, then fix the spec. Produce one coherent spec, not three stitched together.

## The Response Pattern

```
WHEN all 3 spec-reviewer agents complete:

1. MERGE: Collect all issues, deduplicate, identify consensus (2+ agents found same issue)
2. VERIFY: Cross-check each unique issue against the actual spec and user's original request
3. EVALUATE: Is this a real gap, misunderstanding, YAGNI suggestion, or false positive?
4. RANK: Consensus issues first, then Critical → Important → Minor
5. FIX: Fix the spec file directly, one category at a time
```

## Forbidden Responses

**NEVER:**
- Accept all feedback without verification
- Apply three sets of fixes independently
- Add features the user didn't request (even if reviewer thinks they're needed)
- Keep contradictions because "multiple reviewers disagreed"

**INSTEAD:**
- Merge and deduplicate first
- Verify each issue against actual user request
- Fix in priority order with post-fix verification
- Reject YAGNI suggestions with reasoning

## Consensus Detection

- **2+ agents found same issue** → High confidence, likely a real problem
- **Only 1 agent found issue** → Verify before acting (possible false positive)

**Deduplication:**
- Same root cause expressed differently → merge into one issue
- Overlapping issues across sections → check if shared root cause

## Handling Unclear Feedback

```
IF any issue is unclear or ambiguous:
  STOP - do not apply fixes yet
  Cross-reference against original user request and spec
  If still unclear, flag for user decision

WHY: Spec fixes may cascade. Partial fixes = inconsistent spec.
```

**Example:**
```
Agent 1: "Section 3 contradicts Section 5 on data format"
Agent 2: "Data format is ambiguous"
Agent 3: "Section 5 says JSON but Section 3 shows XML example"

Your evaluation:
  Root cause: All agents flagged data format inconsistency
  Merge: Section 3 and Section 5 disagree on data format
  Action: Choose one format (JSON, per modern practice), update both sections
```

## Issue Type Handling

### Real Gaps (Missing Sections, Placeholders, TBD) (Critical)
- Fix directly in the spec file
- Verify fix aligns with user's original intent

### Contradictions (Critical)
- Choose the version matching user's stated goals
- If unsure which is correct, escalate to user for decision

### Ambiguities (Important)
- Choose one interpretation and make it explicit
- Verify choice is consistent with rest of spec

### Scope Boundary Issues (Important)
- Evaluate: Did the user actually ask for this?
- Unrequested: Remove
- Potentially useful but not now: Document outside spec

### Terminology Inconsistencies (Minor)
- Unify to one term throughout
- Choose the more standard/precise term

### YAGNI Suggestions
- Evaluate: Does the user genuinely need this?
- Unrequested: Skip
- Potentially useful but not now: Document but don't add to spec

### False Positives (Reviewer Misunderstood Context)
- Skip with brief reasoning
- Check if spec wording caused the misunderstanding — if so, improve wording

## Fix Order

```
For verified, deduplicated issues:
  1. Placeholders and TBD (Critical)
  2. Inter-section contradictions (Critical)
  3. Ambiguous requirements that could cause wrong implementation (Important)
  4. Missing scope boundaries (Important)
  5. Terminology inconsistencies (Minor)
```

## Post-Fix Verification

After applying all fixes:
- All fixes are internally consistent
- No new contradictions introduced
- Every requirement still maps to user's original request
- No unrequested features added
- All placeholders resolved

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Accepting all feedback blindly | Verify each issue against user request |
| Fixing issues independently | Merge first, fix once |
| Wrong priority order | Critical (blockers) first, then Important, then Minor |
| Adding features reviewer suggested | Only add what user requested |
| Ignoring consensus issues | 2+ agents agree = high priority |
| Keeping contradictions unresolved | Choose one interpretation, apply consistently |

## When To Push Back

Push back when:
- Suggestion adds features beyond user's request (YAGNI)
- Reviewer misunderstood the spec context
- Suggestion would create new contradictions
- Issue is a false positive (spec already addresses it)

**How to push back:**
- Use technical reasoning, quote the relevant spec section
- Reference the user's original request
- Skip false positives with brief reasoning
