# Huneke-Wiegand extensions - research plan

## Objective

Turn the public counterexample into independently checked, structurally understood and
search-ready mathematics. The success target is at least one validated novel result: a sharper
minimality frontier, a family, or a theorem-level mechanism/variant statement.

## Phases

| phase | question | exit gate |
|---|---|---|
| HW-P0 | Are sources, priority and exact scope pinned? | primary dossier, durable record, EXP-001 declaration |
| HW-P1 | Does an independent algebra system reproduce the counterexample? | Singular colon equality plus adversarial control and finite cross-check |
| HW-P2 | Why does the example evade positive rigidity criteria? | exact endomorphism-semigroup verdict and theorem dependency map |
| HW-P3 | How small can such an example be? | candidate calibration; certified lower frontier; reproducible certificates |
| HW-P4 | Is there a family? | falsifiable parametric model with exact instances or a recorded obstruction |
| HW-P5 | What remains true? | surviving-variants matrix with hypotheses and candidate non-applicability |
| HW-P6 | Is there publishable novelty? | manuscript only if P2-P5 produces validated new mathematics |

## Compute discipline

- EXP-001 wall cap: 10 minutes per Singular stage; terminate on no flushed progress.
- SAT scouting is not a proof. Certified frontier runs must emit proof/certificate material and
  pass an independent checker.
- Run candidate calibration and known-positive controls before any frontier search.
- Store source archives outside Git under `E:/_Datos/caos-research/huneke-wiegand/sources/`;
  commit hashes, citations, scripts, hypotheses, artifacts and verdicts.

## Redirections already made

- Do not spend a round writing another Apéry/Dijkstra Python verifier; the public package has one.
- Do not describe expert verification as journal peer review.
- Do not publish a replication-only manuscript as a new counterexample.
- Prefer exact CPU methods; no GPU dependency is justified.

## 2026-08-02 frontier gate

HW-P3's published-frontier prerequisite is closed by EXP-004: exhaustive theorem-tree enumeration
and independently checked DRAT certificates agree for all odd `F<69`. The phase now advances to
EXP-005's selector-CNF scan in strict Frobenius order; no minimality claim is allowed across an
UNKNOWN or uncertified value.

EXP-005 completed that scan without an UNKNOWN: all odd values 69 through 179 have accepted DRAT
proofs and 181 has the independently validated public model. HW-P3 therefore closes with exact
Frobenius minimum 181. HW-P6 is also closed: the validated theorem is published as preprint v0.01,
DOI `10.5281/zenodo.21763583`. HW-P4 remains active after Route G refuted the fixed-offset family;
Route K must search constrained blocks before any new family hypothesis. EXP-007 closes the
separate minimum-layer classification: the public `(Gamma,14)` pair is the unique normalized pair
at `F=181`, supported by projected enumeration and accepted terminal proofs. This strengthens the
published theorem within its original class but does not broaden it to arbitrary modules or rings.

## 2026-08-10 family gate

HW-P4 is closed. EXP-006 Route K certified nonexistence at `s=16,18` inside its scaffold and found
eleven non-seed models at every even `s=20,...,40`. EXP-008 refuted the first fixed-width affine
ray and proved that its layer-9 coverage hole persists for every `q>=9`. EXP-009 repaired exactly
that endpoint mismatch and proves an infinite family for `s=6p`, every integer `p>=4`.

The family theorem is published in manuscript v0.03 at DOI `10.5281/zenodo.21873911`, with the
finite computations clearly separated from the symbolic proof and the public PDF verified
byte-for-byte. The strongest remaining path is repository consolidation, not additional SAT
scouting:

1. promote the complete experiment and publication record through the repository PR path;
2. resume HW-P5 with surviving variants and classification of the new family only after the
   publication state is immutable and verified.

EXP-010 is superseded without a run because its explicit execution gate required EXP-009 to fail.
It remains a frozen possible classification question, not a current experiment result.

## 2026-08-10 post-publication classification gate

