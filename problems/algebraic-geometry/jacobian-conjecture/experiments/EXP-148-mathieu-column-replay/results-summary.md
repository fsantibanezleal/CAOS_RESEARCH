# EXP-148 results summary

Raw run of `run.py` (hypothesis frozen at f6aa87e6). Exit code 0; every value below is an exact fraction from `artifacts/results.json`. No verdict language: `verdict.md` is written by the coordinating session.

## Per route

| Route | Ranges | Cells | Mismatches | Wall time (ms) |
|---|---|---|---|---|
| A | N 2..16, m 1..8, s 0..4 | 600 | 0 | 93 |
| B | N 2..16, m 1..5, s 0..3 | 300 | 0 | 2062 |
| C | N 2..6, (m,s) = (1,0), (1,1) | 10 | 0 | 313 |
| H | N = 2, m 1..8, s 0..4 | 40 | 0 | 10 |

Total wall time 3854 ms. Routes disagreeing on a shared cell: 0. Route C visited 1198080 (sigma, tau) pairs (full S_d x S_d double loop per monomial; the row delta is tested inside it). Cells whose computed value equals the prediction are marked equal in `routes[].equal`; s > m cells (predicted 0) are included in the counts.

## Identity checks

| Identity | Result |
|---|---|
| eq 3-2: a^2 = u v + tau^2 as a polynomial identity | pass: difference has 0 monomials |
| eq 3-4: P(rz) = r^8 P(z), Q(rz) = r^2 Q(z) | pass: monomial degrees 8 and 2, and exact evaluation at 6 rational points with r = 3/2 and 2/5 |
| u P - (1+u)(1-(1+u)^2 tau^2) in the ideal of a-1 and u v + tau^2 - 1 | pass: remainder after a = 1 and u v -> 1 - tau^2 has 0 terms |
| P has 16 monomials | pass: 16 monomials |
| P equals the 16-term list of the preflight | pass: exponents and coefficients compared exactly |
| each monomial of P has equal z-degree and w-degree (phase balance, as used by Lemma 5-5 of the paper) | pass: z-degree 4 and w-degree 4 on all 16 |
| each monomial of P balanced in the Definitions sense (a0, a1) = (b0, b1) | recorded deviation (see below): 5 of 16 monomials satisfy (a0, a1) = (b0, b1); recorded as a deviation of the hypothesis wording, not counted as a failure: the 11 others are degree-balanced and are integrated to 0 by every route |
| eq 3-5: c_m = int_0^1 (1-s^2)^m ds = 4^m (m!)^2/(2m+1)! for m = 1..8 | pass: exact polynomial integral |

## Route A values, N = 2 (computed = predicted in every cell)

| m | s=0 | s=1 | s=2 | s=3 | s=4 |
|---|---|---|---|---|---|
| 1 | 0 | 2/3 | 0 | 0 | 0 |
| 2 | 0 | 8/15 | 8/15 | 0 | 0 |
| 3 | 0 | 16/35 | 32/35 | 16/35 | 0 |
| 4 | 0 | 128/315 | 128/105 | 128/105 | 128/315 |
| 5 | 0 | 256/693 | 1024/693 | 512/231 | 1024/693 |
| 6 | 0 | 1024/3003 | 5120/3003 | 10240/3003 | 10240/3003 |
| 7 | 0 | 2048/6435 | 4096/2145 | 2048/429 | 8192/1287 |
| 8 | 0 | 32768/109395 | 229376/109395 | 229376/36465 | 229376/21879 |

## Route A values, N = 3 (computed = predicted in every cell)

| m | s=0 | s=1 | s=2 | s=3 | s=4 |
|---|---|---|---|---|---|
| 1 | 0 | 4/21 | 0 | 0 | 0 |
| 2 | 0 | 16/165 | 4/45 | 0 | 0 |
| 3 | 0 | 32/525 | 4/35 | 32/595 | 0 |
| 4 | 0 | 256/5985 | 64/525 | 256/2205 | 128/3465 |
| 5 | 0 | 512/15939 | 256/2079 | 1024/5775 | 1024/9009 |
| 6 | 0 | 2048/81081 | 2560/21021 | 20480/87087 | 2048/9009 |
| 7 | 0 | 4096/199485 | 256/2145 | 4096/14157 | 8192/21879 |
| 8 | 0 | 65536/3828825 | 114688/984555 | 458752/1349205 | 229376/415701 |

## Route A, N = 4..16, s = 1 column (computed = predicted in every cell)

