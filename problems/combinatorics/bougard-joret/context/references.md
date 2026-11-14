# Primary references and novelty audit

Access dates: 2026-09-04 and 2026-09-05. [V] primary text checked; [D] derived here; [U] unresolved.

- [V] Nicolas Bougard and Gwenael Joret, *Turan's theorem and k-connected graphs*, Journal of Graph Theory 58 (2008), 1-13, [DOI](https://doi.org/10.1002/jgt.20289), [author PDF](https://gjoret.be/papers/turan.pdf). Section 6 poses the higher-connectivity formula, covers $n=k\alpha$, the large-order range, and $\alpha=2,n\ge2k$. These do not cover the proposed infinite strip, except isolated overlaps.
- [V] Joyentanuj Das and Sayan Gupta, *Counterexample to the Bougard-Joret Conjecture*, [arXiv:2608.18828v1](https://arxiv.org/html/2608.18828v1), 19 August 2026. Theorem 3.1 determines $n=\alpha+k$; Corollary 3.3 gives $f(2k-1,k-1,k)=k^2-1$ for $k\ge4$. Section 4 leaves the second regime unresolved. Discovery priority for this counterexample belongs to these authors.

## Contributions and known overlaps

[D] [EXP-001](../experiments/EXP-001-tree-strip/proof.md) determines $f(2k,k-1,k)=k^2$ for all $k\ge3$ and characterizes every extremal graph relative to a maximum independent set by a nonstar tree and prescribed missing-neighbor fibers. This published v0.01 result remains unchanged.

[D] [EXP-002](../experiments/EXP-002-next-shell/proof.md) determines the full first interior shell: $f(\alpha+k+1,\alpha,k)=\lceil k(\alpha+k+1)/2\rceil$ for $k\ge3$, $2\le\alpha\le k+1$. For alpha two, its equality classification is precisely complements of unions of cycles of lengths at least five. No general classification of all shell extremizers is asserted. The general revised first regime and second regime remain open. See the owning verdict for audit status; v0.02 is published at DOI 10.5281/zenodo.22341644.

Known shell overlaps: $\alpha=k+1$ has $n=2\alpha$ in the original paper; $(6,2,3)$ lies on $n=k\alpha$; $\alpha=k-1$ is EXP-001. Original large-order results contribute no further shell overlap. Harary's classical graph construction is credited to Frank Harary, *The maximum connectivity of a graph* (1962), [DOI](https://doi.org/10.1073/pnas.48.7.1142). [U] Full original text was inaccessible in this refresh; EXP-002 proves every connectivity property it uses rather than relying on an unchecked theorem statement.

Searches: exact title; Bougard Joret corrected boundary 2026; Bougard Joret alpha+k+1; f(2k,k-1,k); Bougard Joret tree 2k. Only the original paper and Das-Gupta's boundary result were found as direct primary matches. Absence from search results is not proof of priority. Both primary papers' relevant final sections are checked in the present session; a second research lane audits the novelty scope.

## Evidence gaps

| Claim | Current evidence | Gap / next action |
|---|---|---|
| Boundary disproof | Das-Gupta Theorem 3.1 and Corollary 3.3 | Credit remains external; no new disproof claimed |
| Strip value and full characterization | EXP-001 proof and exact certificate | No classification of unmarked tree representations claimed |
| Full-shell value and alpha-two classification | EXP-002 written proof and PASS finite certificate | Audit disposition belongs to verdict; general extremizer classification remains open |
| Novelty | Direct primary scope and targeted search | Avoid absolute priority claims; include classical and CAOS overlaps |
| Portfolio currency | [September 5 refresh](2026-09-05-portfolio-refresh.md), all 20 rows | Primary access limits explicit; external computational proofs not replayed |

The September 5 targeted queries added the full next-shell expression and compared both original final sections. No matching full-shell formula was located; absence from search results is not proof of novelty.

## Next-matching sources and contribution (2026-09-05)

[V] Ahanjideh-Ekim-Yildiz, [final 2024 article](https://doi.org/10.1007/s10878-024-01123-z), Conjecture 6.1 and Corollary 3.5, and Banak-Ekim-Taskin, [2023 full author manuscript](https://arxiv.org/html/2304.01729), Proposition 4.1 and Table 3, define the exact novelty floor. The latter already supplies the attaining graph and values through d=12; it leaves T(13,14) between 184 and 185.

[D] [EXP-003](../experiments/EXP-003-triangle-free-next-matching/verdict.md) proves the uniform maximum T(d,d+1)=d squared plus d plus two for every d>=7, by a fixed-order deficit argument and direct Tutte-Berge reduction. It gives a one-edge Bougard bracket, not its exact endpoint. [Detailed source/access ledger](2026-09-05-next-matching-review.md).

[V] Caro-Tuza, *Regular Turan numbers*, Australasian Journal of Combinatorics 78(1) (2020), 133-144, [Theorem 2(iii)](https://ajc.maths.uq.edu.au/pdf/78/ajc_v78_p133.pdf), already supplies the odd-order regular triangle-free extremum. The subsequent Cambie-de Joannis de Verclos-Kang [2023 paper](https://doi.org/10.1002/jgt.22857) also belongs to the regular prior art. Neither is presented as a new consequence here. The new fixed-order theorem concerns arbitrary graphs under a maximum-degree bound.

## Second line: Didin's claimed proof (2026-11-11)

- [V] statements, [U] correctness: Maksim Didin, *A Generalization of Turan's Theorem for Graphs with a Given
  Independence Number*, Zenodo preprint, 18 September 2026,
  [DOI 10.5281/zenodo.22831382](https://doi.org/10.5281/zenodo.22831382). Submitted to J. Graph Theory on
  19 February 2026, under review, not the version of record. Read on the English PDF (SHA-256 `ff71e72f...29258`,
  archived under the data root, `caos-research/bougard-joret/sources/didin-2026`).
  - Theorem 3: m >= t(n + s, alpha) - s, with s = alpha - p, where p is the largest number of components of an
    alpha-core (a spanning alpha-critical subgraph with the same independence number).
  - Theorem 9: every b-connected graph with n > b alpha, b >= 3 and alpha > 1 has
    m >= t(n, alpha) + ceil(b alpha / 2). Remark 5 says this establishes the n > b alpha portion of Bougard-Joret's
    Conjecture 1.
  - Theorem 10: the b-edge-connected form, with tight exceptions at alpha = 2, n = 2b + 1 and at (b, alpha, n) =
    (3, 3, 10). Lemmas 17 and 18 show those exceptions have 2-vertex cuts. Lemma 19 gives
    t(n + s, alpha) - t(n, alpha) >= b s for n > b alpha.
  - The paper gives no characterisation of the graphs attaining Theorem 9.
  - With the Bougard-Joret construction (upper bound), a correct proof settles the second line. The proof was not
    audited here.
- [U] M. A. Didin and D. S. Malyshev, *Generalization of Turan's theorem and some of its corollaries*, Uspekhi Mat.
  Nauk 81(5) (2026) 181-182, [DOI 10.4213/rm10305](https://doi.org/10.4213/rm10305). Metadata only (accepted
  23 October 2025); probably the announcement of the preprint above.
- Consequence for this programme. The second-regime notes v0.01 and v0.02 (2026-11-07/08) called the second line
  open outside Bougard-Joret's proved range; this was missed. The programme's enumeration (EXP-005 to EXP-010) is an
  independent exhaustive check of Didin's Theorem 9 for every open-window triple with n <= 24. EXP-011 adds what
  Didin's paper does not give: the complete extremal graphs at 35 triples, including graphs with no partition into
  alpha cliques, all within the cases Didin's inequality chain allows (EXP-011 second addendum).
- Search record and the other post-2008 citers (all on other invariants, or [U]): CAOS_MANAGE
  `wip/caos-research/bj-lit-second-regime-2026-11-11.md`.
