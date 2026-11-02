# Test planning, SQA and acceptance

Preserve project-native test conventions and scale the artifact to consequence.

## Scope and test case contract

For a coordinated test plan record version/requirements, objectives, in/out scope, product risks, levels/techniques, environment/data, tools, roles/capacity, milestones/dependencies, deliverables, entry/exit, suspension/resumption and defect triage. Tie quality goals to observable thresholds and denominators. Identify tool/testbed/model availability risks with fallback, trigger and owner. Include setup, data preparation, test authoring, execution, investigation, retest and cleanup estimates; dependency readiness alone is not a calendar.

Specify each material case with ID/module, requirement/risk, priority, tester/owner, preconditions, environment/version, input data, actions/steps, expected oracle, actual result/status and evidence. Keep expected and observed outcomes separate. For a manual recovery test, steps must establish saved state, interrupt at a defined point, restart, then compare acknowledged content and durable revision. A prose claim “recovery tested” is insufficient. Use the lighter JSON matrix when that captures enough detail.

Choose automation by failure risk, repetition, target compatibility, reporting/diagnostics, cross-platform needs, team skills, maintenance/support cost and test-data availability. Keep an accountable owner for brittle fixtures and tool upgrades. Automate stable observable behavior; do not automate a changing UI solely to inflate case count. Distinguish planned/created/executed tests, pass/fail/blocked/skipped, defect severity/age and requirement risk coverage. Preserve the reason for missing evidence.

## SQA, mindsets and TDD

SQA concerns the process and evidence as well as the product: define applicable standards, reviews, audits, responsibilities, deviation reporting, corrective actions and follow-up. Inspect whether promised checks happened and whether their evidence was useful. A cost-of-quality analysis separates prevention (training/design), appraisal (review/testing), internal failure (pre-release rework) and external failure (incidents/support/customer harm); compare the same scope/window rather than assuming all testing is waste.

Use demonstration testing to verify intended examples, prevention to challenge requirements/design early, destruction to find counterexamples and evaluation to assess readiness under a stated risk. These are complementary perspectives, not mandatory separate suites. Ask what optimistic assumption each current test shares with the implementation.

For TDD pick one new observable behavior, write the smallest meaningful failing test, run it and confirm the failure is due to missing behavior, implement the minimum coherent change, rerun to green, then refactor with tests green. Repeat in small increments. A test that fails only because of a misspelled import does not establish the intended red phase. Regression-first repair overlaps this loop but does not cover all new-feature TDD.

## Integration and system strategy

Big-bang integration joins many parts at once and makes fault localization difficult. Incremental integration validates a small boundary at a time. Top-down begins at orchestration and uses lower-level stubs; bottom-up begins at low-level components and uses drivers; sandwich combines both toward an explicit seam. Stubs return controlled outcomes; drivers exercise a lower component. Preserve provider-realistic errors, timing and contracts so doubles do not encode an imaginary system.

Example sandwich: test DraftAPI with an in-memory DraftStore stub while independently testing real SQL DraftStore with a driver; then replace the stub at the API/store seam and run atomicity/conflict/restart cases against the actual database. Record transaction, auth, network and persistence assumptions that only the real boundary test can establish. Do not treat one integration strategy as universally finding the most bugs.

For system tests deploy the actual supported configuration in an isolated target, seed deterministic noncustomer data, record revision/config/dependency identity, exercise representative journeys and faults, collect redacted outcomes, then clean up with an owned bounded teardown. Distinguish functional, boundary, load/stress, security, recovery, usability, installation and platform/localization requirements. A test environment mismatch is a finding about confidence, not an excuse to claim the target passed.

## Lifecycle and installation tests

Test readiness/startup, normal operation, graceful shutdown, interruption/restart, stale lock policy and persisted invariants. Make service/process teardown run on failure and enforce a deadline. Verify readiness from behavior rather than a fixed sleep. For installation cover clean install, supported upgrade, configuration/data preservation, permission failure, interrupted install/rollback, repair and removal with an explicit retained/deleted-data policy. Removal tests belong in disposable environments, not the user's real profile.

Test relevant OS/runtime/device combinations selected by supported users and risk; report untested combinations. For cloud deployments include routing/auth/config/data-region boundaries that differ from local runs. For locale tests check timezone boundaries, date/number formatting, encodings, text expansion and relevant cultural assumptions. A compliance category must reference a verified applicable control/version and tested behavior, not a blanket certification.

## Release and user acceptance

Release testing asks whether the integrated version meets external requirements and readiness; defect testing seeks failures in its implementation. Obtain a useful independent perspective for consequential releases rather than having only the author repeat the same assumptions. Map release/system scenarios to business oracles, performance/dependability constraints, known defects and recovery evidence.

An acceptance plan identifies customer/decision owner, target environment, qualification criteria, installation checks, realistic data/tasks, performance bounds where relevant, exit/rollback conditions and evidence location. Alpha is controlled internal user evaluation; beta involves external representative users with consent/support/feedback and limited exposure; customer acceptance is an explicit agreed outcome, not the mere existence of a beta label. Agile participation still needs relevant users rather than convenient insiders. Record what was accepted and by whom; deployment and acceptance are distinct events.
