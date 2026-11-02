# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [What to Look for in Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): Review design, correctness, concurrency, tests and understandability in context. Use evidence for findings rather than style opinions.
- [RFC 9110 HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html): Verify method semantics, retry safety, status codes and validators against the protocol rather than framework folklore.
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/): Use relevant accessibility success criteria with manual keyboard/focus and assistive-technology checks. Automated scans alone do not establish conformance.
- [NIST Secure Software Development Framework](https://csrc.nist.gov/projects/ssdf): Integrate secure development through the lifecycle. Distinguish published final documents and drafts before claiming requirements.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **A one-line display typo:** Inspect the changed view and obvious surrounding states; skip ceremonial requirements documents and mirrored unit tests.
- **A registration endpoint changes capacity accounting:** Identify atomicity and concurrency behavior, validate the boundary and add meaningful regression coverage.
- **New generated code uses an unfamiliar package API:** Check the installed version and official contract before wiring it into the product.
- **The working tree already contains edits:** Identify overlap, preserve user changes and isolate the authorized correction.
