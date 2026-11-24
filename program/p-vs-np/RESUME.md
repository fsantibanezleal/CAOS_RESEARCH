# p-vs-np: RESUME (session handoff)

Updated 2026-11-24 (opened; unit PNP-001 written and sent to review; EXP-001 closed).

## 1. State in one screen

Opened on 2026-11-24 by Felipe's order "continue with the four open ones, dont stop", after the path maps of the four
Millennium problems still open inside their prize statements and the decision recorded in
`program/millennium-review-2026-11-22.md`, Section 9. The target is not a proof of P != NP. It is the transfer
towards Boolean circuits of the superpolynomial lower bound for arithmetic circuits claimed on 2026-11-23 (Anthropic,
"VP != VNP over every field", Lean artifact, unread by a human mathematician; a second claim by OpenAI the same day).

What the programme has (note `context/2026-11-24-boolean-ladder-and-the-two-cases.md`, all derived by the
coordinating session, review pending):

- The ladder S(c): circuits that agree with the Hamiltonian cycle polynomial on inputs 0 and 1 and compute a
  polynomial of degree at most c in each variable. S(1) is the theorem of the paper; S(infinity) over F_2 is a lower
  bound for Boolean circuits that compute the parity of the number of Hamiltonian cycles (it separates P from the
  counting classes, not P from NP).
- In the paper's contracting case, S(c) holds for every fixed c and up to a small power of m [D, conditional on the
  paper, two readings to be confirmed].
- In the paper's flat case the decomposition lemma stops at c = 2: the values at one-hot inputs are cheap for
  circuits of block degree k - 1, and after polarization a balanced cut shares blocks between its two sides [D].
- The paper's open question, which of its two cases occurs: the contracting hypothesis holds with a given mu if and
  only if the metric sqrt(rank) on Mat_mu(F_2) is not a price (the paper for mu >= 3, the note for mu = 2); sqrt(rank)
  is a CAT(0) metric through the spherical building of GL_(2 mu)(F_2), so curvature cannot decide; maps into a
  Hilbert space contract with the ratio 2 - 2^(1-mu) for mu <= 4 [D, MV by EXP-001].

Open: the review of PNP-001; S(2) in the flat case; whether sqrt(rank) on the sixteen matrices of Mat_2(F_2) is a
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

## 4. In flight

- Review of PNP-001 by a reader other than the writer (reviewer on opus), ordered 2026-11-24; report in the
  coordination repository.

## 5. Next actions

1. Apply the review's findings to the note; nothing of it is cited as established before that.
2. PNP-002: confirm on the paper's Appendices E, K and M the two readings on which Proposition 3.1 rests (the
   accelerator is the only use of the circuit after Lemma K.3; the substituted matrix has O(n) non-constant entries
   and is a 0/1 matrix at indicator assignments).
3. PNP-003: the first instance. Is sqrt(rank) on Mat_2(F_2) a price? Search for an asymptotic conversion between
   products of wires that shortens it; read the literature on asymptotic conversion of entanglement structures.
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
