# EXP-068 hypothesis: tensor factorization of extension ideals under gluing

Date: 2026-10-30. Frozen after the source preflight and before the producer, the independent auditor
or any manuscript text is written.

## Source preflight (methodology 12)

- García-Sánchez and Leamer, arXiv:1211.4554v1 (2012), read in full from the source archive whose
  SHA-256 `b9e6421057d9892181f15c5df648036585b5e7420f442d6e234f308583d23d54` matches the pin in
  `context/2026-08-02-frontier-source-and-proof-audit.md`. Section 2 proves Lemma 8 (sums,
  intersections, colons and duals of extensions `a1*A1 + a2*A2`), Proposition 9 (if `A1` is a
  non-principal Huneke-Wiegand ideal then every extension `a1*A1 + a2*B` is Huneke-Wiegand),
  Proposition 10 (`a1*A1 + a2*Gamma2` is Huneke-Wiegand iff `A1` is) and Theorem 13 (gluings of a
  symmetric semigroup with `N`). Their Future Work asks whether the Huneke-Wiegand property for ideals
  with more than two generators is invariant under gluing, and asks for a ring-level version of
  Proposition 9 for `R1 (x)_k R2 / (f(x)1 - 1(x)g)`.
- Consequence for EXP-067: its symmetry and Apery transfer are standard gluing facts, its
  exponent-set transfer is Lemma 8(8) with `A=(0,s)` and `Gamma2=N`, and its rigidity transfer is
  Proposition 10. EXP-067 is a corollary of the 2012 paper (HWB-094 disposition).
- Goto, Takahashi, Taniguchi, Le Truong, arXiv:1305.4238 (2013), Section 2: change of rings to
  intermediate rings `R <= S <= I:I`; no gluing and no tensor decomposition.
- Leamer, arXiv:1211.2896 (2012): the combinatorial torsion criterion; no gluing.
- Roy, arXiv:1808.06600 (2018): gluing used for a numerical condition on complete intersections; no
  tensor torsion statement.
- Not located in these sources: the case of Proposition 9 left open (both factors non-principal and
  not Huneke-Wiegand), a torsion-length law, or a tensor factorization. This is not a novelty proof.

## Question

Let `Gamma = a1*Gamma1 + a2*Gamma2` be a gluing (`a1` in `Gamma2`, `a2` in `Gamma1`,
`gcd(a1,a2)=1`), `k` a field, `R_i = k[Gamma_i]`, `R = k[Gamma]`, and let `y` act on `R1` as `t^a2`
and on `R2` as `t^a1`. For relative ideals `A_i` of `Gamma_i` put `A = a1*A1 + a2*A2`,
`T_i = I_(A_i) (x)_(R_i) I_(A_i*)`, `T = I_A (x)_R I_(A*)`, and let `tau(.)` be the torsion submodule.
Does the torsion of `T` factor through the torsion of `T1` and `T2`?

## Theorem to prove (written proof in `proof.md`, before the run is read as evidence)

1. `R = R1 (x)_(k[y]) R2`, `I_A = I_(A1) (x)_(k[y]) I_(A2)` and `I_(A*) = I_(A1*) (x)_(k[y]) I_(A2*)`.
2. `T = T1 (x)_(k[y]) T2`.
3. Torsion-length law: `l(tau(T)) = a1*l(tau(T1)) + a2*l(tau(T2)) + l(tau(T1) (x)_(k[y]) tau(T2))`, and
   `l(tau(T1) (x) tau(T2)) = sum_(j>=1) b1(j)*b2(j)` where `b_i(j)` is the number of Jordan blocks of
   size at least `j` of `y` acting on `tau(T_i)`.
4. `mu(A) = mu(A1)*mu(A2)` (minimal generators multiply).
5. Characterization: `A` is Huneke-Wiegand (non-principal with torsion in `T`) iff `A1` or `A2` is a
   non-principal Huneke-Wiegand ideal. Equivalently, `A` is a counterexample (non-principal,
   `T` torsion-free) iff neither factor is non-principal Huneke-Wiegand and not both are principal.

## Falsifiable predictions

### P1: torsion-length law (independent route: direct tensor computation)

On every case of a seeded random family of small gluings and relative ideals (at least 200 gluings,
Frobenius numbers of the factors at most 25, ideals with at most three generators), the torsion
length of `T` computed directly from the definition of `I_A (x)_R I_(A*)` (connected components of
the monomial relation graph in each degree) equals item 3 computed from `T1` and `T2` alone.

### P2: characterization (independent route: Leamer partition criterion)

On the same cases, the Huneke-Wiegand predicate of `A` computed by the partition criterion
(García-Sánchez and Leamer Remark 3 with Leamer Theorem 1.4) equals item 5 computed from the
factors, and both agree with `l(tau(T)) > 0` for non-principal `A`; `mu(A) = mu(A1)*mu(A2)`.

### P3: counterexample products with four minimal generators

Take `Gamma1 = Gamma2 =` Pham's semigroup (multiplicity 56, Frobenius 181) with its counterexample
ideal `(0,14)`, and a coprime pair `a1, a2` in it. The extension `A = a1*(0,14) + a2*(0,14)` has
exactly four minimal generators and is not Huneke-Wiegand by the partition criterion. A second
instance glues Pham's semigroup with the CAOS family member of EXP-009 at `p=4`.

### P4: adverse controls

- Replacing `A2` by a non-principal Huneke-Wiegand ideal of `Gamma2` makes `A` Huneke-Wiegand.
- A pair `a1, a2` violating the gluing condition (`a1` not in `Gamma2`) must break item 1 or item 3
  on at least one small case, or the instance is reported as not a gluing by the constructor.
- Perturbing one generator of the P3 ideal so that it is no longer an extension must be detected
  (the extension test fails), and its Huneke-Wiegand status is reported, not assumed.

## What PASS and FAIL prove

PASS supports the written proof with two independent computational routes and controls; the
theorem rests on the proof, not on the finite cases. FAIL of P1 or P2 on any case refutes the stated
factorization or its transcription and stops the focus until the defect is located. P3 PASS gives
explicit counterexample ideals with four minimal generators over symmetric semigroups.

## Premise dependencies

Leamer Theorem 1.4 (torsion iff the partition criterion), the duality `I_(A*) = Hom_R(I_A, R)` for
relative ideals (Leamer Remark 1.7), Lemma 8 of García-Sánchez and Leamer, Pham's semigroup and
ideal (reproduced in EXP-001), and the EXP-009 family.

## Invariant-first note

Item 4 and the Hilbert-series identity `H_(I_A)(z) = H_(I_A1)(z^a1) H_(I_A2)(z^a2)(1 - z^(a1*a2))`
are single invariants that decide item 1 on each case before any torsion computation.

## Compute budget and kill criteria

Commodity CPU, at most 20 minutes in total, exact integer arithmetic only. Kill if the direct tensor
computation exceeds 10 minutes on the small family (then shrink the family and record it).

## Manuscript gate

PASS triggers a focused companion manuscript, `gluing-extensions`, owning EXP-068 as the main
theorem and EXP-067 as a corollary credited to García-Sánchez and Leamer.
