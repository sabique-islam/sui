# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [What to Look for in Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): Review design, correctness, concurrency, tests and understandability in context. Use evidence for findings rather than style opinions.
- [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html): Combine fast focused tests with boundary and contract checks; use expensive end-to-end tests for important journeys.
- [GitHub Actions Secure Use](https://docs.github.com/en/actions/reference/security/secure-use): Limit permissions, protect secrets and treat untrusted workflow input/code carefully. Verify action and runner versions.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **A fetched owner_id is never compared with the signed-in identity:** Demonstrate the cross-owner operation and report the reachable authorization defect with a precise location.
- **A helper has high complexity but no demonstrated defect:** Explain maintainability concerns as optional unless the actual behavior or required quality is violated.
- **A test mocks the database transaction being changed:** Check whether the oracle can detect the real consistency problem; identify missing boundary evidence.
- **A possible null value is excluded by a validated caller contract:** Do not report a speculative crash; show the contract evidence or state the unresolved assumption.
