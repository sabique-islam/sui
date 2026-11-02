---
name: sui-architecture
description: "Make software architecture decisions from quality constraints, ownership and failure modes. Use for service boundaries, data ownership, APIs/ABIs, event-driven systems, concurrency, migrations, architecture reviews or an ADR; avoid imposing a new architecture on a small local fix."
---

# Sui Architecture

Choose an architecture that meets actual constraints and remains understandable to its owners.

## Workflow

1. Map the current request path, data ownership, external dependencies and deployment boundaries. Read contracts and code before drawing the ideal future system. Identify scale, latency, availability, privacy, team and migration constraints.

2. Compare two or three viable approaches including the current design. Evaluate concrete tradeoffs: consistency, coupling, operations, testing, cost, ownership and reversibility. Prefer familiar technology among options that satisfy hard requirements.

3. Define component responsibilities, interface contracts and invariants. Describe timeouts, retry budgets, idempotency, ordering, concurrency and error semantics at failure-prone boundaries. Make trust boundaries explicit.

4. Write a short ADR for consequential choices: context, constraints, alternatives, decision, consequences, evidence, revisit trigger and migration/rollback. Use a component or sequence diagram only when it explains a nontrivial relationship.

5. Validate the riskiest assumption with an executable spike, contract test, representative workload or failure experiment. Implement incrementally with a compatibility path. Record what remains an estimate.

## Decision rules

Do not start with microservices because a case study used them. Distribution needs a reason such as independent ownership, isolation, scaling or release cadence. A modular monolith is a useful baseline, not a universal answer.

Choose patterns by data flow and change pressure: pipes/filters for staged transformation, events for decoupled reactions, layers for responsibility boundaries, client/server for service access, MVC for presentation separation, blackboard for cooperating solvers. Name a pattern only when it clarifies a decision.

Seek high functional cohesion and low coupling. Avoid shared mutable state and control flags that bind unrelated decisions. Evaluate content/common/external/control/stamp/data coupling through the actual contract, not vocabulary quizzes. Concurrency and resource lifetime are architecture concerns when shared boundaries exist.

API compatibility concerns source-level consumers; ABI compatibility concerns independently compiled consumers, symbols, layout and calling conventions. Test both where applicable. For evolving schemas, consider expand/migrate/contract and mixed-version operation.

## Resources and evidence

Use `assets/adr.md` only for a consequential decision. Replace example constraints with measured project constraints.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

## Operational resources

[design methods](references/design-methods.md): Use for pattern/view choice, UML component/sequence semantics, cohesion/coupling, API/ABI/IPC and error/logging contracts.
