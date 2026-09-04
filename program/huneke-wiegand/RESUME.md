# Huneke-Wiegand extensions - session handoff

Updated: 2026-09-04. Lifecycle: EXP-053 is REFUTED on P2 with P1 passed finitely after a resource overrun and a common source class retained; EXP-052 is CONFIRMED FINITELY with an untouched semantic holdout; EXP-051 is REFUTED overall with P1/P2 retained; EXP-050 is REFUTED overall with P1 retained; EXP-049 is REFUTED overall with bounded dual parity certificates retained; EXP-048 is REFUTED overall with explicit completion-chain candidates retained; EXP-047 is CONFIRMED FINITELY; EXP-046 is REFUTED overall with P3 retained; EXP-045 is REFUTED with a stable full-carrier antichain retained; EXP-044 is REFUTED overall with P1/P3 retained; EXP-043 and EXP-042 are CONFIRMED finitely; EXP-041 is REFUTED overall with P1 retained; EXP-040 is REFUTED with P1 retained; EXP-039 is REFUTED with a sector redirect;
EXP-038 is INCONCLUSIVE with both finite
gates passed; EXP-037 is REFUTED; EXP-036 is CONFIRMED
with structural propagation unresolved. The complete `(10,2)` block gives surviving dimensions
`4240` over `GF(2)` and `4168` over both `GF(3)` and `GF(5)`, hence exact excess `e_10=72`. This
refutes the period-six prediction 73 and its 73-point lattice index at the first out-of-sample
cell. Low-degree and canonical residual orders agree exactly. The finite `t=2` sequence is now
`1,4,9,18,31,49,72,102,138`. EXP-038 tests whether the first deficit is a degree-six relation, with
corrected numerator `1+2x+x^2+x^3-x^6`. Its first genuinely new prediction passes: the complete
`(11,2)` block gives `8688/8586` and audited exact `e_11=102`; the complete `(12,2)` block gives
`16822/16684` and audited exact `e_12=138`. Both finite gates pass, but the recurrence and proposed
relation remain unproved. EXP-039 refutes bounded defect-one components but exposes latent sectors
`binom(p-2,3),p-4,p-4,p-5` and their `p=9` support merger. EXP-040 confirms exact `67+5` at
`p=10`, localizing the first correction inside the large component, but refutes its simple
transport with exact `95+7` at `p=11` instead of `96+6`. EXP-041 refutes the proposed semantic
switch: the isolated blocks at `p=8,...,11` have one normalized twelve-atom skeleton, with defects
`3,4,5,7`. The jump is internal to a persistent finite semantic type. EXP-042 computes its exact
first Bockstein: ranks are again `3,4,5,7`, proving exactly that many
nonzero valuation-one Smith factors in the four isolated integer matrices. EXP-043 supplies exact
rational-rank upper certificates and closes their complete 2-primary types as
`(Z/2)^3,(Z/2)^4,(Z/2)^5,(Z/2)^7`. EXP-044 then refutes the proposed two-atom carrier:
`D:B` and `K:C0` are necessary row-projection interfaces, but their union has Bockstein zero.
EXP-045 exhausts the six-row-atom lattice: minimal full carriers are stably masks `59` and `62`,
their intersection mask `58` has ranks `1,2,3,5`, and either completion adds exactly two. For every
tested parameter, EXP-046 leaves each carrier in one connected nonzero unit core; masks `59` and
`62` have zero unit-leaf cancellations. Mask `56` has defects `0,0,0,1` in unchanged semantic
support, so the `p=11` threshold is internal sign/rank behavior. EXP-047 completes the certified
finite relative integer presentation: both
stable completion quotients have exact torsion `(Z/2)^2`, while `56->58` has
`(Z/2)^(p-7)`, with explicit free ranks and no hidden odd or higher 2-power factors. HWB-074 now
owns the uniform semantic basis and parameter-compatible reduction. EXP-048 refutes bounded local
representatives but exposes four explicit interval chains: the two `58->59` Bockstein supports
have sizes `(p-4,p-4)` and the two `58->62` supports have sizes `(2p-8,p-4)`. Their exact row
formulas pass a separate 78-check audit on `p=8,...,11`. The `56->58` canonical section is not one
translation family, so HWB-075 prioritizes integral lifts of the four stable completion chains and
dual parity characters; the threshold block moves to a relative-Morse fallback.
EXP-049 proves that none of the sixteen literal zero-one equations `Ry=2a` is integrally solvable:
the correct torsion representatives require nonzero even corrections `b=a+2c`. Conversely, two
independent parity duals exist for each completion at every tested parameter, and every support has
size at most four. The `58->62` low-pivot duals obey two explicit endpoint-row formulas on the
complete finite range. EXP-050 constructs all corrected representatives `b=a+2c` and exact
witnesses `Ry=2b`, but their large canonical corrections are quotient-section artifacts.
EXP-051 selects before quotient normalization and obtains primary binary witnesses supported on
at most six source columns, with divided-boundary coefficients bounded by two. EXP-052 freezes
semantic formulas using only `p=8,9,10`: the `58->59` divided boundary has six alternating edge
families and support `6p-30`, while `58->62` has four alternating triangular/interval families and
support `binom(p,2)-5`. They reproduce all 36 and 50 coefficient-token rows at untouched `p=11`,
and a separate reconstruction passes 31/31 checks. HWB-076 is done. HWB-077 owns the generic
source-chain identity, the second independent class, bounded dual proof, and separate upper bound.
EXP-053 uniquely pulls that class back at `p=8,9,10` but refutes HNF coordinates as a compact proof
language: supports are 125, 178, and 238 with 78 semantic skeletons, and `p=10` overruns the
resource gate.
The same labelled source chain serves both completions, so HWB-078 now targets one simultaneous
telescoping identity on the union `58->63`.
For every
`p>=4` and
`2<=t<=p-2`, the shifted cubic source is absent
by the positive gap `g(p,t)>=3(p-1)^2`, so every future exact `A_p` value at these targets
transfers to `C_p`.  This is not an infinite characteristic-dependence theorem. The 53-page
manuscript v0.23 passed every publication gate and is public, concept-latest, and fresh-download
verified at DOI `10.5281/zenodo.22181972`. Its 824,114-byte PDF has MD5
`6bcacfa265e840f40e89dcdb87b75f7b` and SHA-256
`c77b08a3724db90b14039c2c88e98325403ef4f656f52137057a27eb6fa5072d`. HWB-062 and HWB-063 are
done: PRs #230/#231 passed required checks and promoted payload tree
`8ea3fbd0dfd136a7b91c508a31146be7d88eded1` through `develop` and `main`.

EXP-035 remains CONFIRMED with its declared P3 mechanism refuted.
For every `p>=4`, the exact zero-row criterion is

```text
[b,F] is a zero incidence row if and only if R_b subset F,
R_b={g in G_p minus {0}:b-g in H_p},
```

and the block

```text
b=10p+t,  F=[3p,4p-2] union {t} union [t+2,p],  2<=t<=p-2.
```

These rows split off a primitive `K_p` coordinate summand and give classes in every homological
degree `p+1,...,2p-3`. The mandatory `(p,t)=(4,2)` smoke gate refutes coordinatewise survival by
an exact integral cycle, but the complete target quotient yields the stronger result

```text
beta_(5,(7,87))(K_4)=5 over GF(2),  4 over GF(3),
beta_(5,(7,87))(A_4)=beta_(5,(7,87))(C_4)=4 over GF(2),  3 over GF(3).
```

The integral kernel cokernel is `Z^4 direct-sum Z/2Z`. HWB-058 and HWB-059 are done. The 51-page
manuscript v0.22 is published and fresh-download verified at DOI
`10.5281/zenodo.22177072`. Its 810,905-byte PDF has MD5
`5ed2409d6688b30147963a7293598440` and SHA-256
`3868f511a047073c9d7bedf25e026f1aaf3a5ab2c05c45d03614675ef6bdf5c2`. HWB-060 is done: PRs
#226/#227 passed required checks and promoted payload tree
`0847e35a7641ab5592afd136f42bcf09ffe514f3` through `develop` and `main`. HWB-061 remains active
for the infinite connecting-parity problem after the confirmed EXP-036 finite/anatomy gate.
HWB-062 and HWB-063 are done with manuscript v0.23, its verified Zenodo version, and repository
promotion through PRs #230/#231.
EXP-034 is CONFIRMED and manuscript
v0.21 is PUBLISHED. Put
`tau_p=8p-1+p(p+1)/2`. The Artinian reduction of the high-variable kernel and a separate unit
connecting-map pivot prove, over every field,

```text
beta_(p,(p+2,tau_p))(K_p)
=beta_(p,(p+2,tau_p))(A_p)
=beta_(p,(p+2,tau_p))(C_p)=1.
```

This is one exact point in the previously unresolved regularity-two strand; both complete lower
strands remain open. HWB-055 and HWB-056 are done. The 48-page v0.21 passed claim, two clean
builds, all-page render inspection, sole-authorship, repository, exact-upload, publication,
concept-latest, and fresh-download gates. It is public at DOI `10.5281/zenodo.22135689`; its
792,863-byte public PDF matches MD5 `13b92773205a49977abb88cd7ab8dde1` and SHA-256
`c717fbb4d6d3178e0fb0786a8a61c9e2c109d97d77a7b9e1308a2274c0f97539` exactly. PR #222 passed
`guards` and `test` and merged the payload to `develop` at `0092685`; PR #223 passed all required
checks and promoted it to `main` at `4cde185`. All three remote branches shared payload tree
`f571fb955560c29489c181a6ce542548619209e0` before this handoff update. HWB-057 is done. EXP-033
remains CONFIRMED. It proves that the quadratic quotient
`A_p=P_p/Q_p` has depth one and regularity two, so the entire cubic mapping cone is minimal over
every field:

```text
B_(C_p)(x,z)=B_(A_p)(x,z)+x z^3 B_(D_p)(x,z).
```

With `c=2p-2`, `m=8p`, and the EXP-032 ranks `lambda_(c,a)`, the complete new strands are

```text
beta_(i,i+3)=sum_(a=1)^(c-1)lambda_(c,a)binom(m,i-1-a),
beta_(i,i+4)=binom(m,i-1-c).
```

Canonical exact arithmetic passes all `p=4,...,300` in 15.159 seconds; the independent
coefficient/structural audit and symbolic route pass. Three budget stops at `p=102,209,267` are
preserved as non-evidence. HWB-052 and HWB-053 are done. The 45-page manuscript v0.20 passed
claim, two clean builds, all-page render inspection, sole-authorship, repository, upload,
publication, concept-latest, and fresh-download gates. It is public at DOI
`10.5281/zenodo.22062161`; the 774,246-byte public PDF matches MD5
`69f45597e879afc8fd91ca4157fb2cf3` and SHA-256
`163a3a2fc6a5d61b6ff97e3ed1089dc3b6e9b320aa9c68ed67d2f1155362d743` exactly. PR #218 passed
`guards` and `test` and merged the payload to `develop` at `28bac50`; PR #219 passed all required
checks and promoted it to `main` at `c1e6b20`. Both remote branches share payload tree
`f51cb2845d20b4fbf7d43029a71af0392bc3d6d9`. HWB-054 is done. The remaining mathematical
frontier is to classify the other EXP-034 incidence cokernels and their multigraded survival in
`0 -> K_p -> A_p -> D_p -> 0`; the cubic comparison maps are no longer unknown.

