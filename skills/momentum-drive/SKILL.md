---
name: momentum-drive
description: MUST use when user says 'execute plan', 'run the plan', 'pick up where we left off', or when tracking execution progress against a master checklist.
---

# Momentum Drive (Task Execution)

## Purpose
Maintains project momentum by tracking step-by-step checklists and ensuring the AI does not lose track of the overarching goal during complex, multi-turn coding sessions.

## Execution Steps
1. **Locate the Plan:** Read the current project checklist (often saved in a local `TODO.md` or memory file).
2. **Execute:** Perform the next unchecked item on the list.
3. **Verify:** Test or audit the code to ensure it works.
4. **Update:** Mark the item as `[x]` in the checklist file.
5. **Prompt:** Ask the user if they are ready to initiate the next momentum cycle.