HW-P5 is now active through EXP-011. The invariant-first route computes the endomorphism overring
of every EXP-009 family member from adjacent value-set blocks, before considering any nearby-face
SAT classification. The predicted exact formula adds a level-7 block
`[p+1,2p-2] union {2p,4p}` and the old Frobenius singleton. A successful symbolic proof would
upgrade the seed-only EXP-002 escape mechanism to the full infinite family. EXP-010 remains frozen
unless this structural route leaves a specific Kunz-face question that cannot be decided directly.

EXP-011 is CONFIRMED. It proves the predicted overring formula, numerical invariants,
nonsymmetry, and uniform Dey-Lyle escape mechanism for every `p>=4`. This closes the
endomorphism/reflexivity row of the surviving-variants matrix. Manuscript v0.04 passed the
claim/build/render gates and is immutably published at DOI `10.5281/zenodo.21876338`. Any next
classification question must be declared separately rather than automatically returning to
EXP-010.

## 2026-08-12 invariant-first type gate

EXP-012 is declared before computation. Instead of opening a broad Kunz-face classification, it
tests the exact pseudo-Frobenius anatomy of `Lambda_p`. The predicted PF set is the union of the
level-6, level-7, and level-8 gap blocks, with no lower pseudo-Frobenius numbers. If proved, the
endomorphism family has type and reduced type `10p`, maximal reduced type, and is uniformly not
almost Gorenstein. The separate trace-ideal criterion from Lindo-Maitra-Zhang is retained as a
future reformulation route after the invariant is settled.

EXP-012 is CONFIRMED. The complete pseudo-Frobenius set is exactly the three final gap blocks,
giving type and reduced type `10p`. Hence the endomorphism family has maximal reduced type, while
`2g-(F+type)=12p-1` proves it is uniformly not almost symmetric. The next invariant-first gate is
the trace/endomorphism equality from Lindo-Maitra-Zhang Corollary 5.6, not an automatic manuscript
version or nearby-face SAT sweep.

## 2026-08-12 exact trace gate

The source-complete preflight shows that trace equality itself cannot separate this family:
`R_p` is one-dimensional Gorenstein, so the reflexive-trace criterion already forces it. EXP-013
is therefore declared around the stronger unsolved datum: an exact common formula for
`tr_R(J_p)=R_p:E_p=tr_R(E_p)`. The prediction differs from `Gamma_p` only at zero and a reflected
level-five block of size `p`, so its colength should be `p+1`. Symbolic block proof remains
load-bearing; two exact reconstructions and corrupted controls test the implementation.

The first `p=4` smoke check corrected one overbroad tail shorthand before campaign execution:
`13s-1` is not in `Gamma_p`, so the common ideal contains `[9s,13s-2]` and the tail from `13s`, not
all integers from `9s`. This initial prediction is preserved as refuted; the equality and colength
claims are unaffected.

EXP-013 is CONFIRMED under that correction. It proves the common trace is exactly `R_p:E_p` and
that `length(R_p/(R_p:E_p))=length(E_p/R_p)=p+1`. The symbolic block proof is supported by 297
two-route exact checks, an independent six-parameter reconstruction, stable hashes, and three
rejected corruptions. EXP-012 and EXP-013 together pass the deliberation gate for a v0.05
candidate; publication remains conditional on the full manuscript and public-artifact workflow.

That workflow is complete. The 15-page v0.05 passed claim audit, clean two-pass build, complete
rendered inspection, sole-authorship and metadata gates, and is immutably published at DOI
`10.5281/zenodo.21907297`. A fresh public download matches the committed 515,650-byte PDF at
SHA-256 `4bd2cfd7351cb6cec1b3fa006c7eb3018732c283b5bb5a1e5c86015435275276`.

## 2026-08-12 duality, stability, and reduction gate

