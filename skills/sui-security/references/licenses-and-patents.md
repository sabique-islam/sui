# OSS rights, licensing and patents

This resource supplies a fact-gathering workflow; live rights decisions require the exact current text, facts and applicable jurisdiction.

## Distinguish rights and source visibility

Copyright concerns protected expression; a license grants specified permissions under conditions; public domain status is not established by absence of a notice; a trademark concerns source/brand identifiers; patents concern particular claims under a jurisdiction and are separate from permission to copy code. An EULA is a contractual/license document, not a synonym for all proprietary rights. Source-visible code without an applicable grant is not automatically open source. Record artifact/version, origin, rightsholder, exact terms and intended use/distribution before reuse.

For choosing a license identify ownership/contributor rights, desired use and modification/distribution permissions, patent concerns, dependency compatibility and business/contributor model. Use the exact established license/version rather than custom wording or popularity rankings. For incoming contributions inspect CONTRIBUTING, developer certificate/CLA if any, inbound/outbound terms and whether copyright is assigned or a license is granted; those are different transactions.

## Family-specific review

MIT/BSD/Apache are families/versions, not a blanket “no obligations” category. For a release inventory applicable copyright/license notices and required acknowledgements from exact terms. Check the BSD variant rather than assuming its clauses. For Apache2.0 review distribution/modified-file/NOTICE conditions and its patent grant/termination and trademark boundaries in the primary text: https://www.apache.org/licenses/LICENSE-2.0 . Preserve source attribution and test the packaged notices, not only the source repository.

For GPL/LGPL/classpath exceptions record exact version/exception, modified component, linking/separation, distribution and network/deployment facts. Do not decide from slogans that all dependencies infect all code or dynamic linking is always exempt. Inspect source availability, corresponding-source/relinking and notice obligations against the actual terms; uncertain combinations need human review. Primary entry points: https://www.gnu.org/licenses/ and https://www.gnu.org/licenses/gpl-faq.html . A failed retrieval must be labelled unavailable, not silently replaced with recollection.

For CC-licensed media/docs/data verify exact version and rights beyond the license. BY needs the stated attribution conditions; BY-SA adds share-alike conditions for relevant adaptations; BY-ND restricts sharing adapted material under its terms. A cropped/translated illustration may raise an adaptation question and third-party likeness/mark rights may remain. Use https://creativecommons.org/cc-licenses/ and the actual legal code; do not treat software-package license detection as clearance for images/datasets.

Dual licensing offers alternative grants subject to their terms; it is not equivalent to an AND expression requiring both. For a compatibility decision draw the direction of inclusion/distribution, exact components/versions and inbound/outbound rights. Record alternatives and uncertainty. A CLA can grant contribution rights without automatically transferring copyright. Historical OpenOffice/LibreOffice/MySQL anecdotes are context, not evidence that a current commercial grant or combination is permissible.

## Inventory and review automation

Run the project's native license/SBOM tool against the actual release artifact plus manifests/lockfiles and preserve component identity, version, dependency relation, detected versus concluded license and unknowns. Use `scripts/sbom_inventory.py BOM.json --policy POLICY.json` for bounded supported inventory and simple allow/deny/review decisions. Unknown, compound, dual-license and exception expressions stay review items; no boolean output is legal compliance. Test transitive and unknown components, missing report, duplicate identity and malformed format; inspect the packaged notice bundle and any source-offer/relinking deliverable separately.

## Patent fact gathering and defense options

Record inventor/ownership, disclosure/filing dates, jurisdiction, actual claims, relevant implementation/prior art and intended act. Novelty, usefulness and non-obviousness/inventive step are legal tests, not a model's novelty score. A patent can grant exclusion rather than an affirmative right to practice every part of a product. Independent invention and copyright permission do not automatically settle a patent claim. Verify the relevant office/statutes/cases for a live decision rather than applying one jurisdiction's historical case discussion globally.

Compare these mechanisms only for the actual problem: Defensive Patent License is a licensing framework (https://defensivepatentlicense.org/); OIN is a network/license context (https://openinventionnetwork.com/); LOT is a transfer/troll-risk program (https://lotnet.com/); patent/prior-art bounties seek evidence about particular claims; Unified Patents offers patent-related challenge/defense services (https://www.unifiedpatents.com/). Check current membership, covered rights, exclusions, costs and obligations directly before selection. No membership or checklist guarantees defense or freedom to operate.
