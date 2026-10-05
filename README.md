# 🧠 Agent Brain: Autonomous Systems Engineer Framework

`Agent Brain` is an open-source configuration framework that transforms your standard AI coding assistant into a highly disciplined, proactive Systems Engineer. 

Instead of a passive chatbot that generates generic UI and forgets complex fixes, this framework injects **zero-prompt learning**, **strict engineering standards**, and a suite of **8 autonomous protocols** directly into your local AI environment.

---

## 🚀 Quick Start Installation

1. Locate your local AI configuration directory (typically `~/.gemini/config/`).
2. Copy the contents of the `rules/` folder from this repo into `~/.gemini/config/rules/`.
3. Copy the contents of the `skills/` folder from this repo into `~/.gemini/config/skills/`.
4. **The Magic Setup:** Open a new chat session and simply say "Hello". The AI will detect that it is uninitialized and will instantly launch an interactive Setup Wizard in the chat. It will ask for your preferences and *automatically rewrite its own configuration files* for you!

---

## ⚡ The 8 Autonomous Protocols (Skills)

This framework equips the AI with an arsenal of advanced protocols. Some are triggered by your commands, while others fire **autonomously** in the background when the AI detects a specific condition.

| Protocol Name | Manual Voice Trigger | Autonomous Trigger | Execution Capability |
| :--- | :--- | :--- | :--- |
| **`synapse-memory`** | *"activate reflection"* | Solves a complex bug | Extracts the root cause and saves it permanently to global rules. |
| **`skill-weaver`** | *"forge this"* | Detects 3x repeated workflow | Automatically writes a new `SKILL.md` to teach itself a new ability. |
| **`sentinel-commit`** | *"commit changes"* | Completes a project milestone | Runs `git status`, diffs the code, and commits changes to Git. |
| **`deep-assimilation`** | *"analyze all and absorb"* | - | Deep-scans the repository to map the entire architectural routing. |
| **`code-sonar`** | *"scan project"* | Before a massive file refactor | Executes terminal commands to trace component dependencies. |
| **`momentum-drive`** | *"execute plan"* | - | Reads a master checklist and executes it step-by-step. |
| **`architect-codex`** | *"log decision"* | Makes a critical trade-off | Logs the "why" behind an architectural choice to a markdown ledger. |
| **`pattern-matrix`** | *"save to library"* | - | Saves or retrieves complex UI/Code templates from the Akashic records. |

---

## 📜 The Startup Mandate

When you start a new session and say hello, the AI is strictly programmed to greet you and remind you of the **Three Core Directives**:
1. **Analyze and Absorb All:** Triggers `deep-assimilation`.
2. **Activate Reflection:** Triggers `synapse-memory`.
3. **Domain Knowledge Assimilation:** Commands the AI to scan your folders for any specialized `-domain` knowledge rules.

---

## 💡 Example User Journey

Here is what it looks like to work with an Agent Brain-powered AI:

> **You:** "Atlas, I need to build a new data parser for our backend."
> 
> **AI (Atlas):** "Let's get this done. I will use Python, as requested. However, before I write a single line of code, provide me with a sample of the exact raw data we are parsing so I can verify the ground truth. We don't guess architectures here." 
> *(Notice: The AI adopted your custom persona, but strictly enforced Rule #1 from `01-global-philosophy.md`)*
>
> *(Later, after fixing a nasty WAF networking bug...)*
> 
> **AI (Atlas):** "The routing anomaly is resolved. I am triggering `synapse-memory` to log the WAF header bypass rule so I never make this mistake again." *(Executes skill autonomously)*
>
> **AI (Atlas):** "I am also triggering `sentinel-commit` to lock in our progress." *(Commits to Git autonomously)*

---

## 🏛️ The Engineering Philosophy

By installing `01-global-philosophy.md`, your AI is bound to strict rules, including:
* **The High-Fidelity Standard:** No more generic "Codex UI" (rounded corners, soft gradients). The AI will default to human-centric, high-fidelity design.
* **The Null-Type Fallback:** The AI will defensively parse all external datasets, assuming data might be null, preventing silent 500 crashes.
* **Ghost Pruning:** When syncing large databases, the AI will use timestamps to cull stale data instead of wiping tables, guaranteeing zero downtime.
