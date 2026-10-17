# Safety Scenarios

## 1) Automatic memory capture from a verified fix
- A bug is fixed with reproducible evidence.
- `synapse-memory` extracts the lesson, marks confidence, persists it, and emits an audit notification.

## 2) Automatic redaction of a secret in a lesson
- A lesson draft includes an API token from logs.
- The pipeline refuses raw token storage, redacts the token, and stores only a generalized safe rule.

## 3) Conflict/supersession for memories or skills
- A new rule conflicts with an existing one.
- The system creates a new entry/version with `supersedes` links and marks prior state `superseded` instead of overwriting.

## 4) Automatic skill creation after repeated successful workflows
- A materially similar workflow succeeds at least 3 times.
- `skill-weaver` generalizes the process, validates structure, versions the skill, and records audit + rollback metadata.

## 5) Disabling autonomous learning
- User disables autonomous learning.
- `synapse-memory` and `skill-weaver` switch to proposal-only behavior with no automatic file persistence.

## 6) Missing file-write capability (proposal fallback)
- Host lacks safe file-write tools.
- The system returns a complete generated memory/skill proposal and clearly states it was not installed.
