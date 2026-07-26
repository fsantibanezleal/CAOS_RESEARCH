# EXP-095: Newton-resolution applicability bridge for the open degree-72 component

## Question

Can the Makar-Limanov--Trakhtenberg Newton-resolution restrictions be applied
to the GGHV open \((72,108)\) case, and if so, do their published
\(D=72\) candidates exclude or retain it?

## Motivation

The final GGHV normalization produces \(P,Q\in K[x,x^{-1},y]\) with
\([P,Q]=x^2\). The Newton-resolution paper instead starts with a polynomial
Jacobian pair \(f,g\in\mathbb C[x,y]\) satisfying \(J(f,g)=1\). A comparison
with the final reduced pair would therefore conflate different rings and
bracket identities.

Before the non-polynomial reductions, however, the GGHV hypothetical pair is
still a polynomial Keller pair. Its degree-72 component has common polygon
factor \(2\), main corner \(A_0=(8,28)\), lower endpoint \(A'_0=(1,0)\), and
final corner \(A_1=(11/4,7)\). These give the integral resolution data

\[
v_0=2A_0=(16,56),\qquad
v'_1=2A'_0=(2,0),\qquad
v_1=2A_1=(11/2,14).
\]

The first candidate printed under \(D=72\) in *Properties of a Jacobian mate*
has exactly those three values and leading form
\(\phi_0=cx(xy^4-r_1)^7\).

## Primary-source facts

1. Makar-Limanov and Trakhtenberg assume an original polynomial \(f\) with a
   polynomial Jacobian mate \(g\) and \(J(f,g)=1\). Their successive
   Newton-resolution identities continue to use \(J(f_i,g_i)=1\).
2. Their published \(D=72\) list includes a first branch with
   \(v_0=2\cdot4(2,7)=(16,56)\), \(v'_1=(2,0)\),
   \(v_1=2(11/4,7)\), and
   \(\phi_0=cx(xy^4-r_1)^7\).
3. GGHV's open case begins with polynomial Newton polygons
   \(3S\) and \(2S\), where
   \(S=\{(0,0),(1,0),(8,28),(0,4)\}\). The degree-72 component is
   the \(2S\) component.
4. GGHV17 records the open complete chain
   \(A_0=(8,28)\), \(A'_0=(1,0)\), \(A_1=(11/4,7)\),
   and \((m,n)=(3,2)\).
5. GGHV later uses Laurent automorphisms and the final morphism
   \(x\mapsto x^{-1}, y\mapsto x^4y\); the final pair lies in
   \(K[x,x^{-1},y]\) and satisfies \([P,Q]=x^2\).

## Premise dependencies

- The GGHV polygon and chain data are the verified transcriptions in
  `context/2026-07-22-gghv-72108-dossier.md`.
- The Newton-resolution hypotheses and \(D=72\) row were reread in the local
  primary PDF recorded by
  `context/2026-07-25-strategy-source-audit.md`.
- No claim is made that the final Laurent normalization preserves every
  Newton-resolution invariant. The test deliberately returns to the original
  polynomial degree-72 component.

## Falsifiable prediction

The exact rational crosswalk will show:

1. direct application to the final GGHV pair is invalid because both its
   ambient ring and bracket identity fail the source hypotheses;
2. application to the original degree-72 component is valid under the
   hypothetical Keller-pair premise;
3. the original component matches the first published \(D=72\) candidate
   exactly in \(D,v_0,v'_1,v_1\);
4. therefore the published Newton-resolution list retains rather than excludes
   the open GGHV case.

## Invariant-first note

The ambient ring and bracket identity decide direct applicability before any
polygon comparison. Once the comparison is moved to the original polynomial
pair, the exact degree and corner identities decide membership in the printed
candidate row. No coefficient-system computation is relevant to this first
bridge.

## What a PASS proves and what a FAIL proves

- PASS: the published Newton-resolution restrictions apply to the original
  degree-72 component and independently reproduce the open GGHV chain. The
  paper's printed \(D\le100\) results do not exclude \((72,108)\).
- FAIL: at least one exact datum differs, so visual similarity was misleading
  and the Newton-resolution route must remain unapplied until the discrepancy
  is resolved.

Neither outcome constructs a counterexample, proves realizability, or raises
the planar degree floor.

## Method and adversarial controls

Run an exact `Fraction`-based crosswalk over the source hypotheses and candidate
data. Require:

1. a polynomial pair with bracket \(1\) passes the applicability gate;
2. a Laurent pair with bracket \(x^2\) fails it;
3. changing \(A'_0\) from \((1,0)\) to \((2,0)\) breaks the candidate match;
4. changing \(A_1\) from \((11/4,7)\) to \((5/2,6)\) breaks the first-branch
   match while identifying the second printed \(D=72\) branch.

## Compute budget and kill criterion

CPU only, exact rational arithmetic, expected runtime below one second. Budget:
10 seconds. There is no checkpoint because the decision is atomic. If the
script does not finish within the budget, record an infrastructure failure and
draw no mathematical conclusion.

Declared 2026-07-25 before running `run.py`.
