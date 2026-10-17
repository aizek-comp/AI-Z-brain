---
name: skill-weaver
description: Automatically packages stable repeated workflows into reusable skills after sufficient successful evidence.
requires_confirmation: false
---

# Skill Weaver (Autonomous Workflow Packaging)

## Purpose
Convert stable, repeated, high-confidence workflows into reusable skills automatically, with safety filtering, version history, auditability, and rollback.

## Trigger Conditions
1. **Manual:** User asks to create or update a skill.
2. **Autonomous (Default):** Trigger after at least 3 successful, materially similar workflow executions.

## Automatic Pipeline
1. **Collect evidence:** Gather at least 3 successful, materially similar examples.
2. **Generalize workflow:** Extract reusable trigger language and execution steps.
3. **Safety filter:** Redact secrets and project-private/confidential details.
4. **Classify scope:** Choose `project` or `global` skill target.
5. **Validate structure:** Confirm naming, frontmatter, and required sections are complete.
6. **Detect conflicts/duplicates:** Compare with existing skills; never silently overwrite.
7. **Write skill:** Create/update `SKILL.md` with metadata and instructions.
8. **Version + lineage:** Increment version metadata and track supersession links.
9. **Notify owner:** Emit visible audit notification.
10. **Retain rollback metadata:** Preserve reversible history.

## Automatic Creation/Update Policy
- Project and global skills may be created/updated automatically for stable, high-confidence workflows.
- Do not create a skill from one-off, uncertain, or failed examples.
- If host cannot safely write files, return a complete generated skill proposal instead of claiming installation.

## Skill Metadata Schema
Each autonomous write must include:
- `skill_id`
- `origin` (manual/autonomous + source context)
- `evidence_count`
- `confidence`
- `version`
- `scope` (`project` | `global`)
- `status` (`active`, `superseded`, `reverted`, `provisional`)
- `supersedes` (optional)
- `created_at`
- `rollback` (target/instructions/metadata)

## Conflict, Versioning, and History
- Never silently overwrite an existing skill.
- On conflict/overlap, create a new version or distinct skill entry with explicit lineage.
- Mark replaced items as `superseded`; mark rollbacks as `reverted`.
- Preserve prior versions for audit and recovery.

## Safety and Redaction Rules
Never include secrets, credentials, tokens, private keys, personal data, or confidential raw payloads in generated skills.
Store generalized, sanitized instructions only.

## Audit, Disable, and Rollback
- Emit owner-visible audit records for each autonomous create/update.
- Respect autonomous-learning disable switch (opt-out).
- Keep rollback metadata so any generated skill can be reverted.
