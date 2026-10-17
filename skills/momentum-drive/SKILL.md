---
name: momentum-drive
description: Checklist-driven execution loop with explicit verification, blockers, and scope control.
writes_files: true
writes_global_state: false
runs_commands: true
requires_confirmation: true
---

# Momentum Drive

## Purpose
Execute multi-step work reliably without losing task state.

## Triggers
- **Manual:** user says execute plan / continue from plan.
- **Recommended:** when tasks have multiple dependent steps.

## Required Evidence
- A concrete checklist source (file or user-provided list).
- Acceptance criteria per item.
- Verification evidence for completed items.

## Safe Execution Steps
1. Confirm checklist source and task scope.
2. Pick the highest-priority unblocked item.
3. Execute only that item.
4. Run targeted verification.
5. Update checklist status using: `[ ]`, `[x]`, `[blocked:<reason>]`, `[deferred]`.
6. Report result and ask whether to continue.

## Verification & Output
Per cycle output:
- Item executed
- Files touched
- Verification run + result
- New blockers/risks
- Next proposed item

## Failure / Blocked Behavior
- If checklist is missing/ambiguous, request clarification before editing files.
- If verification fails, keep item incomplete and report remediation options.

## Capabilities
- Writes files: Yes (project checklist/task docs)
- Writes global state: No
- Runs commands: Yes
- Requires confirmation: Yes (before advancing to next risky step)
