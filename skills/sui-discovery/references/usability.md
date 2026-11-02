# Usability validation

Separate learnability, task efficiency, memorability, errors/recovery, satisfaction and accessibility. A feature being implemented does not make it usable.

## Study method

Choose a decision and representative users/tasks, including relevant disability, experience, language and device constraints. Obtain appropriate consent and collect only needed notes. Define a task outcome without teaching the UI, a timebox and criteria for success, partial success, failure and moderator intervention. Observe unassisted behavior, errors, recovery and user language; ask neutral follow-up questions after the attempt. Record sample composition and uncertainty; small formative studies reveal problems but do not certify population success rates.

Example task: “You wrote a draft yesterday. Find the saved version and recover an earlier paragraph.” Measure unassisted completion, time-to-first-correct-action, recoverable/unrecoverable errors and confidence. Separate product defects from study setup failure. Preserve redacted observations and synthesize the most consequential recurring problem, its proposed change and a repeat task for validation.

Use dogfooding to find rough edges, while noting that developers are experienced insiders. Use observation/contextual inquiry for tacit workflows, interviews for experience, questionnaires for distributions after defining the construct, low-fidelity prototypes for workflow uncertainty and instrumented field tests for actual use. Do not turn survey satisfaction into task performance evidence.

## Experiments and implementation

For A/B tests define one hypothesis, primary metric, guardrails, randomization unit, exposure, sample/power assumptions and stopping policy before reading outcomes. Check assignment contamination, repeated-user correlation, novelty, missing data and harms. A small prototype test is often more useful than an underpowered A/B test. Never describe an uncontrolled before/after change as causal proof.

Make critical actions perceivable, keyboard-operable and understandable; preserve focus order, labels, visible feedback, accessible errors, contrast and motion preferences. For risky actions offer preview/reversal and communicate consequences. Check locale/date/timezone, number/currency formats, text expansion and right-to-left layout where relevant. Test actual assistive technologies and target devices for the requirements that depend on them; automated checks alone do not establish accessibility.

For a cloud app validate latency/offline behavior, tenant boundaries, session recovery and deployment-region/data assumptions. For regulated requirements map a verified versioned obligation to an actual control and test; a test category named “compliance” is not a legal conclusion. Avoid dark patterns: hidden fees, coercive defaults, confusing cancellation and disclosure that prevents informed choice. Surface the tradeoff and an honest alternative.
