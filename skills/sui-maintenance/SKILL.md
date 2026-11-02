---
name: sui-maintenance
description: "Understand and evolve an unfamiliar codebase while preserving behavior, compatibility and ownership. Use for refactoring, technical-debt work, dependency upgrades, code archaeology, API changes, deprecation or handover; distinguish exploration from an authorized rewrite."
---

# Sui Maintenance

Make the next valuable change safer by building a tested model of the affected code and its consumers.

## Workflow

1. Build/run using documented project instructions and inspect the entry point, request path, state ownership and dependencies. Form a bounded working model; do not attempt to understand every file before changing one behavior.

2. Use symbol search, types, tests, logs, debugger probes and profiles to test that model. Follow a representative operation end to end. Record evidence of actual behavior and gaps instead of inventing architecture from directory names.

3. Identify change pressure and debt with a concrete consequence: defects, slow delivery, insecure dependencies, operational toil or cognitive load. Compare targeted repair, containment and replacement; do not equate old or unfashionable code with debt.

4. Establish characterization or contract tests where behavior must remain stable. Refactor in small steps, separate behavior changes and preserve APIs/ABIs/data format as promised. For upgrades inspect release notes, transitive changes, migration steps and rollback limitations.

5. Run affected tests and inspect callers/consumers, update only useful docs and remove obsolete paths deliberately. Record ownership, debt payoff evidence and a deprecation/revisit trigger if ongoing work remains.

## Decision rules

Prefer observed change frequency and failure cost over arbitrary complexity cutoffs. High internal quality is an investment when it supports future changes; speculative abstractions can create their own debt.

Use strangler or anticorruption boundaries when a migration needs coexistence. Maintain compatibility through staged consumers and producers, not a version-number bump alone. Account for internal forks and upstream synchronization.

Use source control for history and restoration; inspect local changes first. Never discard user work, rewrite shared history or remove a feature solely because a static tool calls it unused. Validate reachability and ownership before deletion.

## Resources and evidence

Use `assets/change-plan.md` when a refactor or compatibility migration spans multiple boundaries.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

## Operational resources

[configuration and changes](references/configuration-and-changes.md): Use for SCM baselines, branching, defect/change state transitions and legacy tool procedures.

[ownership and contributions](references/ownership-and-contributions.md): Use for contributor intake, governance, dependency sustainability and handover.
