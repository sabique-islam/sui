---
name: sui-delivery
description: "Design or repair build, CI/CD, configuration, dependency, migration and release workflows. Use for reproducible builds, quality gates, deployment plans, feature flags, canaries or rollback; execute external deployment only within the user's authorized scope."
---

# Sui Delivery

Make the requested change deployable with clear evidence and a recovery path.

## Workflow

1. Inspect the actual build/test commands, lockfiles, runtime versions, CI permissions, deployment target and configuration. Distinguish source, build artifact and running version. Preserve pre-existing failures as baseline evidence.

2. Order fast deterministic checks before expensive suites. Pin appropriate dependencies/actions, keep untrusted inputs out of shell interpolation, scope credentials and cache safely. Keep builds reproducible and publish artifacts from a known revision.

3. Plan data/config/schema changes alongside code. Check database-specific locking, timeouts, mixed-version compatibility and retry semantics. Prefer additive transitions and bounded backfills where needed; test restoration or roll-forward when rollback cannot safely restore data.

4. Define rollout population, duration, comparison signal, smoke check, owner and abort conditions. For risky changes use limited exposure and feature flags where useful. Apply the same discipline to configuration as code.

5. Run authorized checks and prepare a concrete release result. Perform authorized deployment only when prerequisites and scope are clear. Verify the running version and user-visible behavior; report failed, skipped and blocked checks truthfully.

## Decision rules

Continuous delivery means ready to release on demand; continuous deployment automatically releases qualifying changes. Do not confuse the two. A merge is not evidence that production works.

Measure team/service outcomes with current DORA definitions, not per-developer targets. Recheck the current five-metric model when using it. An error budget is a joint policy, not an arbitrary number that blocks all work.

Do not run a migration merely to see whether it is destructive. Check backups, locks, ordering and restore assumptions before a production mutation. Keep secrets out of plans and check output; redaction is best effort and never permission to print credentials.

## Resources and evidence

Use `scripts/run_gate.py plan.json --root /project` to validate and preview a plan. Add `--execute` only for reviewed commands within task authorization. It runs argv without a shell, applies timeouts and records evidence; it does not authorize deployment.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

The gate runner executes only on POSIX systems so process-group cleanup is available; preview works elsewhere. Its working-directory check is not a filesystem sandbox. Commands still inherit the environment and can have side effects. It terminates ordinary same-group descendants, but cannot contain a process that deliberately escapes its process group. Use trusted project checks; never place credentials in command arguments. The runner suppresses stdout/stderr rather than pretending redaction can reliably remove secrets.

## Bind completion claims to the files checked

Read [completion evidence](references/completion-evidence.md) before using reports as durable verification. Declare relevant `inputs` in the gate plan; inspect real suite/build output for meaningful execution. Run `python3 scripts/verify_evidence.py REPORT.json --plan PLAN.json --root /project` before reusing the report after a pause or handoff. Reject source drift, plan mismatch and unbound evidence. Distinguish process success, requirement acceptance and deployed behavior.

## Operational resources

[build release](references/build-release.md): Use for native build graphs, CI/platform recipes, container/SBOM scope and release/install recovery.

[Platform adapters](references/platform-adapters.md): use for target-specific GitHub/Jira, infrastructure, configuration, CI, monitoring, version-control, VM and installer workflows.

[Python CI recipe](assets/python-ci.yml): adapt the actual project paths/configuration and produce its hash-locked `requirements-checks.lock` before use. Action revisions were checked against official v6 references. This is a prepared workflow template; no hosted run is claimed. Add project-native report retention/artifact verification when a target is supplied.
