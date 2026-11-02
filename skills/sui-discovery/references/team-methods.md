# Team delivery methods

Select the practice that solves an actual coordination problem.

## Scrum mechanics

Product owner owns product value, ordering and acceptance context; Scrum master coaches the framework and helps remove impediments; developers create the increment and adapt their plan. Keep product backlog (ordered future outcomes) distinct from sprint backlog (sprint goal plus selected work and delivery plan). Agree a definition of done with relevant test/security/docs/integration expectations before calling an increment complete.

At sprint planning state a coherent goal, inspect ordered items and dependencies, check availability/history/uncertainty, select a feasible set and split it into observable work. Negotiate scope with the product owner as understanding changes; do not rewrite the goal silently. Estimates support planning rather than guaranteeing every selected item.

In a short daily coordination meeting inspect progress toward the goal, next work and impediments. Assign a concrete owner/action for each blocker and move detailed debugging into a follow-up with relevant people. It is not a performance status report to a manager. Keep the task board consistent with actual work: clear states, explicit entry/exit conditions, visible blocked work, a WIP policy when useful and owner per task. A connector-backed update must map actual project fields and preserve unrelated state.

At review demonstrate a usable increment through a representative user scenario, compare the outcome with the goal, collect stakeholder evidence and update the product backlog. At retrospective inspect one specific positive/negative event, identify a plausible cause, choose an improvement experiment with owner/measure and check its result next cycle. Do not make retrospective notes an unused grievance archive.

## XP practices

Run release planning with customer outcomes/priorities, rough estimates, constraints and risks. Run iteration planning with the next small useful stories, developer estimates, capacity and executable acceptance examples. Use a spike for an uncertainty with an explicit timebox and decision criterion. Prefer the simplest design that supports current invariants; refactor after protected behavior, not in place of delivering the feature.

For pairing, driver implements the current small step while navigator tracks invariants, edge cases and direction. Swap roles after a short interval or completed test; pause to ensure both can explain the code. Rotate pairs across ownership boundaries when it shares context. For collective ownership retain reviews, conventions and accountability while enabling safe contributions outside a single maintainer's area. Record critical knowledge and reduce bus-factor dependencies.

Use an available customer/domain proxy with clear decision rights and response expectations. Batch nonblocking questions, preserve decisions with assumptions, and avoid making one unavailable expert the hidden scheduler. Sustainable pace requires capacity below theoretical maximum, slack for integration/support and visible overload. Adjust scope when recurrent overtime is the only way a plan appears viable.

## Lean improvement

Map request-to-value flow with wait time, handoffs and rework. Identify waste such as unused features, queues, repeated manual repair and partially finished work. Pick one constraint and measure a small improvement in end-to-end flow; optimizing one stage while growing downstream queues is not success. Defer reversible choices until the last responsible moment: record the information to learn and the point beyond which delay becomes costly. Empower the people doing the work within explicit quality/authorization constraints.

Worked example: three review handoffs add4days to a30minute change. Measure queue age and rework, establish one available accountable reviewer plus specialist consultation only when the boundary needs it, trial a WIP limit and compare cycle-time distribution and escaped defects. Do not “improve” throughput by omitting verification or manipulating item size.
