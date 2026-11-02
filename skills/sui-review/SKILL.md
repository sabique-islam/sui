---
name: sui-review
description: "Review a proposed software change for consequential correctness, security, concurrency, compatibility, test and operability defects. Use for PRs, diffs or pre-merge review; report actionable evidence and distinguish confirmed findings from questions and style suggestions."
---

# Sui Review

Find defects worth fixing and explain a reachable failure with a precise code location.

## Workflow

1. Establish the comparison base, intended behavior and review scope. Read the entire relevant diff and surrounding callers, schema, configuration and tests. Treat unchanged context as part of the reasoning.

2. Trace inputs through state changes and outputs. Inspect authorization, tenant boundaries, failure paths, races, partial work, resource lifetimes, compatibility and migration behavior. Review added tests for meaningful assertions and production boundaries.

3. Try to falsify each suspected defect using code, a minimal reproduction or the relevant official contract. Rank by actual user impact and reachability; do not manufacture a severity number from speculation.

4. Report each finding with severity, file/line, concrete trigger, causal explanation, impact and a bounded fix direction. Mark an unresolved assumption as a question. Separate optional style observations from blocking defects.

5. State reviewed scope and checks run. If no substantiated issue remains, say so and identify meaningful untested risk. Do not create findings to fill a quota or silently modify code during a review-only request.

## Decision rules

Evaluate code health, not personal preference. Review public contract changes and persisted state before focusing on local formatting. Let linters own routine formatting when the project has them.

Inspect a failing test to decide whether it exposes a regression, incorrect expectation or environmental issue; do not lower the bar to get green. A covered line may have no useful assertion. Check whether test doubles encode an incorrect model of the provider.

Use one finding per independent root cause. Include a tiny example when it makes the defect unambiguous. Be constructive and precise; do not claim whole-system safety from a limited diff review.

## Resources and evidence

Use `assets/finding.md` for complex findings; omit fields that add no information.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

For security-sensitive, public-interface or stateful changes, read [boundary review](references/boundary-review.md). Record the affected callers/consumers and actively test a plausible refutation before promoting a suspected issue to a finding. A missing test is a validation gap, not evidence of a vulnerability. Verify resulting code and checks independently when reviewing delegated work; do not rely on a completion summary alone.

## Operational resources

[pr and inspections](references/pr-and-inspections.md): Use for reviewable PR descriptions, formal inspections and concrete entry/exit criteria.
