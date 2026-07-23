# Beyond 125: the GGHV configuration list for 125 <= max deg <= 150, and the adversarial audit of the (72,108) closure chain

Date: 2026-07-22
Compiled by: Lucy (primary-source transcription + adversarial audit task)

Primary sources, re-downloaded and re-read today from the arXiv LaTeX e-print sources
(temp copies in E:\_Temp\jc-arxiv, deleted after this dossier):

- [GGHV17] Guccione, Guccione, Horruitiner, Valqui, "Some algorithms related to the
  Jacobian Conjecture", arXiv:1708.07936. Single source file
  `Some_algorithms_related_to_the_Jacobian_Conjecture_26_de_agosto_de_2017.tex`,
  2045 lines. All tex line numbers below labeled [17:NNNN] refer to this file.
- [GGHV22] Guccione, Guccione, Horruitiner, Valqui, "Increasing the degree of a
  possible counterexample to the Jacobian Conjecture from 100 to 108",
  arXiv:2204.14178v1. Single source file `Increasing_Lower_Bound_20_04_2022.tex`,
  2262 lines. Tex line numbers labeled [22:NNNN].
- Our prior transcription dossier: context/2026-07-22-gghv-72108-dossier.md
  ("the GGHV dossier" below), whose tex line references were spot-re-verified today
  ([22:1000-1007] Prop 4.3 statement re-read verbatim; [22:286-289] Theorem 2.1
  located, a reference the prior dossier lacked).

Flags: [VERIFIED] = read directly in the named source at the given lines today.
[DERIVED] = mechanical computation from printed formulas, not printed in either paper.
[UNVERIFIED] = not confirmable from the primary text. DERIVATION NEEDED = an input
our sweep pipeline must produce because the papers do not print it.

====================================================================
# PART 1. The complete configuration list, 125 <= max(deg P, deg Q) <= 150
====================================================================

## 1.1 Scope and provenance

[VERIFIED] [GGHV17] section 6 ("Possible counterexamples with max(deg(P),deg(Q)) <= 150",
[17:1792-1872]) is the ONLY printed enumeration covering this range. It lists 34 cases
total: 13 family members [17:1802-1814], 9 sporadic chains of length 1 [17:1828-1836],
11 sporadic chains of length 2 [17:1848-1858], 1 sporadic chain of length 3 [17:1869].

[VERIFIED] Both section 5 and section 6 state ([17:1671], [17:1794]): "We only list the
cases satisfying equality (ecuacion diofantica). The other cases (satisfying
(ecuacion diofantica2)) can be obtained by swapping m with n." So every row below has a
MIRROR configuration with (m,n) -> (n,m) and the degree pair swapped; the 24 rows below
represent 48 oriented configurations. (For the open case (8,28),(11/4,7) the mirror is
what [GGHV22] intro calls "two cases with (deg P, deg Q) = (72,108)" together with the
(9,27) chain; see the GGHV dossier section 1.)

[VERIFIED] Of the 34 cases, exactly 10 have max deg < 125 (the seven red/plain family
rows 64, 112, 75, 75, 84, 99, 96 at [17:1802-1813] plus sporadic 108 [17:1832], 120
[17:1848], 108 [17:1850]); these are the subject of [GGHV22]. The remaining 24 have
125 <= max deg <= 150 and are the complete target list below. [GGHV22] proves nothing
about any of them; its Theorem 2.1 [22:286-289] only states that a counterexample has
max deg >= 125 or degrees (72,108)/(108,72). With our (72,108) closure, these 24 rows
(48 with mirrors) are the entire frontier from 125 to 150.

Degree bookkeeping convention [DERIVED, trivial]: B := v_{1,1}(A0); an (m,n)-pair has
(deg P, deg Q) = (m B, n B); gcd(deg P, deg Q) = B since gcd(m,n) = 1. The papers print
only max{deg P, deg Q} = max(m,n) B; the full pairs below are derived and were checked
against every printed max value (24/24 agree).

## 1.2 The master table, ordered by max degree

Columns: cfg = our label; degrees (deg P, deg Q) = (mB, nB); B = gcd of the degree
pair = v11(A0); g = gcd(A0) (drives the [GGV1, Cor 7.4] q-forcing candidate, see 1.4);
k = the Prop 3.2 integer (printed for family rows; DERIVED via eq. (3.17) for sporadic
rows, see 1.3); src = tex line of the row in [GGHV17].

