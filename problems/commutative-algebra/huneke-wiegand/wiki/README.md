# Huneke-Wiegand extensions - research wiki

Transcribe only closed experiment verdicts and proved derivations.

| record | status | result |
|---|---|---|
| source dossier | complete | candidate, priority, theorem chain and extension surface pinned |
| EXP-001 | CONFIRMED | 322-generator dimension-one toric basis; colon equality; finite agreement; hypersurface control rejects equality |
| EXP-002 | CONFIRMED | exact overring `Gamma union {101,107,181}`, type 24, and forced Ext/Tor escape map |
| EXP-003 | CONFIRMED | SAT calibration and solver-independent exact model checks |
| EXP-004 | CONFIRMED | 48,954 semigroups, 1,503,391 gaps, 1,156 checked UNSAT proofs; published `F<69` frontier reproduced |
| EXP-005 | CONFIRMED | least Frobenius value is 181; checked proofs for every odd 69--179 and exact public model at `(181,14)` |
| generalized-arithmetic exclusion | proved | multiplicity/low-generator argument excludes the 2024 positive family; deletion gcds are all one |
| EXP-006 Route G | REFUTED | only `s=14` passes the fixed-offset sweep through even `s=100` |
| EXP-006 Route K | CONFIRMED | `s=16,18` certified UNSAT; every even `s=20,...,40` SAT and independently checked; eleven non-seed models open extraction |
| EXP-007 | CONFIRMED | the public semigroup at shift 14 is the unique normalized rigid pair at the minimum `F=181`; both terminal proofs pass a fresh audit |
| EXP-008 | REFUTED | exact instances at `q=6,7,8`, but a proved layer-9 residue-7 hole refutes the formula for every `q>=9` |
| EXP-009 | CONFIRMED | explicit infinite counterexample family for every integer `p>=4`; symbolic proof plus independent formula/semantic audit |
| EXP-010 | SUPERSEDED | no run: its gate was false after EXP-009 closed the family question |
| EXP-011 | CONFIRMED | exact endomorphism semigroup for every EXP-009 member; nonsymmetric invariants and uniform Ext/Tor escape |
| preprint v0.02 | published | minimality plus minimum-layer uniqueness, DOI [`10.5281/zenodo.21764868`](https://doi.org/10.5281/zenodo.21764868); v0.01 remains frozen |
| preprint v0.03 | published | family theorem, DOI [`10.5281/zenodo.21873911`](https://doi.org/10.5281/zenodo.21873911); exact public-file hash verified |

CAOS independently reproduces the public counterexample's decisive finite certificate. Discovery
priority remains Son Pham's; EXP-001 is a replication result, not rediscovery. CAOS's novel
extensions are the certified Frobenius-minimality theorem in EXP-005, the complete minimum-layer
classification in EXP-007, the EXP-009 infinite family theorem, and the EXP-011 uniform
endomorphism-overring theorem.

## Uniform endomorphism anatomy

For every integer `p>=4`, let `s=6p` and retain the EXP-009 semigroup `Gamma_p` and normalized
ideal `J_p=(1,t^s)`. Put

```text
Q_p = [p+1,2p-2] union {2p,4p}.
```

EXP-011 proves

```text
v(End_(R_p)(J_p)) = Gamma_p union (7s+Q_p) union {13s-1}.
```

The endomorphism semigroup has multiplicity `24p`, Frobenius number `54p-1`, conductor `54p`,
genus `38p-1`, and embedding dimension `12p`. It is nonsymmetric. The endomorphism ring is
therefore non-Gorenstein and strictly larger than `R_p`. The audited Dey-Lyle implications show
uniformly that `J_p` remains rigid over the endomorphism ring but is not reflexive there, while
the adjacent `Ext` and `Tor` obstruction groups are nonzero.

The proof uses the invariant

```text
v(End_(R_p)(J_p))_k = V_k intersect V_(k+1),
V_p = Gamma_p union (s+Gamma_p),
```

so the new level is exactly `B intersect C=Q_p`. A 297-parameter two-route campaign and an
independent reconstruction audit support, but do not replace, the symbolic argument.
