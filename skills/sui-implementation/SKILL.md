---
name: sui-implementation
description: "Implement a feature or fix in an existing project with repository discovery, readable code, explicit invariants, secure boundaries and proportionate verification. Use for production code changes, type/lint/static checks or analyzer integration; preserve local conventions and avoid unrelated rewrites."
---

# Sui Implementation

Deliver the requested behavior as a small reviewable change with evidence that it works.

## Workflow

1. Read applicable AGENTS.md, relevant code, manifests, tests and callers. Check working-tree changes. Identify the actual entry point and the smallest change boundary; preserve user work.

2. State the intended behavior, invariants and failure semantics. Follow the repository language, naming and service boundaries. For language choice, satisfy hard constraints first, then prefer maintainers' expertise and existing tooling.

3. Implement a coherent increment. Validate untrusted input, enforce authorization at the trusted boundary, handle errors intentionally and release resources. Prefer a clear local solution to speculative abstraction or a broad dependency addition.

4. Verify at the boundary where the behavior can fail. For a defect, demonstrate the original failure and its regression when practical. Run relevant formatter/type/lint/test/build checks; use manual inspection for low-impact reversible edits when that is sufficient.

5. Inspect the final diff and callers for accidental churn, unsafe logs, missing compatibility and stale docs. Report changed behavior, meaningful validation and material limitations; mark unrun checks explicitly.

## Decision rules

Write names that express responsibility and comments that explain constraints or surprising intent. Keep mutable state and side effects explicit. Separate core decisions from network/filesystem/time boundaries when this makes tests and reasoning simpler. Do not force every function into a service or every file into one pattern.

Use guard clauses, exhaustive handling and typed contracts where they reduce ambiguity. Avoid swallowing exceptions, retries on every error, mutable defaults, unbounded queues and shell interpolation. Preserve error context without leaking credentials or personal information.

Treat AI-generated code as an untrusted proposal: inspect dependencies, APIs, boundary behavior and tests. Use deterministic compilers/typecheckers rather than an LLM to decide facts they can establish. A compiling implementation is only one layer of evidence.

## Resources and evidence

Run the project's own checks. If using Sui Delivery's gate runner, inspect its command plan before execution; never substitute its JSON status for the underlying test evidence.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

Load [stack adapters](references/stack-adapters.md) when framework/runtime behavior matters. Prioritize measured user impact and verify the installed version's contract rather than applying every external rule. For consequential changes, bind completion evidence to current source/config/test inputs using Sui Delivery; preserve a direct inspection path for trivial edits.

## Operational resources

[static analysis](references/static-analysis.md): Use to select/configure/triage the named analyzers and distinguish support levels.

Use `scripts/tool_checks.py run` for reviewed native checks and `scripts/tool_checks.py parse` for the documented report subsets. Read the static-analysis guide before treating any result as evidence. Config examples are in `assets/configs/mypy.ini`, `assets/configs/tsconfig.checks.json`, `assets/configs/clang-tidy.yaml` and `assets/configs/sonar-project.properties`; map them to actual project versions/paths rather than blindly overriding project config.
