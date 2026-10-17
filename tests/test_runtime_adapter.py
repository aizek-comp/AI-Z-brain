from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from runtime.ai_z_brain.core import AiZBrainRuntime


class RuntimeAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.state_dir = Path(self.temp_dir.name) / ".ai-z-brain"
        self.runtime = AiZBrainRuntime(state_dir=self.state_dir)

    def test_safe_memory_persistence_includes_metadata(self) -> None:
        result = self.runtime.add_memory(
            lesson="Use explicit file staging during commit.",
            evidence=["scripts/validate_framework.py checks references"],
            context="validated in CI",
            category="workflow",
        )

        self.assertEqual("persisted", result["mode"])
        memory = result["memory"]
        self.assertIn("memory_id", memory)
        self.assertIn("rollback", memory)
        self.assertEqual("active", memory["status"])

        memory_path = self.state_dir / "memories" / memory["scope"] / f"{memory['memory_id']}.json"
        self.assertTrue(memory_path.exists())

    def test_secret_redaction_and_rejection(self) -> None:
        redacted = self.runtime.add_memory(
            lesson="Set token=ghp_1234567890abcdefghij1234567890abc in docs",
            evidence=["token=ghp_1234567890abcdefghij1234567890abc"],
        )
        serialized = json.dumps(redacted)
        self.assertIn("[REDACTED]", serialized)
        self.assertNotIn("ghp_1234567890abcdefghij1234567890abc", serialized)

        with self.assertRaises(ValueError):
            self.runtime.add_memory(
                lesson="-----BEGIN PRIVATE KEY----- sample",
                evidence=["unsafe"],
            )

    def test_conflict_creates_supersession_not_overwrite(self) -> None:
        first = self.runtime.add_memory(
            lesson="Prefer project-scoped persistence by default.",
            evidence=["rules/02-trust-safety-execution-policy.md"],
        )
        second = self.runtime.add_memory(
            lesson="Prefer project-scoped persistence by default.",
            evidence=["README.md"],
        )

        first_id = first["memory"]["memory_id"]
        second_id = second["memory"]["memory_id"]
        self.assertEqual(first_id, second["memory"]["supersedes"])
        records = {item["memory_id"]: item for item in self.runtime.list_memories()}
        self.assertEqual("superseded", records[first_id]["status"])
        self.assertEqual("active", records[second_id]["status"])

    def test_disable_switch_forces_proposal_only(self) -> None:
        self.runtime.set_autonomous_learning(False)
        result = self.runtime.add_memory(
            lesson="Never use broad staging.",
            evidence=["sentinel-commit guidance"],
        )

        self.assertEqual("proposal", result["mode"])
        self.assertEqual([], self.runtime.list_memories())

    def test_three_successful_workflows_create_skill(self) -> None:
        for _ in range(3):
            self.runtime.record_workflow(
                name="Safe bugfix flow",
                steps=["Inspect", "Patch", "Run tests"],
                outcome="success",
            )

        skill = self.runtime.weave_skill("Safe bugfix flow")
        self.assertEqual("persisted", skill["mode"])
        skill_file = Path(skill["skill_file"])
        self.assertTrue(skill_file.exists())

    def test_fewer_than_three_examples_do_not_create_skill(self) -> None:
        self.runtime.record_workflow(
            name="Refactor flow",
            steps=["Inspect", "Refactor"],
            outcome="success",
        )
        result = self.runtime.weave_skill("Refactor flow")
        self.assertEqual("proposal", result["mode"])
        self.assertEqual("insufficient successful materially similar examples", result["reason"])

    def test_duplicate_and_versioned_skill_behavior(self) -> None:
        for _ in range(3):
            self.runtime.record_workflow(
                name="Tested workflow",
                steps=["Plan", "Implement", "Verify"],
                outcome="success",
            )

        first = self.runtime.weave_skill("Tested workflow")
        duplicate = self.runtime.weave_skill("Tested workflow")
        self.assertEqual("duplicate", duplicate["mode"])

        self.runtime.record_workflow(
            name="Tested workflow",
            steps=["Plan", "Implement", "Verify", "Document"],
            outcome="success",
        )
        second = self.runtime.weave_skill("Tested workflow")
        self.assertEqual("persisted", second["mode"])
        self.assertEqual("v2", second["skill"]["version"])

        skills = {item["skill_id"]: item for item in self.runtime.list_skills()}
        first_id = first["skill"]["skill_id"]
        self.assertEqual("superseded", skills[first_id]["status"])

    def test_audit_log_and_rollback_metadata(self) -> None:
        memory = self.runtime.add_memory(
            lesson="Keep rollback metadata for every persisted memory.",
            evidence=["memory schema"],
        )["memory"]

        for _ in range(3):
            self.runtime.record_workflow(
                name="Rollback workflow",
                steps=["Collect", "Generate", "Store"],
                outcome="success",
            )
        skill = self.runtime.weave_skill("Rollback workflow")["skill"]

        self.assertIn("rollback", memory)
        self.assertIn("rollback", skill)

        mem_rollback = self.runtime.rollback_memory(memory["memory_id"])
        skill_rollback = self.runtime.rollback_skill(skill["skill_id"])
        self.assertEqual("reverted", mem_rollback["status"])
        self.assertEqual("reverted", skill_rollback["status"])

        entries = self.runtime.audit_entries()
        actions = {entry["action"] for entry in entries}
        self.assertIn("memory_added", actions)
        self.assertIn("skill_woven", actions)
        self.assertIn("memory_rollback", actions)
        self.assertIn("skill_rollback", actions)


if __name__ == "__main__":
    unittest.main()
