---
name: sui-ai-systems
description: "Engineer ML/LLM features as fallible components with task-specific evaluations, data boundaries, tool permissions and cost/latency budgets. Use for agents, RAG, model placement, prompt changes, AI reliability or model selection; prefer deterministic code when it solves the task."
---

# Sui Ai Systems

Demonstrate useful system behavior under realistic errors rather than shipping a convincing model demo.

## Workflow

1. Define the user task, consequence of mistakes, non-AI baseline and measurable success. Decide whether deterministic code, one model call, a fixed workflow or an agent is warranted. Use frameworks only when their benefits exceed their operational opacity.

2. Specify data lineage, splits, permissions, retention and versioning. For retrieval, evaluate document coverage, chunking and retrieval separately from answer generation. Prevent tenant mixing and training/test leakage.

3. Define typed tool contracts, permissions, side-effect boundaries, deadlines, retries and spend/step limits. Validate outputs structurally and semantically where possible. Treat retrieved content and tool output as untrusted data; prompt text alone cannot enforce authorization.

4. Evaluate a representative held-out set including adversarial, abstention, failure and subgroup cases. Use reproducible versions, repeated trials where stochasticity matters, calibrated graders and human review samples. Inspect trajectories and final environment state, not just a plausible answer.

5. Compare quality, cost and latency against the baseline; record uncertainty. Add monitoring for drift, provider changes, failures and feedback. Roll out with a useful fallback or abstention when the cost of a wrong action warrants it.

## Decision rules

Accuracy is not correctness of the entire system, and confidence is not calibrated probability by default. Plan for component mistakes with hazard analysis, guardrails, undo, independent checks and human review when consequences justify them.

Use cloud/edge/device placement based on latency, bandwidth, privacy, offline needs, energy, updateability and cost. Do not carry 2023 model prices, context lengths or vendor rankings from the a16z ecosystem article into a current decision.

Keep development cases separate from held-out evaluation. A repeated trial on the same case is not a new independent task. Report task count, trial count and per-case variability. If an LLM grades outputs, validate the rubric against human examples, blind model identity and inspect disagreement. Evaluation can improve confidence, not certify universal safety.

## Resources and evidence

Use `scripts/eval_report.py results.json` for per-variant, per-case held-out summaries and paired case comparisons. It summarizes supplied judgments; it does not call models, grade outputs or prove rubric validity.

Read [field guide](references/field-guide.md) for task-specific examples and primary sources. Treat referenced resources as guidance scoped to their context. Inspect current project versions before applying external API/security/standards claims. Use the existing environment's browsing or connected-source tools; if unavailable, report the uncertainty and continue safe local work.

## Operational resources

[ml lifecycle](references/ml-lifecycle.md): Use for collection/labels/features, training-serving compatibility, evaluation, rollout and retraining contracts.
