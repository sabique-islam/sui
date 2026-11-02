# Privacy threat analysis and controls

Primary taxonomy: https://linddun.org/threat-types/. Use data-flow-specific analysis, not a privacy score.

## Data map and fair information practice

Inventory collected/provided/inferred data, subject, purpose, lawful/contractual basis when applicable, source, transformations, recipients, stores/backups, retention, access and deletion. Identify what can be omitted. Pseudonyms remain linkable in context; deidentification/anonymization claims need a threat model and evidence, not a renamed ID column. Encryption at rest does not prevent excessive authorized collection.

Map notice/awareness to comprehensible purpose and recipient disclosure; choice/consent to meaningful controls where appropriate; access/participation to inspect/correct/delete paths; integrity/security to accuracy, restricted access and protected transfer; enforcement to ownership, audit and complaint/remedy. Test the actual control and derived/backed-up data lifecycle, not just the existence of a policy page. Fair-information frameworks are design prompts; determine applicable jurisdiction, law/version and facts separately. Do not treat a historical label or typo as a live legal checklist.

## Seven LINDDUN prompts with a worked flow

Example flow: a student voluntarily submits an event RSVP, the event service stores it, organizers view an aggregate forecast. Identify assets/actors/boundaries and apply all seven categories to each relevant flow/store. Record threat, affected people, mitigation, verification, owner and accepted/not-applicable rationale.

Linking: a persistent identifier joins RSVPs across unrelated clubs. Use purpose-scoped identifiers and prevent unnecessary joins; verify organizer exports cannot correlate unrelated events through hidden IDs. Identifying: a tiny “anonymous” group reveals a person. Limit granular output or use an appropriate aggregation strategy; test small-group and auxiliary-data inference rather than promising a universal anonymity threshold.

Non-repudiation: permanent attributable logs expose a student's past participation. Minimize identifiable audit history to the justified purpose and access window; verify ordinary organizers cannot retrieve expired individual history. Detecting: a presence/absence API reveals whether a student is involved. Avoid unnecessary membership endpoints and distinguish authorization/rate controls from the residual inference; test denied queries and response differences.

Data disclosure: raw RSVPs leak through analytics, logs or backups. Minimize fields, restrict access and encrypt/transmit with a supported channel; test log redaction, cross-role denial and export retention/deletion. Unawareness/unintervenability: students cannot understand or change participation/use. Provide intelligible notice and relevant access/correction/withdrawal controls; test with an actual user task and verify downstream state updates.

Non-compliance: retention/purpose promises or applicable controls are violated by an unowned export. Map each verified requirement to an owner/control/test, include processors/backups and audit the lifecycle; document unresolved obligations rather than claim compliance. LINDDUN categories can overlap. An analysis row marked not applicable needs evidence about the flow, not merely “low risk.”

## Privacy by design and validation

Prefer minimization/default-limited collection, access separation, purpose limits, bounded retention and transparent intervention from design onward. Review telemetry/model features and external services as data recipients. Validate normal, denied, correction, deletion, export and failure/retry paths, including backups and derived features as promised. Track residual reidentification/linking risks and revisit when new data or users change the threat model.