EXP-032 remains CONFIRMED for the complete graded Betti polynomial and
free-module shape of the cubic-colon quotient. The 43-page v0.19 passed claim, two-pass build,
all-page render, metadata, sole-authorship, tests, pipeline, artifact, upload, publication, and
fresh-download gates. It is public and concept-latest at DOI `10.5281/zenodo.22031481`; HWB-050
is done. PRs #213/#214 passed required checks and promoted the exact payload through `develop` and
`main`; HWB-051 is done and all three remote branches shared tree
`c2f9f58488c7a1fa7ccee181a75944f7209b795c` before this handoff update.
EXP-031 is CONFIRMED; manuscript v0.18 is published and
fresh-download verified at DOI `10.5281/zenodo.22030743`. HWB-047 is done and HWB-048 owns
only deferred CAOS_MANAGE ledger reconciliation; research PRs #209/#210 passed all checks and
promoted the exact v0.18 state through `develop` and `main`. EXP-030 and manuscript v0.17 were
promoted through research PRs #205/#206;
HWB-046
owns only deferred CAOS_MANAGE ledger reconciliation because that checkout is occupied by
unrelated staged diffusion work. The integral
colon-Koszul theorem gives

```text
beta_(3,(5,b))=#{ {a,c} subset H_p:a<c and a+c=b-3p },
beta_(3,5)=binom(8p,2)=4p(8p-1),
```

where `H_p={a in G_p:a>=6p}` has size `8p`; the support is
`[15p+1,39p-3] minus {33p-1}`. Together with EXP-028 and the exact Hilbert numerator, the complete
internal-degree-five diagonal over every field is

```text
beta_(2,5)=p(2p-3),
beta_(3,5)=4p(8p-1),
beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3,
beta_(i,5)=0 otherwise.
```

For `0<=r<=2p-4`, the degree-five support is the three intervals
`[3p+2,5p-2]`, `[6p+1,8p-3]`, and `[9p,11p-4]`. The outer multiplicity is
`min(floor(r/2)+1,floor((2p-4-r)/2)+1)` and the middle multiplicity is
`min(r+1,2p-3-r,p-2)`. Integral lexicographic matching and unit Smith forms prove freeness and
characteristic independence. The canonical EXP-029 campaign passes 297 rows, complete small
profiles, two-field controls, an independent rational boundary audit, and arithmetic/Z3 checks.
The 36-page main manuscript v0.16 is published and fresh-download verified at DOI
`10.5281/zenodo.22029468`; its 691,569-byte PDF has SHA-256
`4c2a49ae6e1a959afb8df4a365feb4c815d408f3746b5ef1df14ee5746abd554`. HWB-041 is done. PRs
#203/#204 passed all checks; research work, `develop`, and `main` share payload tree
`f956e8109c986a841394f19ded669feb62164fa1`. HWB-042 now owns only the deferred management-ledger
reconciliation. Higher homological rows and the full Betti table remain open.

EXP-030 identifies the complete cubic-colon quotient with the canonical idealization of the
`p`-th Veronese rational normal curve ring and proves
`beta_(3,6)=8p(7p^2-12p+2)/3` over every field, with exact support
`[3p+4,29p-5] minus ([6p-3,6p+1] union [9p-3,9p])`. The 40-page manuscript v0.17 is published
and concept-latest at DOI `10.5281/zenodo.22030167`. Its 714,021-byte fresh public download has
MD5 `4c7daffba7539f37ea4ecb6d52fad9d9` and SHA-256
`480f135b9ecf8dbcec0fb91e85491f8fcf11e1e3c7417f6415ebeda366b5d640`, exactly matching Git.
PRs #205/#206 passed all required checks; research work, `develop`, and `main` share payload tree
`33b044658401e9216705481ad627dea55dbdf754`. That v0.17 snapshot remains frozen; EXP-031 below
closes `beta_(3,7)` and the third row. Higher rows and the full resolution remain open.

EXP-031 proves `beta_(3,7)=0` by an integral zero-vertex matching. In total degree seven, the only
unmatched triangles have residual `6p-1`; adjoining one of the four low vertices `1,2,3,4`
outside the triangle gives a same-offset tetrahedron with a single unit critical face. Therefore
the complete third row over every field is

```text
beta_(3,4)=p(5p-1)(500p^2-440p+47)/2,
beta_(3,5)=4p(8p-1),
beta_(3,6)=8p(7p^2-12p+2)/3,
beta_(3,7)=0,
beta_(3,j)=0 otherwise.
```

The canonical exact profiles vanish at every offset for `p=4,5`; the smallest case agrees over
two characteristics. Canonical and independent unit-filler counts agree for `p=4,...,12`, and the
arithmetic obligations pass through `p=300`. HWB-045 is done. Higher rows and the full resolution
remain open.

EXP-032 proves the complete ordinary graded Betti polynomial of
`D_p=P_p/(Q_p:f_p)`. Put `c=2p-2`, `m=8p`, and

```text
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1).
```

Then, over every field,

```text
B_(D_p)(x,z)
 =(1+xz)^m(1+sum_(a=1)^(c-1)lambda_(c,a)x^a z^(a+1)+x^c z^(c+2)).
```

Consequently `pd=10p-2`, `reg=2`, and every free-module rank and shift is known. Canonical and
independent exact routes pass every `p=4,...,300`; symbolic identities and complete small tables
pass. This does not construct differential matrices or settle the full resolution of `C_p`.
HWB-049 is done and HWB-050 owns manuscript v0.19.

The 42-page manuscript v0.18 passed claim, two-pass warning-free build, all-page render,
authorship, metadata, upload, and publication gates. Zenodo record `22030743` is concept-latest;
its fresh unauthenticated 725,554-byte PDF has MD5 `558532167c4f2a39e03d1bcced9de18d`
and SHA-256 `0e40aa5ed4feb02209137c2982184a93cfd402ac03cc9d4aa6f9ba86ae4327b7`,
exactly matching Git. HWB-047 is done.

The published baseline remains intact: EXP-026 and focused companion v0.02 are published and
fresh-download verified at DOI `10.5281/zenodo.22002907`, and PRs #190/#191 plus CAOS_MANAGE PR
#559 completed that prior handoff. EXP-025 v0.01 remains immutable at DOI
`10.5281/zenodo.21997378`; EXP-024 v0.13 remains immutable at DOI
`10.5281/zenodo.21995498`.

## 1. State in one screen

Son Pham has priority for the first public counterexample, independently verified by Professor
Craig Huneke. CAOS does not claim that discovery. Its validated extensions are:

1. an independent Singular/4ti2 reproduction of the decisive colon equality (EXP-001);
2. exact endomorphism-overring anatomy and the Ext/Tor escape mechanism (EXP-002);
3. certified Frobenius minimality `F_min=181` in the symmetric numerical-semigroup,
   two-generated monomial-ideal class (EXP-004/005);
4. uniqueness of the normalized pair at that minimum (EXP-007); and
5. an explicit infinite family of counterexamples in the same class (EXP-009); and
6. the exact endomorphism overring and nonreflexive Ext/Tor escape for every family member
   (EXP-011);
7. exact pseudo-Frobenius, trace, conductor, and nonstability anatomy (EXP-012--016);
8. conductor reduction number four, quotient profile `23p-1,14p,2p,1,0`, and Hilbert coefficients
   `(e0,e1)=(24p,39p)` (EXP-017); and
9. depth-zero conductor tangent cones with a unique Valabrega--Valla defect of length `p` and an
   exact coefficientwise-positive Hilbert numerator (EXP-018); and
10. complete tangent-cone torsion `k^p` in degree zero, Buchsbaumness, and unbounded Buchsbaum
    invariant `p` (EXP-019); and
11. the complete graded module over the minimal-reduction polynomial ring, including all Betti
    numbers, projective dimension one, regularity four, and the section identity `25p=e0+I`
    (EXP-020);
12. the canonical conductor special fiber, Cohen--Macaulay type `10p+1`, and nonlevel behavior
    (EXP-021); and
13. the complete defining ideal by `50p^2-17p` quadrics and one cubic, with relation type three
    and non-Koszulness (EXP-022/023).
14. exact presentation-ring edges, including projective dimension, regularity, and extremal Betti
    data (EXP-024);
15. the truncated-monomial primary model and complete reduced grevlex staircase (EXP-025/026); and
16. the first interior Betti strand, with characteristic-free multiplicity-free offset support
    (EXP-027); and
17. the complete second Betti row, with degree-five multiplicities, degree-six vanishing, and
    characteristic independence (EXP-028); and
18. the free colon-Koszul pair basis, exact third-row degree-five profile, and complete
    internal-degree-five diagonal over every field (EXP-029); and
19. the complete cubic-colon idealization and characteristic-free degree-six third-syzygy profile
    (EXP-030); and
20. the integral zero-vertex contraction, degree-seven vanishing, and complete third homological
    row over every field (EXP-031); and
21. the complete graded Betti polynomial and free-module shape of the cubic-colon quotient over
    every field (EXP-032); and
22. the depth-one regularity-two quadratic quotient, minimal cubic mapping cone, and complete
    regularity-three/four strands over every field (EXP-033); and
23. the two-layer kernel incidence theorem and exact first surviving regularity-two Betti class
    in `K_p`, `A_p`, and `C_p` over every field (EXP-034); and
24. the complete primitive zero-row summand, consecutive kernel family, and first
    characteristic-dependent lower multigraded Betti cell (EXP-035).

The public seed is

```text
Gamma = <56,57,58,63,64,70,71,72,73,74,75,76,77,78,79,80,81,82,83,
         87,89,90,93,95,96,97>,
R = Q[t^Gamma] localized at the positive-degree maximal ideal,
I = (t^56,t^70)R.
```

## 2. The objects table

| object | definition | evidence owner |
|---|---|---|
| public `Gamma` | Pham's symmetric numerical semigroup with Frobenius 181 | EXP-001 target |
| public `I` | `(t^56,t^70)`, normalized shift 14 | EXP-001 and source dossier |
| `E_s,D_s` | exponent sets whose equality `D_s=E_s+E_s` is the rigidity criterion | EXP-001/003 |
| `Gamma_p` | growing-interval semigroup for every integer `p>=4` | EXP-009 theorem |
| `I_p` | `(t^(24p),t^(30p))` over the localized ring of `Gamma_p` | EXP-009 theorem |
| `Lambda_p` | `Gamma_p union (7s+Q_p) union {13s-1}`, the value semigroup of `End_(R_p)(I_p)` | EXP-011 theorem |
| `T_p` | common trace/conductor `tr_R(J_p)=R_p:E_p=tr_R(E_p)` | EXP-013--018 theorems |
| `C_p` | conductor special fiber `F(T_p)`, canonically `gr_(T_p)(R_p)/H^0` | EXP-021 theorem |
| `J_p` | defining ideal of `C_p` in its `10p` degree-one variables | EXP-022/023 theorems |
| `Q_p` | quadratic part of `J_p`, with `J_p=(Q_p,f_p)` and `f_p=X_0^2X_(3p)-X_p^3` | EXP-023/027 theorems |
| `D_p` | cubic-colon quotient `P_p/(Q_p:f_p)`, the canonical idealization of the `p`th Veronese rational normal curve ring | EXP-030 theorem |
| `A_p` | quadratic quotient `P_p/Q_p`, depth one and regularity two, with a characteristic-free EXP-034 class and characteristic-dependent EXP-035 cell in row two | EXP-033--035 theorems |
| `K_p` | high-variable kernel in `0 -> K_p -> A_p -> D_p -> 0`, with Hilbert numerator `8p z+10p z^2`, a two-layer incidence resolution, and exact zero-row summands | EXP-033--035 theorems |
| minimum layer | all normalized rigid pairs at the least Frobenius value 181 | EXP-005/007 |

