---
name: synapse-memory
description: Proposal-first learning workflow that records evidence-backed lessons with scope controls and rollback metadata.
writes_files: true
writes_global_state: true
runs_commands: false
requires_confirmation: true
---

# Synapse Memory

## Purpose
Capture verified lessons without silently writing permanent global rules.

## Triggers
- **Manual:** user asks to reflect/show learnings/update rules.
- **Recommended:** after a validated bug fix, migration, or architectural lesson.

## Required Evidence
- Concrete incident/change summary.
- File/test evidence supporting the lesson.
- Scope decision: project or global.

## Safe Execution Steps
1. Draft a **Memory Proposal** before any persistence.
2. Classify scope:
   - project memory (default)
   - global memory (explicit approval required)
3. Assign confidence based on evidence quality.
4. Check conflicts with existing learned rules.
5. Persist approved entries with revision metadata.

## Verification & Output
Memory entry schema:
```yaml
memory_id: mem-YYYYMMDD-<slug>
status: proposed | accepted | superseded | reverted
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
conflicts_with:
  - <memory_id>
approved_by: <user or reviewer>
created_at: <ISO-8601>
rollback: <how to revert/supersede>
```

## Failure / Blocked Behavior
- If evidence is weak, keep status as `proposed` and request validation.
- Do not persist secrets/private data.
- Do not silently write global memory.

## Capabilities
- Writes files: Yes
- Writes global state: Yes (approval-gated)
- Runs commands: No
- Requires confirmation: Yes
