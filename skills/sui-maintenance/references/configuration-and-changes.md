# Configuration, branches, defects and change control

Use repository-native records; a task-state JSON file is not an SCM database.

## Configuration baseline

Identify controlled items: source, requirements/design, tests, build scripts, dependency/tool versions, configuration, schemas/migrations, docs and release artifacts. Record identity/revision, owner, dependency/release relation and status. Baseline a reviewed compatible set; configuration control assesses a proposed change, status accounting records decisions/versions and audits compare what was intended, built and delivered. Keep the plan proportionate to risk and team, including control authority and how emergency changes are reconciled.

For a change request record requester/ID, problem, baseline, alternatives, benefit/cost, urgency, users, compatibility/security/data/test impact, decision owner/authority, accepted/rejected/deferred state, implementation/release target and closure evidence. Reassess dependent artifacts and communicate the changed baseline. A change-control board is an option for coordination, not a required meeting for a solo fix. Link the requirement RTM, code/PR, checks and release so a decision can be traced both directions.

## Branch and merge practice

Inspect dirty/untracked work and current branch before any branch/history operation. Choose trunk-based development for frequent small integrated changes with short-lived branches and useful flags; use a release/maintenance branch when supported versions genuinely diverge. A GitFlow-style develop/feature/release/hotfix structure can help scheduled parallel releases but adds merge/backport cost; do not prescribe it universally.

Keep branch purpose, base, owner, lifetime, target and supported version explicit. Before merging inspect the relevant diff and caller contracts, preserve local changes, run targeted tests and resolve conflicts by understanding both behaviors. Do not overwrite a conflict marker mechanically. For hotfixes identify the affected release, fix/test the smallest boundary, release through the ordinary bounded safety path and reconcile forward/backports. Tag the actual built revision/artifact and verify customer/module-specific lines do not quietly drift. Use a new safe working area when needed rather than destructive resets or force pushes.

## Defect lifecycle

Record discovery/trigger, expected/actual behavior, environment/version, reproduction, impact/severity, owner and safe evidence. Triage validity/duplicate/scope; analyze/assign; fix; independently retest the original symptom and relevant adjacent paths; then close or reopen. Deferred/rejected/duplicate decisions need rationale and linkage; “fixed in source” is not automatically “released to users.” Link verified fixes to the containing release and communicate only within the user's authorization.

Example state path: reported→validated→assigned→fixed→verified→closed, with duplicate/rejected/deferred branches and reopened→assigned when the original trigger still fails. Preserve the old report/evidence rather than rewriting history to erase the failed fix. Use actual tracker transitions/fields from the target connector; do not assume Jira, Bugzilla, FogBugz, Trac/Edgewall or Backlog share a schema.

## Legacy tool inventory

RCS, CVS, ClearCase, GitHub, Perforce and AccuRev are historical source and configuration tools; Make, CruiseControl, FinalBuilder and Maven are build examples. Inspect the project's actual tool/version, baseline/export/merge/build logs and ownership before applying current documentation. Do not silently normalize a historical spelling or category into a different product. Prefer the existing supported workflow, and evaluate migration only with compatible-history/build/release evidence. Source code administration, build, installation and defect tracking are distinct capabilities even when one platform spans several.
