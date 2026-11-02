# Planning, estimation and control

Use for coordinated work and uncertainty, not to manufacture a schedule for a trivial edit.

## Lifecycle and feasibility

Select a lifecycle from change uncertainty, feedback access and failure cost. Waterfall requires sufficiently stable baselines and controlled changes. The V-model explicitly pairs requirements with acceptance tests, system design with system tests, architecture/interfaces with integration tests, and detailed units with unit tests; plan the oracle while defining the corresponding artifact. Iterative work revises the same capability from feedback; incremental work adds useful slices; they can coexist. In a spiral loop define objective/alternatives, analyze the dominant risk with a bounded prototype, engineer the selected increment, then review results and authorize/replan the next risk loop. Exit or change direction when the risk experiment fails its criterion.

Separate product lifecycle (research, launch, support/training, evolution/porting, retirement) from an individual development project and from long-lived maintenance. Record support owner, onboarding/training needs, backward compatibility, data export/retention and retirement communication early enough to affect design. A product lifecycle is not merely the date code is deployed.

## Work breakdown and estimates

Decompose scope into verifiable deliverables, then leaf activities with owner, dependency, estimate range, unit and assumption. Count effort only at leaves; do not add a parent estimate to its children's estimates. Include test data/environments, review, integration, rollout, support and contingency work that materially affects delivery. A spike ends in a decision, not an indefinitely renamed task.

Estimate by analogy or calibrated throughput for comparable completed work. Separate person-hours of effort from elapsed days, calendar exclusions and parallel staffing. Do not assume adding people divides elapsed time linearly. For story estimates, use team-relative examples and uncertainty; velocity is a within-team planning observation, not an individual score or a cross-team comparison.

`scripts/project_plan.py cocomo INPUT.json` exposes historical Basic COCOMO with explicit KLOC and organic/semi-detached/embedded mode. The coefficients and effort/person-month, duration/month and staffing ratios appear in output. Example organic10KLOC gives about26.93person-months and8.72months, roughly3.09average staff. Treat this as an educational calculation pending local calibration. Do not call an unknown future code size a reliable forecast.

## Schedule and critical path

Give each leaf duration, predecessor IDs, resource availability, earliest start, deadline and milestone outputs. Check dependencies are acyclic and estimates use one unit. A forward pass computes ES=max(predecessor EF), EF=ES+duration; a backward pass from project finish computes LF=min(successor LS), LS=LF−duration; slack=LS−ES. Zero-slack tasks lie on at least one critical path. Independent parallel paths can be equally critical.

`scripts/project_plan.py schedule INPUT.json` performs those passes and rejects unknown dependencies/cycles. It intentionally assumes unlimited resources. Add actual people/equipment availability and level conflicts manually before committing a calendar. Map offsets to working calendars/holidays/timezones in the project's scheduling tool, then inspect the actual Gantt/export. A topological task order is not a resource-feasible schedule.

Worked plan: A environment2days; B implementation3days after A; C test data1day after A; D integration2days after B and C. Finish7days; critical A/B/D; C has2days slack. If B and C need the same person, choose an explicit sequencing/resource change and recalculate rather than hiding the conflict in a chart. Use `assets/project-plan.example.json` for this input shape.

## Ownership and risk

RACI means R performs work, A owns the decision/outcome, C gives necessary input, I receives the result. Use exactly one A and at least one R per activity; one person may be both. Name decision rights and escalation path, not just people copied on a task. `project_plan.py raci INPUT.json` checks this policy. For a solo task it is usually enough to name the owner.

Maintain a risk register: event/cause, affected objective, qualitative likelihood/consequence with evidence, trigger, treatment, fallback, owner and next review. Distinguish mitigate, avoid, transfer/share and accept. Do not multiply arbitrary ordinal values into false precision. Example: the staging database may be unavailable by integration day; trigger is no restored test dataset by day2; treatment is early restore validation; fallback is a documented reduced lab with the resulting confidence limit.

## Monitoring and closure

Baseline scope, estimate assumptions, milestones, owners, quality/acceptance and communication cadence. Review actual deliverables, remaining work, spend/capacity, risks and blockers against that baseline. Reforecast when assumptions change; do not hide new scope inside an old burndown. Track planned/created/executed tests and defect aging by meaningful severity alongside delivery, not raw activity counts.

For a burndown, show remaining estimated work and additions/removals each day. For throughput report completed comparable items per window; for cycle time define start/end events and show a distribution including unfinished-item aging. A shorter cycle time obtained by splitting trivial items is not proof of higher value. Record cause and decision when scope/time/cost trade off.

At closure, verify acceptance/handover, known defects, support/runbook ownership, retained evidence and data obligations. Capture one useful lesson and an owned improvement. Stop obsolete environments/services only within task authorization and preserve promised user data.
