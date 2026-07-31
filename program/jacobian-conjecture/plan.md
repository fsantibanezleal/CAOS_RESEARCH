# Jacobian conjecture: active problem plan

Opened 2026-07-20. Area: algebraic geometry. State: exploring. Last strategic audit:
2026-07-30.

This is the current plan. Earlier route proposals remain evidence of the program's development,
but the controlling decisions are in
[`strategy-audit-2026-07-30.md`](strategy-audit-2026-07-30.md).

## Goal

Maintain the exact record around the counterexamples in dimensions at least three, and pursue
rigorous, source-complete progress on the still-open planar Jacobian conjecture. The immediate
planar target is the GGHV reduced $(72,108)$ case, without treating sampled inconsistency,
support-restricted failure, or absence of a finite certificate as a proof.

## Evidence rules for the planar program

1. A verified covector can prove that the specific linearized system it certifies is
   inconsistent.
2. Failure to find a covector is not evidence that a Keller completion exists unless a
   necessity theorem has first been proved.
3. Support sweeps are one-sided. One infeasible support can exclude a certificate degree, but
   all tested supports being feasible proves nothing positive.
4. Results for the reduced bracket $[P,Q]=x^2$ do not inherit theorems stated for Keller pairs
   $[f,g]=1$ without an explicit bridge.
5. Parameter samples, axis charts, and forced-edge families do not establish simultaneous
   symbolic coverage of the 51 free interior coefficients.

## Active phases

