# 05 - Writing standards

- **Language:** English only across the repo (code, docs, wiki, manuscript). The web app carries
  EN/ES i18n strings as the only exception.
- **Style:** no em-dash, no emoji (ADR-0067; CI-enforced). Use comma/colon/semicolon/parentheses.
- **Equations:** KaTeX-compatible LaTeX in Markdown (`$...$` / `$$...$$`); the manuscript uses real
  LaTeX. Every displayed equation is either derived in-place or cited.
- **References:** primary sources with DOI/arXiv/official URL, inline at the point of use; a
  problem-level bibliography lives in `context/references.md`. Claims without a primary source are
  flagged UNVERIFIED and cannot support conclusions.
- **Diagrams:** hand-authored, theme-aware SVGs in `wiki/assets/` (light/dark friendly palette per
  the CAOS visual standards); never screenshots of external figures.
- **Wiki tree per problem:** `wiki/README.md` landing + numbered deep pages (statement and
  history; known-results ladder; mechanism/our analysis; experiments and results; open questions).
  Written VERTICALLY: when a unit (an experiment, a mechanism, a case) is finished, its wiki
  content is transcribed from the context dossier + verdicts in the same working session, never
  reconstructed later from memory.
- **History log:** `history/log.md`, append-only, dated entries; every entry links the experiments
  and decisions of that day. The log records dead ends explicitly.
- **Manuscript:** `manuscript/` LaTeX; findings enter the manuscript only after adversarial
  validation; the manuscript distinguishes clearly between (a) reproduced/validated external
  results, (b) our verified results, (c) our conjectures.
