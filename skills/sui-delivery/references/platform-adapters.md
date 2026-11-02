# Platform and historical tool adaptation

Use this alongside build-release and Sui's tool catalog when the repository actually uses a named platform. A procedure is not a fixture-tested parser or a verified account connection. Current official version documentation and a target-specific trial are required before a live integration claim.

## Adapter contract

Record product/edition/version, owner/authorized target, required connector or executable, config/input/build scope, secrets/permissions, preview/read-only path, bounded run, output schema/exit semantics, collection/completeness checks and recovery. Preserve raw sanitized report fixtures for clean/finding/malformed/failed/incomplete outcomes and normalize only an explicitly supported schema. Run missing-tool/auth failure, empty scope, timeout and unsupported-version cases. Never substitute a plausible generic command or invented output field for a documented product interface.

Prefer the available service connector for GitHub/Jira/project APIs; inspect actual capabilities and fields before adapting, then verify the resulting authorized state. For a CLI/build system use the native project command through Sui Delivery's bounded gate and an appropriate supplied-report parser. For an unsupported proprietary/legacy export, obtain its actual schema/sample first and keep support marked procedure-only until validated. This pack cannot instantiate accounts or prove a target integration without that target.

## Infrastructure and configuration

Cobbler, Foreman and Crowbar are historical provisioning and infrastructure examples. Identify inventory, OS/image/provider, boot/discovery assumptions, credentials and desired state; inspect a plan/diff on an isolated target, provision a disposable node, validate its declared configuration and test removal/recovery. Do not apply a downloaded provisioning template to a real environment as a discovery step.

Puppet, SaltStack and Chef require their actual manifests/states/recipes, dependency/version policy and target inventory. Compile/lint/test the supported configuration; use the version's documented no-change/plan mode; then converge an isolated target and test idempotency, drift and failure/rollback. A successful controller invocation without inspecting node outcomes is incomplete evidence. Use official product docs and the installed release, not a universal command with guessed flags.

## CI, build and deployment

Jenkins/Hudson: inspect the actual controller/agent versions, pipeline/job definition, plugins, credentials, trust of branch/PR code and artifact retention. Build the intended revision on a disposable agent, verify stage/check/report identities and exercise an expected failure. Ant/Maven/Make/CruiseControl/FinalBuilder are build/integration examples with different graph/config/plugin semantics; inspect actual build files and generated artifacts, dependency changes and clean/incremental behavior.

Capistrano/custom deployment tooling: inspect target inventory, SSH/secret scope, release-directory/state conventions, health checks and rollback constraints; stage a bounded release and verify actual running version plus recovery. Yum is a package-management example; Deb/RPM identify package ecosystems/formats, not interchangeable deployment APIs. Validate package dependency/architecture/signature/script/config/data behavior in a disposable supported OS. Do not silently classify Git/SVN/Perforce as CI engines merely because the source table groups them under CI.

Nagios, Sensu and Zabbix: identify actual agents/checks, metric units/window, auth, alert routing and ownership. Inject a benign bounded lab failure, verify it is observed and routed, restore and verify recovery/clear behavior. A dashboard render does not establish a useful alert. Avoid secret/high-cardinality/personal labels and unowned threshold noise.

## Version control, virtualization and installers

Git, RCS, CVS, Subversion/SVN, ClearCase, Perforce and AccuRev require product-native branch/baseline/merge/recovery behavior. Read-only history/status inspection and preservation of dirty work come first. GitHub adds hosting/review/issue/CI APIs; it does not make every local Git operation a verified account integration.

“Vcentre” and Hyper-V require an exact product identity, hypervisor/guest versions, host resources, networking/storage and privilege scope. Confirm an isolated VM lifecycle, snapshot/restore semantics and removal policy before any real host mutation. A VM snapshot is not automatically an application-consistent backup.

DeployMaster, InstallShield, InstallAware and WiseInstaller require the actual supported edition/OS/license/project, prerequisite/bootstrapper and signing/build chain. Inspect generated package contents and validate install/upgrade/repair/uninstall in disposable profiles/VMs. Bugzilla, FogBugz, Trac/Edgewall and Backlog require actual issue types/fields/transitions, duplicate/reopen rules and release links; use connector/API readback to verify any authorized change. Do not send external issue updates without the user's task authorization.

## Stop unsupported identity inference

IDE examples (Visual Studio, IntelliJ IDEA, PyCharm, Xcode, Eclipse) select a development environment and supported plugin/runtime; they are not five independent static analyzers. Vendor logos and historical names need an exact product/version before an adapter. The catalog preserves source names and support tiers, including ambiguous logos or package labels. If a primary source is unavailable, record the uncertainty, continue other authorized local work and avoid inventing a result.
