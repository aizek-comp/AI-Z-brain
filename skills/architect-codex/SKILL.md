---
name: architect-codex
description: Auto-triggers when a non-obvious architectural decision or trade-off is made during conversation to log the reasoning permanently.
---

# Architect Codex (Decision Log)

## Purpose
Ensures that the "why" behind the code is never lost. When the AI and user make a complex architectural trade-off, it is logged into the Codex.

## Execution Steps
1. **Identify Trade-off:** A decision was just made (e.g., choosing NoSQL over SQL, or Client-side vs Server-side rendering).
2. **Draft Entry:** Write a concise log explaining the context, the options considered, and the final decision.
3. **Persist:** Append this log to a `decision-log.md` file in the user's project documentation folder.