## 2a. Infinite family theorem

For every integer `p>=4`, put `s=6p` and define residue sets in `[0,s-1]`

```text
A = [0,p] union [3p,4p-2],
B = ([p+1,3p-1] minus {2p-1}) union {4p} union [5p-1,6p-1],
C = [0,2p] union [3p,5p-2].
```

Let `Gamma_p` contain

```text
{0}, 4s+A, [5s,6s-1], 6s+B, 8s+C,
[9s,13s-2], and every integer at least 13s,
```

with all other nonnegative integers below `13s` gaps. Then `Gamma_p` is symmetric with

```text
multiplicity = 4s = 24p,
Frobenius = 13s-1 = 78p-1,
conductor = 13s = 78p,
embedding dimension = 11p.
```

For the localized semigroup ring `R_p`, the ideal
`I_p=(t^(4s),t^(5s))R_p=(t^(24p),t^(30p))R_p` is nonprincipal and rigid. The symbolic proof is
`experiments/EXP-009-growing-interval-family/proof.md`; it derives closure, symmetry, generation,
the invariants, and the exact equality `D=E+E` from seven interval-sum identities. The finite
campaign is supporting evidence, not the proof.

## 3. Experiment index

| EXP | status | load-bearing output |
|---|---|---|
| EXP-001 | CONFIRMED | independent quotient-ring colon equality; finite agreement; positive control rejected |
| EXP-002 | CONFIRMED | `v(End_R(I))=Gamma union {101,107,181}`, type 24, forced Ext/Tor escape map |
| EXP-003 | CONFIRMED | calibrated SAT model and solver-independent semantic checker |
| EXP-004 | CONFIRMED | complete `F<69` reproduction: 48,954 semigroups and 1,156 accepted DRAT proofs |
| EXP-005 | CONFIRMED | all odd `F=69,...,179` certified UNSAT; exact public model at 181 |
| EXP-006 | CLOSED | Route G refuted; Route K certifies `s=16,18` UNSAT and eleven SAT values `20,...,40`; Route A completed by EXP-009 |
| EXP-007 | CONFIRMED | unique normalized rigid pair at the minimum `F=181` |
| EXP-008 | REFUTED | proposed fixed-width family fails for every `q>=9` at the layer-9 residue-7 obstruction |
| EXP-009 | CONFIRMED | explicit infinite family for every integer `p>=4`; independent formula/semantic audit passes |
| EXP-010 | SUPERSEDED | no run; declared conditional gate became false when EXP-009 succeeded |
| EXP-011 | CONFIRMED | uniform endomorphism-overring formula, nonsymmetric invariants, and family-wide Ext/Tor escape |
| EXP-012 | CONFIRMED | exact `10p` pseudo-Frobenius set, maximal reduced type, and non-almost-Gorenstein boundary |
| EXP-013 | CONFIRMED after correction | exact common trace/conductor ideal and balanced colength `p+1`; original tail shorthand refuted |
| EXP-014 | CONFIRMED | conductor nonstability by criterion and direct witness |
| EXP-015 | REFUTED | first square-tail formula failed at `13s-1` in the `p=4` smoke gate |
| EXP-016 | CONFIRMED | corrected exact square and stability defect `14p` |
| EXP-017 | CONFIRMED | exact reduction number four, quotient profile, and Hilbert coefficients `(24p,39p)` |
| EXP-018 | CONFIRMED | conductor tangent cone has depth zero; unique Valabrega--Valla defect length `p`; exact positive Hilbert numerator |
| EXP-019 | CONFIRMED | full `H^0=k^p` in degree zero; complete maximal annihilator; Buchsbaum non-Cohen--Macaulay; invariant `p` |
| EXP-020 | CONFIRMED | complete `k[x_p]`-module, minimal graded resolution, regularity four, `a=3`, and section identity `25p=e0+I` |
| EXP-021 | CONFIRMED | canonical conductor special fiber; Cohen--Macaulay type `10p+1`; neither level nor Gorenstein |
| EXP-022 | REFUTED | quadratic presentation false; universal necessary cubic `X_0^2X_(3p)-X_p^3` |
| EXP-023 | CONFIRMED | unique higher equation; relation type three; exact count `50p^2-17p+1`; non-Koszul fiber cone |
| EXP-024 | CONFIRMED | `pd=10p-1`, `reg=4`, exact `beta_(2,3)`, complete last row, penultimate `8p`, and canonical generator degrees |
| EXP-025 | CONFIRMED | truncated parametrization, one primary component, nilindex `24p`, curvilinear fat point, local/arithmetic Gorenstein contrast, and differential fingerprint |
| EXP-026 | CONFIRMED | reduced grevlex profile `(50p^2-17p,5p-1,p-2)`, no later boundary, and flat Cohen--Macaulay monomial degeneration |
| EXP-027 | CONFIRMED | `beta_(2,4)=8p` with complete multiplicity-free offset support and exact adjacent `beta_(3,4)` over every field |
| EXP-028 | CONFIRMED | complete second row: exact degree-five three-block multiplicities, `beta_(2,5)=p(2p-3)`, and integral `beta_(2,6)=0` over every field |
| EXP-029 | CONFIRMED | free pair basis on the `8p` high colon variables gives `beta_(3,5)=4p(8p-1)`, exact support, and the complete internal-degree-five diagonal |
| EXP-030 | CONFIRMED | canonical-idealization colon, exact support, and `beta_(3,6)=8p(7p^2-12p+2)/3` over every field |
| EXP-031 | CONFIRMED | integral zero-vertex matching and signed unit filler block give `beta_(3,7)=0` and complete the third row over every field |
| EXP-032 | CONFIRMED | complete graded Betti polynomial and free-module ranks/shifts of the cubic-colon quotient; explicit differentials and the full `C_p` resolution remain open |
| EXP-033 | CONFIRMED | `depth(P_p/Q_p)=1`, `reg(P_p/Q_p)=2`, a minimal cubic mapping cone, and complete regularity-three/four strands over every field |
| EXP-034 | CONFIRMED | exact characteristic-free class `beta_(p,(p+2,8p-1+p(p+1)/2))=1` in `K_p`, `A_p`, and `C_p` |
| EXP-035 | CONFIRMED with P3 mechanism refuted | all primitive zero rows; consecutive `K_p` family; `beta_(5,(7,87))(A_4)=beta_(5,(7,87))(C_4)` is `4` over `GF(2)` and `3` over `GF(3)` |
| EXP-036 | CONFIRMED with structural propagation unresolved | repeated characteristic-dependent targets through `p=9`; distinct kernel and connecting mechanisms; compact factor-two residual; all-parameter cubic-source absence |
| EXP-037 | REFUTED | exact `e_10=72`, not 73; independent order and `GF(5)` audit pass; proposed lattice index fails |
| EXP-038 | INCONCLUSIVE; TWO FINITE PASSES | audited exact `e_11=102` and `e_12=138`; all-parameter recurrence and structural relation remain unproved |
| EXP-039 | REFUTED WITH REDIRECT | bounded defect-one components fail; exact partitions expose four latent orientation-sensitive sectors and a `p=9` support merger |
| EXP-040 | REFUTED; P1 PASSES | exact `67+5` localizes the first correction at `p=10`; `95+7` refutes the declared `96+6` transport at `p=11`; P3 not attempted |
| EXP-041 | REFUTED; P1 PASSES | every frozen component is reproduced; the isolated `R` block keeps one normalized twelve-atom skeleton through `p=11`, refuting the switch; the distinguished row is absent from all defective cores |
| EXP-042 | CONFIRMED FINITELY | exact first-Bockstein ranks `3,4,5,7` prove that many valuation-one Smith factors; high/low pivot atom representatives differ |
| EXP-043 | CONFIRMED FINITELY | audited modular Hadamard certificates prove rational ranks `1002,1607,2450,3586` and complete isolated 2-primary types `(Z/2)^(3,4,5,7)` |
| EXP-044 | REFUTED; P1/P3 PASS | deleting either marked atom kills the Bockstein, but their union also has Bockstein zero; a larger signed circuit is essential |
| EXP-045 | REFUTED WITH STRUCTURAL REDIRECT | exhaustive 256-projection lattice gives stable minimal full carriers `59,62`, core ranks `1,2,3,5`, constant completion two, and a `p=11` threshold at mask `56` |
| EXP-046 | REFUTED; P3 PASSES FINITELY | both minimal full carriers have zero unit-leaf cancellations; every residual is one connected core; mask `56` changes defect inside persistent semantic support |
| EXP-047 | CONFIRMED FINITELY | exact relative modules give `(Z/2)^2` for both stable completions and `(Z/2)^(p-7)` for the threshold quotient; 202 independent determinant checks pass |
| EXP-048 | REFUTED; P1 PASSES FINITELY | canonical relative Bocksteins recover ranks `2,2,p-7`; bounded/local templates fail, but four explicit completion interval chains with support laws `(p-4,p-4)` and `(2p-8,p-4)` survive 78 audit checks |
| EXP-049 | REFUTED; P3 PASSES FINITELY | all sixteen literal equations `Ry=2a` fail exact lattice membership, but two identity-paired dual characters of support at most four exist in every completion; `58->62` has explicit finite dual formulas |
| EXP-050 | REFUTED; P1 PASSES FINITELY | all sixteen corrected representatives `b=a+2c` and exact lifts `Ry=2b` exist, but canonical corrections have support up to 101 and coefficients up to 71, refuting that section as a uniform proof basis |
| EXP-051 | REFUTED; P1/P2 PASS FINITELY | unreduced selection gives two exact independent cycles per completion; primary source support is at most six and divided-boundary coefficients are at most two, while raw support-size extrapolation fails |
| EXP-052 | CONFIRMED FINITELY | formulas trained on `p=8,9,10` exactly predict 36 and 50 coefficient-labelled holdout rows at `p=11`; direct identities and a separate 31-check reconstruction pass |
| EXP-053 | REFUTED ON P2; P1 PASSES FINITELY WITH RESOURCE OVERRUN | exact labelled pullbacks at `p=8,9,10` have supports 125, 178, and 238 with 78 skeletons; both completions use the same source chain, while `p=11` remains locked |

## 3a. Exact evidence anchors

- EXP-005 search aggregate:
  `0f580de2707a00fdd52e1b3c04e7767b97ce7b0a826593b119e9a49ae04da743`.
- EXP-006 Route K external manifest: 80 files, 354,465,653 bytes, aggregate
  `8c4c82415b79f0d1f27e43a60e276c8d67d54170df09cf1a9ef4099f86fb5006`.
