# Detailed design and contract methods

Use this when a component/interface decision needs more precision than a short ADR.

## Views, safety and patterns

Choose a view by the question: runtime/deployment for fault/exposure boundaries, logical component view for responsibilities and data ownership, sequence view for time/order, data view for persistence/invariants. Label abstraction and assumptions; do not infer runtime isolation from two boxes in a logical diagram. Trace each significant view to requirement IDs and show the failure path. A safety review asks what happens if an assumption about timing, hardware range, operator action or duplicate software fails, including common-mode redundant failures.

For pipes/filters, define each stage's input/output contract, buffering/backpressure, error policy and whether partial output is valid. For OO, group state with the invariants and operations that own it; inheritance is not mandatory. For events, define producer/consumer ownership, schema evolution, duplicates/order/replay and idempotency. For a blackboard, define the shared fact representation, solver activation/conflict resolution, convergence/termination and visibility; avoid concurrent uncontrolled writes. For layers, state allowed dependency direction and exceptions rather than assuming every request must pass every layer. For client/server, specify authority, network failure, load and trust boundaries. For MVC separate state/domain decisions, view rendering and interaction orchestration; avoid moving business invariants into UI handlers.

Use a zipper-style alternation of top-down quality constraints and bottom-up implementation evidence when neither abstract design nor code inspection alone settles the decision. Preserve interface decisions in an ADR; revise them when the spike refutes an assumption. For microservice migration compare a modular monolith, service extraction and strangler routes; isolate old/new semantics behind an anticorruption translation with explicit ownership, consistency and rollback. Do not create a distributed boundary without a change-pressure/failure/ownership reason.

## Cohesion and coupling diagnosis

Cohesion categories are diagnostics within a module: coincidental (unrelated work), logical (similar-kind operations selected by a flag), temporal (work grouped because it happens at one time), procedural (same sequence without shared data purpose), communicational (shared data), sequential (output feeds next step), functional (one defined responsibility). Higher functional focus is often useful; don't split a coherent initialization/lifecycle operation solely to improve a label.

Coupling categories inspect the actual cross-module contract: content reaches into private internals; common shares mutable global state; external shares an imposed device/protocol/file convention; control passes flags that dictate another module's choices; stamp passes a large aggregate when only a field is needed; data passes needed values through a clear interface. Ask what change propagates, what invariant becomes unowned and what narrow contract would reduce that propagation. The source's isolated low-cohesion/intercomponent wording is inconsistent; do not repeat it as a definition.

Worked refactor: `process(order, mode='refund')` mixes purchase/refund policies and passes a whole user record for one account ID. First write invariant tests. Expose `refund(order_id, account_id)` with explicit errors and preserve the externally supported API through a temporary adapter. The aim is independently understandable behavior, not more files or fewer parameters at any cost.

## UML component notation

Draw named components/subsystems at one abstraction level. A provided interface is the service offered; a required interface is the service needed. A port marks a component interaction point; an assembly connector joins compatible required/provided interfaces, while a delegation connector routes an external port to an internal part. A dashed dependency arrow points from dependent client to supplier; it does not imply runtime data flow or inheritance. State where interfaces are in-process versus remote. Check that every dependency resolves, interface direction matches the real caller and no diagram-only subsystem ownership is invented.

Example: web UI requires DraftAPI; DraftService provides DraftAPI and requires DraftStore; LocalStore provides DraftStore. Show the storage trust/transaction boundary separately from these logical interfaces. Trace DraftAPI to the restore requirement and its contract tests.

## UML sequence notation

Use participants/lifelines with time progressing downward. A synchronous call waits for a return; an asynchronous message needs explicit later completion/correlation. Number messages only if they help match the contract. Use `alt` with exhaustive guards for success/denial/failure, `opt` for a conditional segment, `loop` with a bound and `par` only when interleaving is intended. Creation/destruction and activation must agree with lifetime. Don't draw a return before the operation that establishes its postcondition.

For atomic save: UI calls service, service validates authorization/version, store commits content+revision, service acknowledges revision, UI shows saved. Add an `alt` for version conflict and storage failure; an acknowledgement before commit would contradict the persistence requirement. Verify the diagram with an integration test that interrupts the write and reopens the store.

## APIs, IPC and ABI checks

Document request/response schemas, meaning/units, authorization, validation, error statuses, idempotency, timeouts, retry ownership, pagination and evolution. Use OpenAPI/Swagger for applicable HTTP contracts and version-specific Protocol Buffers/gRPC definitions for RPC, including unknown/default-field and mixed-client behavior. Generate only with the installed toolchain's reviewed options, then run producer/consumer fixtures and breaking-change checks. A generated client compiling does not prove business compatibility.

For a C library/POSIX boundary, specify ownership, pointer/size relations, return value/errno semantics, partial reads/writes, interruptions, thread-safety and cleanup. For IPC, specify framing, blocking/backpressure, endpoint permissions and crash/disconnect behavior. For async APIs state when success means accepted versus completed, correlation ID, cancellation and late-result handling; don't retry a non-idempotent operation after an ambiguous timeout without reconciliation.

For ABI changes test old compiled consumer/new library and, if promised, new consumer/old library. Inspect exported symbols, calling conventions, data layout/alignment, runtime/toolchain and platform. For API changes compile/type-check representative source consumers. Use an explicit deprecation window and migration path; SemVer signals intent, not a proof of compatibility. Structured analysis/DFD and historical OO methods can be used as contextual alternatives when the project already uses them; avoid imposing a second modeling system.

## Error contracts and observability

Maintain a small error registry with stable code, trigger, severity, retryability, caller action, public-safe message, internal context and owner. Distinguish validation, authentication/authorization, conflict, transient dependency, timeout and invariant failures. Preserve causal context at boundaries; translate only where responsibility changes. Roll back partial effects before claiming failure, or expose recoverable partial completion explicitly.

Example `DRAFT_CONFLICT`: two saves use the same prior revision; return conflict plus safe current-revision context; do not retry blindly or overwrite. `STORE_UNAVAILABLE`: bounded retry belongs to one layer with a deadline; surface unsaved state if exhausted. `CORRUPT_RECORD`: quarantine/recovery path, not an empty draft that silently destroys evidence.

Log structured event name, stable error code, severity, service/version, safe operation ID and request/trace correlation. Propagate correlation through queue messages with bounds; do not trust arbitrary user-provided strings as identity. Keep tokens/content/PII out of logs and metrics labels. Test that one injected dependency error produces a useful correlated event without exposing input secrets; define log retention/access and an alert owner where relevant.
