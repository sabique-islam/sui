# Peer patterns and scope of this comparison

Reviewed 2026-10-31 using first-party project instructions, documentation and selected scripts. This is a capability/implementation audit, not a head-to-head implementation benchmark. Sources on main are mutable snapshots; no upstream commit pin or full project audit is claimed. No upstream installer or code was executed. All new Sui runtime implementations are independently written; linked sources preserve attribution for the ideas studied.

## Compared patterns and resulting changes

### Superpowers

Source: [Superpowers](https://raw.githubusercontent.com/obra/superpowers/main/skills/verification-before-completion/SKILL.md).

Observed pattern: Explicit completion evidence and separating review responsibilities.

Sui action: Sui originally stated verification principles but had no persistent current-input binding. Added plan/source fingerprints and a reusable evidence verifier. Keep proportionate checks instead of rerunning every possible command for a trivial edit.

### GSD (historical template; current home moved)

Source: [GSD (historical template; current home moved)](https://github.com/gsd-build/get-shit-done/blob/main/get-shit-done/templates/state.md).

Observed pattern: A compact current-position and session-continuity artifact.

Sui action: Added opt-in durable state with source drift detection, guarded atomic writes and ready-task computation. The old repository README redirects to https://github.com/open-gsd/gsd-core; do not portray historical commands as current supported APIs.

### GitHub Spec Kit

Source: [GitHub Spec Kit](https://raw.githubusercontent.com/github/spec-kit/main/README.md).

Observed pattern: Connected specification, plans, tasks and verification with distinct entry points.

Sui action: Added requirement-to-task/check links and dependency consistency in resumable state. Retain direct bug-fix and small-change paths instead of requiring the full feature process for every task.

### BMAD Method

Source: [BMAD Method](https://raw.githubusercontent.com/bmad-code-org/BMAD-METHOD/main/README.md).

Observed pattern: Process sizing, explicit decisions and durable context.

Sui action: Added light/standard/critical paths and a clear next-ready task. The reviewed main README distinguishes stable and preview lines; no release-status prediction or upstream installer execution is inferred.

### Vercel Agent Skills

Source: [Vercel Agent Skills](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-best-practices/SKILL.md).

Observed pattern: Priority-organized stack-specific references.

Sui action: Added conditional stack adapters prioritizing important I/O, authorization, cache and bundle boundaries. Do not blindly rewrite unrelated stacks or redistribute the entire upstream rule set.

### Trail of Bits Skills

Source: [Trail of Bits Skills](https://raw.githubusercontent.com/trailofbits/skills/main/plugins/differential-review/skills/differential-review/SKILL.md).

Observed pattern: Risk-focused differential analysis and explicit affected-consumer scope.

Sui action: Added candidate/refutation records and caller/consumer analysis. Keep uncertainty separate from findings; do not automatically increase defect severity merely because a test is missing or require report files for every small review.

### Anthropic Skills / Skill Creator

Source: [Anthropic Skills / Skill Creator](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md).

Observed pattern: Behavioral evaluations, old-version baselines and trigger testing.

Sui action: Added a labelled routing set, a scorer for independently produced predictions and baseline/candidate runs. Keep helper unit tests distinct from measured agent behavior and do not infer global effectiveness from a small routing sample.

## What to verify next

Run helper regressions, explicit stale-evidence/drift cases and the same blinded routing cases against old and new instructions. Verify actual task outputs in fresh threads for representative changes. Treat each result as limited evidence, preserve negative cases and report ties or regressions. Avoid claiming that additional files or a larger test count make Sui universally better than the compared systems.
