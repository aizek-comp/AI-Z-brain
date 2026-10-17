#!/usr/bin/env python3
"""Dependency-free framework validator for AI-Z-brain."""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

REQUIRED_SKILL_SECTIONS = {
    "synapse-memory": [
        "## Trigger Conditions",
        "## Automatic Pipeline",
        "## Memory Record Schema",
        "## Conflict & History Handling",
        "## Uncertainty Handling",
        "## Audit, Disable, and Rollback",
    ],
    "skill-weaver": [
        "## Trigger Conditions",
        "## Automatic Pipeline",
        "## Skill Metadata Schema",
        "## Conflict, Versioning, and History",
        "## Audit, Disable, and Rollback",
    ],
}

AUTONOMOUS_LEARNING_SKILLS = {"synapse-memory", "skill-weaver"}


class ValidationError(Exception):
    pass


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError("Missing frontmatter delimiter '---' on first line")

    frontmatter: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if ":" not in line:
            raise ValidationError(f"Invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()
        i += 1

    if i >= len(lines) or lines[i].strip() != "---":
        raise ValidationError("Missing closing frontmatter delimiter '---'")

    body = "\n".join(lines[i + 1 :])
    return frontmatter, body


def validate_skill(skill_path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    skill_dir = skill_path.parent.name

    text = skill_path.read_text(encoding="utf-8")

    try:
        frontmatter, body = parse_frontmatter(text)
    except ValidationError as exc:
        return [f"{skill_path}: {exc}"]

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if name != skill_dir:
        errors.append(f"{skill_path}: frontmatter name '{name}' must match directory '{skill_dir}'")

    if not description:
        errors.append(f"{skill_path}: missing frontmatter description")

    requires_confirmation = frontmatter.get("requires_confirmation")
    if skill_dir in AUTONOMOUS_LEARNING_SKILLS:
        if requires_confirmation != "false":
            errors.append(
                f"{skill_path}: {skill_dir} must set requires_confirmation: false"
            )
    elif requires_confirmation == "false":
        errors.append(
            f"{skill_path}: only {sorted(AUTONOMOUS_LEARNING_SKILLS)} may set requires_confirmation: false"
        )

    required_sections = REQUIRED_SKILL_SECTIONS.get(skill_dir, [])
    for section in required_sections:
        if section not in body:
            errors.append(f"{skill_path}: missing required section '{section}'")

    if skill_dir == "synapse-memory":
        for key in [
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
        ]:
            if re.search(rf"`{re.escape(key)}`", body) is None:
                errors.append(f"{skill_path}: memory schema key `{key}` not documented")

    if skill_dir == "skill-weaver":
        for key in [
            "skill_id",
            "origin",
            "evidence_count",
            "confidence",
            "version",
            "scope",
            "supersedes",
            "created_at",
            "rollback",
        ]:
            if re.search(rf"`{re.escape(key)}`", body) is None:
                errors.append(f"{skill_path}: skill metadata key `{key}` not documented")

    return errors


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"error: missing skills directory at {SKILLS_DIR}")
        return 1

    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        print("error: no skills found")
        return 1

    all_errors: list[str] = []
    for skill_file in skill_files:
        all_errors.extend(validate_skill(skill_file))

    required_paths = [
        ROOT / "rules" / "02-trust-safety-execution-policy.md",
        ROOT / "docs" / "safety-scenarios.md",
    ]
    for required_path in required_paths:
        if not required_path.exists():
            all_errors.append(f"{required_path}: missing required file")

    if all_errors:
        print("Validation failed:\n")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
