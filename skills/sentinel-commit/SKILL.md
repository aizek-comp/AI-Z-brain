---
name: sentinel-commit
description: Guarded commit assistant that stages only task-scoped files after verification and explicit approval.
writes_files: false
writes_global_state: false
runs_commands: true
requires_confirmation: true
---

# Sentinel Commit

## Purpose
Prepare safe, reviewable commits without staging unrelated work.

## Triggers
- **Manual:** user explicitly asks to prepare/perform a commit.
- **Recommended:** after verified task completion.

## Required Evidence
- Initial git status snapshot for this task (or explicit note that it is unavailable).
- Candidate file list scoped to this task.
- Verification/test results for changed behavior.
- Secret/artifact screening result.

## Safe Execution Steps
1. Capture initial status at task start (`git status --porcelain`).
2. At commit time, compute delta and isolate files changed by the current task.
3. Exclude unrelated files, generated artifacts, and sensitive files by default.
4. Run applicable existing verification (tests/lint/build where relevant).
5. Show concise summary:
   - files to stage
   - short diff/stat
   - verification results
   - excluded files with reason
6. Ask for explicit confirmation with commit message.
7. Stage **only explicit approved files** (`git add <file1> <file2> ...`) and commit.
8. Never push automatically.

## Verification & Output
Output a **Commit Readiness Summary**:
- Initial vs current status
- Approved file list
- Diffstat
- Verification outcomes
- Pending uncommitted/unapproved files

## Failure / Blocked Behavior
- If initial snapshot is missing, switch to manual review mode and require explicit per-file confirmation.
- If verification fails, do not commit until user overrides knowingly.
- Never use `git add .` as a default.

## Capabilities
- Writes files: No
- Writes global state: No
- Runs commands: Yes
- Requires confirmation: Yes
