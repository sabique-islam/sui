# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents): Use simple composable patterns first; distinguish fixed workflows from model-directed agents and account for cost and latency.
- [Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents): Build realistic tasks and reliable graders; evaluate agent trajectories and outcomes, including repeated trials and failure analysis.
- [Google Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml): Establish a simple baseline and sound data/serving pipeline; detect training-serving skew and optimize system outcomes.
- [Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications/): 2023 ecosystem analysis. Reuse its separation of data preparation, retrieval, inference and operations; do not reuse old model prices, product rankings or context sizes.
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): Model assets, boundaries and threats, select mitigations, then validate them. Threat models evolve with the implementation.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **A deterministic parser solves the task:** Use it as the baseline; do not add a model because the product is AI-branded.
- **One easy case is repeated 100 times:** Report one distinct task with trial variability; do not advertise 100 independent successes.
- **A RAG answer is wrong:** Separate missing corpus, failed retrieval, wrong evidence use and generation failure before changing the model.
- **A generated tool argument passes a JSON schema:** Check authorization, business invariants and side effects separately; structural validity is not permission.
