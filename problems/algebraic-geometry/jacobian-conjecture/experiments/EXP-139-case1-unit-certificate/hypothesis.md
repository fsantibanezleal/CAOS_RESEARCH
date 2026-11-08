# EXP-139 preflight: an exact unit-ideal certificate for Case 1 of GGHV Proposition 4.3 at (72,108) (JCB-103)

Date: 2026-11-06. Status: frozen before any computation. CPU only.

## Question

EXP-137 verified Helali's Case 2 exclusion independently and, for Case 1, matched our own 13 compatibility
equations to his and showed, at five primes, that both branch ideals reduce to the unit ideal (addendum A:
modular evidence, not a proof). Is the Case 1 system empty over the algebraic closure, exactly?

## Method (exact)

Our 13 Case 1 compatibility equations (EXP-137 `p3_link.case1_link`, our cascade; no external data) are
polynomials in the six parameters q0..q5 (q1 is the branch parameter s) with coefficients in
K = Q[u]/(H), H of degree 35 (EXP-137's field). Write each coefficient as its canonical polynomial in u of degree
< 35 with rational coefficients, and form the ideal

    I = ( E_1, ..., E_13, H(u) )  in  Q[q0, ..., q5, u].

A common zero of I over the complex numbers is a root u of H together with a Case 1 solution in the field that
root generates; I = (1) exactly when no root of H admits a Case 1 solution. This does not need H to be
irreducible and needs no branch split (s stays a variable). Singular `std` over Q (exact rational arithmetic);
I = (1) iff the reduced standard basis is {1}.

## Gates

1. The same export, specialized at a prime p and a simple root r of H (u -> r), must reproduce addendum A's unit
   result over F_p at the five primes 1021, 1031, 1033, 1049, 1061.
2. Control: the upper-layer equations only (layers 3..-1) plus H(u) must not give the unit ideal (EXP-137 found
   dimension 4 modulo p).

## Prediction

I = (1) (confidence HIGH, from the modular evidence); the exact computation might not finish within the budget
(confidence in finishing: MODERATE).

## Budget and stop condition

Six hours of one Singular process. If it does not finish, record UNKNOWN with the measured cost and fall back to
a multi-modular cofactor certificate (rational reconstruction of a Groebner cofactor representation of 1,
verified exactly over Q), as a separate experiment.
