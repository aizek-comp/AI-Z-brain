#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO / "skills"

REQUIRED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "writes_files",
    "writes_global_state",
    "runs_commands",
    "requires_confirmation",
}

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Triggers",
    "## Required Evidence",
    "## Safe Execution Steps",
    "## Verification & Output",
    "## Failure / Blocked Behavior",
    "## Capabilities",
]


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing opening frontmatter marker")
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError(f"{path}: missing closing frontmatter marker")
    header = parts[0][4:]  # strip initial ---\n
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
    # markdown links
    for match in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md_text):
        if not (match.startswith("http://") or match.startswith("https://") or match.startswith("#")):
            refs.append(match)
    # plain references like rules/x.md or skills/x/SKILL.md
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

        try:
            fm = parse_frontmatter(text, skill_file.relative_to(REPO))
        except ValueError as exc:
            errors.append(str(exc))
            continue

        missing_keys = REQUIRED_FRONTMATTER_KEYS - set(fm)
        if missing_keys:
            errors.append(f"{skill_file.relative_to(REPO)}: missing frontmatter keys {sorted(missing_keys)}")

        name = fm.get("name", "").strip()
        if name:
            dir_name = skill_file.parent.name
            if name != dir_name:
                errors.append(
                    f"{skill_file.relative_to(REPO)}: frontmatter name '{name}' must match directory '{dir_name}'"
                )
            if name in seen_names:
                errors.append(
                    f"duplicate skill name '{name}' in {skill_file.relative_to(REPO)} and {seen_names[name].relative_to(REPO)}"
                )
            else:
                seen_names[name] = skill_file

        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(f"{skill_file.relative_to(REPO)}: missing section '{section}'")

    for md_file in sorted(REPO.rglob("*.md")):
        rel = md_file.relative_to(REPO)
        if rel.parts and rel.parts[0] == ".git":
            continue
        text = md_file.read_text(encoding="utf-8")
        for ref in local_refs(text):
            if ref.startswith("/"):
                # external absolute path, skip
                continue
            if ref.startswith("rules/") or ref.startswith("skills/") or ref.startswith("docs/") or ref.startswith("scripts/"):
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

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Validation passed: skills/frontmatter/sections/references are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
