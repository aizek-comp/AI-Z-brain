---
name: synapse-memory
description: Automatically persists safe, evidence-backed lessons from completed work; manual reflection trigger remains available.
requires_confirmation: false
---

# Synapse Memory (Autonomous Learning)

## Purpose
Persist durable lessons automatically when they are evidence-backed and safe, while preserving redaction, auditability, version history, and rollback.

## Trigger Conditions
1. **Manual:** User asks to reflect, summarize lessons, or update memory.
2. **Recommended:** The assistant detects a potentially reusable lesson and should run this pipeline.
3. **Autonomous (Default):** After a verified fix, repeated success pattern, or major completed feature with clear evidence.

## Automatic Pipeline
1. **Detect lesson:** Extract the reusable rule from concrete evidence.
2. **Classify scope:** Choose `project` or `global` based on applicability.
3. **Safety filter:** Redact or refuse sensitive content before persistence.
4. **Assign confidence:** Mark `high`, `medium`, or `low` confidence from evidence quality.
5. **Conflict check:** Compare with existing memory; never silently overwrite.
6. **Persist:** Write project/global memory automatically for safe, evidence-backed knowledge.
7. **Notify owner:** Emit a visible audit notification summarizing what changed.
8. **Retain rollback metadata:** Keep status/history so entries can be reverted.

## Automatic Persistence Policy
- Project and global memory writes are allowed automatically for safe, evidence-backed lessons.
- No owner approval is required for those bounded autonomous-learning writes.
- If host capabilities cannot safely persist (no file-write tools, uncertain target, failing safety checks), emit a complete proposal instead of claiming persistence.

## Sensitive Data Refusal & Redaction
Never persist raw or recoverable:
- credentials, API tokens, secrets, private keys
- personal data or sensitive personal identifiers
- confidential payloads, proprietary raw dumps, or private customer data
- any content that violates policy, legal constraints, or least-privilege handling

When possible, store only sanitized abstractions (pattern-level rule + non-sensitive evidence summary).

## Memory Record Schema
Each persisted item must include:
- `memory_id`
- `status` (`active`, `superseded`, `reverted`, `provisional`)
- `scope` (`project` | `global`)
- `category`
- `rule`
- `evidence`
- `confidence`
- `conflicts` (list)
- `supersedes` (optional)
- `created_at`
- `rollback` (rollback target/instructions/metadata)

## Conflict & History Handling
- Do not silently overwrite an existing memory.
- On conflict, create a new record linked via `conflicts`/`supersedes` and preserve both entries.
- Reversions must mark records as `reverted` and keep full lineage for auditability.

## Uncertainty Handling
- Low-confidence or unverified lessons must be stored only as `provisional`/low-confidence.
- Provisional entries must not be presented as established fact.
- If confidence cannot be justified from evidence, prefer proposal mode.

## Audit, Disable, and Rollback
- After automatic persistence, emit an owner-visible audit note with memory ID, scope, confidence, and redaction summary.
- Support opt-out/disable switch for autonomous learning.
- Maintain documented rollback metadata so any autonomous write can be reverted safely.