| cfg | max | degrees   | A0      | A0'    | chain A1 (,A2 ,A3)          | (m,n) | k | B  | g  | family    | src |
|-----|-----|-----------|---------|--------|------------------------------|-------|---|----|----|-----------|-----|
| C01 | 125 | (75,125)  | (5,20)  | (1,0)  | (7/5,2)                      | (3,5) | 1 | 25 | 5  | F2, j=1   | 17:1805 |
| C02 | 126 | (84,126)  | (7,35)  | UNPRINTED | (19/7,5)                  | (2,3) | 2 | 42 | 7  | sporadic L1 | 17:1828 |
| C03 | 126 | (126,84)  | (12,30) | UNPRINTED | (16/3,10), (11/6,3)       | (3,2) | 1 | 42 | 6  | sporadic L2 | 17:1854 |
| C04 | 128 | (96,128)  | (8,24)  | (2,0)  | (14/4,6), A1'=(5/4,0), (19/8,3) | (3,4) | 1 | 32 | 8 | F24, j=0 | 17:1814 |
| C05 | 132 | (88,132)  | (11,33) | UNPRINTED | (19/4,8)                  | (2,3) | 1 | 44 | 11 | sporadic L1 | 17:1835 |
| C06 | 135 | (135,90)  | (9,36)  | UNPRINTED | (17/9,4)                  | (3,2) | 2 | 45 | 9  | sporadic L1 | 17:1833 |
| C07 | 135 | (90,135)  | (9,36)  | UNPRINTED | (17/9,4)                  | (2,3) | 3 | 45 | 9  | sporadic L1 | 17:1834 |
| C08 | 135 | (90,135)  | (12,33) | UNPRINTED | (11/3,8)                  | (2,3) | 1 | 45 | 3  | sporadic L1 | 17:1836 |
| C09 | 135 | (90,135)  | (9,36)  | UNPRINTED | (9,24), (11/3,8)          | (2,3) | 1 | 45 | 9  | sporadic L2 | 17:1851 |
| C10 | 140 | (84,140)  | (7,21)  | (1,0)  | (11/7,2)                     | (3,5) | 1 | 28 | 7  | F9, j=1   | 17:1810 |
| C11 | 140 | (56,140)  | (7,21)  | (1,0)  | (13/7,3)                     | (2,5) | 2 | 28 | 7  | F11, j=0  | 17:1811 |
| C12 | 144 | (108,144) | (8,28)  | UNPRINTED | (7/4,3)                   | (3,4) | 1 | 36 | 4  | sporadic L1 | 17:1831 |
| C13 | 144 | (144,96)  | (8,40)  | UNPRINTED | (8,28), (11/4,7)          | (3,2) | 1 | 48 | 8  | sporadic L2 | 17:1849 |
| C14 | 144 | (96,144)  | (12,36) | UNPRINTED | (12,33), (11/3,8)         | (2,3) | 1 | 48 | 12 | sporadic L2 | 17:1855 |
| C15 | 144 | (96,144)  | (12,36) | UNPRINTED | (9,24), (11/3,8)          | (2,3) | 1 | 48 | 12 | sporadic L2 | 17:1856 |
| C16 | 144 | (96,144)  | (12,36) | UNPRINTED | (21/4,9), (19/4,8)        | (2,3) | 1 | 48 | 12 | sporadic L2 | 17:1857 |
| C17 | 144 | (96,144)  | (12,36) | UNPRINTED | (21/4,9), (12/4,5)        | (2,3) | 1 | 48 | 12 | sporadic L2 | 17:1858 |
| C18 | 144 | (144,96)  | (12,36) | UNPRINTED | (12,30), (16/3,10), (11/6,3) | (3,2) | 1 | 48 | 12 | sporadic L3 | 17:1869 |
| C19 | 147 | (42,147)  | (6,15)  | (1,0)  | (7/3,4)                      | (2,7) | 1 | 21 | 3  | F7, j=0   | 17:1807 |
| C20 | 147 | (63,147)  | (6,15)  | (1,0)  | (8/3,5)                      | (3,7) | 1 | 21 | 3  | F8, j=0   | 17:1808 |
| C21 | 147 | (147,98)  | (7,42)  | UNPRINTED | (13/7,6)                  | (3,2) | 2 | 49 | 7  | sporadic L1 | 17:1829 |
| C22 | 147 | (98,147)  | (7,42)  | UNPRINTED | (13/7,6)                  | (2,3) | 3 | 49 | 7  | sporadic L1 | 17:1830 |
| C23 | 150 | (150,100) | (10,40) | UNPRINTED | (16/5,6), (23/10,3)       | (3,2) | 1 | 50 | 10 | sporadic L2 | 17:1852 |
| C24 | 150 | (150,100) | (10,40) | UNPRINTED | (18/5,8), (8/5,3)         | (3,2) | 1 | 50 | 10 | sporadic L2 | 17:1853 |

Row-level verbatim notes [VERIFIED]:
- C17's middle entry is printed "(12/4,5)" [17:1858], an UNREDUCED fraction (12/4 = 3).
  Transcribed verbatim; whether it is intentional (l = 4 bookkeeping) or a typo is
  UNVERIFIED. The parallel entry in C16 is (19/4,8), so l = 4 bookkeeping is plausible.
