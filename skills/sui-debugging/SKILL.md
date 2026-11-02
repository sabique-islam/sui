---
name: sui-debugging
description: "Investigate a reproducible defect, crash, flaky test or performance regression through evidence, hypotheses and causal experiments. Use when behavior is failing or unexplained; mitigate user impact before deep analysis during an incident and avoid repeated speculative patches."
---

# Sui Debugging

Identify the causal failure and prove that the fix addresses it without broadening the problem.

## Workflow

1. Capture expected versus actual behavior, exact error, environment, relevant versions and minimal trigger. Check recent changes and preserve logs safely. During an incident, assess impact and use authorized reversible mitigation first.

2. Reproduce in an isolated local or test environment. Reduce inputs and dependencies until the failure is explainable. Establish whether the problem is code, data, configuration, dependency, infrastructure or the test oracle.

3. Write a short ranked hypothesis list with a discriminating experiment for each. Inspect static control/data flow and dynamic traces, breakpoints, profiles or counters. Change one relevant variable at a time; do not use an unrelated refactor as diagnosis.

4. Fix the root cause at the correct boundary. Add regression evidence proportional to impact, test adjacent cases and verify the actual original symptom. For performance, compare representative workloads under controlled conditions.

5. Report cause, trigger, fix and evidence. After three failed attempts at the same theory, revisit its central assumption and obtain the missing diagnostic instead of trying a fourth cosmetic variation.

## Decision rules

Distinguish correlation from causation and mitigation from repair. A restart hiding the symptom may not establish the cause. Avoid collecting whole databases or secrets when a minimal redacted sample suffices.

For races, identify ordering and state ownership; add a controlled interleaving where possible. For memory/lifetime bugs, use supported sanitizers and minimized inputs. For slow paths, profile before optimizing and separate CPU, I/O, lock waits and queueing. Averages alone can hide tail failure.

Keep a bounded evidence log for difficult investigations: observation, hypothesis, experiment, result and next decision. Do not burden a simple typo fix with an incident report.

## Resources and evidence

Use `assets/investigation.md` for a multi-step investigation; use a direct reproduction for a small defect.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

## Operational resources

[environment probes](references/environment-probes.md): Use to select source/binary/remote/browser probes and supported memory/performance/race evidence.
