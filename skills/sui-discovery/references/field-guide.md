# Field guide

## Evidence to capture

Capture the trigger, expected behavior, actual project constraint, affected boundary and verification result. Distinguish observed facts, assumptions, external guidance and decisions. Keep this proportionate to the task. Do not create a document or an approval gate simply because a template exists.

## Primary starting sources

- [YC Essential Startup Advice](https://www.ycombinator.com/blog/ycs-essential-startup-advice): Launch a narrow useful product, learn from users and iterate. This is product discovery advice, not permission to omit safety or integrity.
- [How to Plan an MVP](https://www.youtube.com/watch?v=1hHMwLxN6EM): YC original lecture; choose a limited initial workflow and feedback loop. The YC library landing page contains no extractable text, so use this original recording.
- [WCAG Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/): Use relevant accessibility success criteria with manual keyboard/focus and assistive-technology checks. Automated scans alone do not establish conformance.

Sources checked 2026-10-31. Reopen relevant current/versioned sources before relying on volatile claims. An old article can supply a design lens without establishing current product capabilities. Do not copy large portions or run downloaded snippets without inspection.


## Concrete decision examples

- **“Make signup fast”:** Specify a journey, realistic traffic, latency percentile, error behavior and measurement environment; do not guess that “fast” means 100 ms.
- **“Build every feature before launch”:** Identify the one useful completed workflow and minimum trustworthy release boundary; defer features without evidence.
- **A two-day integration with unknown provider limits:** Inspect official contracts and run one bounded feasibility spike before giving a schedule.
- **The user already gave acceptance criteria:** Proceed with the authorized work; do not force another discovery interview.
