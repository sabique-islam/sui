# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [OpenTelemetry Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/): Connect signals to system questions; correlate logs, metrics and traces and limit sensitive/high-cardinality data.
- [Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): Use time budgets and bounded randomized retries; avoid magnifying overload or repeating unsafe side effects.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/): Use a limited representative population, comparable control, release-specific observations and an actual rollback path.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **A restart temporarily fixes a leak:** Treat restart as mitigation, then profile retained resources under a representative repeated workload.
- **A regression only happens after a long run:** Consider leaks, stale connections, accumulated state or queue growth; use bounded soak evidence.
- **Logs blame an unavailable dependency:** Check deadlines, retry multiplication, circuit behavior and original request impact before increasing retries.
- **Three patches fail to change the symptom:** Revisit the hypothesis and collect a discriminating trace rather than adding another speculative guard.
