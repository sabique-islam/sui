# Test design and fault sensitivity

Prefer small examples with explicit oracles over a large unreasoned case list.

## Black-box techniques

Partition an input domain into classes expected to behave alike, including invalid/missing classes, then choose representatives. For a supported quantity1..100 test0,1,2,99,100,101 with relevant type/encoding cases. State which numeric and rounding rules the domain accepts. A boundary technique does not justify ignoring authorization or state.

For a decision table list conditions, allowed combinations and expected actions. Example save: authorized? current revision? storage available? Denied authorization must never write; stale revision must conflict; storage failure must not acknowledge; only the valid row commits. Eliminate impossible combinations with an explicit constraint, not by silently omitting them. For state transitions define states, events, guards, effects and forbidden transitions; test both allowed edges and attempts that should preserve state.

Use `scripts/test_design.py pairwise INPUT.json` for bounded independent factors such as OS/browser/role. Verify every factor pair appears. The helper rejects oversized spaces and does not support constraints; add explicit higher-order risk cases and a domain oracle. Pairwise coverage is not exhaustive testing.

## Experience and exploration

Use historical failures, domain invariants, common misuse and actual usage patterns for error guessing. Write an exploratory charter with mission, target, timebox, data/environment, risks and evidence to collect. During the session note actions, observations, questions and reproducible failures; debrief against the mission and convert consequential discoveries into deterministic regression checks. Distinguish exploration from repeatedly clicking without an objective. Usage-based tests need a representative operational profile; rare destructive actions can deserve more attention than their frequency suggests.

## Structural and data-flow testing

Construct a CFG with one node per meaningful block and edges for reachable control transfer, including short-circuit and loop behavior. State entry/exit/exception assumptions. Cyclomatic M=E−N+2P applies under the chosen component convention; identify feasible independent paths rather than claiming every algebraic path can execute. Use Sui Evidence's calculator for graph arithmetic, not automatic source parsing. Statement coverage measures executed statements; decision coverage measures outcomes; condition coverage measures evaluated atomic true/false values. An unevaluated short-circuited condition is not false.

Worked avgAbs example: guard is `numbers == null || numbers.length == 0`; then initialize sum, loop, subtract negative/add nonnegative and return mean. `null` takes the throw path without evaluating length. `[]` evaluates false/true and throws. `[-2,2]` evaluates false/false, takes both sign branches and both loop outcomes, returning2. Together these cover the listed statement/decision/atomic-condition outcomes for this finite-input example. They do not establish MC/DC or all paths. `scripts/test_design.py avg-abs INPUT.json` emits these observations with not-evaluated recorded as null.

For data flow identify definitions and computational/predicate uses of each variable, reaching definitions and def-clear paths (no intervening redefinition). All-defs seeks a reachable use for every definition; all-uses seeks each reachable definition/use obligation; all-du-paths seeks relevant def-clear paths, subject to loops/feasibility bounds. Example `x=0; if flag: x=1; return x`: test flagfalse for the first definition reaching return and flagtrue for the second; merely executing the assignment lines does not prove both reaching-use paths. Track infeasible obligations with a reason.

## Mutation and seeded faults

Mutation changes a small semantic element such as `>` to `>=`, removing an authorization check or changing an arithmetic operator. Run tests on one mutant at a time in isolation, with timeout/resource bounds. A killed mutant must fail due to a useful assertion, not a broken test harness. Investigate survivors as missing assertions, untested behavior or equivalent/unreachable changes; do not treat every survivor as a defect or optimize a score alone.

For fault seeding, keep a separate controlled copy, a seed inventory and bounded injection plan; blind detection participants when the experiment needs it and remove every seed before release. Count detected seeds separately from naturally found defects. Artificial seed detection rates do not establish the number or distribution of unknown real bugs. Never secretly seed faults into production or a shared branch.

## Framework and coverage adapters

For pytest inspect configuration/plugins and collection, run the relevant selection with `python -m pytest --junitxml=report.xml`, inspect collected/executed cases and return status, and normalize JUnit through Sui Implementation's `tool_checks.py parse`. Pytest's no-tests return is not a pass. `assets/python-lab` contains six meaningful pytest cases including a bounded Hypothesis roundtrip property. Record installed versions and invoke inside the project's environment.

For JUnit use the repository's actual Maven/Gradle/JUnit generation, select the target tests, inspect per-test XML and assert collection plus relevant behavior. Do not mix JUnit4/5/6 annotations or assume a universal plugin version. For GoogleTest use fixture lifetime and assertions appropriate to the code, list selected tests, run the test binary with its version's XML report option and inspect executed counts. The strict JUnit-subset parser accepts common GoogleTest reports; preserve runner-specific disabled/parameterized behavior and validate a saved representative output before relying on it.

For Python coverage run the actual tests under `python -m coverage run --branch -m pytest`, then `python -m coverage json -o coverage.json`. Bind source/tests/config plus the test run; parse statement/branch counts and inspect missing risky behavior. For GCC use instrumentation, execute the matching binary and consume `gcov --json-format` from the same build; do not pair stale `.gcda` with new source. For JaCoCo retain bytecode/source/debug-info identity and distinguish instruction/line/branch counters, including its exception-handling convention. Blaze is one organization's build infrastructure, not a required portable coverage tool. Aggregate counts before calculating a combined percentage, and report missing/no-data rather than100% for an empty denominator.

Official version checks: https://docs.pytest.org/en/stable/how-to/output.html ; https://hypothesis.readthedocs.io/en/latest/quickstart.html ; https://coverage.readthedocs.io/en/latest/commands/cmd_json.html ; https://google.github.io/googletest/advanced.html ; https://www.jacoco.org/jacoco/trunk/doc/counters.html ; https://gcc.gnu.org/onlinedocs/gcc/Gcov-Data-Files.html .
