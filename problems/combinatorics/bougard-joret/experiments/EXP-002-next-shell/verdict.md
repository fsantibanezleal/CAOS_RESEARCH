# EXP-002 verdict: CONFIRMED

Date: 2026-09-05. Preflight committed and pushed at `d15f240` before implementation or computation. Authority: [complete proof](proof.md), [exact certificate](artifacts/certificate.json), and the independent audit recorded below. EXP-001 is unchanged.

## Derived result [D]

For every integer $k\ge3$ and $2\le a\le k+1$,

$$f(a+k+1,a,k)=\left\lceil\frac{k(a+k+1)}2\right\rceil.$$

The proof covers the entire admissible first interior shell. Its main construction augments classical Harary graphs with a complement matching, then attaches an independent set through injective missing-neighbor pairs. A self-contained cyclic-gap lemma proves the needed residual connectivity. The degree sequence includes exactly one degree-$(k+1)$ vertex when the degree sum is odd. Complements of cycles, crown graphs, a residual matching, and the EXP-001 path handle the remaining boundaries.

All extremizers for $a=2$ are exactly the complements of disjoint cycles of lengths at least five, on total order $k+3$. The prior complete tree characterization at $a=k-1$ is retained. No classification of all other shell extremizers is claimed.

The full revised first regime and the second regime remain open. Classical overlaps are $a=k+1$ and $(n,a,k)=(6,2,3)$; the previous CAOS version already proved $a=k-1$. The full-shell formula was not located in the primary sources and targeted searches in the [September 5 portfolio refresh](../../context/2026-09-05-portfolio-refresh.md). That is bounded novelty evidence, not guaranteed priority.

## Machine validation [MV]

All arithmetic is exact integer combinatorics, without stochastic choices or numerical tolerances. The finite evidence does not establish the universal quantifier.

| Declared check | Result |
|---|---|
| All $k=3,\ldots,12$, every $a=2,\ldots,k+1$ | 75 constructed graphs pass exact degree, edge, independence and vertex-split flow checks |
| Direct subsets and exhaustive cuts for order at most 16 | 45 cases agree with recursive independence and flow |
| Harary residual cases | 36; both starting and augmented residuals pass exhaustive-cut and flow connectivity |
| Odd degree sum | 15 cases; exactly one degree-$(k+1)$ vertex in each |
| Delete an edge incident to a degree-$k$ vertex | 75 rejected constructions; direct cuts also reject all 45 small cases |
| Complement-cycle controls | Eight partitions, including triangles, 4-cycles and disconnected unions of longer cycles |
| Independent regeneration of the complete order-six census | 32,768 labeled graphs, 60 extremals, exactly the complements of six-cycles; agrees with EXP-001 |

The smoke grid initially completed its mathematical checks but stopped at a baseline schema assertion: EXP-001 uses status `passed`, while the new wrapper expected `PASS`. This was an implementation integration error, corrected before the full run. It did not change the hypothesis, construction or acceptance criteria. The subsequent full run passed. The certificate stores both current and imported checker source hashes and all 75 edge lists. The regenerated census shares the EXP-001 checker library, so it is not described as a wholly independent implementation.

## Adversarial reasoning and independent verification

The derivation was reviewed separately from its implementation. Refutation routes included parity, a missing-neighbor collision, relying on minimum degree alone to bound independence, disconnecting odd Harary graphs, deleting all of the independent set, and leaving only two residual vertices. None produced a counterexample. The cycle-power independence inequality and the two-residual-vertex bridge are explicit load-bearing arguments in the proof.

An independent reviewer reconstructed the 75 saved graphs using NetworkX 3.4.1, without importing the CAOS graph checkers: exact node connectivity equals $k$, independence from maximal cliques of the complement equals $a$, and order, simplicity and edge bounds agree. All 36 saved base Harary graphs also have exact connectivity $d$. The durable [audit.py](audit.py) and [audit receipt](artifacts/independent-audit.json) verify those cases, augmented residuals, all 75 damaged-edge controls and all eight cycle controls. The receipt binds the proof, certificate and three verifier scripts by SHA-256. The complete proof text was independently read after writing; the final audit found no gap in any lemma or boundary case. These are independent computational and reasoning checks within the research workflow, not external peer review or proof-assistant formalization.

## How could this be wrong?

- A mathematical gap could remain despite adversarial review; the complete elementary proof is exposed for scrutiny.
- A matching older theorem could change the novelty assessment; source access and search limits are explicit.
- Shared bugs could affect the two CAOS checkers; the separate NetworkX reconstruction addresses that implementation risk, while the symbolic proof does not rely on any checker.
- Finite tests cannot justify larger parameters by themselves. The bound and the all-parameter construction supply the theorem.

## Consequences and exploration record

The invariant-first degree-sum bound suggested attaining a regular or almost regular graph. The residual-degree lens replaced the previous tree by a Harary graph; complement matchings repaired the degree deficits without weakening connectivity. The independent-set lens supplied a cycle-power bound. This closes BJB-005 with a full formula, rather than only another finite census. It triggers manuscript v0.02 under the existing concept DOI. Next meaningful targets are complete equality classification on the shell, representation uniqueness on the tree strip, or a new committed experiment beyond $n=a+k+1$.
