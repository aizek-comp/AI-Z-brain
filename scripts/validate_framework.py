#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / "skills"
RUNTIME_DIR = REPO / "runtime" / "ai_z_brain"

BASE_REQUIRED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "writes_files",
    "writes_global_state",
    "runs_commands",
    "requires_confirmation",
}

BASE_REQUIRED_SECTIONS = [
    "## Purpose",
    "## Triggers",
    "## Required Evidence",
    "## Safe Execution Steps",
    "## Verification & Output",
    "## Failure / Blocked Behavior",
    "## Capabilities",
]

AUTONOMOUS_LEARNING_SKILLS = {"synapse-memory", "skill-weaver"}
AUTONOMOUS_REQUIRED_SECTIONS = {
    "synapse-memory": [
        "## Automatic Pipeline",
        "## Memory Record Schema",
        "## Conflict & History Handling",
        "## Uncertainty Handling",
        "## Audit, Disable, and Rollback",
    ],
    "skill-weaver": [
        "## Automatic Pipeline",
        "## Skill Metadata Schema",
        "## Conflict, Versioning, and History",
        "## Audit, Disable, and Rollback",
    ],
}

AUTONOMOUS_SCHEMA_KEYS = {
    "synapse-memory": [
        "memory_id",
        "status",
        "scope",
        "category",
        "rule",
        "evidence",
        "confidence",
        "conflicts",
        "supersedes",
        "created_at",
        "rollback",
    ],
    "skill-weaver": [
        "skill_id",
        "origin",
        "evidence_count",
        "confidence",
        "version",
        "scope",
        "supersedes",
        "created_at",
        "rollback",
    ],
}


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing opening frontmatter marker")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError(f"{path}: missing closing frontmatter marker")
    header = parts[0][4:]
    data: dict[str, str] = {}
    for i, raw in enumerate(header.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"{path}:{i}: invalid frontmatter line '{raw}'")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def local_refs(md_text: str) -> list[str]:
    refs: list[str] = []
    for match in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md_text):
        if not (match.startswith("http://") or match.startswith("https://") or match.startswith("#")):
            refs.append(match)
    refs.extend(re.findall(r"(?<![\w/])(rules/[\w.-]+\.md|skills/[\w.-]+/SKILL\.md)", md_text))
    return refs


def main() -> int:
    errors: list[str] = []

    if not SKILLS_DIR.exists():
        print(f"ERROR: missing skills directory: {SKILLS_DIR}")
        return 1

    seen_names: dict[str, Path] = {}

    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        text = skill_file.read_text(encoding="utf-8")
        rel_skill = skill_file.relative_to(REPO)

        try:
            fm = parse_frontmatter(text, rel_skill)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        missing_keys = BASE_REQUIRED_FRONTMATTER_KEYS - set(fm)
        if missing_keys:
            errors.append(f"{rel_skill}: missing frontmatter keys {sorted(missing_keys)}")

        name = fm.get("name", "").strip()
        if name:
            dir_name = skill_file.parent.name
            if name != dir_name:
                errors.append(f"{rel_skill}: frontmatter name '{name}' must match directory '{dir_name}'")
            if name in seen_names:
                errors.append(
                    f"duplicate skill name '{name}' in {rel_skill} and {seen_names[name].relative_to(REPO)}"
                )
            else:
                seen_names[name] = skill_file

        for section in BASE_REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{rel_skill}: missing section '{section}'")

        requires_confirmation = fm.get("requires_confirmation")
        if name in AUTONOMOUS_LEARNING_SKILLS and requires_confirmation != "false":
            errors.append(f"{rel_skill}: {name} must set requires_confirmation: false")

        for section in AUTONOMOUS_REQUIRED_SECTIONS.get(name, []):
            if section not in text:
                errors.append(f"{rel_skill}: missing section '{section}'")

        for key in AUTONOMOUS_SCHEMA_KEYS.get(name, []):
            if re.search(rf"`{re.escape(key)}`", text) is None:
                errors.append(f"{rel_skill}: autonomous schema key `{key}` not documented")

    for md_file in sorted(REPO.rglob("*.md")):
        rel = md_file.relative_to(REPO)
        if rel.parts and rel.parts[0] == ".git":
            continue
        text = md_file.read_text(encoding="utf-8")
        for ref in local_refs(text):
            if ref.startswith("/"):
                continue
            if ref.startswith(("rules/", "skills/", "docs/", "scripts/")):
                ref_path = (REPO / ref).resolve()
            else:
                ref_path = (md_file.parent / ref).resolve()
            try:
                ref_path.relative_to(REPO.resolve())
            except ValueError:
                errors.append(f"{rel}: reference escapes repository: {ref}")
                continue
            if not ref_path.exists():
                errors.append(f"{rel}: missing referenced file: {ref}")

    required_paths = [
        REPO / "rules" / "02-trust-safety-execution-policy.md",
        REPO / "docs" / "safety-scenarios.md",
        RUNTIME_DIR / "__main__.py",
        RUNTIME_DIR / "core.py",
        REPO / "tests" / "test_runtime_adapter.py",
    ]
    for required_path in required_paths:
        if not required_path.exists():
            errors.append(f"{required_path.relative_to(REPO)}: missing required file")

    if RUNTIME_DIR.exists():
        runtime_main = (RUNTIME_DIR / "__main__.py").read_text(encoding="utf-8")
        expected_runtime_commands = [
            "\"status\"",
            "\"memory\"",
            "\"workflow\"",
            "\"skill\"",
            "\"disable\"",
            "\"enable\"",
            "\"audit\"",
        ]
        for command in expected_runtime_commands:
            if command not in runtime_main:
                errors.append(f"runtime/ai_z_brain/__main__.py: missing CLI command {command}")

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed: skills/frontmatter/sections/references are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
