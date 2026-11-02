# Task size, continuity and completion

## Choose the smallest adequate path

Use **light** for a clearly bounded reversible local edit or informational code inspection: inspect the affected context, make only authorized edits, and verify proportionately. Do not create a state file, PRD, ADR or new tests solely because a template exists.

Use **standard** for a feature, nontrivial fix, integration or multi-step investigation: identify behavior and acceptance checks, use a short dependency-aware plan, implement and verify one coherent slice.

Use **critical** when a wrong change can cross authorization/tenant boundaries, lose data, transfer money, break promised public/binary compatibility, worsen a live incident or affect physical safety. Increase boundary, rollback and verification attention; do not infer new user approvals when authorization already covers the action. Use the same path for review-only critical work, while preserving its read-only scope.

Select by consequence and uncertainty, not line count. A two-line authorization edit can be critical. A read-only codebase overview can be light while still requiring meaningful inspection. Stop at the requested deliverable; a review does not authorize fixing, and a plan does not authorize deployment.

## Route by requested outcome

Choose one primary specialist. Use discovery for unclear need/scope, architecture for design decisions, implementation for requested code changes, review for findings, testing for test design, debugging for an unexplained failing behavior, delivery for CI/migrations/releases, reliability for service health/incidents, security for an explicit security/privacy audit, AI systems for model/agent behavior, evidence for technical research and maintenance for understanding/refactoring/compatibility. A critical code review remains review, with security support when warranted. Use Sui itself to coordinate a resumed multi-stage task.

Leave unrelated email, artwork, documents/slides, objective exam quizzes, reminders and interview scorecards to their relevant skills. A software noun inside a reminder or email request does not make it an engineering task. Invoke bunsamosa for interview coaching and use the relevant application/authoring skills for other deliverables. Do not load every Sui skill just because the pack exists.

## Resume useful work, not stale claims

For long or interrupted work, prefer an existing project issue/spec/ADR/state convention. If none exists and continuity warrants it, use a small project-local `.sui/state.json` containing goal, requirements, decisions, tasks/dependencies, check IDs/evidence references, blockers and next action. This is task memory, not the user's private profile. Avoid credentials, personal data dumps and raw logs.

Start from `assets/work-state.example.json` and adapt its explicit input files. Run `python3 scripts/work_state.py INPUT.json` for dependency/traceability analysis. To create a checkpoint use `--root /project --write .sui/state.json --expected-sha256 new`. To update it, supply the exact current file SHA-256 instead of new; never bypass a mismatch. Writes are exclusive-lock, atomic and opt-in. A stale lock needs an ownership/process check, not automatic removal.

On resume run `python3 scripts/work_state.py /project/.sui/state.json --root /project --resume`, inspect current code and user changes, then choose the next ready task. Source drift invalidates the checkpoint's snapshot; reconcile affected work and rerun its checks before updating the snapshot. A task being labelled done is only a declaration. Independently verify linked evidence. Keep deferred work visible rather than treating it as completed.

## Completion evidence

Identify which observation supports each important claim. A successful linter does not establish a successful build; tests do not establish deployment; an agent's summary does not establish the resulting diff or requirements. Inspect the artifact, current inputs and relevant check output before asserting completion.

For consequential checks, use Sui Delivery's run_gate.py with explicit `inputs` covering changed code, relevant tests/contracts, manifests/lockfiles and configuration. The report includes plan digest, source fingerprints, project root and timestamps; verify it with verify_evidence.py against the same plan and current project. If inputs change during a check, the gate cannot pass. If they change afterwards, the verifier rejects it. Checks without an input scope remain explicitly unbound for compatibility; do not present those reports as proof of current-source verification.

This is bounded local consistency evidence. Omitted inputs, changed installed dependencies, external services and forged reports require separate judgment; these helpers do not provide signed build attestation. For trivial edits, a documented visual/manual inspection may be sufficient without a check runner. Do not repeat expensive checks solely because a new message began when the current evidence still applies and project instructions do not require a rerun.
