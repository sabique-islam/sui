---
name: sui-testing
description: "Design and implement risk-based software tests that detect meaningful faults. Use for test strategy, regression tests, boundary/partition/pairwise cases, integration/contracts, fuzzing, mutation, coverage gaps or flaky tests; do not write low-value tests merely to raise counts or coverage."
---

# Sui Testing

Create trustworthy evidence about behavior and expose important failure modes with the smallest useful suite.

## Workflow

1. Define the behavior contract, relevant risks and oracle. Separate unit, component, integration, end-to-end and acceptance evidence. Choose the level that can expose the actual failure rather than mocking it away.

2. Partition inputs by behavior and include meaningful boundaries, malformed inputs, missing values, state transitions, authorization failures and concurrency when relevant. Use pairwise combinations only when interaction assumptions justify them.

3. Choose deterministic fixtures and controlled clocks/randomness. Replace difficult dependencies with narrow doubles while preserving contract tests against real boundaries. Keep test data independent and clean up state.

4. Implement assertions about observable outcomes and invariants, including absence of unwanted side effects. For a regression, show the failing behavior before the fix when feasible. For parsers or rich input spaces, add property-based/fuzz tests with reproducible seeds and minimized counterexamples.

5. Run the relevant suite and diagnose flakes. Inspect uncovered risky behavior and consider mutation tests for weak assertions. Record omissions and environment limits. Stop adding tests once additional work lacks a meaningful risk or acceptance purpose.

## Decision rules

Testing reveals failures, not proof of their absence. Exhaustive testing is rarely possible; combine techniques and vary cases as the suite matures. Inspection and static analysis complement execution, and verification/validation are questions about intent, not synonyms for static/dynamic techniques.

Statement coverage observes executed statements; decision/branch coverage exercises decision outcomes; condition coverage exercises atomic conditions. Short-circuit behavior matters. High condition coverage does not universally imply full decision coverage or vice versa. Cyclomatic complexity counts independent paths in a CFG under stated assumptions; it is not a guaranteed minimum branch-test count or a measure of data complexity.

Coverage is diagnostic, not a universal 80% or 100% quota. Mutation survivors require investigation, including equivalent mutants. Property testing and fuzzing overlap in exploration but are not interchangeable labels for every library. Keep unauthorized production load or chaos out of ordinary test execution.

## Resources and evidence

Use `scripts/validate_test_matrix.py matrix.json` to check case IDs, risk/requirement links, oracles, commands and status consistency. It cannot establish test quality or actual execution.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

## Validate the claim, not only process exit

Check that the intended tests were collected and useful assertions actually ran. Keep original-symptom evidence distinct from a green unrelated suite. Reproduce a regression's unfixed failure in an isolated baseline when practical; preserve dirty user changes rather than using destructive resets. For consequential handoffs, declare code/test/config inputs in Sui Delivery's gate and verify the resulting report against current inputs. Do not add ceremonial tests for a reversible display-only edit.

## Operational resources

[test planning](references/test-planning.md): Use for test/SQA planning, integration/lifecycle/install strategies and acceptance.

[test design](references/test-design.md): Use for black-box/structural/data-flow methods, exploration, mutation, frameworks and coverage.

Use `scripts/test_design.py pairwise INPUT.json` or `avg-abs INPUT.json` for the bounded worked methods. Use `scripts/fuzz_lab.py --iterations 1000` for the local seed/replay lab and [Python property tests](assets/python-lab/test_framed.py) with installed pytest/Hypothesis. Use `assets/test-plan.md` only when the coordinated plan needs it. Inspect real collection/report output through Sui Implementation, not just matrix metadata.

[GoogleTest frame cases](assets/cpp-lab/frame_test.cpp) and [JUnit frame cases](assets/java-lab/FrameTest.java) provide real assertions for the same format. Use the project's supported GoogleTest/CMake or JUnit Jupiter environment; these sources alone are not compiled/native-run evidence.