| N | m=1 | m=2 | m=3 | m=4 | m=5 | m=6 | m=7 | m=8 |
|---|---|---|---|---|---|---|---|---|
| 4 | 1/14 | 4/165 | 2/175 | 64/9975 | 64/15939 | 512/189189 | 128/66495 | 16384/11486475 |
| 5 | 2/63 | 16/2145 | 8/2975 | 256/209475 | 256/398475 | 2048/5486481 | 512/2194335 | 65536/424999575 |
| 6 | 1/63 | 8/3003 | 4/5355 | 128/460845 | 128/1036035 | 1024/16459443 | 256/7460739 | 32768/1614998385 |
| 7 | 2/231 | 16/15015 | 8/33915 | 256/3533145 | 256/9324315 | 2048/170080911 | 512/87041955 | 65536/20994979005 |
| 8 | 1/198 | 1/2145 | 2/24225 | 32/1514205 | 64/9324315 | 64/24297273 | 128/111911085 | 8192/14996413575 |
| 9 | 4/1287 | 8/36465 | 16/508725 | 256/37855125 | 512/270405135 | 512/801810009 | 1024/4140710145 | 65536/614852956575 |
| 10 | 2/1001 | 4/36465 | 8/621775 | 128/54679625 | 256/450675225 | 256/1514530017 | 512/8741499195 | 32768/1434656898675 |
| 11 | 4/3003 | 8/138567 | 16/2860165 | 256/295269975 | 512/2794186395 | 512/10601710119 | 1024/68183693721 | 65536/12338049328605 |
| 12 | 1/1092 | 2/62985 | 2/780045 | 64/187899075 | 16/254016945 | 128/8674126461 | 128/30992588055 | 16384/12338049328605 |
| 13 | 1/1547 | 8/440895 | 8/6500375 | 256/1816357725 | 64/2794186395 | 512/106980893019 | 512/423565370085 | 65536/185070739929075 |
| 14 | 1/2142 | 4/373065 | 4/6500375 | 128/2095797375 | 32/3653936055 | 256/156356689797 | 256/684220982445 | 32768/327432847566825 |
| 15 | 1/2907 | 8/1225785 | 8/25072875 | 256/9281388375 | 64/18269680275 | 512/871130128869 | 512/4203071749305 | 65536/2198477690805825 |
| 16 | 1/3876 | 1/245157 | 2/11700675 | 8/618759225 | 16/10961808165 | 64/290376709623 | 128/3082252616157 | 4096/439695538161165 |

## Controls

- K1: behaved as stated. Observed: 16 of 16 removals give a nonzero pure moment for some m <= 3; every removal changes some value: True.
  - Per removal (monomial exponents z0, z1, w0, w1; m <= 3 nonzero pure moments; table cells changed of 40 at N = 2): (0, 4, 0, 4): [1, 2, 3], 30; (0, 4, 1, 3): [2, 3], 33; (1, 3, 0, 4): [2, 3], 25; (1, 3, 1, 3): [1, 2, 3], 30; (1, 3, 2, 2): [2, 3], 33; (2, 2, 0, 4): [3], 20; (2, 2, 1, 3): [2, 3], 25; (2, 2, 2, 2): [1, 2, 3], 30; (2, 2, 3, 1): [2, 3], 33; (3, 1, 1, 3): [3], 20; (3, 1, 2, 2): [2, 3], 25; (3, 1, 3, 1): [1, 2, 3], 30; (3, 1, 4, 0): [2, 3], 33; (4, 0, 2, 2): [3], 20; (4, 0, 3, 1): [2, 3], 25; (4, 0, 4, 0): [1, 2, 3], 30
- K2: behaved as stated. Observed: with c_m = 1/(m+1) the prediction at N = 2, m = 2 disagrees with the computed value for (m, s) in [(2, 1), (2, 2)]; computed ['8/15', '8/15'] vs alternative ['1/3', '1/3'].
- K3: behaved as stated. Observed: pure moments with (2a+u) replaced by (a+u), N = 2, m = 1..3: [(1, '1/3'), (2, '-1/15'), (3, '-1/5')].
- K4: behaved as stated. Observed: 200 monomials (107 literally balanced, degree <= 12) x N in (2, 3, 5): 600 comparisons, 0 disagreements between A and B.
- K5: behaved as stated. Observed: Route C: N=2: 1/2, 1/3; N=3: 1/3, 1/6; N=4: 1/4, 1/10; N=5: 1/5, 1/15; N=6: 1/6, 1/21.
- K6: behaved as stated. Observed: restricting to z1 = 0: Q has 0 monomials (zero), P restricts to [((4, 0, 4, 0), (-2, 0))]; so Q P^m = 0 on the torus direction.

## Deviations from the hypothesis

- The identity check 'the expansion of P has 16 monomials, each balanced' is true as equal z-degree and w-degree (all 16 monomials have z-degree 4 and w-degree 4, which is the phase balance the paper's Lemma 5-5 uses and what the preflight states). It is false in the sense of the hypothesis's Definitions section, a monomial being balanced when (a0, a1) = (b0, b1): only 5 of the 16 satisfy that (the 11 others, such as z0^3 z1 w0^4, are degree-balanced and are integrated to 0 by Routes A and B because their sphere moment vanishes). The run records both readings; the literal one is stored in `identities` with `pass: false` and `deviation: true` and is not counted as a failure of the instrument. This is a wording point of the hypothesis, not a change to it.
- Route H is implemented as constant term of u^(s-m) (1+u)^m (1-(1+u)^2 t^2)^m, integrated exactly in t over [-1, 1] with weight 1/2, the same as the hypothesis's step 2 (the coefficient of u^(m-s)).
- Route C's integrand for (m, s) = (1, 1) has degree d = 5 and for (1, 0) degree d = 4; for N < d the Weingarten sum uses partitions with at most N parts. Time and range match the hypothesis; no cell was skipped.
- Timings use `time.perf_counter_ns` (integer nanoseconds floored to ms); nothing else uses a clock.