A primary-source audit found that EXP-013's equality of colengths is general one-dimensional
Gorenstein local duality, not a family-specific mechanism. Manuscript v0.06 corrects that novelty
boundary and publishes the genuinely new exact common ideal, its value `p+1`, conductor
nonstability, and the EXP-016 defect `length(T_p^2/t^(4s)T_p)=14p`. The immutable record is DOI
`10.5281/zenodo.21907943`; a fresh public download matches SHA-256
`10cc2bd31026cfe6a921c4cf54832a7df018b0f0b0f38ee196bc597954255dd4`.

EXP-017 then follows the conductor's full reduction sequence rather than returning to broad SAT
scouting. It is CONFIRMED: `Q_p=t^(4s)R_p` is a minimal reduction with exact reduction number four,
the successive Sally-quotient lengths are `23p-1,14p,2p,1,0`, and the Hilbert coefficients are
`e0=24p`, `e1=39p`. Symbolic block proofs are load-bearing; two exact 297-parameter routes and an
independent audit support them. The 18-page v0.07 passed claim/build/render, metadata, sole-author,
publication, and fresh-download gates and is immutable at DOI `10.5281/zenodo.21908188`; its public
SHA-256 is `2dca97dc100424afbeffd525fe66aa4aa43ce65c82c11b9ac43250cd33771e19`.

## 2026-08-12 tangent-cone depth gate

EXP-018 asks the structural question left undecided by the reduction number: whether the conductor
tangent cone is Cohen--Macaulay. The original Valabrega--Valla criterion reduces this to exact
intersections with `Q_p=t^(4s)R_p`. The experiment is CONFIRMED. The only nonzero intersection
quotient is `(Q_p intersect T_p^2)/(Q_pT_p)`, whose exact level-nine residue block has length `p`;
all components at `n=0` and `n>=2` vanish. Consequently `gr_(T_p)(R_p)` has depth zero for every
`p>=4`. Its Hilbert numerator

```text
(p+1)+(9p-1)z+12p z^2+(2p-1)z^3+z^4
```

has only positive coefficients, so Hilbert positivity does not see the obstruction. The next
publication gate is a v0.08 candidate with claim/build/render review. The next research gate after
that is not a larger parameter sweep: it is the full graded torsion/Buchsbaum anatomy, declared as
a separate experiment only after source and finite-target preflight.

The publication gate is complete. The 20-page v0.08 passed claim audit, stable two-pass build,
complete rendered inspection, metadata, sole-authorship, publication, and fresh-download checks.
It is immutable at DOI `10.5281/zenodo.21908490`; the public SHA-256 is
`c8a038adf042a71126e0b0dac170803340e12300521aad1ca05f88bbc3c32f69`. The next active gate is
therefore the separately declared torsion/Buchsbaum anatomy, not further manuscript work or a
larger EXP-018 sweep.

## 2026-08-12 Buchsbaum gate

EXP-019 is CONFIRMED. The complete zeroth local cohomology of the conductor tangent cone is `k^p`,
concentrated in degree zero, and both the degree-zero maximal part `m_p/T_p` and the positive graded
part annihilate it. Consequently every tangent cone in the family is Buchsbaum but not
Cohen--Macaulay, with unbounded Buchsbaum invariant `p`. Quotienting by `H^0` gives a
Cohen--Macaulay ring with Hilbert numerator

```text
1+(10p-1)z+12p z^2+(2p-1)z^3+z^4.
```

The two-route 297-parameter campaign and independent audit pass, but the stable-tail colon proof is
load-bearing. This is a material theorem beyond v0.08, so the active delivery gate is manuscript
v0.09 with full claim/build/render, sole-authorship, Zenodo, and fresh-download verification.

The publication gate is complete. The 21-page v0.09 passed the claim audit, stable two-pass build,
complete rendered inspection, sole-authorship, metadata, publication, and fresh-download checks.
It is immutable at DOI `10.5281/zenodo.21908785`; its public SHA-256 is
`ecf4d1ebe504ad3af74d123c949a953a7f397dabd72ec11c94a631962e1501db`.

## 2026-08-12 Noether-normalization module gate

