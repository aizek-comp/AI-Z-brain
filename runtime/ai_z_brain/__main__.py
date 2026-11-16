from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import AiZBrainRuntime


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m runtime.ai_z_brain", description="AI-Z Brain reference runtime")
    parser.add_argument("--state-dir", type=Path, default=None, help="State directory (default: .ai-z-brain in cwd)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show runtime status")
    sub.add_parser("enable", help="Enable autonomous learning")
    sub.add_parser("disable", help="Disable autonomous learning (proposal-only mode)")

    cfg = sub.add_parser("config", help="Configure runtime settings")
    cfg_sub = cfg.add_subparsers(dest="config_command", required=True)
    cfg_global = cfg_sub.add_parser("set-global-writes", help="Toggle opt-in global write support")
    cfg_global.add_argument("enabled", choices=["true", "false"])

    audit = sub.add_parser("audit", help="Show append-only audit entries")
    audit.add_argument("--limit", type=int, default=20)

    memory = sub.add_parser("memory", help="Manage persisted memory records")
    memory_sub = memory.add_subparsers(dest="memory_command", required=True)
    mem_add = memory_sub.add_parser("add", help="Add memory with safety checks")
    mem_add.add_argument("--lesson", required=True)
    mem_add.add_argument("--evidence", action="append", default=[])
    mem_add.add_argument("--context", default="")
    mem_add.add_argument("--scope", choices=["project", "global"], default=None)
    mem_add.add_argument("--category", default="workflow")
    mem_add.add_argument("--confidence", choices=["low", "medium", "high"], default=None)
    mem_add.add_argument("--supersedes", default=None)

    mem_list = memory_sub.add_parser("list", help="List memory records")
    mem_list.add_argument("--scope", choices=["project", "global"], default=None)

    mem_roll = memory_sub.add_parser("rollback", help="Rollback memory by ID")
    mem_roll.add_argument("memory_id")

    workflow = sub.add_parser("workflow", help="Record/list workflow examples")
    workflow_sub = workflow.add_subparsers(dest="workflow_command", required=True)
    wf_record = workflow_sub.add_parser("record", help="Record a workflow example")
    wf_record.add_argument("--name", required=True)
    wf_record.add_argument("--step", action="append", default=[])
    wf_record.add_argument("--context", default="")
    wf_record.add_argument("--outcome", choices=["success", "failure"], required=True)
    wf_list = workflow_sub.add_parser("list", help="List workflow examples")
    wf_list.add_argument("--name", default=None)

    skill = sub.add_parser("skill", help="Weave/list/rollback generated skills")
    skill_sub = skill.add_subparsers(dest="skill_command", required=True)
    sk_weave = skill_sub.add_parser("weave", help="Generate a skill from repeated successful workflows")
    sk_weave.add_argument("--workflow", required=True)
    sk_weave.add_argument("--scope", choices=["project", "global"], default=None)
    sk_weave.add_argument("--description", default=None)
    sk_list = skill_sub.add_parser("list", help="List generated skills")
    sk_list.add_argument("--scope", choices=["project", "global"], default=None)
    sk_roll = skill_sub.add_parser("rollback", help="Rollback generated skill by ID")
    sk_roll.add_argument("skill_id")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    runtime = AiZBrainRuntime(state_dir=args.state_dir)

    if args.command == "status":
        payload = runtime.status()
    elif args.command == "enable":
        payload = runtime.set_autonomous_learning(True)
    elif args.command == "disable":
        payload = runtime.set_autonomous_learning(False)
    elif args.command == "config":
        payload = runtime.set_allow_global_writes(args.enabled == "true")
    elif args.command == "audit":
        payload = runtime.audit_entries(args.limit)
    elif args.command == "memory":
        if args.memory_command == "add":
            payload = runtime.add_memory(
                lesson=args.lesson,
                evidence=args.evidence,
                context=args.context,
                scope=args.scope,
                category=args.category,
                confidence=args.confidence,
                supersedes=args.supersedes,
            )
        elif args.memory_command == "list":
            payload = runtime.list_memories(scope=args.scope)
        else:
            payload = runtime.rollback_memory(args.memory_id)
    elif args.command == "workflow":
        if args.workflow_command == "record":
            payload = runtime.record_workflow(
                name=args.name,
                steps=args.step,
                outcome=args.outcome,
                context=args.context,
            )
        else:
            payload = runtime.list_workflows(name=args.name)
    elif args.command == "skill":
        if args.skill_command == "weave":
            payload = runtime.weave_skill(
                workflow=args.workflow,
                scope=args.scope,
                description=args.description,
            )
        elif args.skill_command == "list":
            payload = runtime.list_skills(scope=args.scope)
        else:
            payload = runtime.rollback_skill(args.skill_id)
    else:
        raise ValueError(f"Unsupported command: {args.command}")

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
