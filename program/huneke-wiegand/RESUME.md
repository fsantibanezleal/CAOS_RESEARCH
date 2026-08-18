# Huneke-Wiegand extensions - session handoff

Updated: 2026-08-18. Lifecycle: active publication round. EXP-023 is CONFIRMED: for every `p>=4`,
the conductor special-fiber defining ideal consists of its `50p^2-17p` minimal quadrics and the
single cubic `X_0^2X_(3p)-X_p^3`. The relation type is three and the Cohen--Macaulay fiber cone is
not Koszul. The exact `p=4,...,23` campaign, independent total-graph audit, and all-parameter
Presburger connectivity proof pass. Manuscript v0.12 and its Zenodo new version are the current
in-flight delivery; neither publication nor PR promotion is claimed yet. The last published state
is manuscript v0.11 at DOI `10.5281/zenodo.21909961`, promoted through PRs #172 and #173. Release
v0.63.000 remains the repository release baseline; this research round does not claim a new tag.

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

## 4. In flight

EXP-023 is CONFIRMED. Its exact state-graph quotient proves

```text
J_p=((J_p)_2,X_0^2X_(3p)-X_p^3),
(beta_(1,2),beta_(1,3),beta_(1,4),beta_(1,5),...)=(50p^2-17p,1,0,0,...).
```

The all-parameter Presburger cover closes degree-three through degree-five connectivity, and the
published Cohen--Macaulay fiber-cone construction closes every degree above five. The bounded
campaign and independent audit agree, while the first over-budget attempt remains preserved as
`INCONCLUSIVE_BUDGET`. The residual trust boundary is explicit: the Z3 UNSAT leaves do not carry
a separately checked proof object. The active work is manuscript v0.12 claim/build/render QA,
Zenodo new-version publication with public-file verification, then PR promotion.

Previously closed state:

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
- concept DOI `10.5281/zenodo.21763582`.
- The concept latest resolves to record `21909127`; title, version, sole author/ORCID, licence,
  filename, bytes and both hashes were checked from a fresh public download.

## 5. Next actions

1. Expand the manuscript to v0.12 directly from EXP-022/023, with the refuted quadratic conjecture,
   exact one-cubic theorem, validation boundary, and new source citation.
2. Complete claim audit, stable two-pass build, full rendered-page inspection, sole-human-authorship
   audit, and metadata agreement; publish a Zenodo new version and verify a fresh public download.
3. Commit and push each validated milestone, then promote the tested tree through PRs to `develop`
   and `main`. Do not claim a global release tag.
4. Only after delivery, select a new theorem target through a fresh source and novelty preflight.

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

HWB-023 is done. HWB-025 is the active gate: expand manuscript v0.12, complete claim/build/render
QA, publish and fresh-download verify the Zenodo new version, then perform checked PR promotion.
