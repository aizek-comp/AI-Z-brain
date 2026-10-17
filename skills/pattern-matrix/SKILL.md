---
name: pattern-matrix
description: Reusable pattern proposal/retrieval workflow with compatibility checks and safe storage scope.
writes_files: true
writes_global_state: true
runs_commands: false
requires_confirmation: true
---

# Pattern Matrix

## Purpose
Store and retrieve reusable implementation patterns safely.

## Triggers
- **Manual:** user asks to save/reuse a pattern.
- **Recommended:** after a validated reusable implementation appears.

## Required Evidence
- Working example location and context.
- Preconditions/compatibility notes.
- Security/privacy review outcome.

## Safe Execution Steps
1. Build a **Pattern Proposal** first.
2. Classify scope: project library (default) or global library (approval required).
3. Sanitize secrets/proprietary data.
4. Save only generalized pattern + metadata.
5. On retrieval, verify compatibility before use.

## Verification & Output
Pattern proposal schema:
```yaml
id: pattern-YYYYMMDD-<slug>
scope: project | global
source_files:
  - path: <file>
compatibility:
  language: <language>
  framework: <framework/version>
constraints:
  - <constraint>
security_review: pass | fail | needs-review
confidence: low | medium | high
rollback: <how to remove/revert>
```

## Failure / Blocked Behavior
- If compatibility or provenance is unclear, do not store/reuse; request clarification.
- Global writes require explicit approval.

## Capabilities
- Writes files: Yes
- Writes global state: Yes (approval-gated)
- Runs commands: No
- Requires confirmation: Yes
