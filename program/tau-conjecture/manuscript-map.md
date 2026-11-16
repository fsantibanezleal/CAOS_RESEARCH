# Shub-Smale tau conjecture: result and manuscript map

Updated 2026-11-16 (methodology 13 adopted at the strategic review that EXP-015 and census v0.07 trigger). This map
separates mathematical evidence, strategic value, manuscript coverage and external novelty. Experiment verdicts remain
the authority for results; the machine-readable record is `research-governance.json`.

## Status boundary

The tau conjecture (Shub and Smale 1995; Smale's fourth problem) is open, even for exponent 1: for a nonzero integer
polynomial f computed by a constant-free straight-line program of length tau(f), z(f) <= (1 + tau(f))^c for a universal
c, where z(f) counts distinct integer roots. It implies P != NP over the complex numbers in the Blum-Shub-Smale model and
VP^0 != VNP^0 (Buergisser 2009); the real-zeros analogue is false (`plan.md` section 1). The external status was checked
on 2026-10-30 and 2026-11-07: open, no tau-conjecture item on arXiv after 2019 (arXiv:1905.00091) bears on the census,
and no overlap with EXP-015 or census v0.06 was found (`problems/computation-complexity/tau-conjecture/history/log.md`).
The CAOS programme computes the exact growth function z_max(tau) = max{z(f) : tau(f) <= tau} for tau <= 9 and the cost
of k distinct integer roots; it does not claim to prove, refute or bound the conjecture, and no finite computation
decides it (`plan.md`, Non-claims). Markstroem's integer-target census (arXiv:1306.3091) is a different object and is
the external anchor the enumerator reproduces (EXP-001).

Internal exact validation and Zenodo persistence do not establish peer review or worldwide novelty. The searches above
found no overlap [U as to exhaustive priority]; no negative literature search is described as proof of novelty. The
census is, to our knowledge, the first exact census of the growth function; specialist confirmation is still required.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Enumerator anchored to Markstroem's published values; z_max(1..4) = 1, 2, 3, 3 | EXP-001 | CONFIRMED: seven anchors reproduced at every compared depth (14 of 14 values per TCB-001); census exact for tau <= 4 | trusted baseline | `census` |
| z_max(5) = 4; minimal tau for 4 roots is 5; the difference-of-squares mechanism on x^2 - 2 | EXP-002 | CONFIRMED (both predictions) | first record mechanism | `census` |
| z_max(6) = 5; minimal tau for 5 roots is 6; the last-gate lemma; the multiply-by-x move | EXP-003 | census CONFIRMED; our prediction z_max(6) = 4 REFUTED | decides one depth beyond any exhausted frontier without storing it | `census` |
| z_max(7) = 5: the bottom law z = tau - 1 breaks; plateau at 4 and 7 | EXP-004 | CONFIRMED; depth-6 frontier of 25,844,905 states exact | the growth function has plateaus | `census` |
| Tower stall theorems and the family x^2 - c, c <= 200 | EXP-005 (with TCB-016, TCB-020) | CONFIRMED on the load-bearing claim: maximum yield 5, only at c = 2; second series c = m^2 + m + 1 from integer 2-cycles discovered; proofs in the paper | closes the iteration route | `census` |
| Minimal tau for 6 roots is exactly 8 | EXP-006 | CONFIRMED: 408 witnesses, three replayed gate by gate; our emptiness prediction REFUTED | the exact cost of six roots | `census` |
| No 8-gate seven-rooter by multiplication; digit ladders 1, 2, 2, 2, 2, 3, 4 (odd roots) and 1, 1, 1, 2, 2, 3, 3 (p = 3) through tau = 7 | EXP-007 | CONFIRMED (the odd-root prediction REFUTED) | the digit form of the conjecture has its own record family | `census` |
| Depth-8 census: z_max(8) = 6 from the full depth-7 frontier of 1,048,460,912 states | EXP-011 | CONFIRMED (all four predictions); every stage known-answer-gated | decision-complete through depth 8 | `census` |
| No 9-gate seven-rooter with a multiplicative last gate | EXP-012 | CONFIRMED (unconditional): maximum union of root sets 6 | half of the ninth gate | `census` |
| No 9-gate seven-rooter with an additive last gate: z_max(9) = 6, seven-root threshold exactly 10 | EXP-015 (windowed precursors EXP-013, EXP-014) | CONFIRMED without any window: 4,193,843,648,000 candidates, 2,345,860,018 built exactly, 0 seven-rooters; audit 6 of 6 PASS | closes the census at tau = 9; third plateau | `census` |
| Neighbouring worlds: F_p maximum exactly 2^(tau-1); real ladder 1, 2, 3, 4, 6, 8 and rational ladder 1, 2, 3, 3, 4, 5 through tau = 6 | TCB-027, TCB-037, TCB-038 (no experiment folder) | proved (F_p) and exhaustively measured (R, Q) | reads the integer ladder against its neighbours | `census` |
| Solver lane for the depth-8 residual; symmetry quotient | EXP-008, EXP-010, EXP-009 | INCONCLUSIVE (engine-bound) twice; the quotient route measured unsound (95 to 98 percent equal tau) and closed | negative record and method notes | research record |
| Windowed additive scan and the price of the window | EXP-013, EXP-014 | CONFIRMED on the window [-32, 32]; the window decides 99.998 percent of the additive space; superseded as the evidence for the threshold by EXP-015, kept as the paper's ablation row | audit trail | research record |

Experiments outside the primary blocks are research records (inconclusive, measured and closed routes, windowed
precursors); no experiment has been withdrawn, so none is classed superseded (`research-governance.json`,
`experiment_dispositions`).

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `census` | v0.07 | [10.5281/zenodo.24231299](https://doi.org/10.5281/zenodo.24231299) | [10.5281/zenodo.21753438](https://doi.org/10.5281/zenodo.21753438) | what is the exact growth function z_max(tau) of the Shub-Smale conjecture at the bottom of its ladder (tau <= 9), at what cost do k integer roots appear, and which mechanisms realize the records |

The paper is "The Bottom of the Shub-Smale Tau Conjecture: an Exact Census of Integer Roots for Constant-Free
Straight-Line Programs of Length at Most Nine" (35 pages, published 2026-11-14, independent review APPROVE; its history
is v0.01 21753439, v0.02 21763182, v0.03 22035884, v0.06 23980033, all under the one concept DOI).

Split decision (2026-11-16 review, the coordinating session): the census stays one paper. Its parts answer one central
question, the exact maximum number of distinct integer roots by SLP length with its witnesses, thresholds and the
mechanisms behind them; the stall theorems, the digit-restricted census and the three-worlds ladders are instruments and
readings of that census, not separate questions with their own toolkits or audiences. A separate paper is triggered only
when a proposed focus yields a coherent theorem with a different central question (for example rate lemmas for an
infinite family under TC-F5). No immutable published version is rewritten.

## Focus record

- Closed: TC-F0 (instrument and Markstroem anchor), TC-F1 (composition towers and the family loophole), TC-F3 (solver lane
  for the depth-8 residual; closed by EXP-008 and EXP-010, subsumed by EXP-011).
- Dormant: TC-F2 (the neighbouring worlds; deeper ladders need the 25.8M-state or larger frontier and are not scheduled).
- Active: **TC-F4**, the exact census z_max(tau) through tau = 9 with the seven-root threshold. Its success gate was met on
  2026-11-05 by EXP-011 to EXP-015 and carried by census v0.07 on 2026-11-14; it stays the current focus until the
  strategic review with Felipe.
- Proposed, for Felipe at this review (methodology 13: a changed target is shown before it is treated as the continuation):
  TC-F5, witness anatomy (TCB-007): classify the record mechanisms per tau and prove rate lemmas for candidate infinite
  families (the anatomy lens of the plan); then, with lower priority and from the plan and backlog text: TC-F6, the integer
  census past Markstroem's length 11 (TCB-006); TC-F7, ceiling checks against Rojas (additive-complexity co-census); TC-F8,
  the valuation-spectrum hunt (TCB-017).
- Gated: TC-F9, the next census depth (z_max(10) and the eight-root threshold, recorded in {10..13} in `state.md`); it needs
  the depth-8 frontier of about 4 x 10^10 states and 1.1 TB of shards (EXP-011 verdict) and no frontier plan exists.

## Open obligations

- `census`: no open version obligation; v0.07 is current. A new version only for corrections or when a proposed focus
  yields a result (a new Zenodo version on the same concept DOI, never an edit).
- Reads and pages from the backlog: TCB-002 (Shub-Smale 1995, blocked: no open copy, needs library access); TCB-004
  (Cheng 2003 and Strassen 1976/77 have no open copy; Cheng 2004 read); TCB-008 (KPT15, Hrubes 2013, Dutta 2021);
  TCB-009 (Lipton 1994, Shamir 1979); TCB-010 (PosSLP adjacency); TCB-014 (ECCC TR19-142); TCB-011 (wiki pages 01 to 05) and
  TCB-013 (web problem page) remain todo; TCB-033 (digit and mod-p ladders at depth 8, replayable from the stored frontier)
  is todo; TCB-031 (scaling gap beyond the first case) and the depth-7 real and rational ladders are open.
- Record upkeep: `RESUME.md` was last rewritten at round 10 (2026-08-20) and its experiment index stops at EXP-011; its
  state lives now in the dated entries of `state.md` and `history/log.md`.
- The depth-7 frontier (27.3 GiB, 1,048,460,912 states) lives in the data root and its SHA-256 manifest is in the
  repository (`EXP-011-depth8-pipeline/artifacts/frontier7.manifest.md`).
