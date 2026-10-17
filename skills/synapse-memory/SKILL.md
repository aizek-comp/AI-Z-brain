---
name: synapse-memory
description: Automatically persists safe, evidence-backed lessons from completed work; manual reflection trigger remains available.
writes_files: true
writes_global_state: true
runs_commands: false
requires_confirmation: false
---

# Synapse Memory

## Purpose
Capture verified lessons with autonomous-by-default persistence for safe, evidence-backed knowledge while preserving auditability, rollback, and conflict lineage.

## Triggers
- **Manual:** user asks to reflect/show learnings/update rules.
- **Recommended:** after a validated bug fix, migration, or architectural lesson.
- **Autonomous (Default):** after a verified fix, repeated success pattern, or major completed feature with clear evidence.

## Required Evidence
- Concrete incident/change summary.
- File/test evidence supporting the lesson.
- Scope decision: project or global.

## Safe Execution Steps
1. Detect and draft the reusable lesson from concrete evidence.
2. Classify scope (`project` or `global`) based on applicability.
3. Redact/refuse sensitive content before persistence.
4. Assign confidence (`high` | `medium` | `low`).
5. Check conflicts with existing memory; never silently overwrite.
6. Persist safe evidence-backed entries automatically.
7. Emit owner-visible audit notification.
8. Attach rollback metadata and lineage links.

## Automatic Pipeline
1. Detect lesson.
2. Classify scope.
3. Redact/refuse sensitive content.
4. Assign confidence.
5. Check conflicts.
6. Persist.
7. Notify owner.
8. Retain rollback metadata.

## Automatic Persistence Policy
- Project and global persistence is allowed automatically for safe, evidence-backed lessons.
- No owner approval is required for this bounded autonomous-learning workflow.
- If host cannot safely persist (missing write tools, uncertain targets, or safety failure), emit a complete proposal instead of claiming persistence.

## Sensitive Data Refusal & Redaction
Never persist raw or recoverable:
- credentials, tokens, secrets, private keys
- personal data/sensitive identifiers
- confidential payloads or proprietary raw data

Store only sanitized abstractions and non-sensitive evidence summaries.

## Verification & Output
Memory entry schema:
```yaml
memory_id: mem-YYYYMMDD-<slug>
status: active | superseded | reverted | provisional
scope: project | global
category: debugging | architecture | workflow | security | domain
rule: <actionable statement>
evidence:
  files:
    - path: <file>
      note: <what supports the rule>
  checks:
    - <test/command/result>
confidence: low | medium | high
conflicts:
  - <memory_id>
supersedes: <memory_id or null>
created_at: <ISO-8601>
rollback: <how to revert/supersede>
```

## Memory Record Schema
Each persisted item must include:
- `memory_id`
- `status` (`active`, `superseded`, `reverted`, `provisional`)
- `scope` (`project` | `global`)
- `category`
- `rule`
- `evidence`
- `confidence`
- `conflicts`
- `supersedes`
- `created_at`
- `rollback`

## Conflict & History Handling
- Do not silently overwrite existing memory.
- On conflict, create linked entries via `conflicts`/`supersedes` and preserve history.
- Reversions must mark entries `reverted` and keep full lineage.

## Uncertainty Handling
- Low-confidence/unverified lessons must remain `provisional` and not be presented as established fact.
- If confidence cannot be justified, prefer proposal mode.

## Failure / Blocked Behavior
- If evidence is weak, mark as `provisional` and request validation.
- Do not persist secrets/private/confidential data.
- If host write capability is missing, return proposal-only output.

## Audit, Disable, and Rollback
- Emit owner-visible audit records including memory ID, scope, confidence, and redaction summary.
- Respect autonomous-learning disable switch (opt-out) and switch to proposal-only when disabled.
- Keep rollback metadata for safe reversions.

## Capabilities
- Writes files: Yes
- Writes global state: Yes (bounded autonomous learning)
- Runs commands: No
- Requires confirmation: No