- C04's A1' is printed "(5/4,0)" [17:1715], with second coordinate 0 (unlike F22's
  A1' = (5/4,2) [17:1713]). Transcribed verbatim.
- The family-table A0'/A1 data for C01/C04/C10/C11/C19/C20 comes from the section 5
  tables [17:1678-1694] (F2 at 17:1679, F7 at 17:1684, F8 at 17:1685, F9 at 17:1686,
  F11 at 17:1688) and [17:1709-1715] (F24 at 17:1715).

## 1.3 What is printed vs what must be derived, per column

- A0, chain, (m,n), max deg: [VERIFIED] printed for all 24 rows at the cited lines.
- A0' for the 18 sporadic rows: NOT PRINTED anywhere in [GGHV17] section 6 (the tables
  have no A0' column) nor in [GGHV22] (which stops below 125). DERIVATION NEEDED:
  A0' is part of the admissible-chain output (C_0 = (A_0, A_0')) of Algorithm 8 /
  "GetCompleteChains" ([GGHV17] section 2); re-running the chain enumeration with
  degree bound 150 is the only faithful way to recover it. Precedent: for the open
  case (8,28),(11/4,7) the value A0' = (1,0) appears only in [GGHV22]'s Prop 4.3
  figure, not in the [GGHV17] table (GGHV dossier section 7.1). Do NOT guess (1,0)
  for the others; (2,0)-type values occur (F12, F13, F22-F24).
- k for family rows: [VERIFIED] printed in the F-tables. k for sporadic rows:
  [DERIVED] from the printed equation (3.17) of [GGHV17] Prop 3.2 in the form
  k = n(bl-a)/((m+n)b - 1) with (a/l, b) the final corner; every one of the 18 values
  came out a positive integer (a nontrivial consistency check of the transcription).
  These derived k are needed by Phase B (they enter the [GGV1, Prop 8.2]-style
  endpoint dichotomy: compare k = 1 forced in [22:1132-1136] for the open case).
- Degree pairs: [DERIVED] as (mB, nB); all 24 max values match print.
- gcd(A0) = g: [DERIVED]; relevance: in all four [GGHV22] reduced cases the Cor 7.4
  exponent q equaled gcd of the swapped corner ((8,28): q = 4 [22:1013]; (9,27): q = 9;
  (9,24): q = 3; (7,21): q = 7; GGHV dossier sections 2-3). The pattern q = g is OUR
  observation, not a printed theorem; per-case q must be recomputed from
  en_{rho0,sigma0}(F) = (p/q)(a,b) in the actual chain data. DERIVATION NEEDED per case.

## 1.4 Reduction data: what the papers state, and the derivation program

[VERIFIED, negative result] NEITHER paper prints, for ANY of the 24 configurations
above: an initial Newton polygon corner list (the "Step 0" shape), a forced edge form,
a leading-form factorization, a reduced polygon, or a reduced commutator. [GGHV22]'s
Propositions 4.1-4.4 (the only Prop-4.3-style reduced polygons in print) cover exactly
the four sub-125 survivors (9,27), (9,24), (8,28), (7,21) and nothing else. Therefore
every reduced polygon for C01-C24 must be DERIVED through the pipeline; the papers
supply the pipeline itself plus per-case inputs (A0, chain, (m,n), k) only.

Pipeline inputs and steps (each step's citation is to text we or the GGHV dossier
verified in the LaTeX sources):

