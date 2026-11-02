---
name: sui-discovery
description: "Turn an uncertain software request into a small testable scope using user evidence, requirements, acceptance criteria, feasibility and risk. Use for feature discovery, MVP boundaries, SRS, user stories, project plans or unclear success conditions; use startup-gtm for full go-to-market strategy."
---

# Sui Discovery

Define the smallest useful outcome and its acceptance evidence, then progress toward it.

## Workflow

1. Inspect existing product, code, issues and user evidence. State who experiences the problem, the triggering situation, current workaround and observable cost. Separate stated requests from observed need. Do not invent interviews or users.

2. Write functional behavior and measurable non-functional constraints. Use concrete examples for success, rejection, boundary and failure paths. Identify assets, privacy expectations, accessibility and operator needs early.

3. Choose one coherent end-to-end slice. Define explicit exclusions and dependencies. For unknown feasibility, run a bounded spike with a decision criterion. Prefer a range with assumptions over a falsely precise schedule; split work by dependency and learning value.

4. Trace consequential requirements to acceptance checks and owners where relevant. Use INVEST for stories when the project uses stories; use a short behavior contract for small changes instead of a ceremonial SRS.

5. Implement the authorized slice or hand a concrete contract to implementation. Ask one focused question only when the missing answer materially changes scope; continue independent inspection. Report decisions, assumptions, acceptance criteria and the next executable increment.

## Decision rules

Do not equate a feature list with validated demand. For interviews, ask about a recent real event, actions, frequency, stakes and workaround; avoid pitching or asking hypothetical willingness to use. For prototypes, observe a user attempting a task rather than explaining the interface.

Use risk as likelihood and consequence, recording mitigations and indicators; avoid multiplying invented ordinal scores into fake precision. Make ownership clear when coordination exists, but do not add RACI ceremonies to a solo patch. Consider people, process, product and project environment when identifying constraints.

Treat rapid launch as a way to learn from a limited audience. Preserve essential authorization, data integrity, safety and recovery. For financial or physical consequences, verify constraints before a public experiment.

## Resources and evidence

Use `scripts/validate_contract.py contract.json` to check requirement IDs, acceptance checks and traceability. A structural pass does not prove that the requirements are correct.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

For multi-step work, carry the agreed goal, acceptance IDs, dependencies, decisions and blockers into the project's existing planning convention. When no convention exists and continuity warrants it, use Sui's `work_state.py` and work-state example. Check requirement-to-task coverage and dependency readiness before execution. Preserve deferred items and distinguish task status declarations from verified acceptance; do not create persistent planning artifacts for trivial requests.

## Operational resources

[requirements](references/requirements.md): Use for elicitation, SRS, use cases, semantic review and bidirectional traceability.

[planning](references/planning.md): Use for lifecycle selection, feasibility, WBS, estimation, CPM, RACI, risks and control.

[team methods](references/team-methods.md): Use for Scrum/XP/Lean coordination, pairing, ownership and sustainable pace.

[usability](references/usability.md): Use for representative-user studies, experiments, accessibility and localization.

Run `scripts/project_plan.py cocomo|schedule|raci INPUT.json` for explicit planning arithmetic/policy. Run `scripts/traceability.py assets/traceability.example.json` for a full artifact-graph check. Use `assets/project-plan.example.json` and `assets/raci.example.json` for worked inputs; retain semantic/user validation separately.
