# Huneke-Wiegand extensions - session handoff

Updated: 2026-08-20. Lifecycle: EXP-030 is ACTIVE with no result claimed. EXP-029 and manuscript
v0.16 are confirmed, published, fresh-download verified, and promoted through the research
repository. The scoped CAOS_MANAGE ledger remains pending under HWB-042 because that checkout is
occupied by unrelated staged diffusion work. The integral
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
    internal-degree-five diagonal over every field (EXP-029).

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
| `D_p` | predicted cubic-colon quotient `P_p/(Q_p:f_p)`, conjecturally a polynomial extension of a canonical idealization | EXP-030 active |
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
| EXP-030 | ACTIVE | test the canonical-idealization colon and the predicted `beta_(3,6)=8p(7p^2-12p+2)/3`; no result yet |

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

## 4. In flight

EXP-030 is declared and unconfirmed. Put

```text
L_p=[0,p] union [3p,4p-2],
A_i=X_i,                     0<=i<=p,
B_j=X_(3p+j),                0<=j<=p-2.
```

After killing the `8p` high variables in the cubic colon, the predicted low quotient is

```text
k[s,t]^(p) semidirect omega_(k[s,t]^(p)),
H(z)=(1+(2p-2)z+z^2)/(1-z)^2.
```

This would force

```text
beta_(2,3)(P_p/(Q_p:f_p))=8p(7p^2-12p+2)/3.
```

The falsifiable EXP-030 prediction is that these shifted colon classes primitively exhaust the
total-degree-six relative `H_2`, so the same formula equals `beta_(3,6)(C_p)` over every field.
The immediate gate is implementation followed by the mandatory `p=4` smoke. Colon agreement alone
does not prove the Betti formula; complete relative profiles, two-characteristic agreement, and an
integral unit-pivot or Smith proof are required.

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
- concept DOI `10.5281/zenodo.21763582`.
- The concept latest resolves to record `22029468`; title, version, sole author/ORCID, licence,
  filename, bytes and both hashes were checked from a fresh public download.

## 5. Next actions

1. Implement EXP-030 Route A and Route B, then run the mandatory `p=4` smoke command recorded in
   `experiments/EXP-030-colon-idealization-degree-six/hypothesis.md`.
2. If smoke passes, run the bounded `p=4,5,6` campaign, independent idealization audit, and
   integral relative-homology gate. Preserve the first mismatch or budget stop without amendment.
3. When CAOS_MANAGE is safely back on clean `develop`, reconcile and promote only the scoped v0.16
   publication ledger; do not touch its current staged diffusion rename work.

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
- Recognition/idealization: EXP-030 asks whether the entire cubic-colon quotient is a polynomial
  extension of the canonical idealization of a rational normal curve. This converts the first
  degree-six colon term into a forced Hilbert coefficient before the relative-chain audit.

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
