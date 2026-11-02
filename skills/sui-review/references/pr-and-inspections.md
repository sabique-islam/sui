# Pull requests and inspections

Use the repository's template and scale detail to the change.

## Prepare a reviewable PR

Title the concrete behavior change. Describe the trigger and observed before/after behavior, why the boundary changed, relevant requirement/issue/ADR links, compatibility/migration effect and validation actually observed. Include before/after screenshots only when UI behavior benefits from them; redact personal data. List meaningful blocked checks with the cause rather than a generic all-tests-pass claim. Rewrite the description around the final diff after scope changes.

Example: “Reject stale draft saves” describes two tabs saving the same revision; previously the later request overwrote newer content, now the service returns a conflict and preserves the current revision. State the transaction/version check and two-tab regression result. Avoid narrating abandoned patches unless they explain a consequential tradeoff. Confirm the diff is focused and the author can explain affected callers.

## Choose the review practice

Use incremental peer review for ordinary changes, a holistic design review when responsibilities/contracts change, pairing for immediate shared reasoning, and a formal inspection for a consequential artifact with several perspectives. In an inspection identify author, moderator, reader/presenter and recorder/reviewers; share the artifact and entry criteria, inspect independently, log defects with evidence, run a focused meeting, assign rework and verify resolution. Keep defect detection separate from evaluating the author.

Entry criteria may include a stable artifact, clear requirements and completed relevant checks; exit criteria are dispositioned findings, verified important fixes and documented residual risk. Do not turn every typo into a formal meeting. Use Sui Review's refutation method: test a plausible reason the suspected failure is unreachable before reporting it as confirmed. Keep correctness/security/concurrency/operability findings distinct from optional style advice.
