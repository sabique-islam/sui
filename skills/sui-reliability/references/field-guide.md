# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [Implementing SLOs](https://sre.google/workbook/implementing-slos/): Define useful service indicators, objectives and agreed error-budget responses around user experience.
- [Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/): Connect actionable alerts to user-visible reliability and budget consumption rather than arbitrary single thresholds.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/): Use a limited representative population, comparable control, release-specific observations and an actual rollback path.
- [OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/): Connect signals to system questions; correlate logs, metrics and traces and limit sensitive/high-cardinality data.
- [Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): Use time budgets and bounded randomized retries; avoid magnifying overload or repeating unsafe side effects.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **No eligible requests occurred:** Return no-data rather than 100% success; investigate telemetry separately from service availability.
- **Mean latency is low while p99 times out:** Inspect the slow request population and sample counts before declaring the service healthy.
- **A resilience experiment shares a backend with production:** Account for shared blast radius and task authorization; isolate before injection.
- **The service exhausted its error budget:** Apply the agreed service policy and user priorities; do not invent an organizational freeze rule.