- EXP-006 independent audit aggregate:
  `e483b0f66d9b65118b77d758df051b8c9eaea83b15c828720804ad1c29d5a39e`.
- EXP-009 campaign: `p=2,...,300`; exactly `p=2,3` fail; aggregate
  `81d5a8eb6cf2e848807323e3b0bdba58c464779d25cdc788cef027585540dce2`.
- EXP-009 Route K reproduction hashes:
  `p=4`: `5692f234e4398fd967e3dc94a9c203067a3c0634dfbedb9c19143003100bd017`;
  `p=5`: `5ec44ddea51b09125614e0b9518463483ff1fb218d0ad6d704a3c916d1a3887e`.
- EXP-009 independent audit samples `p=4,5,17,73,151,300`, plus all 297 positive-row hashes;
  audit aggregate `eb2aaf17650ed99f4e220a43c53bdd8835c82688a37567bb154c30a1ae520ce9`.
- EXP-020 campaign and audit aggregates:
  `02cf6f62a71de1a897cd46149e8c89d1c55bf810d28dddc02fc6c5330b9c1aed` and
  `c439f7e4fbd3cee983f32e5c6a27b347017c165cdf6d9fee54eb8d53ab634eac`.
- EXP-021 campaign and audit aggregates:
  `3857877586143a3be5f14852feb12bd9efbfdf7c1cde458f30e8cd689155a95b` and
  `1779407050b199039d3f6d808a720ea051a81ef11734fd1bccd1a76ec78c0a9c`.
- EXP-023 campaign, independent audit, and Presburger-query aggregates:
  `d23792c47a2e07785a27ebc71e99619705f7aa53a38ebe7f66ffa03b0518ce83`,
  `a27b3b13fde197b1f011bf07dc2c321d84ab7c895c9aa02d7c2a073e48f18038`, and
  `832c8421fe66359b8c246e3465e27de6ea7829215f892ab815e72b1f44787194`.
- EXP-024 campaign and independent all-row audit aggregates:
  `baf6200a442be9476cd083fde753bbdd9e623c06aa2528f3a7f138ee825637eb` and
  `b6035f615f2b2092351b5a42e5a734c72ba4783adf82943ed41b38fe07ef17e2`.
- EXP-027 campaign, symbolic, and independent-audit aggregates:
  `9bc93c41d899df4a39b85a452257d114000df84730d44f0661c19b7dd8322b63`,
  `b7e760290880e821fbc2ef86b03279edab1543307fd5c58cbb635d9c4b765db8`, and
  `f30b94ce86638732a407a3bb5abb4dfde8a1258441df71a36138dd0ae129d454`.
- EXP-028 canonical campaign aggregate:
  `45f08e6a15e321512629fa4b6ab07161ddcc766ddf56e1d9579175f3444ec32f`; the independent
  rational/Smith audit and symbolic/arithmetic certificate both pass.
- EXP-029 canonical campaign, independent audit, and symbolic aggregates:
  `7564f15534e8a29f875a367d3a324b95041e8eef836d15deac3e35130e1ad37d`,
  `337854eef5d773c84cdd79c7734e63b295fa0337c5a1852e652559c334949b04`, and
  `605733497d6fb0ead97bfd25e26daaa66d546c297751960e1c427f29ff69f279`.
- EXP-030 canonical campaign, independent audit, and symbolic aggregates:
  `de439ff5cf0784b332fcf811b17217579221afca42510f755963c81ff8beaa4d`,
  `bf5034efc37ec23edbd60d87c1eca36d437a9f9fc1e9d38f59816d8a7d3a7a16`, and
  `c519356b98ea0c76ec3d49d5f04e3512f711e601fa6491a8bf28dd337454968c`.
- EXP-031 canonical campaign, independent audit, and symbolic aggregates:
  `d68afbb5c54ebb86abbf420c389e1cacf666071cb35f83e5d2b67eccbc354858`,
  `0be4b659126064328b5ef14a40e488a836f874d2eed9b048d4d3f19da971346e`, and
  `e4bf2e0ae303e905efc9f985b239d059a5255b02d2ddc1d37abab5cc5cb2fc1f`.
- EXP-032 canonical campaign, independent audit, and symbolic aggregates:
  `907438b249b98ca9ffef689b7edb9574cdb0044cc3dd4cb52de523129f7d37ee`,
  `43635c8497dfe57904997326e983c7477e7320809cb2fee661c7933041f47b09`, and
  `f696390447a3ce20397d937aa73baebf23a3c5ae249d4ad1215ff48cb710a2ae`.
- EXP-033 canonical campaign, independent audit, and symbolic aggregates:
  `67bff9217c89f212916220e858ef5168abe2d64cdbd789488e0ce5f49204092a`,
  `6593291efaf092333bc42972c2f05712a151efb46f3f52ed9d28afd329585a4c`, and
  `58ab24887c79c3c075fdefea1f38ff2e1c1ef539490f7f52359149ed2bb1a4c8`.
- EXP-034 canonical, finite-rank, independent, and symbolic aggregates:
  `65ef176dcd9f5bd5467c09e763fdb20c67798de9743443ce5d0e34958c1645ce`,
  `31d70c09d251bb6009b610be05c33a42ccd50e417b84aff2c0db561018e6acc5`,
  `31479abd3c7247fe0ba464eefe06e437a595812c3d6055d0de8d0ced25d12794`, and
  `b3f461298706a394cc0f1a296557e10f52435f78d2f1039452fb726871b79a4d`.
- EXP-035 classification aggregate and target, independent, and symbolic artifact hashes:
  `cc98154e60bdc00fe1f503020aa7d5c66b53ff0cc4ce2158f199d03c2a5fda8b`,
  `4072a9fb7844d07763fae1b08e99da3d94d38cf3a40f980316c38f0931091276`,
  `b92e787bc120b5fa12aac1fc4a10792883e699ed7315055958f3916e8d10b60b`, and
  `b1bfc105f3e9ace368f181ccf10f367fe1f4d23199e49c14275bd8e9b941569e`.
- EXP-037 primary `(10,2)` and alternate-order audit hashes:
  `ca97087466fdd705e22f69e79cdfecfc7dbce0684475b98bd99757cfed030d7b` and
  `a8456b4d2de3fcf53cf97a63b63671656b4968fac80f8b8f151b76f43aba1b05`; the audit certificate
  passes with hash `0c6e72a55202001cd3096e6c4999045eee6ce0aeb7b266d2403c83f93409ce42`.
- EXP-038 audited primary/alternate hashes are
  `7b72b272338acfbd26dfe8e82a7fa425174e5d3fc3729ed785948f7d868a6ca1`,
  `4f7b60229c5e782891f3369ad6075c636a1452455d5df195844e919a2f3a47f1`,
  `960585dff4288a19242d0388f0c229a13701c2112dfa2f9cae415f5a2ff3d14e`, and
  `dbf5f7b34bead8dba6fda769b9561ee311455f62215df8b07370b051f8359097` for `p=11,12`.
- EXP-039 component campaign SHA-256:
  `831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c`; audit certificate
  external SHA-256 `55e3159dd01f9c412ad56a5808eda1f428672341b57ce5dd6eb4e2f266051534`.
- EXP-040 standalone `p=10` and combined `p=10,11` SHA-256 hashes:
  `8107af8e2810414144e5ee94f4caeaa634ca81e14af92b26050b3f50d48648b6` and
  `ad1fec04199ff94b803f95f98650c8c8ab386386240d584f447afbb9fe27668b`; audit certificate
  external SHA-256 `625f9ac10b8aaaf1e2cf4f8ba0d2d12cf1fe3b68745d2c418707c1e8be501482`.
- EXP-041 primary and reverse-profile SHA-256 hashes:
  `069e587b779bd1571d72e1a47bf74f4d1640dae5fbbf09907d2bf798c4941534` and
  `eafad05553cb7401c27ebeafcf686da6b436a25031dbc0f89e638096a6e02a1b`; audit certificate
  external SHA-256 `41b7ce59e354d841d82fe97ec3f74b0c5cc06836e85f332dc0318622b1a41cd2`.
  Its audited normalized isolated-skeleton hash is
  `d0c296e39c7c4f10ffd886b23b3b3d4d9cea0a291dd1aed6fcc079998c57676d`.
- EXP-042 primary SHA-256:
  `3c4ae292fb17a5daf473aee0ed37e473000de686607b5da0a0f4c357a8216ee2`; matrix SHA-256 values
  for `p=8,9,10,11` are `7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff`,
  `00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c`,
  `c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d`, and
  `69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9`. Audit certificate
  external SHA-256 `e35f38a86c4d6ab807d32cb3e8cd99b348e310df1d1a6840818a9ab84157cb8a`.
- EXP-043 primary SHA-256:
  `612d481eff7e00f5c5128d450a5eb05f79aacccb27bcd88c106dc0d5bf7426e6`; audit certificate
  external SHA-256 `6bad2a878e72b54fd3f2db704cb90dff425aff06531cc55ccdd2fde6cff5f01e`.
- EXP-044 primary SHA-256:
  `6766b6ca249f1b02ba9a83a6fb8434eea4e511172c982840fc3c6db6a192e886`; audit certificate
  external SHA-256 `324c98de4cdcf98b4fb6010343df9ceeab4c6347938c36c2614e2850cad254e1`.
- EXP-045 primary SHA-256:
  `569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8`; audit certificate
  external SHA-256 `a1a5bc105ecb7171970dd9b0b8daf4d823190a56b9a0f8e1e64a59479dcac3dd`.
- EXP-046 primary SHA-256:
  `1e78f650ef041eb1f45b4e979ea90a78709ef59ff443e57613edbc9cc6ea15b0`; audit certificate
  external SHA-256 `cae21dd006af047179242b9e5c60b3022c344953da3d57b62f826e4c682ab35a`.
- EXP-047 primary SHA-256:
  `f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c`; audit certificate
  external SHA-256 `bbdfaca4f9ba2032beac04f23b9e1db13fd6f1ca37518b957d91a1f55321c028`.
- EXP-048 primary SHA-256:
  `ba44eae4c9193bc941411b059dc7a7d7a4c69dff3d818e05d3395338e125a400`; its 78-check audit
  passes with internal hash `880e428c8abe78a7430546b1fb3d2e67b48b17e1c3a85b6e04fa402aff75e8da`
  and external SHA-256 `738d3b8e77c3a7cf2ca82692d7d7c9b1b4b97799a82ed3d808f8a6a1e621efed`.
- EXP-049 primary SHA-256:
  `567f554abaa1456133a4c0cd475d1848dad92a36dd8b9412381fe2fab9fc39b7`; its 98-check audit
  passes with internal hash `df2663ed0c81d4db9f24a205667a44868b152a9107177aac52ce4306978eb997`
  and external SHA-256 `fd74e83350c35a6e4e4f6a4778766c9b59e9c30347dc00104b428a904e0e6ca6`.
- EXP-050 results SHA-256:
  `2dc8f85097171e24f4080ce25684127914d86661a6291bab69fb334c2c987983`; its 152-check audit
  has external SHA-256 `eb62ef3e0b7801c44856ad135748f067a3d16846a109788af6e292ac074d99fe`.
