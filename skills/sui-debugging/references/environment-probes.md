# Debugging by execution environment

Start with a minimal failure, then choose evidence available at the real boundary.

## Select a probe

For local source, build with a recorded toolchain and symbols; set a breakpoint or trace around the state transition and inspect actual values/lifetimes. For a local opaque binary, use its supported logs, exit/error contracts, symbols and OS-level observations; do not invent source-level visibility. For a remote service, correlate a bounded request across safe logs/metrics/traces and reproduce in a lab; attach a debugger only when the service scope and operational impact are authorized. For a browser, inspect network request/response, storage, console errors, event sequence and rendering performance using browser developer tools; distinguish cached client behavior from server behavior.

Record exact executable/source revision, config/environment, request/trace ID, capture window and the hypothesis the probe can distinguish. Configure the installed IDE's actual runtime/debug adapter rather than assuming a logo establishes integration. A missing symbol or optimized-out value is a probe limitation, not evidence the invariant held. Preserve minimal redacted findings in the codebase map; don't collect whole customer payloads.

## Memory, performance and races

For native memory errors use the supported compiler sanitizer build or Valgrind mode for the platform; retain build flags, failing input and stack context, reproduce after the fix and test cleanup/lifetime. For CPU/IO latency use a representative profile and separate warmup, queueing, locks and allocations before optimizing. For races define the competing actions, shared state, happens-before requirement and controlled interleaving; a thousand nonfailing repetitions are weaker than a test that forces the failing order.

For an unfamiliar system follow one representative request from entry through state ownership to output, then inspect error/recovery paths. Use source search, caller references, existing tests, runtime probes and history together. An example such as Redis teaches a method; it is not a required project dependency. Confirm source and running binary versions agree before trusting a diagnosis.
