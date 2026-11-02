# Evidence-driven boundary review

Start with intended behavior, comparison base and the changed trust/state boundary. Classify by consequence rather than changed-line count. Inspect direct callers, callees, persisted state and relevant tests; trace transitive consumers when a public or security boundary changes. Record which paths were actually examined instead of claiming a whole-system audit.

For every candidate finding record: attacker/caller capability; entry and reachability; exact precondition; violated invariant; affected data/side effect; applicable guard or transaction; minimal observation/reproduction; plausible refutation; verdict and remaining assumption. Inspect historical fixes when removed validation or changed invariants suggest a regression.

Try to disprove the candidate. A locally missing owner check may be enforced at a trusted caller; inspect that contract before reporting. Conversely a caller guard may be bypassed through another entry point. A mock passing a test does not prove the real authorization/transaction boundary. Missing tests justify a validation gap, not an invented exploitable vulnerability or an automatically higher severity.

Keep confirmed defects, unresolved questions and suggestions distinct. For example, an update API accepting another user's object ID is actionable only if the signed-in caller can reach it without another trusted ownership check; show an unauthorized state change or a reachable causal path. Cite the guard if it refutes the concern. Do not output a finding quota, silently change code or create a report file unless that artifact helps the authorized task.
