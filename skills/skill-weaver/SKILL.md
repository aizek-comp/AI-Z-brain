---
name: skill-weaver
description: Proposal-first skill authoring workflow with evidence, schema checks, and approval gates.
writes_files: true
writes_global_state: true
runs_commands: false
requires_confirmation: true
---

# Skill Weaver

## Purpose
Create or refine skills from validated repeated workflows without silent self-modification.

## Triggers
- **Manual:** user asks to create/update a skill.
- **Recommended:** repeated workflow with clear evidence and stable outcomes.

## Required Evidence
- At least two or more concrete workflow examples.
- Why existing skills are insufficient.
- Risk and scope assessment (project vs global).

## Safe Execution Steps
1. Produce a **Skill Proposal** first; do not write final files yet.
2. Classify target scope:
   - project skill (default)
   - global skill (explicit approval required)
3. Validate naming, required sections, and conflict with existing skills.
4. Request approval.
5. Write/update skill files only after approval.

## Verification & Output
Skill proposal schema:
```yaml
proposal_id: skill-proposal-YYYYMMDD-<slug>
name: <kebab-name>
scope: project | global
problem_statement: <why needed>
trigger_model:
  manual:
    - <phrase>
  recommended:
    - <condition>
required_sections:
  - Purpose
  - Triggers
  - Required Evidence
  - Safe Execution Steps
  - Verification & Output
  - Failure / Blocked Behavior
  - Capabilities
confidence: low | medium | high
conflicts_with:
  - <skill-name>
rollback: <how to revert>
```

## Failure / Blocked Behavior
- If conflict is unresolved, keep proposal status `blocked`.
- Never silently write global skills.

## Capabilities
- Writes files: Yes
- Writes global state: Yes (approval-gated)
- Runs commands: No
- Requires confirmation: Yes