- EXP-051 results SHA-256:
  `f1acaa6b769ec04b7d87a1ac416c184ffac2f5007d18a04efb397c8013ec8b1f`; its 409-check audit
  has external SHA-256 `aa1cddf1d40ca280d9c2bb3e7eaaed2039a204727e39e883eef1ddd1f59df6b4`.
- EXP-052 frozen candidate SHA-256:
  `6a16d8cf2c112a800558d634f6cd058ea00be43986c7b92f7f9406a6d282ca0c`; training, candidate
  check, holdout, and audit artifacts have SHA-256 values
  `259ff476b7bb09c12566e4bd771da5c88af17f541cc5732db4dc7f2067e2ec70`,
  `8b69d8bb37535211c21569249b9dc1f8f9632121fa2c9da3e4e80120169892e7`,
  `0bb32fd050a8e9739ea866ffb6e75b612189899c84c350a1214b60ed78eebc8b`, and
  `22adf44c85ec6e84ccc58be88024cd8ee04efca787a7b7c24a4a786eb0535fb1` respectively.
- EXP-053 training SHA-256:
  `0d6bb8b885d965ed91a94d06a072d8baacca56df65903e10e1c91382f649edfe`; its 62-check audit has
  external SHA-256 `4f283e79434d312c6de06a063b6784c17f6e0b422a4c97054c3a63c4dc822127`.

## 4. In flight

EXP-053 is REFUTED on P2 and passes P1 finitely after a resource overrun. It proves that the same source
chain produces both EXP-052 completion boundaries, while refuting generic HNF pullback as a
semantic route. HWB-078 therefore seeks one direct labelled identity on union mask `63`.
EXP-052 is CONFIRMED FINITELY with an untouched semantic holdout. It gives exact candidate formulas
for one nonzero class in each stable completion, but it is not an all-parameter theorem.
HWB-077 is active: construct labelled source chains proving `R_p y_p=2b_p` for arbitrary `p`,
obtain the second independent class, prove the bounded dual formulas generically, and prove an
independent free-complement or relative-Morse upper bound. EXP-051 shows that sparse unreduced
selection is the correct primal language; EXP-050 shows why canonical quotient sections are not.
EXP-047 remains the exact finite rank-two target, and EXP-049 supplies its finite dual lower-bound
mechanism. The `56->58` threshold quotient remains a separate filtered-relative problem.
EXP-046 is REFUTED overall with P3 retained, and HWB-072 is done. Masks `59` and `62` have no
unit leaves and all tested residuals have one connected core. HWB-073 owns the fill-producing
relative integer comparison. EXP-045 is REFUTED with a stable full-carrier antichain retained.
EXP-044 is REFUTED overall with P1/P3 retained. EXP-043 is CONFIRMED finitely and closes HWB-070.
EXP-042 is CONFIRMED finitely and advances HWB-069; HWB-071/HWB-072 own the relative integral
completion problem.
EXP-041 is REFUTED overall, with its P1 finite classifier retained; HWB-068 is done. EXP-040 is
REFUTED overall, with its P1 finite localization retained. EXP-037 exactly
refutes the previous series at its first new value:

```text
e_10=dim_GF(2) A_(10,2)-dim_GF(3) A_(10,2)=4240-4168=72, not 73.
```

Canonical-order `GF(2)` agrees with the primary low-degree order, and `GF(5)` agrees with
`GF(3)`. The proposed 73-point lattice index is therefore refuted as stated. EXP-038 tests the
smallest relation-style correction

```text
(1+2x+x^2+x^3-x^6)/((1-x)^2(1-x^2)(1-x^3)),
```

which predicts the genuinely new value `e_11=102`. This is a fitted falsification target. Even a
numerical pass cannot prove the proposed degree-six relation without an explicit certificate. The
first two gates now pass: `dim A_(11,2)=8688` over `GF(2)` and 8586 over both odd fields, while
`dim A_(12,2)=16822` over `GF(2)` and 16684 over both odd fields. Thus `e_11=102` and `e_12=138`
with low-degree and canonical orders agreeing. EXP-038 remains inconclusive because no
all-parameter recurrence or degree-six relation is proved. EXP-039 redirects from coefficient
extrapolation to exact connected-component anatomy of the unit-peeled combined core through
`p=9`; a giant defective component will refute that coarse model and activate matched-block or
relative-homology decomposition. EXP-039 performs that component test and refutes bounded
defect-one blocks, but its partitions identify four latent sectors. At `p=9`, the first three
merge with defect `35+5+5=45` and the fourth remains four. EXP-040 finds exact `67+5` at `p=10`,
so the first correction is in the large merged block. At `p=11`, exact `95+7` refutes the declared
`96+6` transport. EXP-041 profiles exact module-side, coefficient-interval, and exterior-block
atoms across `p=8,...,11`. Its switch prediction is refuted: all four isolated components retain
the same eight coefficient tags and the same normalized twelve-atom skeleton. The defects
`3,4,5,7` must therefore be explained by the signed differential inside that skeleton. The
distinguished EXP-035 row is absent from every defective profile and cannot anchor the reduction.
EXP-042 lifts the mod-two kernel through the exact signed integer matrices. Its independently
audited Bockstein ranks are `3,4,5,7`, so the isolated blocks have exactly that many nonzero Smith
factors of 2-adic valuation one. High-pivot image representatives lie in `D:B`; low-pivot
representatives lie in `K:C0`, so the atom localization is not canonical.
EXP-043 uses minimal prefixes of `31,52,83,125` verified 61-bit primes and exact squared Hadamard
bounds to prove rational ranks `1002,1607,2450,3586`. Combined with the Bockstein, the complete
isolated 2-primary cokernels are `(Z/2)^3,(Z/2)^4,(Z/2)^5,(Z/2)^7`.
EXP-044 proves finitely that `D:B` and `K:C0` are necessary row-projection interfaces but not a
sufficient carrier: deleting either and retaining only their union all give Bockstein zero. The
active object is a larger signed circuit among the six normalized row atoms.
EXP-045 exhausts that row-atom lattice. Full carriers are exactly `59,62,63`, with minimal
antichain `{59,62}` for every tested parameter. Their intersection `58` carries `1,2,3,5`, exactly
two below the full ranks; the minimal nonzero carrier changes to `56` at `p=11`.

EXP-036 is CONFIRMED with its all-parameter structural-propagation prediction unresolved.  Its
exact-sum route reproduces EXP-035 and computes the complete `p<=6` triangle plus `(7,2)`,
`(8,2)`, and `(9,2)`.  The exact `A_p=C_p` dimensions over `GF(2)` and `GF(3)` are

```text
(4,2) 4/3, (5,2) 24/20, (5,3) 3/2, (6,2) 95/86,
(6,3) 44/37, (6,4) 2/2, (7,2) 300/282,
(8,2) 808/777, (9,2) 1933/1884.
```

The tested `t=2` kernel cokernels have equal dimensions in all three tested fields for
`5<=p<=9`; their dependence is
created by the connecting quotient across the three tested fields.  The finite excess sequence
`1,4,9,18,31,49` refutes both
the candidate `(p-3)^2` and the later quadratic fit.  At `(4,2)`, 74 exact unit cancellations
leave a compact `5` by `45` residual with two entries `-2` and Smith cokernel
`Z^4 direct-sum Z/2Z`.  Its canonical active support has seven low variables, so the proposed
six-variable projective-plane recognition is not obtained.  Independently, the cubic-source gap
is at least `3(p-1)^2` for every declared `(p,t)`, proving `A_p=C_p` at all family targets.

EXP-035 is CONFIRMED with P3's coordinatewise mechanism refuted. For each `b in B_p`, the
primitive zero-coordinate summand is classified by `R_b subset F`. For `2<=t<=p-2`,

```text
[3p,4p-2] union {t} union [t+2,p],
```

has size `2p-t-1`, giving consecutive kernel classes. The canonical classification passes through
`p=300`. The first connecting smoke case has an explicit integral source cycle, but the complete
target quotient proves characteristic dependence at `p=4`: dimensions are `4` over `GF(2)` and
`3` over `GF(3)` for both `A_4` and `C_4`. HWB-058 through HWB-060 are done. Manuscript v0.22 is
published, fresh-download verified, and promoted.  HWB-061 remains open only for an infinite
description of the parity-sensitive connecting quotient; the finite propagation and cubic
transfer gates are now closed by EXP-036.  HWB-062 opens the in-place v0.23 manuscript update.

EXP-034 is CONFIRMED. With `S_p=P_p/(X_0)` and `M_p=K_p/X_0K_p`, the kernel has an explicit
two-layer offset basis and signed incidence maps `delta_i`. The first missing cell has

```text
b*=8p-1,   F*={1,...,p},   tau_p=8p-1+p(p+1)/2.
```

It is the unique target cell in that multidegree and has no incoming incidence face. Every
possible connecting-map contribution from `D_p` has a unique unit low boundary, so no source
cycle hits it. The long exact Tor sequence and minimal cubic cone give exact multiplicity one in
`K_p`, `A_p`, and `C_p`. Canonical rows pass for `p=4,...,300`; independent semigroup bases pass
through `p=25`; rational literal sources, two finite fields, symbolic inequalities, and controls
pass. HWB-055 and HWB-056 are done; manuscript v0.21 is published and fresh-download verified at
DOI `10.5281/zenodo.22135689`. PRs #222/#223 passed the required checks and HWB-057 is done. The
complete lower strands remain open.

EXP-033 is CONFIRMED. Put `A_p=P_p/Q_p`. The colon intersection and pullback give

```text
Q_p=(Q_p,f_p) intersect (Q_p:f_p),
0 -> K_p -> A_p -> D_p -> 0,
H_(K_p)(z)=(8p z+10p z^2)/(1-z).
```

The EXP-026 regular element `X_0` makes `K_p` one-dimensional Cohen--Macaulay of regularity two.
Depth, Auslander--Buchsbaum, and the terminal Hilbert coefficient then give

```text
depth(A_p)=1,   pd(A_p)=10p-1,   reg(A_p)=2,
beta_(10p-1,10p+1)(A_p)=10p.
```

The cubic shift separates all comparison-map source and target degrees, proving
`B_C=B_A+x z^3 B_D`. Thus both regularity-three/four strands have the complete formulas at the
top of this handoff. HWB-053 is complete: manuscript v0.20 is published and fresh-download
verified at DOI `10.5281/zenodo.22062161`. Structure/content/template guards, Ruff, all 60 tests,
the full registry pipeline, and manifest/artifact consistency pass. The pipeline reconciles four
previously unbaked records, including EXP-033. PRs #218/#219 passed required checks and promoted
the exact payload through `develop` and `main`; HWB-054 is done. The next mathematical route is the
two lower strands of `A_p` through the same `K_p` extension.

EXP-030 is CONFIRMED. Put

```text
L_p=[0,p] union [3p,4p-2],
A_i=X_i,                     0<=i<=p,
B_j=X_(3p+j),                0<=j<=p-2.
```

After killing the `8p` high variables in the cubic colon, the low quotient is

```text
k[s,t]^(p) semidirect omega_(k[s,t]^(p)),
H(z)=(1+(2p-2)z+z^2)/(1-z)^2.
```

The exact colon is `Q_p:f_p=Q_p+(X_h:h in H_p)`. Its Hilbert numerator and high-variable Koszul
extension, followed by integral relative matching, give

