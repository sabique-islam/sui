# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html): A context-sensitive argument for discovering boundaries before distribution; not a universal ban on services.
- [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html): Verify method semantics, retry safety, status codes and validators against the protocol rather than framework folklore.
- [Timeouts, Retries, and Backoff with Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/): Use time budgets and bounded randomized retries; avoid magnifying overload or repeating unsafe side effects.
- [Semantic Versioning](https://semver.org/): Define the public compatibility contract before applying version increments; version numbers alone do not enforce compatibility.
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html): Check lock requirements and validation/rewrite behavior for the deployed database version and exact DDL. Current documentation is not necessarily the project version.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **Four maintainers and a small existing app:** Compare keeping the current deployable unit with extracting a boundary; avoid services with no isolation/ownership need.
- **A payment call times out:** Consider unknown completion, idempotency, reconciliation and user messaging; a blind retry can double the effect.
- **Several consumers share one API:** Map version coexistence, optional fields, old clients and contract tests before removing fields.
- **A dependency or framework sounds cleaner:** Require a concrete constraint it solves and an acceptable ownership/operational cost.
