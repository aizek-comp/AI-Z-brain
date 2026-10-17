---
name: code-sonar
description: Evidence-based project health and risk scan using bounded, non-destructive checks.
writes_files: false
writes_global_state: false
runs_commands: true
requires_confirmation: false
---

# Code Sonar

## Purpose
Audit selected code areas for security, reliability, maintainability, and architecture risks.

## Triggers
- **Manual:** user asks for audit/scan/investigation.
- **Recommended:** before broad refactors or high-risk changes.

## Required Evidence
- Exact scan scope (paths/modules).
- Findings with file path references.
- Severity and confidence for each finding.

## Safe Execution Steps
1. Define scope and avoid full-repo destructive operations.
2. Run existing read-only checks/searches (linters/tests only if already present).
3. Evaluate findings against this checklist:
   - Security boundaries and secret exposure
   - Input validation/parsing safety
   - Error handling and fallback behavior
   - Dependency and architectural coupling
   - Test/verification gaps for changed behavior
4. Separate verified issues from hypotheses.

## Verification & Output
Return a **Sonar Report** table:
`[severity] [confidence] [file] [finding] [impact] [recommended fix]`
Include `No verified issue found` when appropriate.

## Failure / Blocked Behavior
- If tools are unavailable, provide manual checks and mark confidence as limited.
- Do not claim exploitable vulnerabilities without evidence.

## Capabilities
- Writes files: No
- Writes global state: No
- Runs commands: Yes (read-only)
- Requires confirmation: No
