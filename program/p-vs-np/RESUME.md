# p-vs-np: RESUME (session handoff)

Updated 2026-11-24 (opened; PNP-001 reviewed, correct after fixes, findings applied; PNP-006 proved, review pending; EXP-001 and EXP-002 closed; PNP-003 first reading done: not settled).

## 1. State in one screen

Opened on 2026-11-24 by Felipe's order "continue with the four open ones, dont stop", after the path maps of the four
Millennium problems still open inside their prize statements and the decision recorded in
`program/millennium-review-2026-11-22.md`, Section 9. The target is not a proof of P != NP. It is the transfer
towards Boolean circuits of the superpolynomial lower bound for arithmetic circuits claimed on 2026-11-23 (Anthropic,
"VP != VNP over every field", Lean artifact, unread by a human mathematician; a second claim by OpenAI the same day).

What the programme has (note `context/2026-11-24-boolean-ladder-and-the-two-cases.md`, derived by the coordinating
session and reviewed on 2026-11-24 by a reader other than the writer: correct after fixes, twelve findings applied):

- The ladder S(c): circuits that agree with the Hamiltonian cycle polynomial on inputs 0 and 1 and compute a
  polynomial of degree at most c in each variable. S(1) is the theorem of the paper; S(infinity) over F_2 is a lower
  bound for Boolean circuits that compute the parity of the number of Hamiltonian cycles (a statement on a counting
  class; NP not inside P/poly implies it in the infinitely-often form, and it is not known to imply anything on NP).
- Over F_2, under the contracting hypothesis for F_2 itself, S(c) holds for every fixed c and up to a small power of
  m [D, reviewed, conditional on the paper and on one count the paper does not print]. Not over a general field: the
  substituted matrix has entries -1 and a - 1 there (review finding J1).
- In the paper's flat case the decomposition lemma stops at c = 2: the values at one-hot inputs are cheap for
  circuits of block degree k - 1, and after polarization a balanced cut shares blocks between its two sides [D].
- The paper's open question, which of its two cases occurs: the contracting hypothesis holds with a given mu if and
  only if the metric sqrt(rank) on Mat_mu(F_2) is not a price (the paper for mu >= 3, the note for mu = 2); sqrt(rank)
  is a CAT(0) metric through the spherical building of GL_(2 mu)(F_2), so curvature cannot decide; maps into a
  Hilbert space contract with the ratio 2 - 2^(1-mu) for mu <= 4 [D, MV by EXP-001].

Open: S(c) over a general field; the count of non-constant entries; S(2) in the flat case; whether sqrt(rank) on the sixteen matrices of Mat_2(F_2) is a
price; the test of the proof against an oracle gate.

## 2. The objects table

| Object | Definition / authority |
|---|---|
| prize statement | "Does P = NP?" (official description by S. Cook, Clay Mathematics Institute) |
| HC_m | Hamiltonian cycle polynomial of the m x m matrix of variables; complete for VNP over every field |
| the paper | Claude (Anthropic), "VP != VNP over every field", `anthropics/formal-math`, `vp-vnp/paper.pdf`, SHA-256 `882f5eef...`, 2026-11-23 |
| c-functional circuit | a circuit whose polynomial agrees with HC_m on {0,1}^(m x m) and has degree at most c in each variable (note, Section 2) |
| S(c) | every c-functional circuit for HC_m has superpolynomially many gates |
| spectral point, price | Definition 2.1 of the paper; a price is a limit of scaled metrics d_phi |
| D(r) | root mean square distance, in a price on Mat_mu(F_2), of two matrices whose difference has rank r |
| contracting, flat hypothesis | Definition D.1 of the paper; Theorem D.2: one of them holds |
| transversal | matrices with independent column spaces and independent row spaces |
| sqrt(rank) | the metric sqrt(rank(a - a')) on Mat_mu(F_2); the price that exists if the contracting hypothesis fails |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-rank-metric-finite-checks | the finite facts on Mat_mu(F_2), mu = 2, 3, 4, used by the note: character ratios, negative type, spanning sets, cliques, the transversality graph | CONFIRMED (2026-11-24) | ratios 3/2, 7/4, 15/8 = 2 - 2^(1-mu); rank is not of negative type; every spanning and connectivity fact used in Proposition 5.2 holds |
| EXP-002-character-sums-closed-forms | do the closed forms of the character sums agree with exhaustive counts (mu <= 4) and satisfy the inequality (mu <= 40)? | CONFIRMED (2026-11-24) | D(mu)^2 <= (2 - 2^(1-mu)) D(1)^2 for maps into a Hilbert space, every mu >= 2, equality only for combinations of rank-one characters (proved in the note; the experiment guards the algebra) |

## 4. In flight

- Nothing running. The review of PNP-006 is to be ordered with the next unit.

## 5. Next actions

1. PNP-002: the count E = O(n) of the non-constant entries on the construction of Corollary E.2 and Proposition
   M.2 (the other reading, that only the accelerator uses the circuit, is confirmed by the review on pages 57 to 59).
2. Review of PNP-006 by a reader other than the writer.
3. PNP-003: the first instance. Is sqrt(rank) on Mat_2(F_2) a price? The first reading (2026-11-24) found nothing
   that settles even the four-point sub-question; since the square is a positive combination of cut metrics, only an
   argument through sums of terms of mixed type can exclude it. Next: the eight-point sub-configuration (two opposite
   matrices and the six between them), which is not Euclidean, against the crossing inequality with hubs.
4. PNP-004: the written test of the contracting case against an oracle gate (relativization, algebrization).
5. PNP-005: S(2) in the flat case, starting from k = 3 (the trace of a product of three matrices).

## 6. Where everything lives

- Path map and decision: `program/p-vs-np/research-lines-2026-11-24.md`, `program/millennium-review-2026-11-22.md`.
- Notes: `problems/computation-complexity/p-vs-np/context/`.
- Experiments: `problems/computation-complexity/p-vs-np/experiments/`.
- Sources with SHA-256: the data root, `caos-research/millennium-open-four-2026-11-24/p-vs-np/` (the dossier's) and
  `.../main-session/` (the coordinating session's: the paper, the official descriptions).
- Coordination (briefs, reports, status): the coordination repository, `plans/caos-research/millennium/` and
  `wip/caos-research/`.

## 7. Gotchas

- The text extraction of the paper loses the mathematical symbols; read the PDF pages.
- No proof assistant is installed on the default device; no Lean statement of the paper was checked.
- Every statement that uses the paper is conditional on it. The paper is unrefereed and one day old.
- The Boolean end of the ladder is a statement on counting classes. Never write it as progress on P against NP.
- Over a field other than F_2 the paper's reduction puts -1 and a - 1 into the matrix: a circuit that is right only
  on 0/1 inputs says nothing there.
- A deletion of a branch never goes in the same batch as the merge it depends on (incident of 2026-11-24, no loss).
