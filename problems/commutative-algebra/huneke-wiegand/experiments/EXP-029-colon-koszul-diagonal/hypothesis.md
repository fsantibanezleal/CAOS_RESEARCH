# EXP-029 - colon-Koszul degree-five diagonal

Declared: 2026-08-20, before implementation or canonical artifact generation. Backlog: HWB-035.

Fix `p>=4`. Retain

```text
C_p=P_p/J_p,       J_p=(Q_p,f_p),
f_p=X_0^2X_(3p)-X_p^3,
H_p={a in G_p : a>=6p}.
```

EXP-027 proves

```text
(Q_p:f_p)_1=span_k{X_a:a in H_p},       |H_p|=8p.
```

## Predictions

- P1: for every field `k`,

  ```text
  beta_(3,5)(C_p)=binom(8p,2)=4p(8p-1).
  ```

- P2: the complete offset-graded profile is

  ```text
  beta_(3,(5,b))=#{ {a,c} subset H_p : a<c and a+c=b-3p }.
  ```

  If `A_p(t)=sum_(a in H_p)t^a`, the same integer profile is

  ```text
  [t^(b-3p)] (A_p(t)^2-A_p(t^2))/2.
  ```

- P3: its support is exactly

  ```text
  [15p+1,39p-3] minus {33p-1},
  ```

  so it has `24p-4` offsets.

- P4: the relevant integral second homology is free abelian with a basis indexed by unordered
  pairs in `H_p`. There is no hidden characteristic exception.

- P5: together with EXP-028 and the frozen Hilbert numerator, the complete internal-degree-five
  diagonal is

  ```text
  beta_(2,5)=p(2p-3),
  beta_(3,5)=4p(8p-1),
  beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3,
  beta_(i,5)=0 for i outside {2,3,4}.
  ```

## Premise dependencies

- EXP-023 CONFIRMED: `J_p=(Q_p,f_p)` with one cubic.
- EXP-024 CONFIRMED: the exact Hilbert numerator, regularity four, and minimal shifts.
- EXP-025 CONFIRMED: the truncated-monomial model and cumulative offset sets.
- EXP-027 CONFIRMED: integral relative squarefree-divisor chains and the exact linear colon.
- EXP-028 CONFIRMED: the complete second row and unit integral matching framework.

The exact premise hashes are frozen in the dated preflight and must be checked by the runner.

## Method

1. Construct the total-degree-five relative offset-Koszul complexes through cell size four.
2. Apply the integral lexicographic matching through relative dimension three.
3. Classify the surviving pair triangles `{p,a,c}` and every transient critical triangle.
4. Prove that unit Morse boundaries cancel all transient triangles and no pair triangle.
5. Independently reconstruct the primitive lower bound from the Koszul second syzygies on the
   `8p` linear colon variables in the minimal mapping cone.
6. Derive P5 only after P1-P4 are established.

## Exact campaign

- Mandatory smoke at `p=4`, with complete profiles over `GF(2)` and `GF(1000003)`.
- Complete `GF(2)` profiles at `p=5,6`.
- Closed pair-profile, support, and total checks for every `p=4,...,300`.
- Integral Smith or unit-Morse audits at representatives of the left endpoint, interior,
  exceptional hole, transient low region, and right endpoint.
- An independent implementation must rebuild selected rational ranks and the pair convolution
  without importing the campaign rank code.
- Symbolic arithmetic must prove the support endpoints, unique hole, count, total, and the
  degree-five coefficient identity for arbitrary `p>=4`.

## Adversarial controls

The implementation must reject:

- including the forbidden offset `33p-1`;
- allowing repeated pairs `a=c` or ordered pairs;
- replacing the high colon set by all of `G_p`;
- treating every critical triangle as a homology class before the Morse boundary;
- deleting a transient critical tetrahedron;
- inferring integral freeness from agreement over two fields;
- deriving both adjacent Betti entries from one alternating coefficient; or
- continuing after premise mismatch, budget exhaustion, or unresolved nonunit Smith factors.

## PASS, FAIL, and trust boundary

- A finite campaign PASS proves only the checked ranks, profiles, and implementation identities.
- Any profile, support, total, mapping-cone, or coefficient mismatch refutes the affected
  prediction and stops the campaign.
- Budget exhaustion, premise drift, unresolved Morse differential, or unresolved integral torsion
  is `INCONCLUSIVE`.
- `CONFIRMED` requires the all-parameter integral matching, primitive mapping-cone lower bound,
  mandatory smoke, bounded campaign, independent audit, and symbolic endpoint/count proof.

## Invariant-first and one-sidedness

The selected invariant is the linear space `(Q_p:f_p)_1`, already proved to have basis the `8p`
high variables. Its second Koszul wedges predict both the total and the entire offset profile.
This is strictly cheaper and more discriminating than a full third-row resolution.

A computational PASS cannot prove P1-P5 for all `p`; it validates the implementation and the
declared formula. A computational FAIL refutes at least one prediction. The mapping cone gives a
lower bound only until the relative matching proves completeness.

## Budget and kill criterion

CPU only and deterministic. Formula campaign: 120 seconds. Explicit profiles: 300 seconds.
Independent audit: 180 seconds. Symbolic certificate: 120 seconds. Atomic checkpoints and flushed
progress are mandatory. A route is stopped at twice its declared budget and recorded as
`INCONCLUSIVE_BUDGET`; no theorem follows from a partial run.

