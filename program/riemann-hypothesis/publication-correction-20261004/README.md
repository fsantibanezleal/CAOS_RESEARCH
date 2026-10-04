# Manuscript publication separation: incident and correction

The session incorrectly placed supporting research archives in manuscript
Zenodo records, then bound that mixed structure into receipts and app gates.
This violated the user's manuscript-only publication workflow. A correct
hash was insufficient evidence of correct publication packaging.

The full authenticated account audit inspected 271 entries and 270 published
records across all historical versions. Of 245 manuscript publications, 242
contained only their PDFs and three contained four additional ZIP archives.
The other 25 records were separately classified software releases.

Corrected records and evidence companions:

| Manuscript record | Separate evidence record | Relocated archives |
|---|---|---|
| Levinson v0.02, 10.5281/zenodo.23132248 | 10.5281/zenodo.23135349 | One 80-member source ZIP |
| Levinson v0.03, 10.5281/zenodo.23134787 | 10.5281/zenodo.23135354 | One 85-member source ZIP |
| Distinct-zero Gram v0.01, 10.5281/zenodo.23128663 | 10.5281/zenodo.23135359 | 233-member runtime and 61-member mathematical-source ZIPs |

Each existing manuscript DOI, PDF, title, author and scientific version is
preserved. Public downloads match the original PDF receipts and the relocated
archive bytes. Each manuscript links its evidence companion; every companion
links its specific manuscript version. Only ZIP placement and related metadata
were corrected through Zenodo's supported owner grace-period process.

The after-audit reconciles all 274 entries, including 273 published records and one
untouched unpublished entry. All 245 manuscript records now contain only their
PDFs. All 267 unrelated existing publications retain their complete metadata,
file sets and DOIs. All four former manuscript ZIP endpoints return 404, while
the separate companion downloads match the original bytes. The audit verifies
file placement and preservation; it does not re-prove every scientific theorem.

Original mixed-deposit publication receipts remain historical evidence.
Current-publication.json is the manuscript-only view; evidence-companion.json
is the separate artifact publication. Packaging-correction.json records the
correction. The manifest binds all three views for each affected manuscript.

Riemann research and the proposed 0.77.000 app release were paused at the user's
request. No owned mathematical experiment process was active. EXP-023 remains
stopped and incomplete; its sources and poststop preservation archive remain
untouched. The unfinished app changes are preserved on
work/riemann-hypothesis/paused-app-20261004 at dcb213bb, pushed as WIP, with no
promotion or deployment claim. Research PR #376 remains a draft.

Publication admission and app links now accept manuscript-only records plus
separate evidence, with focused corruption checks and a comparison preserving
the delivered app's scientific payload. Local rendered verification passed all
20 scenarios, 120 tab visits and 1,760 screenshot byte checks. The 16 focused
manuscript/evidence link views were also manually inspected; the full screenshot
matrix was checked automatically. Receipts and screenshot manifests are stored
alongside this record. The private correction mirror is pushed to develop.

Remaining repair gates: promote only the repair and verify the production
deployment and its links. This work does not authorize resuming research or
promoting the paused result.
