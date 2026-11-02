# Quality measurement with explicit models

A metric starts with a decision, entity, numerator/denominator, unit, window, exclusions and collection method. Keep raw observations and uncertainty so another person can reproduce the interpretation.

## Size, complexity and function points

For SLOC state physical versus logical statements and comment/blank/generated/vendor-code rules. Record original language/size, any normalization factor and its source/calibration before calculating an equivalent-size value. Do not compare productivity from LOC or silently mix languages using a universal multiplier. A formatter can change line count without changing behavior.

Halstead vocabulary is distinct operators plus distinct operands, length is total operator/operand occurrences and volume is length times log2(vocabulary), under an explicit tokenizer convention. `scripts/quality_metrics.py halstead INPUT.json` performs only that arithmetic; a parser/tokenizer or defect-prediction claim would need separate evidence.

For cyclomatic complexity construct the CFG, state node/edge/component and entry/exit assumptions, then M=E−N+2P. The script accepts an explicit graph, checks IDs and counts weak components. Review infeasible paths, exceptions and source mapping manually. It does not infer data complexity, code quality or the minimum number of branch tests.

For OO metrics define exactly what counts: methods/class (including inherited/generated policy), depth of inheritance to the chosen root, number of immediate children, coupling to other classes and method calls/response set. Normalize the scope/tool rules before comparing and use the metric to inspect a concrete design risk. High/low values can be justified by responsibility; do not enforce a universal number or individual ranking.

Function points classify external inputs (EI), outputs (EO), inquiries (EQ), internal logical files (ILF) and external interface files (EIF), using functional/user boundaries rather than source tables alone. Supply simple/average/complex counts and an internally consistent declared weight table. Published weight tables can disagree with a worked example. Never silently choose the number that makes the total look right. The script refuses a missing table and returns category totals/UFP. Convert to effort only with an explicitly supplied calibrated person-hours/FP factor, and show estimation uncertainty separately.

## Defects and reliability

Fault density is observed defects divided by the stated software size. Module defect share is module defects divided by all observed defects. Phase distribution is defects attributed to a phase over the defined cohort total. Escape/leakage depends on a specified pre/post boundary and observation window; e.g2post-release defects out of8pre+2post is20%, not2divided by code size. Classify severity/type consistently and preserve unknown attribution. More detected defects may mean better tests, not worse engineering.

For reliability define failure, operating environment/profile, exposure unit, repair boundaries and censoring. Exposure/failure count is an observed mean operating-time ratio, not automatically a future MTBF or probability of failure-free operation over a time interval. The reciprocal rate and exponential survival interpretation require explicit stationary/model assumptions. No failures in100hours is a limited observation, not infinite reliability; no exposure is no data. Sui Reliability's request SLI answers a different event-based question.

For coverage record instrumented/source/test identity, statement/decision/condition/function or branch definitions, executable denominator and excluded/unreachable behavior. For test progress distinguish planned/created/executed, status and relevant-risk coverage. For autonomous systems separate model accuracy from whole-system failure exposure/mileage and define crash/error population; one model score cannot establish a safety rate.

## Statistics and incentives

Use sample counts, distribution/tails and matching workloads. Nine observations at 10ms and one at 5210ms have a 530ms mean, not 500ms. `quality_metrics.py latency` implements nearest-rank p50/p95/p99; state the algorithm and sample unit. Do not average already aggregated percentiles as if that produced a pooled percentile. Check missingness, sampling, confounding, changing populations and repeated/correlated observations before a causal claim.

Interpret the coverage paradox through test-suite size, risk selection and assertion quality rather than assuming coverage causes correctness. Benchmark the same workload/environment/version with raw data and uncertainty. Inspect how a target could be gamed before using it: LOC, commits, story points, bug counts and coverage are poor individual-productivity objectives. Pair a decision metric with guardrails and real user outcomes.
