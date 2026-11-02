# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [Monolith First](https://martinfowler.com/bliki/MonolithFirst.html): A context-sensitive argument for discovering boundaries before distribution; not a universal ban on services.
- [What to Look for in Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): Review design, correctness, concurrency, tests and understandability in context. Use evidence for findings rather than style opinions.
- [Semantic Versioning](https://semver.org/): Define the public compatibility contract before applying version increments; version numbers alone do not enforce compatibility.
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html): Check lock requirements and validation/rewrite behavior for the deployed database version and exact DDL. Current documentation is not necessarily the project version.
- [SPDX Overview](https://spdx.dev/learn/overview/): Describe components and licensing with a recognized interchange model; an SBOM is inventory, not a security or legal guarantee.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **An unfamiliar repository has thousands of files:** Trace the affected operation, entry point and state; build a bounded model before editing.
- **A large refactor also changes behavior:** Separate the transformations or supply independent characterization/acceptance evidence for both.
- **An internal fork is far behind upstream:** Inspect customizations and compatibility; compare upstreaming, rebasing or containing the fork with a migration plan.
- **Static analysis calls a public export unused:** Inspect external consumers and reflection/registration paths before removing it.
