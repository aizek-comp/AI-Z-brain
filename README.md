# 🧠 AI-Z Brain: Autonomous Systems Engineer Framework

`AI-Z Brain` is a Markdown configuration/protocol pack for shaping assistant behavior.

It defines guardrails and autonomous-learning workflows, but it is **not** an enforced runtime. Actual execution depends on host capabilities and policy enforcement in the environment where these files are used.

---

## 🚀 Quick Start

1. Copy `rules/` into your local assistant rules directory (for example `~/.gemini/config/rules/`).
2. Copy `skills/` into your local assistant skills directory (for example `~/.gemini/config/skills/`).
3. Start a new chat/session and apply your preferred persona/setup flow.

---

## ⚡ Skills Matrix

| Skill | Manual Trigger | Autonomous Trigger | Confirmation Required | Notes |
| :--- | :--- | :--- | :---: | :--- |
| `synapse-memory` | "activate reflection" | Evidence-backed completed fixes/features | No | Automatically persists **safe, redacted** memory entries with audit + rollback metadata. Global writes are limited to this bounded autonomous-learning workflow. |
| `skill-weaver` | "create skill" / "forge this" | 3+ successful materially similar workflows | No | Automatically creates/updates **safe, redacted** reusable skills with version history and rollback metadata. Global writes are limited to this bounded autonomous-learning workflow. |
| `sentinel-commit` | "commit changes" | N/A | Yes | Commits/pushes and other durable mutations require explicit owner confirmation. |
| `deep-assimilation` | "analyze all and absorb" | N/A | Context-dependent | Repository mapping and analysis protocol. |
| `code-sonar` | "scan project" | Before high-risk refactors | Context-dependent | Dependency and impact analysis protocol. |
| `momentum-drive` | "execute plan" | N/A | Context-dependent | Checklist-driven execution protocol. |
| `architect-codex` | "log decision" | Critical trade-offs | Context-dependent | Architecture decision capture protocol. |
| `pattern-matrix` | "save to library" | N/A | Context-dependent | Pattern capture/retrieval protocol. |

---

## 🔐 Trust & Safety Model

Durable/high-impact actions still require confirmation, including commits, pushes, destructive mutations, and external side effects.

Autonomous exceptions are intentionally narrow:
- `synapse-memory` may auto-persist safe, evidence-backed lessons.
- `skill-weaver` may auto-create/update safe, evidence-backed skills.

Both autonomous workflows require:
- sensitive-data redaction/refusal
- owner-visible audit notifications
- versioning/conflict lineage
- rollback metadata
- proposal fallback when safe persistence is unavailable

You can disable autonomous learning (opt-out). When disabled, these workflows must run in proposal-only mode.

---

## 🧪 Validation

Run:

```bash
python scripts/validate_framework.py
```

The validator checks core skill frontmatter/sections and required safety documentation files.
