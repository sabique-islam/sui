# Pinned offline schema validation

Use `scripts/schema_check.py INPUT --manifest CACHE.json` before claiming full conformance to an exact official JSON/XSD schema. The inventory normalizer is a different, deliberately bounded operation.

Retrieve the official versioned schema and its required references through the task's research tools. Review provenance/license and record each original URL, content hash and canonical schema URI. Cache only required files in one directory; never execute downloaded content. A manifest has `type` (`json` or `xsd`), `root` (one cached relative path) and `files` records with `path`, absolute canonical `uri` and lowercase SHA256. No implicit network retrieval is allowed. A missing reference, changed hash, unsupported dialect or missing library blocks validation.

For JSON install a version-pinned jsonschema/referencing combination in the project/maintenance environment. Supported dialects are Draft7 and2020-12; a cached resource without its own dialect uses the root dialect. Every cached schema is schema-checked. The manifest retrieval URI supplies the relative-reference base, including a bare Draft7 `$ref` root. Non-JSON numeric constants and duplicate properties are rejected. For XSD use a supported lxml build; includes/imports must resolve to explicitly cached URIs and input entities/DTDs are rejected. Error reports retain paths/keywords or line/type, without echoing document values.

The pack's local native trial generated a real Syft CycloneDX1.6 BOM, validated against the official bom/SPDX-license/JSF schemas, and rejected a controlled invalid BOM. That does not imply future SPDX3 or other schema/dialect support, official SWID conformance for an unprovided schema, authenticity, inventory completeness, vulnerability absence or legal clearance. For a live target match generator, schema, input artifact and applicable policy versions before release.

Use `scripts/sbom_inventory.py` afterwards for supported component/dependency/license normalization and review. Preserve the original report and schema manifest. Unknown licenses and compound expressions remain human review items.