1. Step 0 (initial shape). The corners of N(P), N(Q) are a common polygon
   {(0,0), A0', A0, (0,c)} scaled by m and n respectively; [GGHV22] proves this
   per-case (e.g. [22:1009-1010] for (8,28): {(0,0),(1,0),(8,28),(0,4)} times (3,2)).
   The fourth corner (0,c) is NOT given by a printed closed formula ((8,28) -> (0,4);
   (9,27) -> (0,9); (9,24) -> (0,6); (7,21) -> (0,7); no obvious single rule; the
   per-case proofs use [GGV1]/[GGV2] machinery). DERIVATION NEEDED per configuration;
   this is the first genuinely mathematical (not mechanical) step of the sweep.
2. Swap x <-> y and apply [GGV1, Corollary 7.4] to the A0-edge direction: compute
   en_{rho0,sigma0}(F) = (p/q)(a,b), extract q, forcing l_{rho,sigma}(P) = lambda R^{qm}
   with en(R) = (a/q, b/q) (for (8,28): (rho0,sigma0) = (-1,4), en = (21,6) = (3/4)(28,8),
   q = 4, en(R) = (7,2) [22:1012-1015]). DERIVATION NEEDED: per-case direction and q.
3. Constrain Pred_P(1,0) via [GGV6, Prop 2.5] and/or Algorithm 1
   "PossibleStartingPoints" ([GGHV22] p.8; transcribed in full in the GGHV dossier
   section 5, Phase B3). Branch on the factor multiplicities of the forced lower-edge
   form ([22:1073-1090] pattern: one vs two distinct linear factors, giving the
   a/b/c-style branch trichotomy). DERIVATION NEEDED: per-case branch list; there is
   no a priori guarantee of exactly three branches for the new cases.
4. Cut edges by y -> y + lambda x^{-k} automorphisms of L^(l); top-edge forced form
   analog of "y (x^4 y - alpha)^7" [22:1132]. Kill branches with
   [vdE, Prop 10.2.6] and [GGV2, Prop 3.12](2) where applicable.
5. Opposite-vertex arithmetic + [GGV1, Prop 8.2]: candidate (a,b) list, divisibility
   filter, k in {1,2,...} dichotomy, parallelism forcing (the k values of our table
   feed here). DERIVATION NEEDED per case.
6. Final inversion x -> x^{-1}, y -> x^c y; chain rule [phi(P), phi(Q)] = -[P,Q] x^{c-2}
   [22:1229 pattern]. CRITICAL for the sweep: the reduced commutator is NOT always x.
   The (8,28) case ended at [P,Q] = x^2; the c for each new case comes out of step 4-5
   geometry, so the reduced bracket target x^{c-2} is per-case DERIVATION NEEDED.
   Any machine sweep that hardcodes [P,Q] = x will be silently wrong on cases like C13.

Head starts the printed record does give:

- C13 ((8,40),(8,28),(11/4,7),(3,2), max 144) ends in the SAME final corner and (m,n)
  as the open (72,108) case, k = 1 [DERIVED]. Its sibling (8,32),(8,28),(11/4,7),(3,2)
  (max 120) was discarded in [GGHV22] section 3 WITHOUT reaching a reduced polygon,
  via a Cor 7.4 forcing l_{1,0}(P) = lambda(x^2 y^7 (y-1))^{4m} and [GGV2, Prop 3.29]
  (GGHV dossier section 7.1). Testing whether that section-3 argument extends to
  (8,40) is the cheapest first attack on C13. If it does not, C13's reduction plausibly
  lands near our (72,108) reduced systems (same final corner), where our certificate
  machinery is already tooled. Both statements are conjectural: DERIVATION NEEDED.
- C08, C09, C14, C15 end in final corner (11/3,8), the same final corner as F17 and as
  the discarded (9,27)/(9,24) chains whose reductions are Props 4.1/4.2 and whose
  killed systems are [GGHV22] section 5 (Theorem 5.1 with [P,Q] = x + g(y)). The
  section 5 machinery is the natural template for these four; whether Theorem 5.1's
  en/st hypotheses generalize to (m,n) = (2,3) at B = 45, 48 (P-side polygon scaled
  differently) is DERIVATION NEEDED, not a printed fact.
- C16, C17 pass through (21/4,9); C23, C24 and C03/C18 end in corners with l = 10, 6;
  these have no printed sibling reductions at all: fully new Phase B runs.
- Family rows C01, C10, C11, C19, C20 (A0 in {(5,20),(7,21),(6,15)}) have DISCARDED
  smaller siblings in their own families (F2 j=0 = 75 discarded in [GGV3] section 5;
  F9 j=0 = 84 discarded in [GGHV22] section 6 via [GGV6, Thm 7.3], see GGHV dossier
  7.4; F7/F8 j=0 ARE C19/C20, nothing smaller). The F9 j=0 discard's factor analysis
  (l_{7,-2}(P) = lambda((z^7-lambda1)^2(z^7-lambda2))^m etc.) is the closest printed
  model for C10. C04 (F24) and C11 (F11, the only k = 2 family row in range) have no
  discarded siblings and no printed reduction data whatsoever.
- C02's mirror family: [VERIFIED] the remark [17:1788-1790] says the F13 j=1 case was
  analyzed extensively by Orevkov (reference [O], Lemma 4.1(a)); F13 j=1 is outside
  our range (max 600) but Orevkov's methods are flagged by the paper itself as
  relevant prior art for sporadic chains.

## 1.5 What [GGHV22] adds or refines for this range

1. [VERIFIED] Theorem 2.1 [22:286-289]: the floor statement that makes this list the
   frontier. Nothing else in [GGHV22] touches max deg >= 125.
2. [VERIFIED] The reduction template (Props 4.1-4.4 + sections 5-6 systems) that our
   pipeline (1.4) instantiates; transcribed in the GGHV dossier sections 2-5.
3. [VERIFIED] Family exclusions ALREADY done in [GGHV17] itself, which shrink nothing
   in our range but matter for bookkeeping: F18-F21 cannot arise from a standard
   (m,n)-pair ([17:1726-1786], the (6,3) last-lower-corner contradiction via
   [GGV2, Remarks 3.2 + 3.29] and [GGV1, Prop 6.5]); the F22 (2,3) case is discarded
   by Proposition "caso antisimetrico" [17:1874-1927]. No F18-F22 member lies in
   [125,150] anyway ([DERIVED]: smallest F22 member above 96 is (3,5) at 160;
   F18/F20 smallest are 168/210).
4. Verbatim quote to keep the target honest [VERIFIED, 22:276-277]: "With enough
   computing power we would be able to raise it up from 108 to 125, since there is
   only one case left." GGHV promise 125, not 150; everything beyond 125 is new
   territory where even the reduced polygons are unpublished.

## 1.6 Sweep-facing summary

To push the floor from 125 toward 150 the machine program needs, in order:
(i) re-run the chain enumeration (Algorithms 1-9 of [GGHV17], all pseudocode printed)
with bound 150 to recover the UNPRINTED A0' and direction data and to independently
confirm the 34-row census; (ii) per configuration, derive Step 0 (the only step with
no printed algorithm); (iii) run Phase B to get reduced polygons + reduced bracket
x^{c-2} per case; (iv) instantiate the certificate machinery per reduced system.
Expected cheap wins first: C13 (section-3-style discard or open-case-adjacent
reduction), then C08/C09/C14/C15 (Theorem 5.1 template). The 24 rows double to 48
with (m,n) mirrors; mirrors share reductions up to transposition (same caveat as the
(72,108)/(108,72) orientation remark, which for these cases must be re-verified
per case, not assumed).

====================================================================
# PART 2. Adversarial audit of the (72,108) closure chain
====================================================================

Materials examined: program/jacobian-conjecture/72108-closure-statement.md (the
VALIDATED statement), the GGHV dossier, 72108-assembly-checklist.md (sessions 32/36),
experiment verdicts EXP-052 through EXP-062, EXP-063 hypothesis + artifacts, git
status/log of the working tree at audit time. Posture: hostile referee. Nothing below
is softened.

## 2.0 The headline finding

THE EVIDENCE CHAIN CITES WORK THAT DOES NOT EXIST IN THE RECORD. The validated
closure statement cites "EXP-062/063" for axis-symbolic interior generality (item 7)
and "EXP-063 remark + spot check" for orientation (item 8). As of this audit:
EXP-063 has a hypothesis.md and run.py, its artifacts/output-2026-07-22.txt is EMPTY
(zero bytes), it has NO verdict.md, and the entire EXP-063 directory is UNTRACKED in
git (?? in git status). Meanwhile the manuscript already gained the closure section
(commit f27ccf4). Concretely: the interior sweep stands at 4 of ~30 case-c points
(EXP-062 item 3), the a/b interior points have NO axis-symbolic certificates at all
(EXP-061: two numeric samples per chart, upgrade "queued"), and the orientation
spot-check was never run. A referee who diffs the statement against the artifacts
finds this in ten minutes. Either run EXP-063 to completion and commit it, or amend
the statement's evidence chain before ANY external use.

## 2.1 (a) Logical dependencies on GGHV's published text, and citation status

D1. [GGHV22] Theorem 2.1 (every case except (72,108) with max deg < 125 is discarded).
    Load: without it the closure raises nothing; it is half the floor-raise.
    Citation status: GGHV dossier cites it by page (p.2) WITHOUT a tex line. Now
    supplied: [22:286-289]. PARTIAL until the dossier is updated.
    Deeper exposure: Theorem 2.1's own proof depends on the (9,24) = (66,99) discard,
    and the GGHV dossier itself records ([UNVERIFIED / gap noted], section 4.2) that
    NO printed corollary specializes Theorem 5.1 to the three Prop 4.2 polygon
    classes; the bridging is claimed only in the intro and section title. Our floor
    claim INHERITS this published-record gap and the statement does not mention it.
D2. The open-case identification ((8,28),(11/4,7),(3,2) is the unique sub-125
    survivor). Citation status: GOOD; [22:251-252, 255-268, 304-320] in the dossier,
    plus [17:1832] for the chain row (supplied by Part 1 above; the dossier had only
    a page reference p.27).
D3. Prop 4.3 statement (reduced polygons, L^(1), [P,Q] = x^2). Citation status: GOOD;
    [22:1000-1007], re-verified verbatim today. This is the single load-bearing
    reduction: the entire certificate program runs on these polygons.
D4. Prop 4.3 PROOF internals used beyond the statement: the a/b/c branch trichotomy
    [22:1073-1090], the forced top-edge form and its cut [22:1132], the Prop 8.2
    step k = 1 [22:1132-1136], the intermediate polygons [22:1137-1186], the final
    inversion and bracket bookkeeping [22:1229]. Citation status: GOOD (tex-lined in
    the dossier). BUT: our closure uses the proof's intermediate forcings as
    constraints on the reduced pair (the forced families), which is legitimate only
    under the reading that the constructed reduced P,Q is the image of the original
    pair through the printed transformations (true as written) AND that the branch
    enumeration is exhaustive. Exhaustiveness of a/b/c is asserted by the proof's
    case split on Pred values; we did not independently re-verify that the printed
    case split covers all Pred possibilities. UNVERIFIED beyond trusting the proof.
    Also note the printed edge-name mismatch at [22:1132] ({(28,8),(1,0)} vs
    {(28,8),(0,1)}), resolved by our interpretation; flagged in the dossier but the
    closure statement does not carry the flag.
D5. The verbatim-edge claim (statement item 6): "y^8 (xy - t)^8 is the VERBATIM
    forced form under GGHV's stated inversion". Citation status: the INPUTS are
    tex-lined (D4), but the mapping computation itself (factor (x^3 y - alpha_2)^{4m}
    -> (xy - t)^8 with the y^8 prefactor assembled from the shifted alpha_1 factor
    and x-powers) is a session-36 HAND computation recorded in the checklist with no
    machine artifact. I re-derived it during this audit and it checks, but the record
    has no independent verification artifact. WEAK LINK in an otherwise
    machine-certified chain.
D6. The right-edge structure R = x^4 y^7(a_0 + a_1 y) with l_{1,0}(P) = R^2,
    l_{1,0}(Q) = R^3, used to parametrize the EXP-061 a/b charts and the checklist's
    item 2. Citation status: NOT GGHV text at all. The dossier flags it [DERIVED]
    (section 2.2 sanity check and section 4.4): the analog of [GGV1, Props 1.13/2.1]
    applied to a case with commutator x^2 in L^(1). Neither [GGV1] proposition has
    been transcribed or its hypotheses checked for this setting (the dossier itself
    warns the x^2 bracket "breaks" parts of the section 5/6 template). If the R^2
    forcing is unsound here, the a/b chart parametrization and its vanishing-locus
    bookkeeping change. Mitigation available in the record: the checklist claims
    certificates over FREE edge coefficients "subsume the relation", which if the
    runs truly kept the edge coefficients free demotes D6 from load-bearing to
    cosmetic; the EXP-061 verdict's chart language (a0, a1 symbolic per chart) is
    consistent with free coefficients but does not state which lattice points on the
    right edge (e.g. (8,15)) were free vs forced. NEEDS an explicit statement.
D7. The N() convention: our vanishing-locus exclusions (a0 = 0 excluded because
    (8,14) "is a VERTEX", EXP-061; beta = 0 similarly, EXP-062) require that
    "N(P) = {corner list}" in Prop 4.3 means the polygon EQUALS the listed hull,
    i.e. vertex coefficients are nonzero. [GGHV22] does not redefine N(); the
    convention is inherited from [GGV1] (arXiv:1401.1784), which we have NEVER
    transcribed. If N(P) = {...} tolerated degenerate vertices, the excluded loci
    (a0 = 0 etc.) would be live cases needing their own certificates. UNVERIFIED;
    one tex line from [GGV1] closes it.
D8. Background propositions inside Prop 4.3's proof ([GGV1, Cor 7.4 / Prop 8.2],
    [GGV2, Prop 3.12], [GGV6, Prop 2.5], [vdE, Prop 10.2.6]). Never transcribed;
    the closure is explicitly conditional on Prop 4.3 as published, which the
    statement's residuals DO say. Acceptable as a stated conditionality, but note
    the condition is really "Prop 4.3 and its entire citation tree".

