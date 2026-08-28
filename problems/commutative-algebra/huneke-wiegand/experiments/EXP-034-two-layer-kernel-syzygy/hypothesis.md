# EXP-034 hypothesis - two-layer kernel and first unavoidable nonlinear syzygy

Status at declaration: **ACTIVE, NO RESULT CLAIMED**. Final status: **CONFIRMED**; see `proof.md`
and `verdict.md`.

## Question

For every integer `p>=4`, put `N=10p`, let `H_p` be the `8p` high offsets killed by
`Q_p:f_p`, and let

```text
B_p=[6p,24p-1] minus H_p,      |B_p|=10p.
```

Can the Artinian reduction of the EXP-033 kernel determine a previously unknown lower-strand
Betti class of `A_p=P_p/Q_p` without computing a full minimal resolution?

## Falsifiable prediction

Let `S_p=P_p/(X_0)` and `M_p=K_p/X_0K_p`. The prediction has two separately graded parts.

1. **Two-layer theorem.** There are offset bases

   ```text
   (M_p)_1={u_h:h in H_p},
   (M_p)_2={v_b:b in B_p},
   m_(S_p)(M_p)_2=0,
   X_g u_h=v_(g+h) if g+h in B_p, and 0 otherwise.
   ```

   If `V_p` is spanned by the variables `X_g`, `g in G_p minus {0}`, define

   ```text
   delta_i: exterior^i(V_p) tensor k^(H_p)
            -> exterior^(i-1)(V_p) tensor k^(B_p)

   delta_i(e_F tensor u_h)
     =sum_(g in F, h+g in B_p) (-1)^pos e_(F minus {g}) tensor v_(h+g).
   ```

   Then

   ```text
   beta_(i,i+1)^(P_p)(K_p)=dim ker(delta_i),
   beta_(i-1,i+1)^(P_p)(K_p)=dim coker(delta_i).
   ```

2. **Explicit obstruction and survival test.** Put

   ```text
   b*=8p-1,
   F*={1,...,p},
   tau_p=b*+sum_(g=1)^p g=8p-1+p(p+1)/2.
   ```

   The codomain cell `e_(F*) tensor v_(b*)` is predicted to have no incoming face under
   `delta_(p+1)`, hence to give a primitive class

   ```text
   beta_(p,(p+2,tau_p))^(P_p)(K_p)>=1.                    (1)
   ```

   The stronger prediction is that this class is outside the image of

   ```text
   Tor_(p+1)^(P_p)(D_p,k)_(p+2,tau_p)
      -> Tor_p^(P_p)(K_p,k)_(p+2,tau_p),                  (2)
   ```

   and therefore

   ```text
   beta_(p,(p+2,tau_p))^(P_p)(A_p)>=1.                   (3)
   ```

Failure of the basis model, any additional representation of `8p-1`, an incoming face to the
declared cell, or a unit boundary in the same multidegree refutes the relevant part. Failure of
(3) does not refute (1); it redirects the experiment to the exact connecting-map rank.

## Premise gate

Before every canonical calculation, verify these SHA-256 hashes:

```text
EXP-030 proof  1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729
EXP-032 proof  4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c
EXP-033 proof  e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c
EXP-033 verdict 674b2940259465f0a2cba96261a8bb021e103cb3e51db50a8aac4f64c0c5927b
```

A mismatch gives `INCONCLUSIVE_PREMISE`, not a mathematical failure.

## Validation routes

### Canonical route

- derive `G_p`, `H_p`, and `B_p` directly from the frozen block formulas;
- verify the two-layer multiplication table and `X_0` reduction for `p=4,...,300`;
- enumerate the representation set
  `R_b={g in G_p minus {0}:b-g in H_p}` and test `R_(8p-1)={1,...,p}`;
- construct the exact target multidegree complex around (1), record integer ranks and Smith data,
  and reject filled-gap, missing-variable, wrong-sign, and wrong-shift controls;
- compute the same multidegree of `D_p` from its low idealization tensored with the high Koszul
  factor before making a survival claim.

### Independent route

Reconstruct the offset sets from numerical-semigroup membership rather than importing the
canonical block constructors. Build the relevant Koszul columns by literal monomial
multiplication and compare ranks over `QQ`, `GF(2)`, and `GF(1000003)` for the declared small
parameters. The independent route must not import canonical incidence or subset-sum functions.

### Symbolic route

Prove uniformly that

```text
R_(8p-1)={1,...,p}.
```

Then show directly that every possible preimage of `e_(F*) tensor v_(8p-1)` would require an
element of `R_(8p-1) minus F*`, which is empty. Primitivity follows because the surviving
coordinate is a standard basis coordinate over `Z`.

The survival step must be an all-parameter multigraded argument or an explicit integral
connecting-map normal form. An ordinary Hilbert-series identity cannot prove it.

## PASS, partial result, and FAIL

- **PASS** requires the two-layer theorem, the primitive class (1), and the survival theorem (3),
  each with canonical, independent, and written all-parameter support.
- A proved (1) with an unresolved or refuted (3) is a **relevant partial result**, not a full pass;
  persist the exact boundary and next connecting-map target.
- **FAIL** requires a certified counterexample to the two-layer model or the claimed class.

## Budget and kill criterion

- Canonical offset campaign: 120 seconds.
- Exact small-parameter multigraded ranks: 300 seconds per field and parameter.
- Symbolic and coefficient reconstruction: 180 seconds.
- Stop a route as `INCONCLUSIVE_BUDGET` at its cap. Do not launch a raw full-resolution sweep.

## Publication gate

A surviving class in `A_p` changes the published lower Betti boundary and opens main-manuscript
v0.21 plus a Zenodo new-version gate. A class proved only for `K_p` is persisted as a structural
theorem but does not by itself trigger publication. A separate manuscript is justified only if
the two-layer incidence method yields a reusable theorem beyond this family.
