# 05 - Experiments index

| EXP | Question | Verdict | Key output |
|---|---|---|---|
| [EXP-001](../experiments/EXP-001-validate-counterexample/) | Is the announced N=3 counterexample valid? | **confirmed** | det $JF = -2$ identically; fiber over $(-\tfrac14, 0, 0)$ is EXACTLY the 3 announced points (Groebner). |
| [EXP-002](../experiments/EXP-002-structure-reverse-engineering/) | What structure makes F work? | **confirmed** | Weighted skew-product; reduced Keller identity $J_2 = 2c_1^2$ (2 variables); fiber cubic at $w = u c_1/2$; generating identity for $a_1$. |
| [EXP-003](../experiments/EXP-003-seed-family-constructor/) | Does the v1 constructor generalize? | **partially refuted** | Sharp at $d = 2$ (F unique up to scale); v1 lift unsolvable for $d \ge 3$; failure analysis yields the potential form. |
| [EXP-004](../experiments/EXP-004-constructor-v2-potential-form/) | Is constructor v2 correct and productive? | **confirmed** | General family: det $= -k\,p(1)^2$ always; fiber degree $d + 1$; NEW counterexamples (P3, P4, P5) with exact rational collisions; reconstruction inverse. |
| [EXP-005](../experiments/EXP-005-2d-obstruction/) | Why can't the mechanism reach N = 2? | **confirmed with caveats** | 2D equivariant Keller reduces to ONE univariate ODE; one-invariant collapse proposition; no Keller slices of F. Caveats: injectivity scan vacuous (fixed in EXP-006). |
| [EXP-006](../experiments/EXP-006-2d-branch-symbolic-enumeration/) | Is the 2D equivariant class really rigid? | **confirmed** | Non-vacuous scan (216 instances, 648 in-image fibers): every instance injective, and in fact LINEAR; rigidity conjecture survives a real bounded-degree attack. |
| [EXP-007](../experiments/EXP-007-asymptotic-variety/) | Where do preimages escape? | **confirmed** | Family theorem: escape roots = multiple fiber roots ($s = -W'/m$). $A(F) = \{C=0\} \cup \{27A^2C^2 - 18ABC + 16A + B^3C - B^2 = 0\}$; end-to-end escape demo; collisions are generic, off the locus. |
| [EXP-008](../experiments/EXP-008-degree-laws-minimality/) | Degree laws and minimality? | **confirmed** | Degrees $(5d-3, 5d-4, 4)$ for $d = 2..5$; fiber floor 3; NEW fiber-degree-6 counterexample (seed $w - 3w^5$, det $-20$); $(7,6,4)$ = announced F is minimal within the family; global degrees 3..6 open. |
| [EXP-009](../experiments/EXP-009-char-p-reductions/) | Does the certificate survive char p? | **confirmed** | P3 mod 13 and mod 101: explicit non-injective Keller maps over $\mathbb{F}_\ell$ of degree $12 < \ell$ (below the characteristic, unlike $x - x^p$). |
| [EXP-010](../experiments/EXP-010-2d-rigidity-all-weights/) | Rigidity for ALL weights? | **confirmed** | THEOREM: every $\mathbb{G}_m$-equivariant Keller map of $\mathbb{C}^2$ is linear (classification + positive kill factor; 648 identity checks; empty constrained solves). |
| [EXP-011](../experiments/EXP-011-real-fiber-census/) | The real picture of F? | **confirmed** | Census 1 or 3 real preimages split by the discriminant wall ($D > 0$: 3, $D < 0$: 1); two exact routes agree; real surjectivity on a 36-target grid; real Keller corollary recorded. |
| [EXP-012](../experiments/EXP-012-weight-system-landscape/) | Do sibling weighted mechanisms exist? | **confirmed 1-4, refuted 5** | Landscape mapped: m = 1 is the JC(2) bridge (93 instances injective); m = 3 empty (valuation proof) or rigid (60 instances); the m = 4 potential family is EMPTY (Groebner certificate). The m = 2 mechanism is UNIQUE among scanned systems. |
| [EXP-013](../experiments/EXP-013-leading-form-cascade/) | The tropical route to JC(2)? | **confirmed 1-2, partial 3** | At every sampled ray, real Keller maps are the degenerate boundary of the EXP-010 classification (56 checks); exhaustive JC(2) certificate at (2,2); (2,3)/(3,3) queued behind a solver artifact (documented with an explicit witness). |
| [EXP-016](../experiments/EXP-016-cascade-verification/) | Is the consequence cascade real? | **confirmed** | All five chains verified from primary sources; corollaries now assertable (Mathieu false for SU(3); GMC, vanishing, Image false; full Dixmier false with Dixmier(1) open). |

Planned next: JC-P3 continuation (global-minimality search, degrees 3..6, GPU-widened ansatz
enumeration), JC-P4 cascade verification from primary sources, optional formal hardening of the
rigidity theorem (Lean), M3 web app with the baked census/wall artifacts (see
[../../../../program/jacobian-conjecture/backlog.md](../../../../program/jacobian-conjecture/backlog.md)).
