---
name: deep-assimilation
description: MUST use when user says 'analyze all and absorb', 'absorb all', or asks to deeply analyze and absorb a whole project or codebase into memory.
---

# Deep Assimilation (Context Absorption)

## Purpose
Allows the AI to perform a massive, autonomous deep-dive into an unfamiliar codebase, mapping out its architecture, dependencies, and core logic before starting work.

## Trigger Conditions
1. **Manual:** User says 'analyze all and absorb' or requests a deep project scan.

## Execution Steps
1. **Survey the Directory:** Use terminal commands (like `tree` or directory listing) to view the root folder structure.
2. **Identify Core Files:** Locate the main entry points (e.g., `package.json`, `main.py`, `docker-compose.yml`, or `src/index`).
3. **Deep Read:** Actively use file-reading tools to open and read the core architecture files, routing layers, and global state files.
4. **Compile the Mental Map:** Synthesize how the project is wired together (Frameworks used, Database paradigms, styling systems).
5. **Report:** Output a highly structured "Deep Assimilation Report" to the user, proving you understand the architecture, and state that you are ready to begin work.
