---
name: code-sonar
description: MUST use when user says 'survey project', 'scan project', 'investigate', 'deep dive', or when the AI needs to assess project health before planning.
---

# Code Sonar (Deep Audit)

## Purpose
Allows the AI to run a high-level diagnostic scan over a codebase to identify technical debt, security flaws, or architectural inconsistencies before executing new features.

## Trigger Conditions
1. **Manual:** User asks for an audit, health check, or investigation of a specific directory.
2. **Autonomous:** You are about to refactor a massive file and need to scan its dependencies first.

## Execution Steps
1. **Execute Scans:** Use terminal tools (like `grep` or linting commands) to sweep the codebase for specific patterns or issues.
2. **Review Traces:** Follow the data flow from frontend components down to the backend proxy/database layers.
3. **Report:** Output a "Sonar Ping" report detailing the health of the scanned modules.