A fresh source sweep redirects the next round from a generic inequality for the Buchsbaum
invariant to the complete module over the minimal-reduction polynomial ring. EXP-020 is declared
before implementation. With `F_p=k[x_p]` and `x_p=(t^(4s))^*`, the EXP-017--019 data predict

```text
G_p isomorphic to (F_p/(x_p))^p direct-sum F_p direct-sum F_p(-1)^(10p-1)
    direct-sum F_p(-2)^(12p) direct-sum F_p(-3)^(2p-1) direct-sum F_p(-4).
```

The invariant-first proof uses the graded structure theorem over `k[x_p]`; an exact
conductor-power Apery-column decomposition is the independent route. A nearby Kunz-face sweep and
Rees-algebra local cohomology remain deferred until this finite structural target is adjudicated.

EXP-020 is CONFIRMED. The entire conductor tangent cone decomposes into a rank-`24p` free module
plus `p` copies of `F_p/(x_p)` in degree zero. It follows that the projective dimension over the
Noether normalization is one, the regularity is four, the top-local-cohomology `a`-invariant is
three, and `length(G_p/x_pG_p)=25p=e0(T_p)+I(G_p)`. The exact Apery-column campaign passed all 297
parameters and the independent audit rebuilt six parameters and rehashed every row. This material
theorem triggers manuscript v0.10; no publication is claimed before its full immutable workflow.

The publication gate is complete. The 22-page v0.10 passed claim audit, stable two-pass build,
complete rendered inspection, sole-authorship and metadata checks, publication, and fresh-download
verification. It is immutable at DOI `10.5281/zenodo.21909127`; the public PDF is 578,949 bytes
with SHA-256 `00a78fd8101f106724877b3fdbc933c51024a872a2b9a4f05692358b4d1a9d03`.
The remaining gate is repository PR promotion, not further EXP-020 computation.

## 2026-08-12 conductor fiber-cone gate

The next round is redirected from a broad neighboring-family sweep to the special fiber
`C_p=F(T_p)`. EXP-021 is declared before implementation. Its load-bearing prediction is
`T_p^2=m_pT_p`; this would identify the natural tangent-cone map's kernel with the already proved
`H^0(G_p)` and yield a graded-algebra isomorphism

```text
G_p/H^0(G_p) isomorphic to C_p.
```

The same exact value data predict Cohen--Macaulay type `10p+1` and a nonlevel Artinian reduction
with socle in degrees two and four. The mandatory order is hypothesis, smoke gate, exact campaign,
independent audit, symbolic proof, and only then manuscript/publication deliberation. A defining
ideal is a separate later gate and is not assumed here.

EXP-021 is CONFIRMED. The first complete attempt correctly stopped as inconclusive at the campaign
budget; an exact bitset optimization then completed all 297 parameters inside the unchanged
budget, and the independent audit passed. The symbolic proof establishes
`T_p^2=m_pT_p` and the natural algebra isomorphism `G_p/H^0 isomorphic to F(T_p)` for every
`p>=4`. The Artinian reduction has socle dimensions `10p` in degree two and one in degree four,
so the type is `10p+1` and the fiber cone is nonlevel. The active delivery gate is manuscript
v0.11; HWB-023 remains separate and must not delay accurate publication of this theorem.

The v0.11 delivery gate is complete. The 25-page preprint passed claim audit, stable two-pass
build, complete rendered inspection, sole-authorship and metadata checks, publication, and fresh
public-download verification. It is immutable at DOI `10.5281/zenodo.21909961`; the public
589,535-byte PDF has SHA-256
`0b3a9131e3c419c0a89cb064ea6beb7c696006171fe18bec578e7ba963a520ce`. Repository PR promotion
remains required before HWB-023 can be considered for a separate declaration.

Repository promotion is complete. PR #172 passed `guards` and `test` and merged the complete
EXP-021/v0.11 round to `develop` at `178a7361043198e8785a739fde77074b126370dd`; PR #173 passed
all required checks and promoted it to `main` at
`7abd10403a5798af4757223bfa0cfa2135aed048`. The remote branch trees are identical at
`21791e6a6c182fa12f00a5f255a6faab23dd7058`. The remaining action is the documentation handoff;
no release tag is claimed.

