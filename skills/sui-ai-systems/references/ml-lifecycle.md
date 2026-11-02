# ML and LLM delivery contract

Treat the model as one fallible component of a system with users, data, tools and recovery.

## Pipeline and compatibility

Specify a task/non-AI baseline, consequence of each error, data permission/purpose, collection process, provenance, label definition and adjudication, cleaning/filter rules, feature schema/units and train/dev/test split policy. Fit preprocessing only on training data; keep entity/time/tenant leakage out of the held-out task. Record data snapshot, preprocessing/feature version, training code/config/seed, model identity, evaluation set/rubric and serving contract as one versioned manifest.

Before promotion check feature names/order/types/defaults, tokenizer/preprocessor revision, model input/output schema and supported runtime. Run the same feature fixtures through training and serving to detect skew. Compare with the deterministic or previous-model baseline on a representative held-out set and harmful/failure/abstention/subgroup cases. Do not use test cases as a repeatedly tuned development set. Sui's eval_report summarizes supplied judgments and costs/latencies; it does not train, call, grade or certify models.

Worked feature manifest: event forecast v2 uses only voluntary RSVP count and aggregate past attendance, feature schema `rsvp_count:int>=0` and `past_fill_rate:float[0,1]`, data snapshot D7, transform F3, model M4 and output expected count plus uncertainty bound. Hold out later events by time and prevent repeat-event/individual leakage. A new feature transform F4 cannot silently serve M4 if its units/order differ; block promotion until compatibility fixtures and an evaluation pass.

## Deployment and feedback

Define artifact/dependency identity, placement (device/edge/cloud), latency/bandwidth/energy/privacy/offline constraints, deadline, fallback/abstention, tool permissions and spend/step budgets. Distinguish typed syntax from semantic truth. Use limited rollout and compare user-level outcome/error/cost/latency against the prior version. Roll back model and compatible feature/config versions together, preserving stored-data compatibility.

Monitor input/schema failures, drift in relevant populations, quality proxies calibrated against delayed true outcomes, guardrail/tool errors, cost/latency and human overrides. A drift alarm triggers investigation; it does not automatically authorize retraining or redeployment. Record the new data's permission/labels, rebuild on a versioned pipeline, reevaluate unchanged held-out/refresh policy, review regressions and obtain the ordinary release decision. Preserve feedback quality and prevent the model's own predictions from becoming unreviewed labels.

For LLM agents inspect task trajectories, final environment state and unintended side effects; calibrate any model grader on blinded human examples and review disagreements. Tool output/retrieved text is untrusted input. A prompt cannot enforce authorization that belongs at a tool/service boundary. Prefer one deterministic operation or one model call over an opaque agent when it meets the task.
