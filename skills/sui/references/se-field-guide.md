# Software engineering field guide

## Contents

1. Use principles proportionately
2. Lifecycle and delivery
3. Requirements and planning
4. Architecture and interfaces
5. Implementation and collaboration
6. Test strategy and evidence
7. Reliability and metrics
8. AI-enabled systems
9. Security, privacy and open source

## Use principles proportionately

Adapt process to risk, reversibility, uncertainty and team size. A small typo patch needs inspection; an authorization change needs boundary tests; a migration needs data/recovery reasoning. Use system constraints and observed change pressure, not the age or prestige of a method.

## Lifecycle and delivery

Connect need, design, code, verification, release and maintenance even during rapid iteration. Select waterfall-like upfront work where stable dependencies demand it, iterations for learning, increments for usable slices and risk-driven spikes for unknowns. Integrate security throughout. Agile values feedback and adaptation; Scrum is one organizing approach, XP supplies technical practices and Lean highlights waste/feedback. Use INVEST and the four Ps only when they clarify work. Treat configuration updates and code as release risks, as the CrowdStrike case motivates.

## Requirements and planning

Separate user goals, functional behavior and measurable quality constraints. Make requirements concise, unambiguous, feasible and verifiable. Elicit real behavior through interviews, observation, personas/use-case flows and prototypes. Validate the understanding, maintain traceability and analyze changes. Estimate from decomposed work, unknowns and historical project evidence; use COCOMO/function points only with calibrated assumptions, not as magical precision. Record scope/time/cost tradeoffs, risks, owners and dependency critical paths when coordination warrants them.

## Architecture and interfaces

Decompose by responsibility and ownership; show different views for different questions. Compare architecture patterns against quality scenarios. Prefer high cohesion and low coupling. Cohesion categories are coincidental, logical, temporal, procedural, communicational, sequential and functional. Coupling categories are content, common, external, control, stamp and data. Use these as diagnostic lenses, not a demand to rename every module. Specify error contracts, synchronous/asynchronous semantics, API/ABI compatibility and state ownership. Include usability, accessibility, error prevention and reversibility as system qualities.

## Implementation and collaboration

Choose a language that meets hard runtime constraints, then favor maintainers' expertise and ecosystem fit. Write clear structured code with consistent names, defensive boundaries, safe resource handling and test seams. Combine incremental review, linters/types, deeper static analysis where useful and dynamic evidence. Build a bounded codebase mental model through entry points, patterns, IDE navigation, probes and tests. Use baselines, branches, controlled changes, reproducible builds and explicit release policies to preserve working states. Maintain SBOMs and dependency ownership where appropriate. Pay down technical debt when its concrete future cost warrants it; do not equate unfashionable code with debt.

## Test strategy and evidence

Define an oracle and representative risk coverage. Combine partitions, boundaries, pairwise, properties, fuzzing, mutation and scenario tests as appropriate. Test units, contracts, integration, complete journeys and acceptance conditions at the boundary that can fail. Use stubs for controlled dependencies, not to conceal the real integration. Preserve release/regression evidence. Static/dynamic analysis and verification/validation describe different dimensions. Coverage shows execution; it does not establish correctness or useful assertions. Account for short circuit and loops.

## Reliability and metrics

Measure user-visible success, failure, latency and resource saturation. Define numerator, denominator, unit, window and sampling. Use percentiles and uncertainty; check confounding and gaming. Goodhart's law cautions against individual quotas on proxy metrics. LOC/Halstead/cyclomatic/OO metrics can reveal investigation targets, not general productivity or maintainability truths. Distinguish failure rate, time-between-failure, defect density, defect distribution and leakage denominators. Plan load, stress, soak and controlled resilience experiments with recovery. Redundant software can share a common-mode failure.

## AI-enabled systems

Distinguish AI for engineering from engineering a fallible ML system. System needs extend beyond training code: data, serving, monitoring, feedback and safety. Compare a deterministic baseline; anticipate mistakes through independent checks, guardrails, undo, human oversight and hazard analysis. Evaluate final task outcomes, components and slices. Choose model placement by latency, bandwidth, privacy, offline needs, energy and cost. Treat confidence and model accuracy as insufficient guarantees.

## Security, privacy and open source

Map assets, attackers, trust boundaries and threat paths; derive measurable security requirements, reduce attack surface, layer controls, verify them and plan incident response. Distinguish authentication/authorization/confidentiality/integrity/replay defenses. Combine authorized pentests with code-focused fuzzing. Minimize collection and retention and make privacy promises enforceable. Apply LINDDUN and Privacy by Design where personal data exists. Distinguish source visibility from license rights, copyleft from permissive conditions and copyright from patents. Inspect actual distribution/modification/linking conditions, attribution, trademarks and contribution terms; do not treat a short summary as a legal conclusion. Consider human impact, accessibility, fairness and incentives throughout the lifecycle.

