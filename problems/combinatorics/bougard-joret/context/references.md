# Primary references and novelty audit

Access dates: 2026-09-04 and 2026-09-05. [V] primary text checked; [D] derived here; [U] unresolved.

- [V] Nicolas Bougard and Gwenael Joret, *Turan's theorem and k-connected graphs*, Journal of Graph Theory 58 (2008), 1-13, [DOI](https://doi.org/10.1002/jgt.20289), [author PDF](https://gjoret.be/papers/turan.pdf). Section 6 poses the higher-connectivity formula, covers $n=k\alpha$, the large-order range, and $\alpha=2,n\ge2k$. These do not cover the proposed infinite strip, except isolated overlaps.
- [V] Joyentanuj Das and Sayan Gupta, *Counterexample to the Bougard-Joret Conjecture*, [arXiv:2608.18828v1](https://arxiv.org/html/2608.18828v1), 19 August 2026. Theorem 3.1 determines $n=\alpha+k$; Corollary 3.3 gives $f(2k-1,k-1,k)=k^2-1$ for $k\ge4$. Section 4 leaves the second regime unresolved. Discovery priority for this counterexample belongs to these authors.

## Contributions and known overlaps

[D] [EXP-001](../experiments/EXP-001-tree-strip/proof.md) determines $f(2k,k-1,k)=k^2$ for all $k\ge3$ and characterizes every extremal graph relative to a maximum independent set by a nonstar tree and prescribed missing-neighbor fibers. This published v0.01 result remains unchanged.

[D] [EXP-002](../experiments/EXP-002-next-shell/proof.md) determines the full first interior shell: $f(\alpha+k+1,\alpha,k)=\lceil k(\alpha+k+1)/2\rceil$ for $k\ge3$, $2\le\alpha\le k+1$. For alpha two, its equality classification is precisely complements of unions of cycles of lengths at least five. No general classification of all shell extremizers is asserted. The general revised first regime and second regime remain open. See the owning verdict for audit status; v0.02 publication is pending.

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
