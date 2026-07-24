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
- Honest labeling in-text: machine-verified [MV], derived [D], conjectural
  [C]; refuted predictions and retractions stay in the paper (they are part
  of the record and the method).
- Manuscript versions in the \date line (v0.0X) bump with each substantive
  expansion.

## Zenodo publication (the upload rule)

- Every manuscript is PUBLISHED on Zenodo as a preprint (CC-BY 4.0) once its
  first coherent version exists: deposit metadata persisted as zenodo.json
  next to main.tex AND mirrored in _CAOS_MANAGE/manuscripts/<problem>/<paper>/
  (metadata.md with DOIs, version history, next-version trigger).
- Upload via the vault tooling (_CAOS_MANAGE/tools/zenodo/, token in
  credentials/providers/zenodo/): create the deposit via API; publishing is
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
  changelog names the upgrade and the experiments behind it; a RETRACTION or
  correction likewise ships as a new version prominently labeled, never a
  silent swap.
- Trigger inventory per paper lives in the mirror metadata.md
  (next-version trigger line): keep it current.
