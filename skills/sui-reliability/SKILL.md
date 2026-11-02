---
name: sui-reliability
description: "Investigate or improve service reliability, performance, observability and incident response. Use for SLI/SLO design, latency tails, load/soak/chaos experiments, error budgets, capacity or postmortems; do not impose enterprise operations on a small local tool."
---

# Sui Reliability

Protect the user-visible outcome using useful measurements, bounded failure and recovery.

## Workflow

1. Identify critical journeys, dependencies and failure impact. Define a meaningful SLI, eligible events, good events, objective and window. Describe how missing telemetry and no traffic are handled.

2. Inspect traffic, errors, latency distribution, saturation and queue behavior using available logs/metrics/traces. Segment by affected version, tenant or region without exposing personal data. Distinguish observed facts from estimated capacity.

3. Choose fixes around failure mechanisms: deadlines, bounded retries/backoff, idempotency, queue limits, bulkheads or graceful degradation. Do not add every resilience pattern by default; check whether a fallback preserves correctness.

4. Validate using representative load, controlled fault injection or soak testing in an authorized environment. Define limits, abort criteria and recovery before experiments. Confirm instrumentation can actually detect the intended failure.

5. During incidents mitigate and communicate clearly; afterwards record timeline, contributing conditions, detection gaps and owned follow-ups. For normal improvements, report measured change, uncertainty and ongoing signal.

## Decision rules

Use percentiles and sample counts rather than an average alone. Compare equivalent workloads and warmup/cache states. Do not infer causation from an uncontrolled before/after graph.

Define SLO and SLA separately; avoid inventing an external promise from an internal target. Alert on actionable user impact with an owner and runbook. Consider burn-rate windows and false-positive cost instead of paging for every raw threshold.

Redundant copies of the same faulty logic can share a failure mode. Chaos is a controlled experiment with a hypothesis, blast radius and recovery plan; do not break production just because an example mentions Netflix.

## Resources and evidence

Use `scripts/slo_report.py events.json --target 0.999` for request-based budget arithmetic. Read its definition of good/eligible events; it cannot infer a business SLO or replace a monitoring backend.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

## Operational resources

[experiments](references/experiments.md): Use for representative load/stress/soak, time reliability, chaos, incident response and DevOps handoffs.

Use `scripts/load_probe.py --demo --execute` for the bounded loopback harness. Keep its client-side sample/saturation limitations explicit. Remote targets require their own authorized scope.
