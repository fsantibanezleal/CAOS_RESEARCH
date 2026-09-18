# 09 - Manuscripts and publication (binding for every problem)

Adopted 2026-07-24 (Felipe's directive). Results that survive validation MUST
be persisted as manuscripts and published; memory and wiki alone are not the
record of a closed block.

## When a manuscript is created or expanded (the trigger rule)

As soon as a problem accumulates ENOUGH MATERIAL: machine-validated results
plus at least one item that is NOVEL (a new theorem, certificate family,
counterexample, witness, method, or a completed honest campaign including its
refutations), the session MUST create the problem's manuscript, or expand the
existing one, or SPLIT into several (foundational / campaign / consequences,
as the jacobian record did) when one paper stops being coherent. Expansion is
continuous: each closed block of results lands as a chapter/section in the
SAME round it closes, transcribed FROM THE VERDICTS AND DOSSIERS, never from
memory (wiki 04/05 and experiment verdicts are the sources).

## Where and how

- LaTeX under manuscripts/<problem>/<paper>/ (main.tex + built main.pdf
  committed; two-pass pdflatex; MiKTeX).
- Author block: Felipe Santibanez-Leal with \orcidlink{0000-0002-0150-3246}
  (usepackage orcidlink after hyperref) + the CAOS Research program line.
- Claim-status labels in-text: machine-verified [MV], derived [D], conjectural
  [C]. Refuted predictions, counterexamples and negative results stay in the
  paper, written AS RESULTS (a remark with its counterexample), never as the
  story of an earlier claim being withdrawn.
- Page-1 header block and version macros (\docversion, \docdate, \versiondoi,
  \conceptdoi): _CAOS_MANAGE/conventions/manuscript-header-standard.md. The
  version bumps with each substantive expansion.

## Scientific voice (binding, adopted 2026-09-17 on Felipe's directive)

A manuscript describes the problem, the method, the experiments or
computations, the results, their limits and the conclusions. Its body never
talks about the document itself (its versions, "this version", "an earlier
version stated"), about its Zenodo deposit or DOIs (those live only in the
page-1 header block), or about the working vocabulary of this programme
(campaign, verdict, ledger, dossier, declared hypotheses, smoke run or gate,
session, adversarial audit of our own work, "honest"). Experiment identifiers
may be cited as archived computations ("computation EXP-118"). Rules and the
replacement table: _CAOS_MANAGE/conventions/manuscript-scientific-voice.md.
Gate, run before every build that will be deposited and enforced in CI:
`python scripts/check_manuscript_voice.py manuscripts/<problem>/<paper>`.

## Zenodo publication (the upload rule)

- Every manuscript is PUBLISHED on Zenodo as a preprint (CC-BY 4.0) once its
  first coherent version exists: deposit metadata persisted as zenodo.json
  next to main.tex AND mirrored in _CAOS_MANAGE/manuscripts/<problem>/<paper>/
  (metadata.md with DOIs, version history, next-version trigger).
- Upload via the vault tooling (_CAOS_MANAGE/tools/zenodo/, token in
  credentials/providers/zenodo/): a new version goes through
  publish_revision.py (voice gate, DOI reserved first, the PDF prints its
  own DOI, live checksum verified); publishing is
  AUTHORIZED to run autonomously (Felipe reviews after publication and
  requests changes as further versions). Record id + DOIs go into the
  metadata.md the same session.

## The update strategy (versions, never edits)

- Published files are FROZEN: every change ships as a Zenodo NEW VERSION
  (actions/newversion via API: replace the PDF, bump metadata version,
  publish). The concept DOI always resolves to the latest; per-version DOIs
  cite frozen states.
- Web/app links use the CONCEPT DOI; papers cite version DOIs.
- A claim UPGRADE (scope strengthening) always means a new version whose
  VERSION NOTES on the Zenodo record (and the vault metadata.md) name the
  upgrade and the experiments behind it; a RETRACTION or correction likewise
  ships as a new version labeled in its version notes, never a silent swap.
  The PDF body states the corrected science directly and does not narrate
  the change.
- Trigger inventory per paper lives in the mirror metadata.md
  (next-version trigger line): keep it current.
