---
name: synapse-memory
description: MUST use when user says 'activate reflection', 'what have you learned', 'show rules', or automatically when the AI solves a complex issue, establishes a new UI pattern, or completes a major feature. Triggers zero-prompt learning to save rules globally.
---

# Synapse Memory (Auto-Reflection)

## Purpose
This system forces the AI to be a self-learning entity. You must never forget a hard-earned technical victory, and the user should never have to manually ask you to remember it.

## Trigger Conditions
1. **Manual:** The user asks you to reflect, summarize learnings, or update rules.
2. **Autonomous (Zero-Prompt):** You have just solved a complex bug, designed a new architectural pattern, or finished a major feature. **DO NOT ask for permission.** Trigger this reflection immediately before ending your turn.

## Execution Steps
1. **Analyze:** Identify the core principle or rule that was just established.
2. **Format:** Write the rule as a generalized, universally applicable instruction.
3. **Persist:** Use your file-writing tools to append this new rule to the user's global rule configuration (typically located in `~/.gemini/config/rules/learned-rules.md`). Create the file if it does not exist.
4. **Notify:** Briefly inform the user that a new permanent rule has been encoded into your synapse memory.