## 2.2 (b) Axis-symbolic or sampled evidence, exhaustively, vs the Honest residuals

Inventory of every non-fully-symbolic link (statement's evidence items in order):

1. EXP-052 (item 2): 5 sampled P's. Statement says "sampled emptiness" honestly. OK.
2. EXP-053 (item 3): t symbolic, but only 3 lower strata SAMPLED; the "constant 576"
   universality claim was subsequently REFUTED by EXP-054 (covector not rigid).
3. EXP-055/056 (item 3): first-order correctors symbolic (26/26); second order
   250/250; TERMINATION REFUTED at orders 1 and 2; order-3 residuals 17 percent
   nonzero; ladder never completed. The stratum-wide universal certificate does not
   exist in the record.
4. EXP-057/058 (item 4): rank 124 / kernel = constants verified at FOUR SAMPLED t
   values (1, 2, -3, 5/7); EXP-058's own caveat says kernel dimension could jump at
   special t. The all-orders solvability lemma itself ([m,1] = 0) is genuinely
   symbolic and clean; only the rank-124 side is sampled. Also: kernel computed for
   the bare-stratum P0 on the RESTRICTED row pool, not for general P.
5. EXP-059 (not cited by the statement, correctly): 40 sampled determinants; its own
   verdict states the chart-covering argument is "REQUIRED, not optional" and it was
   never done. Fine as long as nothing cites it.
6. EXP-061 (item 5, cases a/b): pairings symbolic in the two chart variables a0/a1,
   but INTERIOR coefficients at TWO SAMPLES per chart; the promised axis-symbolic
   upgrade for a/b was queued and NEVER RUN (EXP-063 empty). The Q-side coverage is
   an argument (bigger-polygon emptiness), not a run; the argument is sound for
   fixed P but note it imports the case-c-family P coverage limitations.
7. EXP-062 (item 5, case c): t-gauge verified on ONE orbit sample plus a stated
   one-line chain-rule identity (not machine-checked in general); beta symbolic;
   interior 4 of ~30 points axis-symbolic; rest queued, never run.
8. EXP-063 (items 7-8): DOES NOT EXIST as evidence (empty artifact, no verdict,
   untracked). See 2.0.
9. The beta = 0 hand-off (EXP-062 item 2): at beta = 0 the case-c family degenerates
   and the verdict says "the EXP-053/055 stratum certificates take over", i.e. the
   hand-off target is the NON-UNIVERSAL (first-order-only) stratum evidence. A locus
   of the forced family is thus covered only by sampled/perturbative evidence, and
   this hand-off is not itemized in the residuals.

Cross-check against the statement's Honest residuals section: it declares (i) the
axis-vs-simultaneous gap, (ii) the Prop 4.3 conditionality, (iii) the H-pool caveat.
It does NOT declare: the EXP-063 nonexistence (worse: the evidence chain cites it as
if complete); the 4-of-~30 partiality of the case-c axis sweep; the ZERO axis
coverage on a/b interiors; the beta = 0 hand-off to non-universal evidence; the
sampled-t rank/kernel basis of item 4; the one-sample gauge verification; D1's
inherited (66,99) bridging gap; D6's derived (not published) right-edge forcing; D7's
unverified N() convention. The residuals section is therefore INCOMPLETE as a
referee-facing disclosure, even though its two named residuals are accurately
described. One correct note in our favor: the H-restricted row pool is NOT a
soundness caveat for the certificates themselves (an inconsistent subsystem makes
the full system inconsistent); it limits only the ladder/kernel constructions. The
statement could claim this affirmatively instead of leaving "pool-boundary caveats"
vague.

## 2.3 (c) The forced families vs the full generality Prop 4.3 requires

The decisive question: what does Prop 4.3 actually FORCE, and over what set must
emptiness be proved?

1. The STATEMENT of Prop 4.3 [22:1000-1007] forces only: P, Q in L^(1), [P,Q] = x^2,
   and N(P), N(Q) equal to the listed polygons (two cases). It forces NO interior
   coefficients, NO edge factorizations. Read alone, closure requires emptiness for
   ALL coefficient assignments on those polygons (vertex coefficients nonzero under
   the D7 convention; every other lattice point, including edge-interior points,
   completely free).
2. The PROOF additionally forces edge forms (a/b/c branches, forced top edge, k = 1
   dichotomy). Using them is legitimate (D4 caveats aside), and shrinks the required
   set to the union of the three forced families. Our closure argument lives here.
   But the referee must be told explicitly that the closure is proved on the
   proof-strengthened families, not the bare statement, with the exhaustiveness of
   the branch split (D4) as an inherited dependency.
3. Within the forced families, the interior coefficients remain FULLY FREE
   parameters. Prop 4.3 does NOT force them, ever. So the closure must hold for ALL
   interior values. What the record certifies: every sampled point (dozens across
   EXP-052..062, all inconsistent); each coefficient one-at-a-time symbolic at 4 of
   ~30 case-c points; NOTHING one-at-a-time on a/b; first-order-only perturbative
   universality on the pre-gauge stratum. Axis-symbolic + samples does NOT imply
   emptiness over the full parameter space: the consistent locus, if nonempty, is a
   proper closed subvariety, and axis slices plus finitely many samples can miss a
   positive-dimensional component entirely (the EXP-054 refutation is this program's
   own proof that extrapolating from slices fails). Conclusion: AS A THEOREM, the
   closure is NOT proved. As stated ("machine-certified closure ... no Jacobian
   pair of degrees (72,108) exists", headline of the statement), it overclaims
   relative to its own residuals section; the honest form is "certified on the
   forced families at every tested point and along every tested one-parameter
   slice; the simultaneous-symbolic certificate is outstanding".
4. Two boundary strata deserve explicit adjudication and currently have none:
   (i) beta = 0 (hand-off to non-universal stratum evidence, 2.2 item 9);
   (ii) the t = 0 wall: the case-c family has t != 0 (two distinct factors) and
   cases a/b are NOT the t = 0 limit of the stratum parametrization (they live on
   the smaller case-2 polygons); the record covers a/b separately (good), but no
   written argument states that {case c, t != 0} union {a, b} exhausts case (1) and
   case (2) of Prop 4.3 down to every degeneration the statement's polygons permit.
   The checklist's subset arguments cover the Q side; the P-side degeneration lattice
   (which vertex coefficients can vanish without leaving Prop 4.3's hypotheses) is
   exactly the D7 question.
5. Orientation: the Q -> -Q sign absorption argument is mathematically trivial and
   correct as written in the EXP-063 hypothesis; but it is RECORDED nowhere that has
   evidentiary status (empty artifact). One linsolve run plus a verdict closes it.

## 2.4 (d) Ranked hardening tasks before any external claim

1. RUN EXP-063 IN FULL and commit it: all remaining case-c interior points
   axis-symbolic (~26), the ENTIRE a/b interior axis sweep (currently zero), the
   orientation spot-check, verdict.md, git add. Until then, amend the closure
   statement's items 7-8, which cite nonexistent evidence. (Hours of compute;
   removes the audit's headline finding.)
2. The simultaneous-symbolic interior certificate, or a finite substitute. Three
   routes already identified in the record: (i) prove ladder TERMINATION on the
   fixed pool (solvability is done via k = 1); (ii) the EXP-059 chart-covering
   argument (finitely many 125x125 minors whose nonvanishing loci cover the
   parameter space: finite, checkable, and the row-set-changed trials already
   exhibit alternative charts); (iii) direct Groebner/QE on the reduced systems per
   forced family (small: 61 P-parameters, 125 Q-unknowns, linear in Q, so this is
   really rank[M|r] > rank[M] as a constructible-set statement; eliminating Q makes
   it a symbolic rank condition in <= 61 parameters). Without one of these, the
   claim must stay "at every tested point", not "no pair exists".
3. Close D7 with one tex line from [GGV1] (N() equality convention / vertex
   nonvanishing), since every vanishing-locus exclusion in EXP-061/062 leans on it.
   If the convention is containment, enumerate and certify the degenerate strata.
4. Machine-verify the session-36 verbatim-edge mapping (D5) and record which right
   edge coefficients were free in EXP-061 (D6). If any were forced by the derived
   R^2 relation, either re-run with them free (strictly stronger, small systems) or
   transcribe [GGV1, Props 1.13/2.1] from arXiv:1401.1784 and verify their
   hypotheses under commutator x^2.
5. Write the branch-exhaustiveness note (D4): one paragraph mapping the printed
   Pred case split [22:1073-1090] to the a/b/c families plus the [22:1132] edge-name
   mismatch resolution, so the referee sees the proof-strengthening step and its
   textual basis in one place. Include the t != 0 / beta = 0 stratum-boundary
   adjudication (2.3 item 4).
6. Add the D1 disclosure: the floor-raise inherits GGHV's published-record gap on
   the (9,24) = (66,99) bridging (no printed corollary from Theorem 5.1 to the
   Prop 4.2 classes); update the dossier with Theorem 2.1's tex line [22:286-289].
   Optionally close the gap ourselves by checking Theorem 5.1's hypotheses against
   the three Prop 4.2 polygon classes (looks mechanical; would make the 125 floor
   independent of the unprinted bridging).
7. Rank/kernel at special t: replace the four sampled t's with a symbolic rank
   statement over QQ(t) (or a discriminant analysis identifying all t where the
   rank drops), for the record's tidiness; jumps only add kernel and thus only add
   solvability conditions, so this is low risk but currently sampled.
8. Pool-boundary re-verification: re-run the headline certificates (576, 200 a0^3,
   23592960 beta, 368640) on an enlarged row pool once, to show insensitivity; and
   state affirmatively in the manuscript that row restriction is sound for
   inconsistency certificates.
9. External audit path (after 1-8): offer the certificate bundle to GGHV, as the
   statement itself proposes; their referee eyes on Prop 4.3's role would discharge
   the conditionality more credibly than anything we can do internally.

Ranking rationale: 1 is a record-integrity defect (cited evidence missing);
2 is the mathematical gap between "certified everywhere we looked" and "closed";
3-5 are soundness dependencies of the existing certificates; 6-8 are disclosure and
robustness; 9 is strategy. Items 1, 3, 4, 5 are cheap (hours to a day). Item 2 is
the only one that can genuinely fail, and if route (ii) or (iii) works it also
retires most of item 8.

## Source hygiene

- Temp downloads lived in E:\_Temp\jc-arxiv and are deleted after this dossier.
- All [17:NNNN]/[22:NNNN] line numbers were read in the extracted e-print tex files
  today; the [GGHV22] numbers agree with the prior dossier's where they overlap
  (Prop 4.3 at 22:1000-1007 re-confirmed verbatim).
- Nothing in Part 1 beyond the printed tables was asserted without a [DERIVED] or
  DERIVATION NEEDED flag; the k values for sporadic rows and all degree pairs are
  derived; A0' for all 18 sporadic rows is UNPRINTED in the primary sources.
