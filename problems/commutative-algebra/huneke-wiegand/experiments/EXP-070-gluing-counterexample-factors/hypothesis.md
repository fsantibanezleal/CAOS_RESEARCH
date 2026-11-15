# EXP-070 hypothesis: the gluing factorization on factors that are counterexamples

Date: 2026-11-14. Frozen before any code of this experiment is written or run.

## Why

EXP-068 proved that for a gluing `Gamma = a1*Gamma1 + a2*Gamma2` and relative ideals `A_i` of `Gamma_i`, the extension
`A = a1*A1 + a2*A2` satisfies `T = T1 (x)_(k[y]) T2` with `T_i = I_(A_i) (x) I_(A_i*)`, the torsion-length law
`l(tau(T)) = a1*l(tau(T1)) + a2*l(tau(T2)) + sum_(j>=1) b1(j)*b2(j)`, `mu(A) = mu(A1)*mu(A2)`, and that `A` is
Huneke-Wiegand iff `A1` or `A2` is a non-principal Huneke-Wiegand ideal. Its seeded validation (200 small gluings,
factor Frobenius numbers at most 10) never contained a factor that is a counterexample, a non-principal ideal whose `T`
is torsion-free, which is the case the gluing paper (`manuscripts/huneke-wiegand/gluing-extensions`, v0.01, Corollary
5.2) is about. The independent audit of 2026-11-10 (CAOS_MANAGE `wip/caos-research/msaudit-hw-other-2026-11-10.md`, D2
finding 1 and plan item 1) asks for a validation whose factors include counterexample ideals. This experiment is that
validation; it changes no claim of EXP-068.

## Instrument

- Producer: `code/hwcert/gluing.py` (`semigroup_mask`, `ideal_from_generators`, `minimal_generators`, `dual`,
  `tensor_torsion` with the Jordan type of `y`, `is_huneke_wiegand` by the partition criterion, `glue_generators`,
  `extension_generators`, `predicted_length`, `hilbert_identity_holds`, `is_extension`), as EXP-068 `run.py` uses it.
- Independent route: the direct torsion length and the Huneke-Wiegand predicate of EXP-068 `audit.py` (plain integer
  sets and breadth-first search; shares no code with `hwcert.gluing`), imported from that file.
- Large factors (each with its ideal, the status of that ideal recomputed in this run):
  - B1: Pham's semigroup `Gamma_P` (the 26 generators of EXP-068 `run.py`, multiplicity 56, Frobenius 181), ideal
    `(0,14)`, a counterexample;
  - B2: the CAOS family member `C_4` (EXP-009 `audit.py` `independent_mask(4)`: 44 generators, multiplicity 96,
    Frobenius 311), ideal `(0,24)`, a counterexample;
  - B3 (control): `Gamma_P` with ideal `(0,1)`, a non-principal Huneke-Wiegand ideal;
  - B4 (only if the budget allows after B1 to B3): `C_5` (55 generators, multiplicity 120, Frobenius 389), ideal
    `(0,30)`.
- Small partners `S` with their ideals: `<2,3>`, `<2,5>`, `<3,4>`, `<3,5>`, `<3,4,5>` and `<4,5,6,7>`, each with the
  principal ideal `(0)` and the relative ideal `(0,1)` (1 is a gap of each); the Huneke-Wiegand status of every partner
  ideal is computed, not assumed.
- Gluing parameters: `Gamma = a1*Gamma_B + a2*S` with `a1` the least nonzero element of `S` and `a2` the least element
  of `Gamma_B` coprime to `a1` (so `a1` is in `S`, `a2` is in `Gamma_B`, `gcd = 1`). This gives 36 cases for B1 to B3
  and 12 for B4.

## Predictions

- P1 (torsion-length law): on every case, the torsion length of `T` computed directly on the glued semigroup equals
  the law computed from the two factors alone. For a counterexample factor `l(tau(T_B)) = 0`, so the cross term is 0
  and the prediction is `a2*l(tau(T_S))`.
- P2 (characterization): on every case the partition-criterion predicate of `A` equals the factor rule, agrees with
  `l(tau(T)) > 0` for non-principal `A`, and `mu(A) = mu(A_B)*mu(A_S)`. In particular every case with a counterexample
  factor and the principal partner ideal is a counterexample (non-principal, torsion length 0), and every case with a
  non-principal Huneke-Wiegand partner ideal is Huneke-Wiegand.
- P3 (independent route): the torsion length and the predicate of EXP-068 `audit.py` agree with the producer on every
  case it completes within its per-case limit (900 s); the cases it does not complete are listed.
- P4 (Hilbert identity): `H_A(z) = H_(A_B)(z^a1) H_(A_S)(z^a2) (1 - z^(a1*a2))` on every case.
- Controls:
  - C1 (not a gluing): for each of B1 and B2 with `S = <2,3>`, replacing `a1` by a gap of `S` coprime to `a2` must break
    the Hilbert identity or be refused by the constructor;
  - C2 (not an extension): for the case B1 x `<2,3>` with the principal partner ideal, adding 1 to the largest minimal
    generator of the extension ideal must make `is_extension` false; the Huneke-Wiegand status of the perturbed ideal is
    reported, not assumed.

## Out of reach, declared now

The direct torsion of a gluing of two counterexample factors (the paper's Examples 5.4 and 5.5, Frobenius 23,645 and
53,599) is not computed: `tensor_torsion` enumerates the pairs of every degree up to about
`maxgen(A) + c(Gamma) + c(A*)`, more than `10^9` pairs for those instances, beyond this budget. They remain consequences
of the proved theorem, checked by the partition criterion in EXP-068 P3. The run records the window size of each case
so this cost model can be checked.

## What PASS and FAIL prove

- PASS: the law and the characterization hold, by two routes that share no code, on gluings in which one factor is a
  counterexample (both the published Pham ideal and the CAOS family member), including the case in which the extension
  is itself a counterexample; this is the case the gluing paper is about.
- FAIL of P1 or P2 on any case: a counterexample to EXP-068's theorem or a defect in the instrument; the case is
  re-run by the independent route and reported before any reading.

## Budget

Three hours of wall time, at most 10 worker processes (another job uses 14 of the 32 logical processors), no WSL.

## Premise dependencies

- EXP-068 (CONFIRMED, `verdict.md`, `proof.md`): the theorem under test and the producer and auditor routines.
- Pham's ideal `(0,14)` is a counterexample (Pham, arXiv:2609.07615; EXP-068 run log); `C_4` with `(0,24)` is a
  counterexample (EXP-009, CONFIRMED). Both statuses are recomputed in this run by the partition criterion and by the
  factor torsion length, and the run stops if either differs.

## Kill criterion

Three hours of wall time. A case whose producer computation exceeds 1,800 s is recorded as not completed; B4 is skipped
if B1 to B3 are not done after two hours. A verdict covers only the completed cases.

## Invariant-first note

Two cheap invariants were considered: the Hilbert-series identity decides that `A` has the extension structure but not
its torsion, and the partition criterion decides the Huneke-Wiegand predicate but not the torsion length. Neither tests
the length law, so the direct torsion computation is required.
