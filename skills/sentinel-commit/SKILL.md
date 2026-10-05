---
name: sentinel-commit
description: MUST use when committing code changes, completing a task, or proactively after finishing any work to ensure no work is left behind.
---

# Sentinel Commit (Vigilant Version Control)

## Purpose
Ensures absolute vigilance over the codebase state. Code is never left uncommitted after a successful milestone or task completion.

## Trigger Conditions
1. **Manual:** User says 'commit', 'save changes', or 'push'.
2. **Autonomous:** You have successfully completed a requested feature, bug fix, or refactor.

## Execution Steps
1. **Status Check:** Run `git status` to see what has changed.
2. **Diff Review:** If necessary, run `git diff` to understand the exact changes made.
3. **Execute:** Run `git add .` followed by `git commit -m "[Conventional Commit Message]"`.
4. **Report:** Briefly inform the user that the milestone has been safely secured by the Sentinel Commit protocol.
