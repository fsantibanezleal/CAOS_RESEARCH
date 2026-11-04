# EXP-004 verdict: the endpoint of the Bougard bracket

Date: 2026-11-04. Status: **CONFIRMED, uniform derivation [D], independent audit PASS, finite corroboration
[MV]**. The hypothesis and the complete proof were committed before any computation. The universal statement
rests on the [proof](proof.md); the computations corroborate it and do not replace it.

## Result

For every integer $d\ge7$,

$$f(2d+3,2,d+2)=d^2+4d+2 .$$

This closes BJB-014: EXP-003 left the one-edge bracket $d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2$. The prediction
of the hypothesis (the upper endpoint) holds. The lower value is excluded by a structural theorem about all
extremal graphs of EXP-003 Theorem 1: every triangle-free graph on $2d+3$ vertices with maximum degree at most
$d$ and $d^2+d+2$ edges has two vertices with the same $d$ neighbours (a $K_{2,d}$), so its complement has a
vertex cut of size $d+1$. The attaining graph is EXP-003's complement of the subdivided crown. For example
$f(19,2,10)=98$; the excess over the degree-sum prediction is $\lfloor d/2\rfloor-1$.

Not claimed: a classification of the extremal graphs (only the shared-neighbourhood property), the full
Bougard-Joret problem, the second regime $n>k\alpha$ (BJB-016) or other AEY matching levels (BJB-015).

## Validation

| Route | Scope | Result |
|---|---|---|
| Independent adversarial audit (Opus reviewer, separate context) | Every part of proof.md re-derived: reduction, identity $a+b=2$, type structure, helper lemma, $r\le1$, the three $r=2$ cases, the reduction of all 25 ordered pairs $(p,q)$ by rotation and reflection | PROVED, 0 blockers; three wording fixes applied (below). Report: CAOS_MANAGE `wip/caos-research/bj-exp004-proof-audit-2026-11-04.md` |
| Auditor's own checks | Type-size enumeration for $d=7..12$ against the derived sizes; its own z3 encoding at $d=7$; attaining graphs for $d=7..10$ | All agree (scripts not archived by the auditor; outputs quoted in the report) |
| `run_cfg.py`, configuration-split SAT, $K_{2,d}$-free | $d=7$: all 8 defect configurations | 8 of 8 UNSAT (0.2 s to 363 s) |
| `run_cfg.py`, $K_{2,d}$-free | $d=8$: all 8 defect configurations | 7 of 8 UNSAT (0.2 s to 1993 s); `-,-` UNKNOWN at the 3000 s limit. That configuration is impossible without any search: two defective vertices with no cycle neighbour give $a\ge4$, against $a+b=2$ (proof.md identity (1)); at $d=7$ it is UNSAT |
| `run_cfg.py`, free controls | $d=7$: configurations none, `0,2`, `0,1`; $d=8$: none, `0,2` | SAT where extremal graphs exist (d=7 none and `0,2`; d=8 `0,2`), so the encoding is not over-constrained |
| `check_models.py` (networkx, independent of z3) | every SAT control model | each is triangle-free, order $2d+3$, $\Delta\le d$, $d^2+d+2$ edges, has a $K_{2,d}$ and a complement of connectivity at most $d+1$ (`artifacts/models-check.json`) |
| `run.py`, global lazy-cut SMT (the method declared in the hypothesis) | $d=7$: the known-answer gate (target $d^2+d+1$) and the search, with and without the $K_{2,d}$-free clauses | none finished within its cap (50 minutes without, 2 hours with the clauses; exit 124); no output. Superseded by the configuration split, which uses only the Section 2 structure facts the audit re-derived |

Configuration labels (`run_cfg.py`): none, `-` (one defective vertex without cycle neighbour), `0` (one at
$c_0$), `0,0` `0,1` `0,2` (two, at $c_0$ and $c_q$), `-,0`, `-,-`. Rotation and reflection reduce every placement
to these.

## Post-audit edits to proof.md

Wording only, recorded in its status line: the helper lemma is renamed Lemma H (EXP-003 also has a Lemma 3);
the equality step of Section 4.2 is stated explicitly ($n_{p+3}+(n_{p+2}+n_{p+4})=2d-1$ against the bounds
$d-1$ and $d$); Section 5 lists the use of $d\ge5$ in 4.3.

## Deviations from the hypothesis

The hypothesis planned the global lazy-cut search (`run.py`) for $d=7$ and $d=8$. It did not finish in the cap.
The corroboration recorded above uses the configuration split instead, which is a different encoding with the
same target (no extremal graph without a $K_{2,d}$; a $K_{2,d}$ already gives the cut). The deviation affects
only the finite corroboration, not the proof.

## Reproduction

From `problems/combinatorics/bougard-joret/experiments/EXP-004-bracket-endpoint/` with the repository venv:

    python run_cfg.py --k2d --timeout 3600 -- 7 "0,0"      # one configuration; repeat for each label and d
    python run_cfg.py --free --timeout 3600 -- 7 ""        # control
    python check_models.py

## Residual risks

The proof is internally reviewed, not peer reviewed and not formalized. The finite checks cover $d=7$ and $d=8$
only and assume the Section 2 structure (five-cycle, types, at most two defective vertices), which is itself
part of the audited proof.