## 2026-08-17 defining-ideal gate

HWB-023 is active as EXP-022 after a fresh source and novelty preflight. Abdolmaleki--Kumashiro,
International Journal of Algebra and Computation 34(7) (2024), Theorem 2.8, guarantees a defining
set through degree five because EXP-021 proves the fiber cone Cohen--Macaulay and EXP-017 gives
reduction number four. It does not determine this family's minimal equations.

EXP-022 tests the sharper value-congruence conjecture that the full defining ideal is generated in
degree two. The exact predicted number is `50p^2-17p`. The mandatory order is `p=4` degreewise
smoke, first-obstruction preservation or bounded campaign, independent audit, symbolic
connectivity proof, and only then wiki/manuscript deliberation. No defining-ideal theorem or
publication is claimed at declaration.

EXP-022 is REFUTED. The `p=4` gate found one necessary cubic and no degree-four/five equations;
complete `p=5,6` diagnostics reproduced the profile. Symbolically,
`X_0^2X_(3p)-X_p^3` is a nonzero defining relation whose two monomials are isolated under every
quadratic move, proving nonquadraticity for all `p>=4`. The exact universal quadratic count remains
`50p^2-17p`. The corrected one-cubic upper bound is not inherited automatically and requires a
separately declared experiment and uniform connectivity proof.

EXP-023 is declared for that corrected upper bound. It replaces full monomial enumeration with an
independent degreewise state graph on `(generator offset, preceding fiber offset)` and targets the
complete presentation `J_p=((J_p)_2,X_0^2X_(3p)-X_p^3)`. Confirmation requires campaign and audit
agreement, uniform interval-graph connectivity in degrees three through five, and the published
degree-five completeness theorem. Relation type three and non-Koszulness remain predictions.

EXP-023 is now CONFIRMED. The state graph identifies minimal equations with component defects.
An exact Presburger cover proves that degree three has exactly one exceptional two-component total,
`3p`, while degrees four and five have no defect. The unique joining equation is
`X_0^2X_(3p)-X_p^3`. The campaign passes `p=4,...,23`, the independent total-graph audit rebuilds
`p=4,13,23` and rehashes every row, and the first over-budget attempt remains preserved as
`INCONCLUSIVE_BUDGET`. Abdolmaleki--Kumashiro's degree-five bound then closes the higher tail.

The defining ideal therefore has first Betti row

```text
(beta_(1,2),beta_(1,3),beta_(1,4),beta_(1,5),...)
=(50p^2-17p,1,0,0,...),
```

relation type three, and `50p^2-17p+1` minimal equations. The necessary cubic proves the
Cohen--Macaulay special fiber is not Koszul. This material theorem opens HWB-025: manuscript v0.12,
claim/build/render QA, Zenodo new-version publication, and checked PR promotion. The symbolic
trust boundary must remain explicit because the Z3 UNSAT leaves do not have a separately checked
proof object.

The v0.12 publication gate is complete. The 27-page preprint passed the claim audit, warning-free
stable build, complete rendered inspection, sole-human-authorship and metadata checks before
upload. Zenodo record `21988601`, DOI `10.5281/zenodo.21988601`, resolves as concept latest; a
fresh unauthenticated download matches the committed 615,252-byte PDF at SHA-256
`98d730fb8afaf40149d028bdde0b1c3ba9851f1dbcd15475567e56bb7eb17d3f`. HWB-026 is now the only
delivery gate: checked PR promotion to `develop` and `main`, followed by merge/tree reconciliation.
No release tag is part of this round.

Repository promotion is complete. PR #176 passed `guards` and `test` and merged the full
EXP-022/023 plus v0.12 record to `develop` at `aecb5b5c6daa83efd30f7c11a38436896fe59d12`.
PR #177 passed all required checks and promoted that tested state to `main` at
`80de49e5e42ca52d143333f029eaaac637464194`. Remote `develop` and `main` are tree-identical at
`5469624bab95a087aaef37630ea9c2a27c656054`. Documentation-only PR #178 then passed `guards` and
`test`, and PR #179 passed all required checks and completed the durable handoff. No delivery gate
or experiment remains active; any next theorem requires a new source and novelty preflight.

