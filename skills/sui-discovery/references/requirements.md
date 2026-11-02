# Requirements and traceability

Use the smallest artifact that preserves the decision. Expand to this method when several stakeholders, interfaces, safety/privacy concerns or downstream teams need an agreed baseline.

## Elicit evidence before writing requirements

Identify users, purchasers, operators, support, security/privacy, maintainers and external regulators only where relevant. Record each person's goal, decision rights, available evidence and conflicts. Select techniques by uncertainty: an interview for motivation/recent behavior; observation for tacit workflows; document analysis for existing rules; a questionnaire for distribution after the hypothesis is understood; a facilitated workshop for competing goals; a prototype/role play for interaction ambiguity. Do not turn a checklist into substitute user evidence.

For an interview, ask about the latest actual incident, sequence, workaround, frequency and cost. For an observation, obtain task-appropriate consent, explain what will be recorded, avoid unnecessary personal data, watch without coaching, and distinguish an observed action from an inferred need. Capture workarounds, handoffs, social constraints and exceptions. Validate the synthesis with participants, preserve disagreements and avoid projecting one expert's workflow onto all users. A persona is an evidence-backed archetype; an assumed persona must be labelled a hypothesis with a validation action.

Example: a support agent copies ticket details into a spreadsheet because reassignment loses context. The requirement is to preserve a readable ownership history, not automatically to build a spreadsheet export. A scenario names actor, goal, starting state, trigger, sequence and outcome; a persona adds relevant goals/context/access needs without invented demographic precision.

## Feasibility and classification

Compare build, buy, integrate and current workaround against hard constraints. Use a table of technical feasibility (spike and failure bound), economic cost (one-off plus operations), operational fit (owners/training/support), schedule/dependency risk and contractual/privacy constraints. Record assumptions and a cheapest discriminating experiment. Recommend one option with a revisit trigger; a guessed ROI is an assumption, not evidence.

Distinguish user goals from system obligations. A functional requirement describes behavior; a quality requirement gives a measurable constraint; organizational requirements come from internal policy/process; external requirements arise from a verified contract or jurisdiction; domain requirements encode subject-matter rules. Derive system obligations from user goals and identify cross-cutting security/accessibility constraints. Avoid labelling every technology preference an immutable requirement.

Example: user goal U1 is “recover my draft after a crash.” System R1 is “after an acknowledged save, reopening the same local profile restores the last acknowledged content.” R2 is a measurable restoration-time target in a stated environment. R3 restricts cross-profile access. A persistence implementation is a design choice, traceable to these requirements.

## Semantic requirement review

Review each requirement for necessity, singular behavior, clear actor/trigger, measurable acceptance, feasible dependencies and source/owner. Review the whole set for missing error/denied/empty/upgrade cases, contradictory values, consistent terms/units, priorities and unresolved conflicts. Ask another stakeholder to restate it without the author's explanation. Structural validators cannot establish these qualities.

Use INVEST when stories are useful: Independent (minimize cross-story blocking), Negotiable (goal rather than frozen solution), Valuable (beneficiary and outcome), Estimable (uncertainty bounded), Small (one verifiable increment), Testable (observable oracle). Split a large “manage accounts” story into create, recover and deactivate workflows; do not split only by UI/backend/database layers when that leaves no user outcome.

Validate with users by walking through a realistic scenario and prototype, including failure/recovery, rather than obtaining approval for jargon. Verify the written artifact against agreed rules and interfaces. A fishbone analysis can expose candidate causes under people/process/data/environment/tooling; test those hypotheses against evidence. It cannot establish requirement completeness by drawing a diagram.

## Optional SRS baseline

Create sections for purpose/scope; product context and actors; terminology; external user/software/hardware/network interfaces; assumptions/dependencies; numbered functional requirements; measurable quality and security requirements; domain/external constraints; acceptance and traceability; unresolved decisions; revision/approval ownership. Include a context diagram only if it resolves a boundary. Use stable IDs and change history. Preserve modifiability by separating behavior, rationale and design choices; reject contradictory duplicates.

Example external interface: import UTF-8 CSV with documented header, maximum size, malformed-row behavior, authorization and all-or-nothing semantics. The SRS specifies those contracts; parsing-library choice belongs to design. Validate interface assumptions against actual consumers, not only the UI.

## Use cases and discovery models

In a use-case diagram place actor roles outside a named system boundary and goal-oriented use cases inside. Associations represent participation; an external service can be an actor. Do not model individual UI clicks as actor goals. Use include for a genuinely reused required subflow and extend for conditional extension with explicit condition; avoid a diagram that disguises a sequence model. Check every use case has a beneficiary and every important actor goal is represented.

Write a use-case specification with ID, goal, actors, trigger, preconditions, main numbered flow, alternate/exception branches, postconditions and linked requirements/tests. Branch “3a: payment declined” from main step3, describe preserved state and return/termination; do not silently jump back to a step whose preconditions no longer hold. For “restore draft,” precondition is an accessible profile, trigger is opening a saved draft, alternate is missing/corrupt storage, postcondition is recovered content or an explicit actionable failure without overwrite. Derive one acceptance case for each material outcome.

## Bidirectional SDLC traceability

For consequential requirements, map user/system requirement IDs to architecture section, detailed design, code files, unit/functional/system/acceptance tests and security validation where relevant. Follow links forward to show planned realization and backward to find orphan code/tests or gold plating. Keep artefacts versioned and owned. A reasoned waiver is better than an invented link for a level that does not apply.

Use `scripts/traceability.py assets/traceability.example.json` to check graph IDs, required-kind coverage, reverse orphans and change records. Add `--root /project` to check code locators. It verifies graph structure, not that a link proves the behavior. `validate_contract.py` remains the lighter path for a single change.

Handle changes with ID, baseline, requester, rationale, alternatives, impacted requirements/design/code/tests/users, cost/risk, decision owner, accepted/rejected/deferred status and target release. Rebaseline only after the project-native decision, update linked artifacts and verify affected acceptance evidence. Communicate changed assumptions to owners. Do not silently treat an implementation deviation as a changed requirement.