| Phase | Work | State and gate |
|---|---|---|
| JC-A | Preserve and publish the exact dimension at least three record | rolling; no current compute |
| JC-B | Complete the $[125,150]$ primary-source frontier reconciliation | active; EXP-094 shows C10/C11/C19/C20 are not excluded by the cited remark; 16 unprinted \(A'_0\) values remain |
| JC-C | Test modern Newton and approximate-root restrictions against the GGHV reduction | direct transport decided by EXP-097: absolute resultant degree is not typed after Laurent localization without a boundary-divisor ledger |
| JC-D | Reformulate universal inconsistency as a constructible determinantal-strata problem | active; EXP-125/126 reduce \(F_3,F_6\) to finite residuals; \(F_7\), finite points, and \(A=0\) remain |
| JC-E | Degree-three certificate decision | done by EXP-075; one exact four-parameter slice is infeasible, so no global cubic covector exists |
| JC-F | Global geometric routes: fibres, properness, and parameter spaces | hold; resume only after a rigorous bridge to the reduced system is stated |
| JC-G | Manuscripts, wiki, data, and public record | rolling; update only from adjudicated results |

## Ordered next work

1. Preserve EXP-125/126 as complete. On \(AS\ne0\), \(F_3\) leaves
   \(Q_9Q_{15}=0\) and \(F_6\) leaves \(Q_{18}Q_{30}=0\).
2. Declare EXP-127 on \(F_7\). Reconstruct its distinct persisted
   cross-prime basis, reduce the graph numerator modulo \(F_7(X,B)\), and
   compute the exact function-field norm without expanding algebraic roots.
3. Continue to the finite \(F_3/F_6\) and base-locus point strata only after
   the \(F_7\) quotient is adjudicated. Treat \(A=0\) separately.
4. Treat the complete EXP-118--121 \(T_B\) cover as a regression gate. Do not
   spend compute re-eliminating or adding charts to the closed restriction.
5. Reopen intersection-\(21\) transport only if the graph recursion stalls,
   large, and only with the complete boundary-divisor ledger required by
   EXP-097.
6. Continue the independent [125,150] frontier task:
   - preserve C10/C11/C19/C20 as unresolved by GGV2 Remark 2.32;
   - derive the 16 unprinted $A'_0$ values through the declared chain algorithm;
   - preserve C01/C04 as open absent an exact exclusion.
7. Keep EXP-093 cancelled. EXP-075's exact support at reordered index 2662 proves that no global
   degree-three polynomial covector exists, so the proposed four-million-unknown solve has no
   target.
8. Keep EXP-109 as a bounded chart-control only. Do not continue coefficient
   slices as the main programme.

## Routes not currently authorized for compute

- EXP-075 continuation: stop after the reproduced decisive hit at index 2662. The remaining
  247,237 supports cannot change the degree-three exclusion.
- EXP-079 as a flat or regular-singular connection: retire the formulation. No connection,
  singular point, or implication from regularity to polynomial termination was defined.
- EXP-081 collision-covector projection: retire unless an explicit map between the two dual
  spaces is constructed.
- EXP-092 LND/line-fibre route: hold. For the reduced pair, $D_P(Q)=[P,Q]=x^2$, not a unit
  slice, so the Keller-pair argument does not transfer directly.
- EXP-093 full degree-three solve: cancel. EXP-075 proves its target is empty.
- EXP-110 all-\(125\)-minors of \(M\): retire. EXP-111 proves that the
  constant \(Q\)-column makes every such minor vanish identically, so the
  target is vacuous.
- Further coefficient-slice enumeration: demote. It cannot close the
  51-parameter family.
- Raw 125-column minors on the \(d=0\) \(T_B\) plane: retire. EXP-115 proves
  that \(P\) itself enters the admissible \(Q\)-space there, so \([P,P]=0\)
  forces a polynomial right kernel. Quotient by this kernel first.
- Treating \((a,b)=(0,0)\) as a generic quotient anchor: retire. EXP-116
  finds the deeper exact rank stratum \(112/113\); normalize at \((0,1)\).
- Treating the \(d=0\) quotient residual as a two-dimensional elimination
  target: retire. EXP-117 reduces \(b\ne0\) to nine squarefree invariant
  points in \(z=a^3/b^7\), plus the divisor \(b=0\).
- Reusing the EXP-115 \(G\)-basis to attack the \(L\) or \(Q\) residual:
  retire. EXP-120 factors its determinant as \(X^{30}LQR\), so it vanishes
  identically on both target components. Select bases on the surviving
  finite schemes instead.

## Cancelled EXP-093 scale facts

There are 51 perturbation parameters and a 165-dimensional gauge space.

- Through parameter degree two:
  $(\binom{51}{1}+\binom{52}{2})165=227{,}205$ certificate unknowns.
- Through parameter degree three:
  $(\binom{51}{1}+\binom{52}{2}+\binom{53}{3})165=4{,}092{,}495$ certificate unknowns.
- The homogeneous order-four target alone has
  $\binom{54}{4}\cdot125=39{,}531{,}375$ scalar conditions before exploiting sparsity,
  symmetry, or elimination.

The earlier shorthand “227k+ unknowns” described the degree-two scale, not the proposed
degree-three system. The size audit made a pilot necessary; the subsequently recovered and
reproduced EXP-075 hit makes even that pilot unnecessary.

## Stop and go rules

- Prefer a source theorem or distinguishing invariant before coefficient computation.
- Do not start a run expected to exceed five minutes without a declared experiment, smoke test,
  checkpoint path, cost estimate, and stop condition.
- Any proposed transfer from a true Keller pair to the reduced GGHV pair must display the map and
  verify which hypotheses survive.
- Do not launch EXP-093. Any future degree-four or higher construction needs a new declared
  resource and proof-value gate.
- A claimed $(72,108)$ exclusion still requires coverage of every forced branch and every free
  interior coefficient, followed by independent verification of the GGHV assembly.

## Exploration cadence

The systematic exclusion spine remains active with three complementary lenses:

- Newton/valuation structure at infinity;
- commutative-algebra certificate modules and stratified covers;
- global geometry and parameter-space components.

Every round records which assumption was tested, what would falsify the route, and whether the
result can prove exclusion, can only filter candidates, or is exploratory.
