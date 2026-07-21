# 01 - Problem lifecycle

`proposed -> scoped -> opened -> exploring -> consolidating -> published -> dormant | closed`

| State | Meaning | Entry gate (artifacts that must exist) |
|---|---|---|
| `proposed` | Listed in the portfolio with a one-paragraph pitch. | A row in `program/portfolio.yaml`. |
| `scoped` | Has a problem sheet: statement, verified status, feasibility class (A/B/C), GPU relevance. | Scoping sheet in the portfolio dossier or `program/<slug>/`. |
| `opened` | Full deep-research pass done; strategy chosen. | `problems/.../context/` dossiers persisted; `program/<slug>/plan.md` + `state.md` + `backlog.md` written. |
| `exploring` | Experiments running. | At least EXP-001 with hypothesis + verdict. |
| `consolidating` | Findings validated; exposition being written. | Adversarial-validation records for every claim headed to the wiki. |
| `published` | Surfaced on the web app. | Wiki complete, SVGs authored, web page screenshot-verified, `06-web-publication.md` checklist green. |
| `dormant` / `closed` | Parked honestly, or finished with a verdict. | A dated state note explaining why, and what would reopen it. |

Rules.

- A problem cannot advance a state without the gate artifacts; the transition is logged in
  `program/<slug>/state.md` and in the problem's `history/`.
- One problem is brought to `published` before the next is `opened` (the one-product-at-a-time
  rule). `scoped` sheets for future problems are always allowed.
- Feasibility classes: A = real experimental surface (search/verification/statistics can move
  understanding); B = meaningful verification or visualization surface; C = mainly expository.
