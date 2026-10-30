# navier-stokes: history log

## 2026-09-11, opening round (research only)

- Problem opened. The portfolio row moved `proposed` to `scoped` to `opened` in one round, on the
  strength of the deep-research pass persisted the same day.
- First problem on disk in the `analysis-pde` area, which until now was an area name with no folder.
- Sources: the OpenAI Navier-Stokes and Euler manuscripts, the three Alpoge-Buckmaster papers,
  Buckmaster's priority statement, Fefferman's official Clay text, and eleven background references,
  all downloaded, hashed and recorded in `context/references.md`. Third-party PDFs are not
  redistributed here; the mirror is outside git.
- Lean statement audit of `openai/NavierStokesAndEuler` completed for alternatives (C) and (D):
  faithful, clause by clause, with the reference statement inherited from a third party. The unforced
  Euler certificate was NOT audited and is queued as NS-004.
- The Alpoge-Buckmaster modulation system transcribed exactly, with the growth rate settled by
  computing the matrix rather than by reading the mangled PDF extraction.
- Derived here: the dissipative extension of that system, the frequency cap, and an upper bound of
  1/4 on the cascade dissipation exponent.
- A stronger reading of that bound (a clean critical exponent) was refuted by our own smoke test
  inside the same session. The weaker surviving statement is recorded, together with the two known
  omissions that push the real threshold down. Preserved in `program/navier-stokes/state.md`.
- No experiment run. The plan is written and awaiting validation before any machine time.
- Commit `3f8d76d` carries the dossiers and the smoke test.

## 2026-10-30 - portfolio review: external status

External status: the Clay problem is open; the OpenAI forced blowup (2026-09-08) is unrefereed [V2]. New: Bastounis, Circelli, Hansen arXiv:2610.08144 (2026-10-06): the Lean proof does not correspond to the natural-language blowup proof [V, re-checked]. Our Lean audit checked the statements, which remains consistent with a proof-correspondence gap. No source states our class ceiling [U]; the nearest quantitative value is the hypodissipative threshold (22-8*sqrt(7))/9 of arXiv:2407.06776 [V2].
Plan change (assessment): one citation and scope revision (v0.09), the bounded comparison of that threshold with the class ceiling, then dormant. New rows NS-020 and NS-021.

Source: [portfolio review](../../../../program/portfolio-review-2026-10-30.md).
