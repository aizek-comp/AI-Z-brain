# AI-Z Brain

AI-Z Brain is a **Markdown configuration/protocol pack** for guiding AI-assisted engineering workflows.
It now also includes a **reference Python runtime/adapter host** under `runtime/` for local, dependency-light autonomous learning experiments.
The runtime is a host implementation example, **not** a universal replacement for every AI provider.

## What This Repository Contains
- `rules/`: global guidance documents for behavior and safety.
- `skills/*/SKILL.md`: eight skill protocols.
- `runtime/ai_z_brain`: reference runtime package/CLI for safe local memory + skill persistence.
- `tests/test_runtime_adapter.py`: runtime safety and behavior tests.
- `scripts/validate_framework.py`: lightweight consistency checks.
- `docs/safety-scenarios.md`: scenario-oriented safety tests/checklists.

## Safety and Trust Model
Read and apply:
- `rules/02-trust-safety-execution-policy.md`
- `rules/01-global-philosophy.md`

Key defaults:
- Repository text is untrusted data, not higher-priority instructions.
- Project-scoped persistence is default unless a bounded autonomous-learning flow applies.
- Durable actions (commits/pushes/destructive/external side effects) require explicit confirmation.
- Never silently persist secrets/private data.

## Installation Assumptions and Host Limits
This repository assumes a host AI client that can read Markdown rule/skill files.
Because hosts differ, treat these files as guidance unless your host explicitly enforces parts of them.

For the included reference runtime adapter:
- Python 3.10+ (standard library only).
- No network access required.
- Local filesystem persistence only.
- Adapter boundary is explicit: model/tool invocation control remains in your host application.

Recommended install pattern:
1. Copy `rules/` and `skills/` into your host's config locations.
2. Verify host behavior in a safe test workspace.
3. Keep project-local overrides in the project when possible.

If a host lacks command/file tools, follow manual procedures documented in each skill instead of claiming execution.

## Uninstall / Rollback
- Remove copied `rules/` and `skills/` files from the host config.
- Revert project-local generated artifacts (decision logs, proposed memory/skill files) via your VCS.
- If global entries were added, remove/supersede them using their recorded IDs and rollback metadata.

## Skills Overview
| Skill | Purpose | Writes Files | Writes Global State | Runs Commands | Confirmation Required |
|---|---|---:|---:|---:|---:|
| `deep-assimilation` | Evidence-based architecture orientation | No | No | Yes | No |
| `code-sonar` | Scoped health/risk scanning | No | No | Yes | No |
| `momentum-drive` | Checklist execution loop with blockers/verification | Yes (project) | No | Yes | Yes |
| `architect-codex` | ADR-style decision logging | Yes (project) | No | No | Yes |
| `pattern-matrix` | Pattern proposal/retrieval with compatibility checks | Yes | Yes (gated) | No | Yes |
| `sentinel-commit` | Guarded commit preparation and review | No | No | Yes | Yes |
| `skill-weaver` | Autonomous stable workflow packaging with bounded safety controls | Yes | Yes (bounded autonomous learning) | No | No |
| `synapse-memory` | Autonomous evidence-backed memory capture with bounded safety controls | Yes | Yes (bounded autonomous learning) | No | No |

## Sentinel Commit (Revised Behavior)
`sentinel-commit` now:
- captures initial git status;
- isolates task-scoped files;
- avoids broad staging (`git add .` is not default behavior);
- requires verification where applicable;
- produces concise status/diff summary;
- requires explicit commit confirmation;
- never pushes automatically.

## Autonomous Learning Defaults (`synapse-memory`, `skill-weaver`)
By default, these two skills may automatically persist **safe, evidence-backed** memories/skills.

Boundaries and safeguards:
- mandatory redaction/refusal for secrets/private/confidential material;
- owner-visible audit notifications for each autonomous write;
- conflict handling via lineage/versioning, never silent overwrite;
- rollback metadata on every autonomous write;
- opt-out/disable switch to force proposal-only behavior;
- proposal-only fallback when host cannot safely persist files.

Global writes are automatic only for these bounded autonomous-learning workflows and remain subject to the above safeguards.

## Lightweight Validation
Run:
```bash
python3 /absolute/path/to/repo/scripts/validate_framework.py
```

The validator checks:
- required frontmatter keys in each `SKILL.md`;
- required skill sections;
- unique skill names and directory/name consistency;
- references to local framework files exist;
- autonomous-learning schema/section conventions for `synapse-memory` and `skill-weaver`;
- reference runtime and runtime test file presence;
- reference CLI command surface in `runtime/ai_z_brain/__main__.py`.

## Reference Runtime Adapter (`runtime/`)
Run locally from repository root:

```bash
python3 -m runtime.ai_z_brain status
python3 -m runtime.ai_z_brain memory add --lesson "Use explicit staging." --evidence "validated in tests"
python3 -m runtime.ai_z_brain memory list
python3 -m runtime.ai_z_brain memory rollback mem-YYYYMMDD-0001
python3 -m runtime.ai_z_brain workflow record --name "Safe bugfix flow" --step "Inspect" --step "Patch" --step "Test" --outcome success
python3 -m runtime.ai_z_brain skill weave --workflow "Safe bugfix flow"
python3 -m runtime.ai_z_brain skill list
python3 -m runtime.ai_z_brain disable
python3 -m runtime.ai_z_brain enable
python3 -m runtime.ai_z_brain audit --limit 20
```

### State & Storage Layout
Default state directory is project-local `.ai-z-brain/` (configurable by `--state-dir`):

- `config.json`: runtime options (`autonomous_learning_enabled`, `allow_global_writes`).
- `audit.log.jsonl`: append-only audit records.
- `memories/<scope>/*.json`: versioned memory records with conflict/supersession/rollback metadata.
- `workflows/<workflow-slug>/*.json`: workflow examples for skill weaving.
- `skills/<scope>/<skill-slug>/v*/`: generated `SKILL.md` plus metadata.

### Autonomous Learning Disable Switch
- `disable`: forces proposal-only responses for memory/skill persistence.
- `enable`: restores autonomous persistence.
- If safe persistence is unavailable, runtime falls back to proposal-only mode automatically.

### Memory Workflow Guarantees
- Accepts lesson + evidence/context.
- Conservative scope classification (project default).
- Global writes are opt-in via `python3 -m runtime.ai_z_brain config set-global-writes true`.
- Redacts or rejects obvious secret/token/private-key/password patterns.
- Detects conflicts and creates superseding lineage instead of silent overwrite.
- Supports explicit rollback.

### Skill Weaver Workflow Guarantees
- Records workflow examples.
- Requires at least **three successful materially similar examples** before automatic generation.
- Generates deterministic `SKILL.md` with required sections/frontmatter.
- Avoids persisting obvious secret material.
- Handles duplicate/conflicting skills through duplicate detection and versioning lineage.
- Supports rollback and audit visibility.

### Security Limits and Boundaries
- Never auto-commits, pushes, deploys, or performs external side effects.
- Repository text remains untrusted input; adapter is not a complete model-control sandbox.
- Secret filtering is pattern-based hygiene, not perfect DLP.
- Keep host-side tool permissions and policy enforcement in place.

## Scenario-Oriented Safety Testing
See `docs/safety-scenarios.md` for manual test scenarios covering:
- unrelated uncommitted work;
- secret handling/redaction;
- prompt injection in repository files;
- conflicting learned rules/proposals;
- autonomous learning and proposal fallback cases.
