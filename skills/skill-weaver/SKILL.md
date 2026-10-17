---
name: skill-weaver
description: Automatically packages stable repeated workflows into reusable skills after sufficient successful evidence.
writes_files: true
writes_global_state: true
runs_commands: false
requires_confirmation: false
---

# Skill Weaver

## Purpose
Create or refine reusable skills from stable repeated workflows with autonomous-by-default behavior, safety filtering, conflict/version lineage, auditability, and rollback.

## Triggers
- **Manual:** user asks to create/update a skill.
- **Recommended:** repeated workflow with clear evidence and stable outcomes.
- **Autonomous (Default):** after at least three successful, materially similar workflow executions.

## Required Evidence
- At least three successful materially similar workflow examples.
- Why existing skills are insufficient or need update.
- Risk and scope assessment (`project` vs `global`).

## Safe Execution Steps
1. Collect and verify qualifying examples.
2. Generalize workflow into reusable triggers/steps.
3. Redact secrets and project-private/confidential data.
4. Classify target scope (`project` or `global`).
5. Validate naming, frontmatter, and required sections.
6. Detect conflicts/duplicates; never silently overwrite.
7. Write/update skill and version lineage metadata.
8. Notify owner and retain rollback metadata.

## Automatic Pipeline
1. Collect examples.
2. Generalize workflow.
3. Redact sensitive/private data.
4. Classify scope.
5. Validate structure.
6. Detect conflicts/duplicates.
7. Write skill.
8. Version lineage.
9. Notify owner.
10. Retain rollback metadata.

## Automatic Creation/Update Policy
- Project and global skills may be created/updated automatically for stable high-confidence workflows.
- Do not create a skill from one uncertain or failed example.
- If host cannot safely write files, output a complete proposal instead of claiming installation.

## Verification & Output
Skill metadata schema:
```yaml
skill_id: skill-YYYYMMDD-<slug>
origin: manual | autonomous
evidence_count: <int>
confidence: low | medium | high
version: <semver-or-revision>
scope: project | global
status: active | superseded | reverted | provisional
supersedes: <skill_id or null>
created_at: <ISO-8601>
rollback: <how to revert/supersede>
```

## Skill Metadata Schema
Each autonomous write must include:
- `skill_id`
- `origin`
- `evidence_count`
- `confidence`
- `version`
- `scope`
- `status`
- `supersedes`
- `created_at`
- `rollback`

## Conflict, Versioning, and History
- Never silently overwrite existing skills.
- On overlap/conflict, create explicit version/lineage links.
- Mark replaced versions `superseded` and rollbacks `reverted`.
- Preserve history for audit and recovery.

## Safety and Redaction Rules
Never include secrets, credentials, tokens, private keys, personal data, or confidential raw payloads in generated skills.
Store generalized, sanitized instructions only.

## Failure / Blocked Behavior
- If evidence is insufficient or unstable, keep proposal provisional/blocked.
- If host write capability is unavailable, provide proposal-only output.

## Audit, Disable, and Rollback
- Emit owner-visible audit records for each autonomous create/update.
- Respect autonomous-learning disable switch (opt-out), switching to proposal-only mode when disabled.
- Keep rollback metadata so generated skills can be reverted.

## Capabilities
- Writes files: Yes
- Writes global state: Yes (bounded autonomous learning)
- Runs commands: No
- Requires confirmation: No