```text
beta_(2,3)(P_p/(Q_p:f_p))=beta_(3,6)(C_p)=8p(7p^2-12p+2)/3.
```

The support is `[3p+4,29p-5] minus ([6p-3,6p+1] union [9p-3,9p])`, containing `26p-17` offsets.
Complete profiles at `p=4,5,6` total `704,1560,2912`; the corrected independent audit matches every
coefficient and selected rational ranks; the symbolic certificate passes. The first audit attempt
that inserted forbidden offset `8p-1` is preserved as invalid non-evidence. HWB-043 is done.

EXP-029 remains CONFIRMED. Its free pair basis gives
`beta_(3,(5,b))=#{ {a,c} subset H_p:a<c and a+c=b-3p }`, where `|H_p|=8p`, and the complete
internal-degree-five diagonal displayed at the top of this handoff.

EXP-028 is CONFIRMED. For every `p>=4` and every field, the complete second row is

```text
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(2,4)=8p,
beta_(2,5)=p(2p-3),
beta_(2,6)=0,
beta_(2,j)=0 otherwise.
```

The degree-five support and profiles are

```text
[3p+2,5p-2]: m_out(r),
[6p+1,8p-3]: m_mid(r),
[9p,11p-4]: m_out(2p-4-r),
m_out(r)=min(floor(r/2)+1,floor((2p-4-r)/2)+1),
m_mid(r)=min(r+1,2p-3-r,p-2).
```

The integral relative-chain matching yields a unit Smith form in degree five and no critical edge
in degree six. The exact campaign covers `p=4,...,300`; complete profiles at `p=4,5,6` total
`20,35,54`; the smallest case agrees over `GF(2)` and `GF(1000003)`; the independent audit rebuilds
rational ranks and Smith factors; and the arithmetic/Z3 certificate checks count and endpoint
identities. Proof and verdict live under `experiments/EXP-028-complete-second-betti-row/`.

The v0.15 expansion of the main conductor-fiber manuscript passed complete claim/build/render,
sole-authorship, metadata, authenticated draft, publication, and fresh-download gates. It is
public as record `22016550`, DOI `10.5281/zenodo.22016550`; its 674,169-byte PDF matches committed
SHA-256 `e7d3fb747f01b6c44c84ca9c2cf25a746cd2d05eb0996163f4a18e9e3cea1be9`. HWB-039 is done.
PR #198 passed `guards` and `test` and merged to `develop` at `b83b9aa0`; PR #199 passed both jobs
and promoted the identical payload to `main` at `5ce1efa3`. Work, `develop`, and `main` share tree
`e35f420f59a5343ea09da15985786ab0b65897d6`. CAOS_MANAGE PR #566 promoted the scoped controls and
ledger to `main` at `ddafe393`; management `develop` and `main` share tree
`f234e662fa13834787c994b789d6607b486c19ec`. HWB-040 is done. A separate manuscript remains
deferred until higher-row results create a distinct narrative.

Previously closed state:

EXP-024 is CONFIRMED. Its deductive homological argument proves

```text
pd=10p-1, reg=4,
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(10p-1,10p+1)=10p,
beta_(10p-1,10p+3)=1,
beta_(10p-2,10p+2)=8p.
```

The canonical module has `10p` generators in degree `-1` and one in degree `-3`. The campaign and
independent audit agree for all 297 parameters. The theorem determines exact resolution edges,
not the interior Betti table. Manuscript v0.13 is a published and fresh-download-verified 29-page
preprint at DOI `10.5281/zenodo.21995498`. Repository promotion is complete: PR #182 merged to
`develop` at `26c52103`, PR #183 merged to `main` at `f24b078b`, and documentation PRs #184/#185
closed the durable handoff at tree `b70a3990583057a92e591c34d5f9e9c101185e8c`.

EXP-011 is CONFIRMED. With `s=6p`, it proves

```text
Q_p = [p+1,2p-2] union {2p,4p},
Lambda_p = Gamma_p union (7s+Q_p) union {13s-1}.
```

The invariants are multiplicity `24p`, Frobenius `54p-1`, conductor `54p`, genus `38p-1`, and
embedding dimension `12p`. The symbolic proof uses adjacent value-set blocks; the deterministic
campaign and audit aggregates are
`e21926a689178a6c70b3b6e8319053edd0fd13f164ced9565d3b976e6159c0b0` and
`2ed711045ad83a3b47fb3e71d4c75ae9bfa9be1a5dd9a8c4072d5f170510343b`.

Manuscript v0.04 passed its claim audit, clean two-pass build, and complete 12-page rendered
inspection before publication.

EXP-012 is CONFIRMED. It proves

```text
PF(Lambda_p) = (6s+B^c) union (7s+Q^c) union (8s+C^c),
type(Lambda_p) = reduced_type(Lambda_p) = 10p.
```

The consequence is maximal reduced type and failure of almost symmetry for every `p>=4`.
The invariant-first proof uses the last multiplicity window plus explicit witnesses excluding all
lower gaps. The exact campaign and independent audit aggregates are
`9bed38fb1c786c3740e000dde7ea7d79a7e7c83fa584ff12fc2c4623b5d503ec` and
`0315c4c22c41e0d2b8a5abb27f717a4d4a6f7356ef30ca388206d739e0de2c37`.

EXP-013 is CONFIRMED after one preserved correction. With `H_p=(s-1)-Q_p`, it proves

```text
tr_(R_p)(J_p)=R_p:E_p=tr_(R_p)(E_p)=T_p,
length(R_p/T_p)=length(E_p/R_p)=p+1.
```

The exact value set has blocks `4s+A_p`, `5s+(A_p union B_p)`, `6s+B_p`, `8s+C_p`, the full
interval `[9s,13s-2]`, and the tail from `13s`. The initial shorthand `[9s,infinity)` was refuted
at `13s-1` by the first smoke run before any campaign artifact. Corrected campaign and audit
aggregates are `77448398a26b958c66818b7ac4aaa4b542bad11cdba5ec7c8f7fe76db37526e2` and
`d55ed876d7918cb4c46d8e5f3894a508d172693bde4b4c76cb67c42fcfbf0ac1`.

EXP-016 is CONFIRMED after EXP-015 preserved the failed first square tail. It proves
`length(T_p^2/t^(4s)T_p)=14p`. EXP-017 continues the exact powers and proves reduction number four,
successive quotient lengths `23p-1,14p,2p,1,0`, and `e0(T_p)=24p`, `e1(T_p)=39p`. Its campaign
and independent-audit aggregates are
`e9c3c887648f08cf67c614b381f00c8c6520dcd1bb89f8cdece62293bfd06030` and
`0f6ed70676ffb8972b8b167ad52c4f9d2851f69c3b1d96f4023e5e3d5825c781`.

EXP-018 is CONFIRMED. For `Q_p=t^(4s)R_p`, the only nonzero Valabrega--Valla component is
`(Q_p intersect T_p^2)/(Q_pT_p)`, with exact length `p`; every component at `n=0` and `n>=2`
vanishes. Hence `gr_(T_p)(R_p)` has depth zero. Its Hilbert numerator is
`(p+1)+(9p-1)z+12pz^2+(2p-1)z^3+z^4`, despite all coefficients being positive. Campaign and
independent-audit aggregates are `9631c644732f0921be3b3027e18a01110f23dad897fbf2cb14dd3a493eda5971`
and `7c2abcd290bc3461fc5251bc3372e20a7fa25c888e3b2ed635368b4dda0781ff`.

EXP-019 is CONFIRMED. The complete zeroth local cohomology is the same `p`-class obstruction,
concentrated in degree zero, and the full homogeneous maximal ideal annihilates it. Thus every
conductor tangent cone is Buchsbaum but not Cohen--Macaulay, with unbounded Buchsbaum invariant
`p`; the quotient by `H^0` is Cohen--Macaulay. Campaign and independent-audit aggregates are
`854d7889d9d7b911b462e4d483e021210ae2873ae0ec0091ec30e8fb29d6dbf7` and
`0b01853febc9e9754e28abcd099a7ae3a97f4cc0ab92f3a345ab2ae03cd3c68a`.

Published baseline:

- v0.01 DOI `10.5281/zenodo.21763583`: Frobenius minimality.
- v0.02 DOI `10.5281/zenodo.21764868`: minimum-layer uniqueness. Public PDF SHA-256
  `93a07d124c7b3f2cf144a5343d31ca40e312a80d99308b3ef567c7065f126bb9`.
- v0.03 DOI `10.5281/zenodo.21873911`: explicit infinite family. The public 399,272-byte PDF has
  MD5 `bd9767de4a530150073f654c76ba84a0` and SHA-256
  `f2edff24e924a8d38bc7becd380a69f30fa6b2466c3f584802b829f14d1393cf`.
- v0.04 DOI `10.5281/zenodo.21876338`: uniform endomorphism-overring theorem. The public
  491,757-byte PDF has MD5 `248297d0a833ba21dce27d738a50e92f` and SHA-256
  `025cea4c59c4301ff6925cfe43353c7ac1c6cd8b4fc56a8c6d648347f418e825`.
- v0.05 DOI `10.5281/zenodo.21907297`: pseudo-Frobenius/type and exact trace/conductor theorems.
  The public 515,650-byte PDF has MD5 `75a1102cc9dab8785ee00ba7f93012e7` and SHA-256
  `4bd2cfd7351cb6cec1b3fa006c7eb3018732c283b5bb5a1e5c86015435275276`.
- v0.06 DOI `10.5281/zenodo.21907943`: duality correction and exact conductor-stability theorem.
  The public 526,699-byte PDF has MD5 `4ff26288ef70a875ebf3f17cb726ff16` and SHA-256
  `10cc2bd31026cfe6a921c4cf54832a7df018b0f0b0f38ee196bc597954255dd4`.
- v0.07 DOI `10.5281/zenodo.21908188`: conductor reduction number and Hilbert data. The public
  539,211-byte PDF has MD5 `5ed0616521a3363fb9cb6507babf9745` and SHA-256
  `2dca97dc100424afbeffd525fe66aa4aa43ce65c82c11b9ac43250cd33771e19`.
- v0.08 DOI `10.5281/zenodo.21908490`: depth-zero conductor tangent cone and exact Hilbert series.
  The public 552,905-byte PDF has MD5 `29a4c70d45517a61d6eb01f028487b39` and SHA-256
  `c8a038adf042a71126e0b0dac170803340e12300521aad1ca05f88bbc3c32f69`.
- v0.09 DOI `10.5281/zenodo.21908785`: complete tangent-cone torsion, Buchsbaumness, invariant,
  and Cohen--Macaulay quotient. The public 567,854-byte PDF has MD5
  `c0605ace2b60d6830fd6e68d68d883b0` and SHA-256
  `ecf4d1ebe504ad3af74d123c949a953a7f397dabd72ec11c94a631962e1501db`.
- v0.10 DOI `10.5281/zenodo.21909127`: complete Noether-normalization module, minimal graded
  resolution, regularity, `a`-invariant, and parameter-section identity. The public 578,949-byte
  PDF has MD5 `830ae1fd2e2fbf923a86cbf575e9a841` and SHA-256
  `00a78fd8101f106724877b3fdbc933c51024a872a2b9a4f05692358b4d1a9d03`.
