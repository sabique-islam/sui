# Test plan working contract

Identify project/revision, requirement baseline, decision owner and target environment.

Record scope/in-scope risks and explicit exclusions; measurable quality goals and denominators; levels/techniques; representative data and teardown; tool/framework/version/collection command; people/capacity; setup/author/run/triage/retest estimates and calendar dependencies; deliverable/report location; entry/exit and suspension/resumption criteria; severity/aging/duplicate/reopen triage; environment/tool/model/resource risks with trigger/fallback/owner.

For every consequential requirement record test objective, method, component, owner, SDLC timing, environment/tool, oracle and actual evidence. For security objectives include abuse/denied cases and the final risk disposition. Preserve blocked and deferred rows without marking them passed. Before closure inspect whether the original symptom/business scenario was actually exercised.

Case fields: id, module, requirement/risk links, priority, tester/owner, preconditions, environment/version, input, numbered action, expected outcome, actual outcome, status, evidence.

Worked recovery case: R1; persistence; high; engineering; acknowledged draft revision5 exists in disposable profile; interrupt a new save at the precommit seam; restart; expected revision5/content remain intact and unacknowledged work is not claimed saved; actual result plus run ID recorded after execution. This template itself is not execution evidence.
