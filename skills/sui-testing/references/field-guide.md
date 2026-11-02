# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html): Combine fast focused tests with boundary and contract checks; use expensive end-to-end tests for important journeys.
- [DORA Test Automation](https://dora.dev/capabilities/test-automation/): Build fast trustworthy feedback and shared ownership of tests; reducing slow feedback matters more than counting tests.
- [OWASP ASVS](https://asvs.owasp.org/): Select versioned security requirements proportional to application risk; the retrieved site offers ASVS 5.0.0. Recheck exact control IDs.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **An inclusive age range has min/max bounds:** Choose representatives below/at/inside/at/above the bounds; state integer versus continuous input assumptions.
- **A third-party service is unavailable locally:** Use a narrow stub for local deterministic behavior and preserve a separate provider contract check when feasible.
- **Coverage rises without better assertions:** Inspect whether wrong outputs or missing effects fail the suite; consider mutation or explicit invariant checks.
- **A flaky test depends on wall-clock time:** Control the clock or establish deterministic ordering; do not merely retry until green.
