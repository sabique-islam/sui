# Build, CI, release and supply chain

Use actual project commands and targets.

## Build graph and reproducibility

Map source/resources/generated files, dependencies and output artifacts in the native build system. Distinguish its DAG from Sui's task-order helper. Use the tool's graph/dry-run inspection only after reviewing code-execution implications, then test that a changed source/header/config causes required rebuilds and an unchanged input avoids unnecessary work. Declare generated prerequisites, compiler/options and external dependencies; incomplete cache keys can produce a green stale artifact.

Capture source revision plus dirty patch where applicable, lockfile, toolchain/runtime, relevant environment/config and base-image/dependency identities. Prefer one documented build entry point and outputs from that build. Check a clean build in an isolated environment, a dependency change, a missing input and a cache-disabled comparison where risk warrants it. Do not implement a second build system merely to produce a diagram.

## CI policy and platform integration

Order fast syntax/type/lint/static checks, meaningful unit/contract/integration suites, packaging, supply-chain checks and target smoke tests by cost and dependencies. Keep triggers, branch/event trust, credentials, action versions, concurrency/cancellation, cache inputs, output retention and failure policy explicit. Do not expose secrets or writable tokens to untrusted PR code. Static success, test success, artifact creation and deployment are separate observations.

For GitHub Actions inspect repository/event permissions and existing workflows; use immutable reviewed action revisions, read-only default contents permission and narrowly scoped job elevation. Verify hosted run identity, selected revision, actual collected checks and produced artifact, not just a workflow file. For Jira inspect project issue types, field IDs, statuses/transitions and issue/sprint permissions through the available connector; map requirement/acceptance/bug/release IDs, preserve existing custom fields and verify resulting state after an authorized change. For GitHub–Jira linkage confirm actual issue/PR association in the target project. Do not create account credentials, send messages or change external issues solely because this template mentions an integration.

For Docker build only when the project needs it. Resolve a supported base image to a verified digest/platform, install from an appropriate lockfile, separate build-only dependencies, exclude secrets/context junk, run as a constrained nonroot user where supported, keep config external and exercise readiness/shutdown. Inspect image/artifact provenance and scan the built image. No Docker daemon or platform account is assumed by the pack.

## Supply-chain inventory and checks

Generate inventory from the actual release artifact and compare with manifest/lockfile expectations. Syft can generate CycloneDX/SPDX; Trivy can produce or scan supported SBOMs and needs an appropriate vulnerability database; Dependency-Check performs SCA with supported report formats including SARIF, not a universal legal clearance. GitHub native SBOM export and Actions generation depend on repository features/permissions and selected scope. Reconcile missing/transitive/optional/bundled components and tool exclusions.

Use Sui Security's `sbom_inventory.py` for explicit supported SPDX2.3/CycloneDX1.5–1.7/SWID2015 subsets. Validate the original against its official versioned schema before claiming schema conformance; the local normalizer explicitly does not provide full conformance. Preserve original report, source/artifact identity, generator/version/options, hash, timestamps, dependency graph and license unknowns. Identity diff is not automatically an upgrade decision. Scan advisories against actual installed versions/reachability, triage false positives and record owner/fix/accepted risk.

SPDX, CycloneDX and SWID are different inventory standards, not interchangeable tools. Do not silently parse SPDX3 with a2.3 adapter or flatten nested CycloneDX components without marking loss. Do not turn absent vulnerabilities, unknown licenses or a failed database download into a clean report.

## Release, install and recover

Define audience/population, target version/config, duration, comparison signal, smoke journey, owner, stop/rollback trigger and support path. Test the actual rollback/restore assumption in a disposable environment. A database migration may need roll-forward plus restore rather than an inverse script; preserve mixed-version compatibility and bounded backfills. Configuration/feature flags require the same review and provenance as code.

For installation/bootstrapper tooling identify target OS/permissions/prerequisites, file/service/registry/config changes, data location, upgrade/repair/rollback and retained/deleted-data policy. Validate clean install, supported upgrade, permission failure, interruption and uninstall on disposable targets. DeployMaster, InstallShield, InstallAware and WiseInstaller are historical Windows installer products; verify exact edition/version/support and project-native build/export procedures before using them. Do not replace a supported installer merely to add another product name.

After an authorized release verify running version, user-visible behavior and relevant signals. Record blocked environments/accounts distinctly from failed checks. Sui's gate provides endpoint content equality for declared files and local process records, not immutable execution, signed provenance or deployment success.

Official starting points: https://github.com/anchore/syft ; https://trivy.dev/docs/latest/supply-chain/sbom/ ; https://dependency-check.github.io/DependencyCheck/dependency-check-cli/arguments.html ; https://cyclonedx.org/specification/overview/ ; https://spdx.github.io/spdx-spec/v2.3/ ; https://csrc.nist.gov/projects/Software-Identification-SWID . Inspect the deployed version before copying commands.