- v0.11 DOI `10.5281/zenodo.21909961`: canonical conductor special fiber, exact type, and
  nonlevel theorem. The public 589,535-byte PDF has MD5
  `1ad22a6a87c0c6a5a80f8a913d06ca95` and SHA-256
  `0b3a9131e3c419c0a89cb064ea6beb7c696006171fe18bec578e7ba963a520ce`.
- v0.12 DOI `10.5281/zenodo.21988601`: full defining ideal, exact first Betti row, relation type
  three, and non-Koszulness. The public 615,252-byte PDF has MD5
  `c8b810a763b9bb55d076a454df49b413` and SHA-256
  `98d730fb8afaf40149d028bdde0b1c3ba9851f1dbcd15475567e56bb7eb17d3f`.
- v0.13 DOI `10.5281/zenodo.21995498`: homological edge theorem. The public 635,617-byte PDF has
  MD5 `d6ce72589100d1f57986da000501fdc7` and SHA-256
  `cc9e721c3f0155181b963095a0b0efcc37e023546b32c6dd61b772a3d30ec7ed`.
- v0.14 DOI `10.5281/zenodo.22013515`: first interior Betti strand.
- v0.15 DOI `10.5281/zenodo.22016550`: complete second Betti row.
- v0.16 DOI `10.5281/zenodo.22029468`: colon-Koszul degree-five diagonal. The public 691,569-byte
  PDF has MD5 `ad69991f41c4f35da3c03f2c1ce343e9` and SHA-256
  `4c2a49ae6e1a959afb8df4a365feb4c815d408f3746b5ef1df14ee5746abd554`.
- v0.17 DOI `10.5281/zenodo.22030167`: complete cubic-colon idealization and degree-six third
  strand. The public 714,021-byte PDF has MD5 `4c7daffba7539f37ea4ecb6d52fad9d9` and SHA-256
  `480f135b9ecf8dbcec0fb91e85491f8fcf11e1e3c7417f6415ebeda366b5d640`.
- v0.18 DOI `10.5281/zenodo.22030743`: integral degree-seven vanishing and complete third row. The
  public 725,554-byte PDF has MD5 `558532167c4f2a39e03d1bcced9de18d` and SHA-256
  `0e40aa5ed4feb02209137c2982184a93cfd402ac03cc9d4aa6f9ba86ae4327b7`.
- v0.19 DOI `10.5281/zenodo.22031481`: complete cubic-colon Betti polynomial.
- v0.20 DOI `10.5281/zenodo.22062161`: minimal cubic cone and complete top two strands. The public
  774,246-byte PDF has MD5 `69f45597e879afc8fd91ca4157fb2cf3` and SHA-256
  `163a3a2fc6a5d61b6ff97e3ed1089dc3b6e9b320aa9c68ed67d2f1155362d743`.
- v0.21 DOI `10.5281/zenodo.22135689`: first surviving lower-strand class. The public 792,863-byte
  PDF has MD5 `13b92773205a49977abb88cd7ab8dde1` and SHA-256
  `c717fbb4d6d3178e0fb0786a8a61c9e2c109d97d77a7b9e1308a2274c0f97539`.
- v0.22 DOI `10.5281/zenodo.22177072`: primitive zero-row classification and first
  characteristic-dependent lower cell. The public 810,905-byte PDF has MD5
  `5ed2409d6688b30147963a7293598440` and SHA-256
  `3868f511a047073c9d7bedf25e026f1aaf3a5ab2c05c45d03614675ef6bdf5c2`.
- v0.23 DOI `10.5281/zenodo.22181972`: finite propagation through `(9,2)`, two torsion
  mechanisms, compact localization, and family-wide cubic transfer. The public 824,114-byte PDF
  has MD5 `6bcacfa265e840f40e89dcdb87b75f7b` and SHA-256
  `c77b08a3724db90b14039c2c88e98325403ef4f656f52137057a27eb6fa5072d`.
- concept DOI `10.5281/zenodo.21763582`.
- The concept latest resolves to record `22181972`; title, version, sole author/ORCID, licence,
  filename, bytes and both hashes were checked from a fresh public download.

## 5. Next actions

1. Construct one labelled source-domain chain directly against the union of the frozen EXP-052
   formulas on `58->63`, and prove `R_p y_p=2(b_p^A+b_p^B)` symbolically for arbitrary `p`.
2. Extract and holdout-test a semantic formula for the second independent class in each
   completion, then prove both support-four parity-dual formulas by generic signed incidence.
3. Build the independent upper bound: reduce the quotient left after the two detected classes to
   a free module by a parameterized relative-Morse matching or explicit integral complement.
4. Treat `56->58` separately by dual parity characters or a relative algebraic-Morse filtration;
   its canonical representatives refute the single-translation-family model.
5. Localize `(5,3)` and `(6,3)` integrally to decide whether their equal kernel rank defects share
   a signed core; keep this separate from the connecting-only `t=2` mechanism.
6. Open a separate manuscript only after a complete strand, an infinite connecting theorem, or a
   comparably transferable result is proved.
7. Reconcile only the scoped CAOS_MANAGE Huneke-Wiegand mirror on its existing `develop` branch;
   preserve its unrelated dirty work.

### Lenses ledger

- Exclusion: positive theorem hypotheses are tested against exact family invariants, not guessed.
- Anatomy: EXP-011 upgrades the seed-only endomorphism calculation to a proved parametric theorem.
- Invariant: adjacent blocks `V_k intersect V_(k+1)` decide the exact overring without SAT.
- External dialogue: Maitra-Mukundan redirects the next round to maximal reduced type, while
  Lindo-Maitra-Zhang opens a separate trace/endomorphism route.
- Trace redirection: because `R_p` is Gorenstein, equality of the two traces is not discriminatory;
  EXP-013 targets their exact common value ideal and colength instead.
- Adversarial: minimal-generator and Apéry PF reconstructions plus corrupted PF formulas are
  required.
- Noether-normalization: EXP-020 tests whether the entire tangent-cone defect is isolated in `p`
  exponent-one cyclic summands over the minimal-reduction polynomial ring.
- Fiber-cone restoration: EXP-021 tests whether killing that torsion is canonically the special
  fiber algebra, and uses its Artinian reduction to decide type, levelness, and Gorensteinness.
- Factorization graph: EXP-022/023 translate minimal defining equations into connected components
  of equal-total offset factorizations and isolate one primitive cubic circuit.
- Exact symbolic exclusion: affine Presburger cells close every degree-three through degree-five
  component uniformly, with finite campaign and independent graph routes as adversarial support.
- Relative-chain matching: EXP-027/028 turn offset-graded Betti entries into integral homology and
  use unit pivots/Smith forms to isolate actual classes without characteristic extrapolation.
- Colon-Koszul redirection: EXP-029 reads the exact linear cubic colon two-sidedly. Its second
  Koszul wedges supply all degree-five third syzygies; integral relative `H_2` matching proves
  completeness and a primitive, characteristic-free pair basis without a raw resolution sweep.
- Recognition/idealization: EXP-030 identifies the entire cubic-colon quotient with the canonical
  idealization of a rational normal curve. Its Hilbert numerator and integral relative normal form
  determine the complete degree-six third strand without a raw resolution sweep.
- Two-layer Artinian reduction: EXP-034 kills the regular element on `K_p`, converts its resolution
  to offset-labelled incidence maps, and separates existence of a kernel class from survival
  through the multigraded connecting map.
- Forbidden-neighbor zero rows: EXP-035 uses `R_b subset F` to split off primitive integral
  cokernel coordinates before any rank computation, then tests the connecting map on the first
  block below the `D_p` row-two threshold.
- Torsion anatomy: the failed EXP-035 pivot reveals a `Z/2` incidence cokernel factor. Complete
  target quotients replace coordinatewise survival guesses, and characteristic comparison becomes
  the next invariant-first route.
- Torsion recognition: EXP-036 confirms a compact factor-two residual but its canonical active
  support has seven low variables, so the declared six-variable projective-plane recognition is
  not obtained.
- Connecting-parity redirection: exact `t=2` kernel-cokernel dimensions agree in the three tested
  fields for
  `5<=p<=9`; the next invariant is the mod-two homology of the connecting quotient, not the Smith
  form of the kernel matrix or a polynomial fit to finite dimensions.
- Component/graded-module view: EXP-038's two new values support but do not prove the corrected
  Hilbert numerator. EXP-039 tests the cheapest exact structural consequence first: whether the
  signed residual support splits into bounded recurring defect-one blocks. Failure activates a
  finer matched-block or squarefree-divisor-complex homology analysis.
- Merged-sector relation: EXP-039 refutes bounded components but turns the old coefficient law
  into four exact finite sectors. EXP-040 tests whether the `-x^6` correction is carried entirely
  by their merged orientation-sensitive block, with relation multiplicities one and two.
- Sector-identity correction: EXP-040 localizes the first correction at `p=10` but refutes the
  naive component transport at `p=11`. The next invariant is the semantic interval tag of each
  component, not another rank total or an assumed persistent support label.
- Semantic-tag recognition: EXP-041 applies exact affine interval atoms and a frozen-component
  regression. Its declared lineage switch is false: one normalized twelve-atom skeleton persists,
  so the next invariant is its signed differential rather than another component label.
- Signed-normal-form route: HWB-069 prioritizes integral matched-block cancellation in the isolated
  component. Relative squarefree-divisor homology and OI/FI finite generation are proof frameworks
  only after explicit chain maps are constructed; toric gluing remains downstream because no
  toric-ideal or chain splitting is yet proved.
- Bockstein gate: EXP-042 proves finite first-Bockstein ranks `3,4,5,7` under independent
  reductions. This counts valuation-one Smith factors exactly. Its row-atom representative is
  pivot dependent, preventing a false canonical localization claim.
- Rational-rank closure: EXP-043 makes all `(r+1)` minors divisible by a distinct-prime product
  larger than twice their Hadamard bound. This proves `rank_Q=r` and completes the tested isolated
  2-primary torsion without a full Smith form.
- Signed-circuit localization: EXP-044 refutes the two-atom carrier. Both marked atoms are
  necessary interfaces, but their union is insufficient. The complete six-row-atom subset lattice
  is the next bounded gate; integral reduction remains mandatory afterward.
- Carrier lattice: EXP-045 gives stable minimal full masks `59,62`, common core ranks `1,2,3,5`,
  and constant completion two. Relative integral presentations, not further global ranks, are now
  the active finite proof gate.
- Arithmetic deletion-contraction: matroids over rings provide a module-valued vocabulary for the
  row-subset lattice. EXP-046 refutes the cheaper unit-core mechanism: the minimal full carriers
  have no leaves and all residuals stay connected. No uniform matroid-over-rings structure is
  claimed.
- Fill-producing relative reduction: HWB-073 uses certified fraction-free Hermite or
  Schur-complement operations to remove free directions and expose the two parity classes.
  EXP-047 completes the exact finite Smith step; HWB-074 must now turn it into a uniform semantic
  reduction. A field-only reduction is diagnostic, not an integral proof.
- Semantic Bockstein transport: EXP-048 replaces opaque HNF classes by four explicit growing
  interval chains for the stable completions. Their linear growth refutes a bounded-critical-set
  premise but supplies the first concrete `p->p+1` targets. The new proof obligation is an exact
  source lift plus dual parity functionals, not another canonical quotient basis.
