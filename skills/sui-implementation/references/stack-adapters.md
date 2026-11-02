# Apply stack guidance conditionally

Inspect manifests, lockfiles, runtime versions and existing conventions before loading stack-specific guidance. Match advice to actual execution semantics and verify against the deployed version's official docs. A rule collection supplies investigation targets, not automatic refactoring instructions.

For React/Next.js, inspect request waterfalls and large client bundles before micro-optimizing render details. Start independent I/O together only when there is no data dependency or shared transaction requirement; preserve cancellation and error semantics. Trace server mutation authorization and cache lifetime/keys, particularly tenant and user data; do not put request-specific mutable state into a cross-request singleton. Keep accessibility, focus and error states part of the behavior contract. Measure representative user impact before claiming performance improvement.

For Python/backend code, inspect blocking I/O inside async paths, transaction/connection lifetime, mutable shared state and cancellation. Check the actual framework's request and authentication boundaries. For SQL, preserve parameterization, authorization predicates and transactional invariants; consult the deployed database's locking/DDL documentation before migrations. For C/C++ or native interfaces, inspect bounds, lifetime, units, ownership and ABI consumers, using supported sanitizers and compiler diagnostics where useful.

For a regression test, establish the original symptom and an assertion that detects it; observe the unfixed failure when practical using an isolated baseline or a safe temporary edit. Do not use destructive restoration commands on a dirty working tree. For a small copy or formatting edit, a visual/diff check can be sufficient.

Primary starting example: [Vercel React Best Practices](https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-best-practices/SKILL.md), reviewed 2026-10-31. Its priority-organized references motivated conditional loading. This Sui guide is independently written and does not redistribute its rule library or promise that each rule fits every project.
