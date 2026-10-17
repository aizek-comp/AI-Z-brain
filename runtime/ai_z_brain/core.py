from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

DEFAULT_CONFIG = {
    "autonomous_learning_enabled": True,
    "allow_global_writes": False,
}

_SCOPE_VALUES = {"project", "global"}
_STATUS_VALUES = {"active", "superseded", "reverted", "provisional"}

_SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_\-\/=+]{8,}"),
    re.compile(r"\b(?:ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
]


@dataclass
class MemoryRecord:
    memory_id: str
    status: str
    scope: str
    category: str
    rule: str
    evidence: dict[str, Any]
    confidence: str
    conflicts: list[str] = field(default_factory=list)
    supersedes: str | None = None
    superseded_by: str | None = None
    created_at: str = ""
    rollback: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowExample:
    workflow_id: str
    name: str
    slug: str
    steps: list[str]
    context: str
    outcome: str
    created_at: str


@dataclass
class SkillRecord:
    skill_id: str
    status: str
    origin: str
    evidence_count: int
    confidence: str
    version: str
    scope: str
    name: str
    slug: str
    supersedes: str | None
    superseded_by: str | None = None
    created_at: str = ""
    rollback: dict[str, Any] = field(default_factory=dict)
    workflow_signature: str = ""


class AiZBrainRuntime:
    def __init__(self, repo_root: Path | None = None, state_dir: Path | None = None) -> None:
        self.repo_root = (repo_root or Path.cwd()).resolve()
        self.state_dir = (state_dir or (self.repo_root / ".ai-z-brain")).resolve()
        self.memories_dir = self.state_dir / "memories"
        self.workflows_dir = self.state_dir / "workflows"
        self.skills_dir = self.state_dir / "skills"
        self.audit_path = self.state_dir / "audit.log.jsonl"
        self.config_path = self.state_dir / "config.json"

    def setup(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.memories_dir.mkdir(parents=True, exist_ok=True)
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        if not self.config_path.exists():
            self._write_json(self.config_path, DEFAULT_CONFIG)

    def now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _read_json(self, path: Path, default: Any | None = None) -> Any:
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, value: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=path.parent) as tmp:
            json.dump(value, tmp, indent=2, sort_keys=True)
            tmp.write("\n")
            temp_path = Path(tmp.name)
        temp_path.replace(path)

    def _append_audit(self, action: str, payload: dict[str, Any]) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": self.now(),
            "action": action,
            "payload": payload,
        }
        with self.audit_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry, sort_keys=True) + "\n")

    def get_config(self) -> dict[str, Any]:
        self.setup()
        loaded = self._read_json(self.config_path, {}) or {}
        cfg = dict(DEFAULT_CONFIG)
        cfg.update(loaded)
        return cfg

    def set_autonomous_learning(self, enabled: bool) -> dict[str, Any]:
        cfg = self.get_config()
        cfg["autonomous_learning_enabled"] = bool(enabled)
        self._write_json(self.config_path, cfg)
        self._append_audit("autonomous_learning_toggled", {"enabled": bool(enabled)})
        return cfg

    def set_allow_global_writes(self, enabled: bool) -> dict[str, Any]:
        cfg = self.get_config()
        cfg["allow_global_writes"] = bool(enabled)
        self._write_json(self.config_path, cfg)
        self._append_audit("allow_global_writes_toggled", {"enabled": bool(enabled)})
        return cfg

    def _sanitize_text(self, value: str) -> tuple[str, bool]:
        redacted = value
        did_redact = False
        for idx, pattern in enumerate(_SECRET_PATTERNS):
            if idx == 0 and pattern.search(redacted):
                raise ValueError("Refusing to persist private key material")
            if pattern.search(redacted):
                redacted = pattern.sub("[REDACTED]", redacted)
                did_redact = True
        return redacted.strip(), did_redact

    def _sanitize_many(self, values: list[str]) -> tuple[list[str], bool]:
        sanitized: list[str] = []
        redacted = False
        for value in values:
            cleaned, changed = self._sanitize_text(value)
            sanitized.append(cleaned)
            redacted = redacted or changed
        return sanitized, redacted

    def _classify_scope(self, requested_scope: str | None) -> tuple[str, str]:
        cfg = self.get_config()
        if requested_scope == "global":
            if cfg.get("allow_global_writes"):
                return "global", ""
            return "project", "global scope requested but allow_global_writes is disabled"
        return "project", ""

    def _next_id(self, prefix: str, collection: Path) -> str:
        date = datetime.now(timezone.utc).strftime("%Y%m%d")
        count = len(list(collection.rglob("*.json"))) + 1
        return f"{prefix}-{date}-{count:04d}"

    def _load_memory_records(self, scope: str | None = None) -> list[MemoryRecord]:
        records: list[MemoryRecord] = []
        roots = [self.memories_dir / scope] if scope else sorted(self.memories_dir.glob("*"))
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*.json")):
                raw = self._read_json(path)
                if not raw:
                    continue
                records.append(MemoryRecord(**raw))
        return records

    def add_memory(
        self,
        lesson: str,
        evidence: list[str],
        context: str = "",
        scope: str | None = None,
        category: str = "workflow",
        confidence: str | None = None,
        supersedes: str | None = None,
    ) -> dict[str, Any]:
        self.setup()
        sanitized_lesson, lesson_redacted = self._sanitize_text(lesson)
        sanitized_evidence, evidence_redacted = self._sanitize_many(evidence)
        sanitized_context, context_redacted = self._sanitize_text(context)
        chosen_scope, scope_note = self._classify_scope(scope)
        redaction_applied = lesson_redacted or evidence_redacted or context_redacted
        cfg = self.get_config()
        if confidence is None:
            confidence = "high" if len(sanitized_evidence) >= 3 else "medium"

        if not cfg.get("autonomous_learning_enabled"):
            proposal = {
                "mode": "proposal",
                "reason": "autonomous learning disabled",
                "memory": {
                    "scope": chosen_scope,
                    "category": category,
                    "rule": sanitized_lesson,
                    "evidence": sanitized_evidence,
                    "context": sanitized_context,
                    "confidence": confidence,
                },
            }
            self._append_audit("memory_add_proposal", proposal)
            return proposal

        existing = self._load_memory_records(chosen_scope)
        active = [m for m in existing if m.status == "active"]
        conflicts = [m for m in active if m.rule.casefold() == sanitized_lesson.casefold()]

        superseded_record: MemoryRecord | None = None
        if supersedes:
            superseded_record = next((m for m in active if m.memory_id == supersedes), None)
        elif conflicts:
            superseded_record = conflicts[0]

        record = MemoryRecord(
            memory_id=self._next_id("mem", self.memories_dir),
            status="active",
            scope=chosen_scope,
            category=category,
            rule=sanitized_lesson,
            evidence={"items": sanitized_evidence, "context": sanitized_context},
            confidence=confidence,
            conflicts=[m.memory_id for m in conflicts],
            supersedes=superseded_record.memory_id if superseded_record else None,
            created_at=self.now(),
            rollback={"operation": "memory rollback", "target": "memory_id", "id": ""},
        )
        record.rollback["id"] = record.memory_id

        try:
            mem_path = self.memories_dir / chosen_scope / f"{record.memory_id}.json"
            self._write_json(mem_path, asdict(record))
            if superseded_record:
                superseded_record.status = "superseded"
                superseded_record.superseded_by = record.memory_id
                prev_path = self.memories_dir / superseded_record.scope / f"{superseded_record.memory_id}.json"
                self._write_json(prev_path, asdict(superseded_record))
        except OSError:
            proposal = {
                "mode": "proposal",
                "reason": "safe persistence unavailable",
                "memory": asdict(record),
            }
            self._append_audit("memory_add_proposal", proposal)
            return proposal

        result = {
            "mode": "persisted",
            "memory": asdict(record),
            "redaction_applied": redaction_applied,
            "scope_note": scope_note,
        }
        self._append_audit("memory_added", result)
        return result

    def list_memories(self, scope: str | None = None) -> list[dict[str, Any]]:
        self.setup()
        return [asdict(m) for m in self._load_memory_records(scope)]

    def rollback_memory(self, memory_id: str) -> dict[str, Any]:
        self.setup()
        for record in self._load_memory_records():
            if record.memory_id == memory_id:
                record.status = "reverted"
                path = self.memories_dir / record.scope / f"{record.memory_id}.json"
                self._write_json(path, asdict(record))
                result = {"memory_id": memory_id, "status": record.status}
                self._append_audit("memory_rollback", result)
                return result
        raise ValueError(f"Memory not found: {memory_id}")

    def record_workflow(self, name: str, steps: list[str], outcome: str, context: str = "") -> dict[str, Any]:
        self.setup()
        safe_name, redacted_name = self._sanitize_text(name)
        safe_steps, redacted_steps = self._sanitize_many(steps)
        safe_context, redacted_context = self._sanitize_text(context)
        slug = slugify(safe_name)
        workflow = WorkflowExample(
            workflow_id=self._next_id("wf", self.workflows_dir),
            name=safe_name,
            slug=slug,
            steps=safe_steps,
            context=safe_context,
            outcome=outcome,
            created_at=self.now(),
        )
        path = self.workflows_dir / slug / f"{workflow.workflow_id}.json"
        self._write_json(path, asdict(workflow))
        result = {
            "workflow": asdict(workflow),
            "redaction_applied": redacted_name or redacted_steps or redacted_context,
        }
        self._append_audit("workflow_recorded", result)
        return result

    def list_workflows(self, name: str | None = None) -> list[dict[str, Any]]:
        self.setup()
        slug = slugify(name) if name else None
        roots = [self.workflows_dir / slug] if slug else sorted(self.workflows_dir.glob("*"))
        workflows: list[dict[str, Any]] = []
        for root in roots:
            if not root.exists():
                continue
            for path in sorted(root.glob("*.json")):
                item = self._read_json(path)
                if item:
                    workflows.append(item)
        return workflows

    def _generate_skill_markdown(self, record: SkillRecord, examples: list[dict[str, Any]], description: str) -> str:
        sample_steps = examples[-1]["steps"] if examples else []
        example_steps_md = "\n".join(f"{i+1}. {step}" for i, step in enumerate(sample_steps)) or "1. Perform validated workflow steps."
        return (
            f"---\n"
            f"name: {record.slug}\n"
            f"description: {description}\n"
            "writes_files: true\n"
            f"writes_global_state: {'true' if record.scope == 'global' else 'false'}\n"
            "runs_commands: false\n"
            "requires_confirmation: false\n"
            "---\n\n"
            f"# {record.name}\n\n"
            "## Purpose\n"
            f"Execute the {record.name} workflow safely and consistently from proven examples.\n\n"
            "## Triggers\n"
            f"- Use when handling workflow family: `{record.slug}`.\n\n"
            "## Required Evidence\n"
            f"- At least {record.evidence_count} successful materially similar examples.\n\n"
            "## Safe Execution Steps\n"
            f"{example_steps_md}\n\n"
            "## Verification & Output\n"
            "- Verify outcome is successful and no secret material is persisted.\n"
            f"- Skill ID: `{record.skill_id}` version `{record.version}`.\n\n"
            "## Failure / Blocked Behavior\n"
            "- If workflow context diverges or validation fails, stop and return proposal-only guidance.\n\n"
            "## Capabilities\n"
            "- Writes files: Yes\n"
            f"- Writes global state: {'Yes' if record.scope == 'global' else 'No'}\n"
            "- Runs commands: No\n"
            "- Requires confirmation: No\n"
        )

    def _skill_records(self, scope: str | None = None) -> list[SkillRecord]:
        records: list[SkillRecord] = []
        roots = [self.skills_dir / scope] if scope else sorted(self.skills_dir.glob("*"))
        for root in roots:
            if not root.exists():
                continue
            for meta in root.glob("*/*/metadata.json"):
                raw = self._read_json(meta)
                if raw:
                    records.append(SkillRecord(**raw))
        return records

    def weave_skill(self, workflow: str, scope: str | None = None, description: str | None = None) -> dict[str, Any]:
        self.setup()
        slug = slugify(workflow)
        chosen_scope, scope_note = self._classify_scope(scope)
        examples = [w for w in self.list_workflows(workflow) if w.get("outcome") == "success"]
        if len(examples) < 3:
            proposal = {
                "mode": "proposal",
                "reason": "insufficient successful materially similar examples",
                "required": 3,
                "actual": len(examples),
                "workflow": workflow,
            }
            self._append_audit("skill_weave_proposal", proposal)
            return proposal

        if not self.get_config().get("autonomous_learning_enabled"):
            proposal = {
                "mode": "proposal",
                "reason": "autonomous learning disabled",
                "workflow": workflow,
                "evidence_count": len(examples),
            }
            self._append_audit("skill_weave_proposal", proposal)
            return proposal

        signature = hashlib.sha256(json.dumps(examples, sort_keys=True).encode("utf-8")).hexdigest()
        existing = [s for s in self._skill_records(chosen_scope) if s.slug == slug and s.status == "active"]
        for active in existing:
            if active.workflow_signature == signature:
                result = {"mode": "duplicate", "skill": asdict(active), "scope_note": scope_note}
                self._append_audit("skill_duplicate", result)
                return result

        version_number = 1
        previous_active: SkillRecord | None = None
        if existing:
            previous_active = max(existing, key=lambda item: int(item.version.lstrip("v")))
            version_number = int(previous_active.version.lstrip("v")) + 1

        record = SkillRecord(
            skill_id=self._next_id("skill", self.skills_dir),
            status="active",
            origin="autonomous",
            evidence_count=len(examples),
            confidence="high",
            version=f"v{version_number}",
            scope=chosen_scope,
            name=workflow,
            slug=slug,
            supersedes=previous_active.skill_id if previous_active else None,
            created_at=self.now(),
            rollback={"operation": "skill rollback", "target": "skill_id", "id": ""},
            workflow_signature=signature,
        )
        record.rollback["id"] = record.skill_id
        markdown = self._generate_skill_markdown(
            record,
            examples,
            description or f"Autogenerated skill for {workflow} from validated examples.",
        )

        try:
            version_dir = self.skills_dir / chosen_scope / slug / record.version
            self._write_json(version_dir / "metadata.json", asdict(record))
            with NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=version_dir) as tmp:
                tmp.write(markdown)
                tmp.write("\n")
                temp_path = Path(tmp.name)
            temp_path.replace(version_dir / "SKILL.md")

            if previous_active:
                previous_active.status = "superseded"
                previous_active.superseded_by = record.skill_id
                prev_dir = self.skills_dir / previous_active.scope / previous_active.slug / previous_active.version
                self._write_json(prev_dir / "metadata.json", asdict(previous_active))
        except OSError:
            proposal = {
                "mode": "proposal",
                "reason": "safe persistence unavailable",
                "skill": asdict(record),
            }
            self._append_audit("skill_weave_proposal", proposal)
            return proposal

        result = {
            "mode": "persisted",
            "skill": asdict(record),
            "skill_file": str((self.skills_dir / chosen_scope / slug / record.version / "SKILL.md")),
            "scope_note": scope_note,
        }
        self._append_audit("skill_woven", result)
        return result

    def list_skills(self, scope: str | None = None) -> list[dict[str, Any]]:
        self.setup()
        return [asdict(s) for s in self._skill_records(scope)]

    def rollback_skill(self, skill_id: str) -> dict[str, Any]:
        self.setup()
        for record in self._skill_records():
            if record.skill_id == skill_id:
                record.status = "reverted"
                meta = self.skills_dir / record.scope / record.slug / record.version / "metadata.json"
                self._write_json(meta, asdict(record))
                result = {"skill_id": skill_id, "status": record.status}
                self._append_audit("skill_rollback", result)
                return result
        raise ValueError(f"Skill not found: {skill_id}")

    def audit_entries(self, limit: int | None = None) -> list[dict[str, Any]]:
        self.setup()
        if not self.audit_path.exists():
            return []
        entries = [json.loads(line) for line in self.audit_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if limit is not None:
            entries = entries[-limit:]
        return entries

    def status(self) -> dict[str, Any]:
        cfg = self.get_config()
        return {
            "state_dir": str(self.state_dir),
            "config": cfg,
            "memory_count": len(self._load_memory_records()),
            "workflow_count": len(self.list_workflows()),
            "skill_count": len(self._skill_records()),
            "audit_entries": len(self.audit_entries()),
        }


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "skill"