- Integral-lift separation and duality: EXP-049 proves the zero-one semantic supports are not
  literal torsion vectors and isolates the required even corrections. The dual side is much
  smaller: all finite certificates use at most four rows, and the `58->62` pair has fixed endpoint
  formulas. This now outranks a global primal Smith reduction for the lower bound, while a
  relative-Morse/free-complement theorem owns the upper bound.
- Canonical-section obstruction: EXP-050 proves existence of every corrected lift but shows that
  HNF-selected correction growth is a coordinate artifact, not evidence against a uniform chain.
- Unreduced-cycle selection: EXP-051 finds the simple object before quotient normalization. Its
  primary source cycles use at most six columns and its exact divided boundaries use only
  coefficients of absolute value one or two.
- Leakage-controlled semantic holdout: EXP-052 freezes the formula after `p=8,9,10` and only then
  opens `p=11`; exact multiset prediction, direct multiplication, and an independent rebuild all
  pass. This is materially stronger than interpolation but remains finite evidence.
- Common-source union: EXP-053 refutes semantic compression through generic HNF pullback but shows
  that both first-class completion formulas are restrictions of one source chain. The union
  `58->63` is therefore the correct target for a single direct telescoping construction.

## 7. Gotchas

- The broad Huneke-Wiegand conjecture is already false by the public seed. CAOS's new theorem is
  an infinite family in numerical semigroup rings with two-generated monomial ideals; it is not a
  classification of arbitrary modules or arbitrary one-dimensional Gorenstein domains.
- Son Pham retains discovery priority for the first public counterexample.
- Expert verification is not journal peer review.
- Never import or execute upstream verifier code as independent CAOS evidence.
- A finite sweep is not the infinite-family proof; the affine interval argument is load-bearing.
- Solver SAT needs independent semantics. Solver-only UNSAT cannot carry a theorem; use an accepted
  certificate or a complete exact symbolic reduction with an independent route and disclose any
  remaining solver trust boundary. Equality in a finite window needs a proved tail.
- The family is outside the generalized-arithmetic-sequence positive class, but this does not
  exhaust all surviving variants.
- Published Zenodo versions are immutable; corrections or extensions require a new version.

## 6. Where everything lives

| what | path |
|---|---|
| problem tree | `problems/commutative-algebra/huneke-wiegand/` |
| programme record | `program/huneke-wiegand/` |
| experiments | `problems/commutative-algebra/huneke-wiegand/experiments/` |
| manuscript | `manuscripts/huneke-wiegand/frobenius-minimality/` |
| external evidence | `E:/_Datos/caos-research/huneke-wiegand/` |
| management mirror | `_CAOS_MANAGE/plans/caos-research/huneke-wiegand/` |

## Resume command

Read root `Entry_point.md`, this file, `plan.md`, `state.md`, `backlog.md`, and the latest relevant
experiment verdict. Continue the highest-priority unblocked item without changing the product
branch or importing the candidate repository's verifier as CAOS evidence.

## 2026-08-12 in flight - EXP-021

EXP-021 is CONFIRMED. It proves `T_p^2=m_pT_p` and the canonical graded-algebra identification
`G_p/H^0 isomorphic to F(T_p)`. The fiber cone is Cohen--Macaulay of type `10p+1`, but its
Artinian socle occurs in degrees two and four, so it is neither level nor Gorenstein. The exact
campaign passed all 297 parameters after one preserved budget-only attempt; the independent audit
rebuilt six parameters and rehashed every row. Manuscript v0.11 is published and fresh-download
verified at DOI `10.5281/zenodo.21909961`. The active gate is repository PR promotion. After that,
HWB-023 defining ideals is the strongest identified next path, but it requires a separate
hypothesis and source preflight before implementation.

PR promotion is complete: #172 merged the tested theorem/publication round to `develop` at
`178a7361`, and #173 promoted the identical tree to `main` at `7abd1040`. Remote `develop` and
`main` share tree `21791e6a`. Persist this handoff through the same PR path before declaring
HWB-023. No global release tag is part of this research round.

## 2026-08-17 in flight - EXP-022

The EXP-021 promotion handoff is complete. HWB-023 is now active as EXP-022 after a separate
source and novelty preflight. The published Abdolmaleki--Kumashiro theorem bounds the defining
degrees by five. EXP-022 tests the stronger family-specific conjecture that the defining ideal of
`F(T_p)` is generated by its quadratic value-congruence kernel, which would give

```text
beta_(1,2)=50p^2-17p,  beta_(1,j)=0 for j>=3.
```

No such theorem is yet claimed. The exact next command is the mandatory `p=4` degreewise smoke
gate after implementing Route A and its independent closed-basis checks. Preserve and report the
first disconnected congruence component if quadratic generation fails.

EXP-022 is now closed REFUTED. The first disconnected component is the universal relation

```text
X_0^2X_(3p)-X_p^3.
```

Its two monomials admit no quadratic move, proving `beta_(1,3)>=1` and nonquadraticity for every
`p>=4`; meanwhile `beta_(1,2)=50p^2-17p`. Exact complete runs at `p=4,5,6` find first Betti
profiles `(732,1,0,0)`, `(1165,1,0,0)`, and `(1698,1,0,0)` through degree five. The next action is
to declare, before any broader run, the corrected one-cubic presentation hypothesis and attack its
uniform connectivity upper bound. No manuscript or publication update is yet triggered.

EXP-023 is now declared for the corrected claim

```text
J_p=((J_p)_2,X_0^2X_(3p)-X_p^3),
beta_(1,3)=1, beta_(1,j)=0 for j>=4.
```

Its independent route uses `O(p^2)` congruence states rather than degree-five monomial
enumeration. The immediate action is to reproduce `p=4,5,6`, then run the bounded campaign and
derive the uniform interval-graph connectivity proof. Relation type three, the exact total equation
count, non-Koszulness, and any manuscript trigger remain unconfirmed predictions.

## 2026-08-18 in flight - EXP-023 and manuscript v0.12

EXP-023 is CONFIRMED. The state graph proves that, modulo lower equations, every valid total has
one component except degree-three total `3p`, where the two components are represented by
`X_0^2X_(3p)` and `X_p^3`. Degrees four and five have no defect. The published relation-degree
bound therefore gives the full defining ideal and exact first Betti row
`(50p^2-17p,1,0,0,...)` for every `p>=4`.

The `p=4,...,23` exact campaign passes in 249.611 seconds, and the separately encoded audit
reconstructs `p=4,13,23` while rehashing all 20 rows. The exact Presburger cover closes 133
terminal negated queries as UNSAT with no counterexample or unresolved leaf. The first attempt that
crossed its five-minute budget remains preserved as inconclusive. The solver/encoding trust
boundary is recorded in the verdict because no separately checked UNSAT proof object exists.

HWB-023 and HWB-025 are done. Manuscript v0.12 passed claim/build/render and sole-authorship QA,
was published as Zenodo record `21988601`, and its fresh public download matches the committed
615,252-byte PDF at SHA-256
`98d730fb8afaf40149d028bdde0b1c3ba9851f1dbcd15475567e56bb7eb17d3f`. Delivery is complete:
PR #176 passed `guards` and `test` and merged to `develop` at
`aecb5b5c`; PR #177 passed all required checks and promoted it to `main` at `80de49e5`. Remote
`develop` and `main` shared tree `5469624bab95a087aaef37630ea9c2a27c656054`. Documentation-only
PR #178 passed `guards` and `test`; PR #179 passed all required checks and completed the handoff.
At that handoff, no further experiment was declared.

## 2026-08-18 in flight - EXP-024

A fresh primary-source and novelty preflight corrected one stale v0.12 open question: regularity
over the full presentation polynomial ring is already forced to equal four. EXP-024 now asks how
much more of the resolution follows from the exact h-vector, Artinian socle, and EXP-023 first
Betti row. The declared targets are

```text
pd=10p-1,
reg=4,
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(10p-1,10p+1)=10p,
beta_(10p-1,10p+3)=1,
beta_(10p-2,10p+2)=8p.
```

The canonical module has `10p` minimal generators in degree `-1` and one in degree `-3`.
EXP-024 is CONFIRMED by the symbolic proof, two independent degree-three derivations, exact
297-parameter campaign, all-row independent audit, selected source reconstructions, frozen
premise hashes, and seven adversarial controls. Manuscript v0.13 adds this theorem without a
split, passed its 29-page claim/build/render and sole-authorship gates before upload, and is
published at DOI `10.5281/zenodo.21995498`. A fresh public download matches the committed PDF.
A separate manuscript is deferred to a future standalone Groebner/full-resolution/primary-
decomposition theorem.

## 2026-08-18 published - EXP-026 companion v0.02

EXP-025 made the deferred Gröbner problem finite through its truncated-monomial parametrization.
EXP-026 then proved the complete reduced grevlex basis, exact quadratic/cubic/quartic profile,
explicit reduced tails, absence of later elements, and flat Cohen--Macaulay monomial degeneration.
The optimized campaign passes all 297 parameters through `p=300`; an independent clique audit
reconstructs seven small and large cases; 16 fresh-process Presburger obligations close the
cubic/quartic boundary; and the infinite tail closes deductively by `X_0` stabilization.

The focused companion was expanded in place rather than split: the new theorem studies the same
conductor fiber cone as EXP-025, while a future complete interior Betti table may still justify a
separate manuscript. The eight-page v0.02 artifact passed a warning-free two-pass build, complete
150-DPI page inspection, extraction, PDF metadata, exact claim map, source-boundary, and sole-human-
authorship gates. Zenodo reserved and embedded version DOI `10.5281/zenodo.22002907` under concept
DOI `10.5281/zenodo.21997377` before the final rebuild.

Authenticated draft inspection matched title, version, sole creator/ORCID, filename, 453,621-byte
size, and MD5 before publication. The public API confirms the same identity, CC BY 4.0, and a
two-record version chain containing v0.01 and v0.02; the concept DOI resolves to v0.02. A fresh
unauthenticated download matches SHA-256
`12cc380bcc72613694b24cc9f74284f8f3d35e4958ec3569b6ebacce3225e398`. HWB-034 is complete.
HWB-036 owns the remaining checked promotion and durable-handoff gate. No new theorem experiment
is active; HWB-035 remains the strongest distinct research candidate and requires a fresh
source/novelty preflight before declaration.

## 2026-08-18 complete - EXP-026 promotion handoff

PR #190 passed `guards` and `test` and merged the complete EXP-026 theorem, artifacts, focused
companion v0.02, and verified publication record to `develop` at merge commit
`6b9d4670e9e6c0316e135f4e1148bfbb007508ba`. PR #191 passed all required checks and promoted the
same tested state to `main` at `5dfb1af5dcf404425ac88116476f317e6697f48a`.

Remote research work, `develop`, and `main` share payload tree
`1fb094d102e1f91a6c9754cca26d7f57666450fb`. CAOS_MANAGE stayed on `develop`; PR #559 promoted
only the scoped Zenodo workflow and ledger to `main` at
`5bfd7fdbecfddb7da7966bc55bf73c452501f43e`, with management `develop` and `main` tree-identical
at `372cd71d3acca38b92f872cd0995b5b9a264d543`. HWB-036 is complete. No release tag belongs to this
research-only round.
