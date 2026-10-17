# Trust, Safety, and Execution Policy

## 1) Durable actions that always require confirmation
The following actions always require explicit owner confirmation:
- commits, pushes, tags, releases, and branch mutations
- destructive file/database mutations and irreversible rewrites
- external side effects (deployments, network calls with side effects, credential changes)

These protections are never bypassed by autonomous workflows.

## 2) Autonomous learning exceptions (bounded)
Two bounded exceptions are allowed for evidence-backed autonomous learning writes:
- `synapse-memory`: safe memory persistence
- `skill-weaver`: safe skill creation/update

For these two workflows only, owner pre-approval is not required when safety checks pass.

## 3) Mandatory controls for autonomous writes
Autonomous writes must include all of the following:
- redaction/refusal of secrets, credentials, private keys, personal data, and confidential raw payloads
- owner-visible audit notification of what changed
- explicit versioning/lineage (`supersedes`, status transitions)
- rollback metadata and reversible history
- conflict handling without silent overwrite

## 4) Opt-out / disable switch
Autonomous learning must be user-configurable and disableable.
When disabled, `synapse-memory` and `skill-weaver` must produce proposal-only outputs and not persist files automatically.

## 5) Runtime limitation reminder
This repository is a Markdown protocol pack. It documents intended behavior but cannot itself guarantee runtime enforcement; actual behavior depends on host/tool capabilities.
