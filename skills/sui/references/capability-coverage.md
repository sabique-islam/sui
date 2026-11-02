# Capability coverage and maintenance

Use the focused specialist's operational resources for the task. Do not load every tool guide into ordinary work.

## Evidence tiers

`assets/capability-baseline.json` preserves 121 method entries and 42 conditional integration entries. Topics overlap; these are not 163 independent defects. `assets/capability-coverage.json` maps every item to installed resources and its completion criterion. Run `scripts/check_coverage.py /path/to/personal-skills` for ID and file integrity. A structural pass is not semantic completeness or a verified project integration.

Method-ready means an actionable workflow, worked example or calculator was added. Report-adapter-tested means a specified bounded report subset has fixtures; it does not mean the vendor account/platform was exercised. Native-trial-passed means an actual local tool run on the recorded fixture. Procedure-ready means prerequisites, scope, steps and evidence requirements are documented, with live execution still requiring the actual target/tool/account. Mixed support retains the distinction within grouped source entries.

Read `assets/validation.json` and `assets/native-validation.json` for observed tests and limitations. Faulty native static fixtures are expected to produce findings. Planned product acceptance checks in a forward trial are not executed product tests. No production deployment, live network assessment, hosted CI run or authenticated vendor integration is inferred from local pack validation.

## Tool selection

Run `scripts/tool_catalog.py QUERY --limit 20`. The catalog preserves named tools, IDEs, standards, methods and historical examples separately through their kind/support/resource fields; a catalog entry is not automatically a runnable analyzer. Resolve actual skill directories by frontmatter name. Never install a guessed similarly named package or substitute vendor branding for a product.

Use project-native versions/configuration and primary documentation before configuration or consequential claims. Existing YC sources inform user/scope learning; a16z informs ecosystem perspectives. Neither overrides compiler/test behavior, security boundaries or current technical/legal primary sources. Refresh version-sensitive facts and record unavailable retrieval rather than inventing certainty.

## Reproduce and extend validation

Run `python -m unittest discover -s scripts/tests -q` from Sui for core helpers; install the pinned optional validation dependencies from `assets/validation-deps.txt` in an isolated maintenance environment for JSON-schema/XSD tests. Missing optional packages produce explicit skips in the test runner and blocked helper results; report skips rather than claiming the full extended suite passed. No dependency installation is automatic.

For native trials use each specialist's documented command and the actual project environment: clean/faulty mypy/TypeScript/compiler cases; the bundled pytest/Hypothesis lab under branch coverage; GoogleTest/JUnit example sources with their supported runtime; GCC/gcov on a matching instrumented build; Syft on a disposable dependency fixture; and official cached schema validation with valid/invalid controls. The seeded fuzz lab and load-probe demo run locally. Preserve versions, source/tool hashes, command/return code, scope and actual report. Do not count repeated/generated cases as independent engineering tasks.

Before saving a revision run the skill frontmatter validator on every changed installed skill, validate the complete pack/file inventory, check this ledger and inspect UI metadata and resource links. Independently exercise consequential changes on fresh tasks/artifacts with no hidden answer leakage. Keep helper tests separate from real-repository effectiveness evidence. Only then save and verify every skill update.
