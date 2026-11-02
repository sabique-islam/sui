# Ownership, dependencies and contribution intake

Adapt to the actual project's governance.

Inspect maintainer/decision rights, CONTRIBUTING, code of conduct, style/checks, tests/docs requirements, security-reporting route and CLA/DCO terms before contributing. Prepare one focused change, reproduce the issue, run relevant checks, update affected docs and keep feedback tied to observable behavior. Do not assume every project requires identical legal terms or that a PR can merge without the project's owner decision.

For a dependency record internal owner, current version/pins/lockfile/provenance, maintainer activity and release/security support, concentration/bus-factor risk, customization/fork divergence, replacement difficulty and recovery plan. Stars/downloads alone do not establish sustainability. Fund/support upstream when appropriate, and avoid creating an unmaintained private fork for a fix that can be shared under the actual license and authorization.

Worked scenario: a one-maintainer parser used by your import path becomes archived. Inventory exposed formats/callers and versioned data contracts; add real malformed-input regression fixtures; evaluate a compatible maintained replacement and a minimal temporary maintained fork; assign upgrade/security ownership; migrate in a bounded slice with rollback and test old stored data. Treat source visibility, copyright permission and assurance as separate questions. Record the residual support risk and revisit date rather than automatically replacing every small dependency.

For handover preserve a request-path map, invariants, build/run/check commands, failure/recovery paths, owners and unresolved decisions. Keep architecture/design/test/requirement links current when refactoring. Shared ownership means other maintainers can reason about and safely change a boundary, not that nobody is accountable for it.
