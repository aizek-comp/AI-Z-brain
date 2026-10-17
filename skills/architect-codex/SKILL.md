---
name: architect-codex
description: ADR-style decision logging for non-trivial trade-offs with evidence and revisit criteria.
writes_files: true
writes_global_state: false
runs_commands: false
requires_confirmation: true
---

# Architect Codex

## Purpose
Record why important technical decisions were made.

## Triggers
- **Manual:** user asks to log/document a decision.
- **Recommended:** after non-trivial trade-offs that affect architecture.

## Required Evidence
- Decision context and constraints.
- Options considered.
- Chosen option with rationale.

## Safe Execution Steps
1. Draft an ADR entry proposal.
2. Confirm target file/location in project docs.
3. Append only after user confirmation.
4. Link related tickets/PRs if available.

## Verification & Output
Use this template:
```
# ADR-XXXX: <Title>
- Status: Proposed | Accepted | Superseded
- Date: YYYY-MM-DD
- Context:
- Options considered:
- Decision:
- Consequences:
- Revisit triggers:
- Rollback/superseded-by:
```

## Failure / Blocked Behavior
- If evidence is weak, keep status as `Proposed` and request missing context.
- Do not log secrets or sensitive operational details.

## Capabilities
- Writes files: Yes (project ADR/decision log)
- Writes global state: No
- Runs commands: No
- Requires confirmation: Yes
