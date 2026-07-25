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
- **Manuscript:** `manuscripts/<problem>/<slug>/` LaTeX; findings enter the manuscript only
  after adversarial validation; the manuscript distinguishes clearly between (a)
  reproduced/validated external results, (b) our verified results, (c) our conjectures.

## Manuscript front-matter standard (binding; a reader must never have to guess what the document is)

Adopted 2026-07-24 after an audit found two manuscripts shipping without any
document-type marking. Every manuscript in `manuscripts/` carries ALL of:

1. **A running header naming the document type**, on every page after the first:
   `\usepackage{fancyhdr}` with `\fancyhead[L]{\small CAOS Research <TYPE>}` and
   `\fancyhead[R]{\small <Short title> \textperiodcentered\ v<X.YY>}`.
   `<TYPE>` is one of **Preprint** (a full record intended for a DOI), **Technical
   Report** (an instrument or dataset description), or **Note** (a short focused
   record). The type must match the Zenodo `publication_type` of its deposit.
2. **A document-type statement on page 1**, boxed under the title, stating the type,
   that it is not peer reviewed, and, when the work is replication-first, whose
   results are being replicated versus what is ours.
3. **Author line with ORCID**: `\usepackage{orcidlink}` and
   `\author{Felipe Santiba\~nez-Leal\,\orcidlink{0000-0002-0150-3246}\\ \small CAOS
   Research program, \texttt{github.com/fsantibanezleal/CAOS\_RESEARCH}}`.
4. **Version in the date block**: `\date{YYYY-MM-DD\\[2pt]\normalsize Version X.YY}`,
   matching the version in the Zenodo deposit and in the vault metadata file.
5. **Navy colored links** (`linknavy`, `colorlinks=true`), never `hidelinks`.

Exemplar to copy: `manuscripts/jacobian-conjecture/foundational/main.tex` preamble.
The PDF is visually checked after every version bump (render page 1 and one
interior page) before the deposit is uploaded.

## MANUSCRIPT TITLE-PAGE STANDARD (adopted 2026-07-24)

Every manuscript must state its DOCUMENT TYPE and provenance on the rendered
page, not only in repository metadata. A reader holding the PDF alone must be
able to tell what it is, what version, and whether it has been refereed.

Required, in this order:
1. Title, author with `\orcidlink{...}`, and the programme affiliation line.
2. `\date{<YYYY-MM-DD>\[2pt]
ormalsize Version <X.YY>}`. The date field
   carries ONLY the date and the version. Do NOT bury the document type or a
   changelog sentence in it (both were done before this standard and read badly).
3. A boxed status banner immediately after `\maketitle`, centred, containing:
   - the DOCUMENT TYPE in bold (`PREPRINT`, or `TECHNICAL NOTE` / `REPORT` as
     applicable) followed by `not peer reviewed` when true;
   - the programme name and the paper's place in its series;
   - version and date;
   - the CONCEPT DOI as a hyperlink, labelled as resolving to the latest version;
   - the licence and the public source/record URL.
4. Running headers via `fancyhdr`: left `CAOS Research Preprint`, right
   `<short title> . v<version>`, page number centred in the footer; the title
   page uses the `plain` style (footer number only, no rule).

The document type must match the Zenodo `publication_type` of its deposit. If a
paper is published as a preprint, the page must say PREPRINT.

Rationale: a self-published record carries its own provenance. A PDF that omits
type, version, DOI and licence is indistinguishable from a draft once it leaves
the repository.
