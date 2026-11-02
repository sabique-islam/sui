# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [DORA Software Delivery Performance Metrics](https://dora.dev/guides/dora-metrics/): The current retrieved guide has five metrics. Measure at service level and avoid individual quotas or cross-context league tables. Recheck definitions before use.
- [YC Essential Startup Advice](https://www.ycombinator.com/blog/ycs-essential-startup-advice): Launch a narrow useful product, learn from users and iterate. This is product discovery advice, not permission to omit safety or integrity.
- [Emerging Architectures for LLM Applications](https://a16z.com/emerging-architectures-for-llm-applications/): 2023 ecosystem analysis. Reuse its separation of data preparation, retrieval, inference and operations; do not reuse old model prices, product rankings or context sizes.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/): Use a limited representative population, comparable control, release-specific observations and an actual rollback path.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **A popular blog recommends a library:** Inspect current official support, version, limitations, license and a representative project test before choosing it.
- **A before/after benchmark improves:** Check workload, sample size, cache/warmup, machine, concurrency and confounders before claiming causation.
- **A source URL exists but could not be read:** Mark unavailable or seed; do not count it as retrieved support.
- **A 2023 ecosystem article names a default model:** Retain its architectural questions; verify current APIs, costs and comparative quality independently.
