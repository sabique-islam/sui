# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [DORA Continuous Delivery](https://dora.dev/capabilities/continuous-delivery/): Maintain the ability to release safely on demand. Continuous delivery and automatic production deployment are distinct.
- [DORA Software Delivery Performance Metrics](https://dora.dev/guides/dora-metrics/): The current retrieved guide has five metrics. Measure at service level and avoid individual quotas or cross-context league tables. Recheck definitions before use.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/): Use a limited representative population, comparable control, release-specific observations and an actual rollback path.
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html): Check lock requirements and validation/rewrite behavior for the deployed database version and exact DDL. Current documentation is not necessarily the project version.
- [GitHub Actions Secure Use](https://docs.github.com/en/actions/reference/security/secure-use): Limit permissions, protect secrets and treat untrusted workflow input/code carefully. Verify action and runner versions.
- [SLSA Specification](https://slsa.dev/spec/): Use provenance and build integrity appropriate to the release. Verify specification version and never infer provenance from a passing scan.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **A schema change removes a column used by an older running version:** Plan version coexistence and staged expansion/contraction; app rollback alone cannot restore deleted data.
- **A configuration-only update changes a parser:** Test and stage it as a release; “not code” does not mean it cannot fail.
- **A check command starts a background server and exits:** Do not report completion from the launcher alone. Use a managed lifecycle with readiness, smoke checks and teardown.
- **The user requested a draft release plan:** Prepare concrete artifacts and verification; do not publish or deploy merely because a plan exists.
