# 05 - Experiments index

| EXP | Question | Verdict | Key output |
|---|---|---|---|
| [EXP-001](../experiments/EXP-001-validate-counterexample/) | Is the announced N=3 counterexample valid? | **confirmed** | det $JF = -2$ identically; fiber over $(-\tfrac14, 0, 0)$ is EXACTLY the 3 announced points (Groebner). |
| [EXP-002](../experiments/EXP-002-structure-reverse-engineering/) | What structure makes F work? | **confirmed** | Weighted skew-product; reduced Keller identity $J_2 = 2c_1^2$ (2 variables); fiber cubic at $w = u c_1/2$; generating identity for $a_1$. |
| [EXP-003](../experiments/EXP-003-seed-family-constructor/) | Does the v1 constructor generalize? | **partially refuted** | Sharp at $d = 2$ (F unique up to scale); v1 lift unsolvable for $d \ge 3$; failure analysis yields the potential form. |
| [EXP-004](../experiments/EXP-004-constructor-v2-potential-form/) | Is constructor v2 correct and productive? | **confirmed** | General family: det $= -k\,p(1)^2$ always; fiber degree $d + 1$; NEW counterexamples (P3, P4, P5) with exact rational collisions; reconstruction inverse. |
| [EXP-005](../experiments/EXP-005-2d-obstruction/) | Why can't the mechanism reach N = 2? | **confirmed with caveats** | 2D equivariant Keller reduces to ONE univariate ODE; one-invariant collapse proposition; no Keller slices of F. Caveats: injectivity scan vacuous (EXP-006 queued). |

Planned next: EXP-006 (branch-symbolic 2D equivariant enumeration), EXP-007 (asymptotic variety
of F, exact), then JC-P3 minimality and JC-P4 cascade verification (see
[../../../../program/jacobian-conjecture/backlog.md](../../../../program/jacobian-conjecture/backlog.md)).