## 2026-08-18 extremal Betti gate

The fresh source and novelty preflight ranks exact presentation-ring edge homology above a full
resolution or Groebner-basis attack. EXP-024 is declared before implementation. With
`N=10p`, `c=N-1`, and h-polynomial

```text
1+(10p-1)z+12pz^2+(2p-1)z^3+z^4,
```

it predicts projective dimension `c`, regularity four, the complete last Betti row from the
Artinian socle, `beta_(2,3)=2p(500p^2-330p+31)/3`, and
`beta_(c-1,c+3)=8p`. The immediate gate is the `p=4` two-route smoke after implementation,
followed by the bounded campaign, independent audit, and symbolic proof. No EXP-024 theorem,
manuscript v0.13, or Zenodo version is yet claimed.

EXP-024 is CONFIRMED. Auslander--Buchsbaum and the degree-four h-polynomial give projective
dimension `10p-1` and regularity four. Two independent degree-three derivations give

```text
beta_(2,3)=2p(500p^2-330p+31)/3.
```

Regular linear reduction and the exact Artinian socle give the complete last row; the
`z^(c+3)` coefficient isolates `beta_(c-1,c+3)=8p`, and graded duality gives `10p` canonical
generators in degree `-1` plus one in degree `-3`. The exact campaign and all-row independent
audit pass for `p=4,...,300`, with aggregates `baf6200a...637eb` and `b6035f61...f17e2`.

The same-manuscript decision is closed: v0.13 is a coherent extension of the special-fiber
presentation, while a split remains deferred to a standalone Groebner/full-resolution theorem.
The 29-page v0.13 candidate passed claim, warning-free build, complete render, identity, and
sole-authorship gates before upload. It is now immutably published CC BY 4.0 at DOI
`10.5281/zenodo.21995498`; concept latest is record `21995498`. A fresh unauthenticated download
matches the committed 635,617-byte PDF at MD5 `d6ce72589100d1f57986da000501fdc7` and SHA-256
`cc9e721c3f0155181b963095a0b0efcc37e023546b32c6dd61b772a3d30ec7ed`. The active gate is checked
repository promotion to `develop` and `main`, followed by exact merge/tree reconciliation.

Repository promotion is complete. PR #182 passed `guards` and `test` and merged the full
EXP-024/v0.13 publication state to `develop` at
`26c5210302ede4681111a4503776190954c33f59`. PR #183 passed all required checks and promoted the
identical tested state to `main` at `f24b078b98376224b38753f7294d26627147c4ea`. The remote work,
`develop`, and `main` refs share tree `5c828789a5d993a35a1e42743860600d156c9f99`. No release tag is
claimed. A new theorem round requires a fresh source and novelty preflight.

The documentation-only handoff was subsequently promoted by PRs #184/#185. Before the next
round opened, remote work, `develop`, and `main` shared final tree
`b70a3990583057a92e591c34d5f9e9c101185e8c`; the earlier `5c828...` tree is the theorem and
publication payload, not the final documentation handoff.

## 2026-08-18 curvilinear primary-structure gate

A new source and novelty preflight redirects the next round from an unbounded explicit Groebner
basis search to the nonreduced projective geometry already latent in EXP-021/023. Existing
literature supplies the nonradical fiber-cone and curvilinear-scheme context but no identified
formula for this conductor family. EXP-025 is declared before implementation.

With `q=24p` and degree-one offset set `G_p`, the target parametrization is

```text
C_p isomorphic to k[x y^a : a in G_p] inside k[x,y]/(y^q).
```

Because `0,1 in G_p`, this predicts

```text
C_p/(X_0-1) isomorphic to k[y]/(y^q),
radical(J_p)=(X_a:a>0),
J_p is (X_a:a>0)-primary,
nilindex(nil(C_p))=q.
```

