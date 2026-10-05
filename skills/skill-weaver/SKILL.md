---
name: skill-weaver
description: Auto-triggers when the AI detects a repeated pattern handled ad-hoc 3+ times, or when user says 'create skill', 'new skill', 'level up'. Automates the creation of a new specialized skill directory.
---

# Skill Weaver (Autonomous Self-Improvement)

## Purpose
Allows the AI to automate its own self-improvement by packaging repetitive workflows, specialized domain knowledge, or complex prompt sequences into reusable skills.

## Trigger Conditions
1. **Manual:** User explicitly asks you to "create a skill" or "forge this".
2. **Autonomous:** You notice that you and the user have manually executed the same complex multi-step workflow 3 or more times. Propose weaving it into a skill.

## Execution Steps
1. **Define the Skill:** Determine the exact triggers and the markdown instructions needed for the new skill.
2. **Create the Architecture:**
   - Create a new directory inside `~/.gemini/config/skills/` named after the skill.
   - Create a `SKILL.md` file inside that directory.
3. **Write the Core:** Write the YAML frontmatter (`name`, `description` with auto-triggers) and the markdown instructions into the `SKILL.md` file.
4. **Confirm:** Let the user know their AI assistant has permanently leveled up and acquired a new capability.
