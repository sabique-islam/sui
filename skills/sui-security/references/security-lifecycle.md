# Security across delivery

Use actual assets and consequences; do not require an enterprise program for a local display fix.

## Risk to requirement

Map asset, actor, entry point, trust boundary and realistic abuse event. Record likelihood/consequence with supporting evidence, affected objective, treatment, owner, indicator and residual risk; avoid precision from invented numeric scores. Turn priority risks into specific measurable achievable relevant time-bound security objectives, then stable requirement IDs and controls/tests.

Example risk: a user guesses another draft's ID and reads it. Objective: every read/write/export checks owner at the service boundary for the next release, with denied cross-owner cases and a code review of all entry points. Requirement SEC1 links the asset/threat, owner, authorization contract, enforcement code, negative test and release evidence. “Use encryption” alone does not address that authorization risk.

## Phase outputs and training

At requirements identify assets, privacy expectations, abuse cases and security objectives; at design record data flows/trust boundaries, mitigations and interface/lifetime contracts; at implementation apply approved toolchain and secure coding controls; at verification execute denied/malformed/fuzz/static checks with ownership and scope; at release review residual risk and servicing readiness; after release monitor, triage and remediate incidents and dependency issues.

Assign a responsible security reviewer where consequence warrants it. Provide baseline training on untrusted inputs, auth versus authorization, secrets/logging, dependency updates and privacy; add specialist practice for maintainers of authentication, cryptography, native parsers or incident handling. Assess with a realistic task or boundary test, track the gap/owner and refresh when responsibilities/tooling change. Attendance at training is not evidence a control works.

Maintain a project-specific approved toolchain record with compiler/linker/runtime versions, relevant warnings/sanitizers, dependency/source provenance and exception owner. Maintain prohibited/risky API patterns by language and safe alternative, such as shell interpolation of untrusted input or an unbounded native memory operation. Enforce through the repository's supported linter/compiler/scanner and review justified exceptions with expiry. A universal ban list copied across languages is not useful enforcement.

## Security validation and final review

For each consequential objective/requirement record component, threat, method (review/static/dynamic/fuzz/pentest/manual), owner, SDLC timing, test environment/tool version, oracle and observed evidence. Review false positives, uncovered paths, suppressions and deferred bugs against a defined release bug bar. Include dependency/inherited components and configuration as well as source code. Link this plan to the SRS/RTM and ordinary test plan rather than creating contradictory parallel status.

Before release inspect the threat model, requirement coverage, tool outputs, unresolved findings, exception owners, recovery plan and incident contacts. Decide who can stop/roll back or issue an emergency fix; define service hours/escalation appropriate to impact, including round-the-clock coverage where the actual service requires it. Identify responsibilities for third-party or inherited code and how advisories reach owners. Verify contact and recovery paths in a bounded exercise; a final-security-review checkbox alone is not readiness.

## Network and replay boundaries

Separate eavesdropping/confidentiality from tampering/integrity, identity/authentication from permission/authorization, and message freshness from successful encryption. Define which channel/endpoint authenticates whom, how trust anchors/keys are managed and how anti-replay state or idempotency works. Test a duplicated valid request and a tampered/expired request against the actual enforcing component. IP/email/DNS spoofing and person-in-middle examples motivate realistic boundaries; verify deployed protocol/library settings from official current documentation rather than reproducing an outdated cipher or protocol version.