The geometric form is a saturated length-`q` curvilinear fat point with tangent dimension one.
It is locally Gorenstein although its homogeneous coordinate ring has type `10p+1` and is not
level. Its affine differential module is predicted to be
`Omega^1=(k[y]/(y^q,qy^(q-1)))dy`, explicitly separating the characteristics dividing `q` from
all others. The immediate gate is a post-implementation `p=4` smoke, then the exact `p=4,...,300`
campaign, independent audit, and symbolic proof. If the complete package is confirmed, it meets
the prior split criterion and opens a focused companion manuscript rather than v0.14 of the
already broad Frobenius-minimality manuscript.

EXP-025 is CONFIRMED. The exact campaign passes every `p=4,...,300` with aggregate
`f3373f4f58287fd3f553b95efa226e7938170d32f24eea6a014ca47f9d6b39b6`; the disjoint-layer audit
rehashes and independently reconstructs all 297 rows with aggregate
`84c00be8ff64002e8738a5d4307d71df73dfa7595e810c7e764f6f5b6c8f143e`. The symbolic proof gives
the truncated model, exact primary component, sharp exponent, saturation, curvilinear fat point,
local/arithmetic Gorenstein separation, and characteristic-sensitive differential module for all
`p>=4`.

The split decision is therefore closed in favor of a focused companion preprint and separate
Zenodo concept record. The next gate is manuscript claim/build/render and sole-authorship QA; no
manuscript DOI or publication is yet claimed.

The focused companion v0.01 is now a validated six-page candidate. Its claim map, warning-free
two-pass build, complete final 150-DPI render inspection, PDF metadata, source boundary, and
sole-human-authorship gates pass. The frozen no-DOI candidate is 424,453 bytes at SHA-256
`cb78f46f2e3e2250594523a0dffe16806eefc499c44fa1b6b8a67ab3d074f07d`. The active reversible gate
is creation of a separate Zenodo concept draft, followed by DOI insertion and a complete repeat of
the validation before any upload or publication.

Separate Zenodo draft `21997378` is now reserved with version DOI
`10.5281/zenodo.21997378` and concept DOI `10.5281/zenodo.21997377`. After inserting both
identifiers, the 424,886-byte PDF repeated the warning-free two-pass build, complete six-page
150-DPI inspection, metadata, identity, and sole-authorship gates. Its SHA-256 is
`e9d51bb63492c37eae4ddb7a6790e50c1a3292006bd23660a0bbe2c69c19be4a`. The active gate is now
attachment of exactly this candidate, followed by publication and fresh public-record
verification.

The attachment, publication, and independent public checks are complete. Version DOI
`10.5281/zenodo.21997378` and concept DOI `10.5281/zenodo.21997377` resolve to record `21997378`.
The public title, version, sole creator/ORCID, licence, filename, byte count, and MD5 agree, and a
fresh unauthenticated download exactly matches the committed SHA-256
`e9d51bb63492c37eae4ddb7a6790e50c1a3292006bd23660a0bbe2c69c19be4a`. The remaining gate is the
checked work-to-`develop` and `develop`-to-`main` promotion plus durable handoff reconciliation.

Repository promotion is complete. PR #186 passed `guards` and `test` and merged the EXP-025
theorem, companion preprint, and verified publication record to `develop` at
`1c94632f5bb631fd4d85916488dc7a943a899109`. PR #187 passed all required checks and promoted the
same tested state to `main` at `18e7d9728c3a8c210ea6a36d81bba6b6325cc536`. The research work,
`develop`, and `main` refs share payload tree `53e5e61ffeeb5816497e3e477921bc94c4a5f91d`. CAOS_MANAGE
PR #557 merged the publication ledger to `main` at `ec11d010246341347fd4d11b49b29998ec9a6cf1`;
its `develop` and `main` refs share tree `f7db0c50a75491738dbfad998d235458f4bb69ee`. HWB-033 is
closed. No release tag is part of this research-only round.
