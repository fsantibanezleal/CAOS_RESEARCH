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

## 2026-08-18 in flight - EXP-026 explicit grevlex staircase

EXP-025 makes the deferred Groebner problem finite: for grevlex ordered by decreasing offset with
`X_0` last, every surviving `(degree,total offset)` has one canonical smallest factorization.
EXP-026 is declared before implementation to prove that the minimal initial boundary has profile

```text
degree 2: 50p^2-17p,
degree 3: 5p-1,
degree 4: p-2,
degree >=5: 0.
```

The pre-declaration probe matches six explicit cubic families and one quartic family for every
`p=4,...,15`, and finds no leading generator divisible by `X_0`. The immediate action is a
reproducible `p=4` smoke, followed by the exact campaign, independent factorization audit, and a
Hilbert-function proof that the proposed boundary is the entire initial ideal. If confirmed, the
result expands the focused curvilinear companion to v0.02; a manuscript split is deferred to a
future complete interior Betti table or a genuinely broader method.

EXP-026 is CONFIRMED. The reduced basis has exact degree profile
`(50p^2-17p,5p-1,p-2)`, total size `50p^2-11p-3`, six cubic families, one quartic family, and no
later boundary. The optimized exact campaign passes all 297 parameters in 8.474 seconds; the
independent clique audit reconstructs selected small and large cases through `p=300`; and 16
fresh-process Presburger obligations prove all-parameter cubic/quartic completeness, soundness,
and reduced tails. The infinite degree tail closes deductively from
`N_(n,s)=X_0^(n-4)N_(4,s)` for `n>=4`.

The manuscript trigger is crossed. HWB-029 is closed for the Groebner problem, HWB-035 now owns
the distinct interior-Betti question, and HWB-034 is active for v0.02 of the focused curvilinear
companion plus a Zenodo new version.

The focused companion v0.02 passed claim/build/render, extraction, metadata, identity, and
sole-authorship QA and was published as Zenodo record `22002907`, version DOI
`10.5281/zenodo.22002907`. The concept DOI resolves to the new version, and the fresh public PDF
matches the committed 453,621-byte artifact at SHA-256
`12cc380bcc72613694b24cc9f74284f8f3d35e4958ec3569b6ebacce3225e398`. HWB-034 is done. At that
publication checkpoint, PR-based promotion and final tree/handoff reconciliation remained under
HWB-036. A new interior-Betti experiment was not declared in this publication round.

Promotion is complete. PR #190 merged the checked round to `develop` at `6b9d4670`; PR #191
promoted it to `main` at `5dfb1af5`. Research work, `develop`, and `main` share payload tree
`1fb094d102e1f91a6c9754cca26d7f57666450fb`. CAOS_MANAGE PR #559 promoted the matching Zenodo
ledger, and management `develop`/`main` share tree
`372cd71d3acca38b92f872cd0995b5b9a264d543`. HWB-036 is done. No experiment is active; HWB-035
requires a fresh source and novelty preflight before any new declaration.

## 2026-08-19 - EXP-027 first interior Betti strand

A fresh source and novelty preflight ranked relative offset-Koszul complexes above raw full
resolutions, consecutive-cancellation bounds, and an immediate Apéry/Kunz-face attack. The
truncated-monomial model identifies every offset strand with a relative squarefree-divisor chain
complex. EXP-027 was committed before implementation with the predictions

```text
beta_(2,4)=8p,
beta_(3,4)=p(5p-1)(500p^2-440p+47)/2.
```

EXP-027 is CONFIRMED. An integral lexicographic matching bounds the degree-four relative first
homology by one on `{3p+a:a in G_p,a>=6p}` and zero elsewhere. Independently,

```text
(Q_p:f_p)_1=span{X_a:a in G_p,a>=6p}
```

gives one primitive minimal mapping-cone class at every one of those `8p` offsets. The coefficient
of `z^4` in the frozen Hilbert numerator then determines the adjacent `beta_(3,4)`. This proves the
formulas over every field and excludes integral torsion.

The exact campaign passes all 297 parameters; explicit relative-chain profiles pass every offset
for `p=4,5,6`; the `p=4` profile agrees over `GF(2)` and `GF(1000003)`; six all-parameter symbolic
counterexample queries are UNSAT; and the independent audit reconstructs the `p=4` complex plus
six formula samples. The method is a relevant new result but does not close the full interior
table.

HWB-037 now owns a v0.14 expansion of the main conductor-fiber manuscript and Zenodo new-version
workflow. A separate manuscript is deferred until the method yields a substantial additional
strand or a theorem beyond this family. HWB-038 owns later PR promotion and durable reconciliation;
neither publication nor promotion is yet claimed.

The v0.14 manuscript then passed its complete claim audit, warning-free 31-page build, complete
rendered inspection, metadata, identity, and sole-authorship gates. Zenodo record `22013515`, DOI
`10.5281/zenodo.22013515`, is public under the existing concept DOI. The fresh unauthenticated
656,437-byte PDF matches SHA-256
`df5e12d2256f4967881df0f35df44b415777c4826f38447a33cfdeb1b7399e10` exactly. HWB-037 is done;
HWB-038 is active for checked work-to-`develop` and `develop`-to-`main` promotion plus management
ledger reconciliation.

Promotion is complete. PR #194 passed `guards` and `test` and merged the full EXP-027 theorem,
artifacts, v0.14 manuscript, and verified Zenodo record to `develop` at `68ebac5b`. PR #195 passed
its own required checks and promoted the result to `main` at `6319887e`; all research delivery
branches share payload tree `84910601b3a5b406c3725f64a0903d8116ad922f`. CAOS_MANAGE PR #562
promoted the exact Zenodo controls and publication ledger at `8c3fcca1`; management `develop` and
`main` share tree `f46e52f048dcdcadfae5d7bbd68cecdaadac78c5`. HWB-038 is done. No release
tag is claimed for this research-only round.

## 2026-08-19 - EXP-028 complete second Betti row

The EXP-027 relative-complex method was extended before opening a broader search. EXP-028 declared
the two remaining possible entries in homological degree two, the full degree-five multigraded
profile, integral torsion-freeness, and degree-six vanishing before canonical artifact generation.
Raw full resolutions, Hilbert-numerator cancellation alone, and higher-row enumeration were ranked
below the invariant-first degree-five/six chain calculation.

EXP-028 is CONFIRMED. For every `p>=4` and every field,

```text
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(2,4)=8p,
beta_(2,5)=p(2p-3),
beta_(2,6)=0,
beta_(2,j)=0 otherwise.
```

For `0<=r<=2p-4`, degree-five support is
`[3p+2,5p-2] union [6p+1,8p-3] union [9p,11p-4]`. The outer blocks have multiplicity
`min(floor(r/2)+1,floor((2p-4-r)/2)+1)` and the middle block has multiplicity
`min(r+1,2p-3-r,p-2)`. Integral lexicographic matching gives only unit pivots and zero Smith
factors with precisely those ranks; degree six has no critical edge. This proves characteristic
independence rather than inferring it from finite fields.

The optimized canonical campaign passes 297 formula rows through `p=300`, complete profiles at
`p=4,5,6`, degree-six all-offset checks, and two unrelated fields at `p=4`. An independent SymPy
route rebuilds rational ranks and Smith factors, while a separate arithmetic/Z3 certificate checks
the count and endpoint identities. The first canonical attempt exceeded the declared budget after
280 rows because a redundant cubic-cost witness enumeration ran in every formula row; it remains
non-evidence, and the corrected campaign limits explicit witnesses to six parameters.

HWB-039 expanded the existing manuscript because the theorem completes one homological row but
does not yet justify a separate narrative. The warning-free 34-page v0.15 passed complete rendered
inspection and sole-human-authorship gates, then was published at DOI
`10.5281/zenodo.22016550`. A fresh unauthenticated 674,169-byte download matches SHA-256
`e7d3fb747f01b6c44c84ca9c2cf25a746cd2d05eb0996163f4a18e9e3cea1be9`; record `22016550` is
concept-latest. HWB-039 is done. HWB-040 owns checked repository and management-ledger promotion;
higher homological rows remain the strongest next research direction after that delivery closes.

Promotion is complete. PR #198 passed `guards` and `test` and merged the complete EXP-028 theorem,
artifacts, v0.15 manuscript, and verified Zenodo record to `develop` at `b83b9aa0`. PR #199 passed
both required jobs and promoted the identical payload to `main` at `5ce1efa3`; all research
delivery branches share tree `e35f420f59a5343ea09da15985786ab0b65897d6`. CAOS_MANAGE remained
on `develop`; PR #566 promoted only the scoped v0.15 controls and ledger to `main` at `ddafe393`,
with management branches sharing tree `f234e662fa13834787c994b789d6607b486c19ec`. HWB-040 is done.
No release tag is claimed for this research-only round.

## 2026-08-20 - EXP-029 colon-Koszul degree-five diagonal

A fresh source, novelty, and path preflight redirects HWB-035 from an immediate whole-third-row
enumeration to a sharper mapping-cone invariant. EXP-027 already proves

```text
(Q_p:f_p)_1=span{X_a:a in G_p,a>=6p},
```

and this space has dimension `8p`. Read-only exact probes at `p=4,5` show that every observed
`beta_(3,(5,b))` is indexed by an unordered pair of those high variables, shifted by the cubic
offset `3p`. EXP-029 is declared before implementation with the predictions

```text
beta_(3,5)=binom(8p,2)=4p(8p-1),
support=[15p+1,39p-3] minus {33p-1}.
```

The selected proof route combines primitive mapping-cone lower-bound classes with an integral
relative `H_2` matching that must cancel every transient critical triangle by unit tetrahedron
boundaries. If this succeeds, the frozen Hilbert numerator and EXP-028 give

```text
beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3,
```

completing the internal-degree-five diagonal. The explicit grevlex initial ideal was checked and
is neither stable nor strongly stable in either natural order, so degeneration remains a bound,
not the selected formula engine. No EXP-029 result, manuscript version, or publication is claimed
before the declared integral, computational, audit, and symbolic gates pass.

All declared EXP-029 gates now pass. The integral relative normal form leaves precisely the free
basis indexed by unordered pairs `{a,c}` of the `8p` high-colon variables, in offset `3p+a+c`.
Hence

```text
beta_(3,5)=4p(8p-1),
support=[15p+1,39p-3] minus {33p-1}.
```

Together with EXP-028 and the exact Hilbert numerator, this gives

```text
beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3
```

and completes internal degree five over every field. The canonical campaign aggregate is
`7564f15534e8a29f875a367d3a324b95041e8eef836d15deac3e35130e1ad37d`; the independent audit
aggregate is `337854eef5d773c84cdd79c7734e63b295fa0337c5a1852e652559c334949b04`; and the optimized
symbolic aggregate is `605733497d6fb0ead97bfd25e26daaa66d546c297751960e1c427f29ff69f279`.
The first symbolic implementation exceeded its declared budget by materializing all support
integers and is preserved as non-evidence; the constant-memory endpoint implementation passed the
same obligations through `p=10000`. EXP-029 is CONFIRMED and HWB-041 now owns the v0.16 manuscript
and Zenodo new-version gate. The next mathematical target remains `beta_(3,6)`, not an unbounded
full-resolution sweep.

HWB-041 is complete. The existing manuscript was expanded to v0.16 with the exact multigraded
pair profile, integral normal form, complete degree-five diagonal, evidence ledger, and explicit
third-row/full-table boundary. The DOI-bearing 36-page PDF passed two clean LaTeX builds and
complete rendered inspection, then was published under the existing concept DOI as record
`22029468`, DOI `10.5281/zenodo.22029468`. A fresh unauthenticated 691,569-byte download matches
MD5 `ad69991f41c4f35da3c03f2c1ce343e9` and SHA-256
`4c2a49ae6e1a959afb8df4a365feb4c815d408f3746b5ef1df14ee5746abd554`. HWB-042 now owns the
checked repository and management-ledger promotion; no release tag is claimed for this
research-only round.

Research promotion is complete. PR #203 passed `guards` and `test` and merged the complete
EXP-029 theorem, artifacts, manuscript v0.16, and verified publication record to `develop` at
`0c9638d537bf29d1500007efeee0ba68e83bf020`. PR #204 passed all required checks and promoted the
complete tested `develop` state to `main` at `633e547762460d6751e563565b577ff53da24425`.
Research work, `develop`, and `main` share payload tree
`f956e8109c986a841394f19ded669feb62164fa1`. The CAOS_MANAGE v0.16 mirror is deliberately deferred:
that checkout is on `task/difusion-rename-all-explorations-20260820` with extensive staged
diffusion renames, so touching or switching it would violate the parallel-session boundary.
HWB-042 remains open only for that scoped management reconciliation. No release tag belongs to
this research-only round.

## 2026-08-20 - EXP-030 cubic-colon idealization

The next HWB-035 target is redirected from a broad degree-six chain enumeration to recognition of
the cubic colon. Write the `2p` low variables as `A_i=X_i` for `0<=i<=p` and
`B_j=X_(3p+j)` for `0<=j<=p-2`. EXP-030 predicts that, after the known `8p` high colon variables
are killed, the residual quotient is

```text
k[s,t]^(p) semidirect omega_(k[s,t]^(p)),
```

the square-zero canonical idealization of the rational normal curve ring. Its predicted Hilbert
series is `(1+(2p-2)z+z^2)/(1-z)^2`. The forced low-variable coefficient and its Koszul extension
are

```text
beta_(2,3)^low=8p(p-1)(p-2)/3,
beta_(2,3)(P_p/(Q_p:f_p))=8p(7p^2-12p+2)/3.
```

The experiment makes the falsifiable stronger prediction that these shifted classes primitively
exhaust total-degree-six relative `H_2`, giving the same formula for `beta_(3,6)(C_p)` over every
field. The canonical route proves the colon presentation and computes exact offset homology; an
independent square-zero parametrization and two-characteristic/Smith route are mandatory. A finite
campaign cannot replace the all-parameter integral matching proof. No result, manuscript update,
or publication is claimed at declaration.

EXP-030 is CONFIRMED. The complete colon is

```text
Q_p:f_p=Q_p+(X_h:h in H_p),
```

and its quotient is the canonical idealization of the `p`th Veronese rational normal curve ring.
The low quotient has Hilbert series `(1+(2p-2)z+z^2)/(1-z)^2`. Its multigraded Hilbert numerator,
the `8p`-variable Koszul extension, and an integral relative normal form give

```text
beta_(3,6)=8p(7p^2-12p+2)/3
```

over every field, with support
`[3p+4,29p-5] minus ([6p-3,6p+1] union [9p-3,9p])`. The canonical profiles at `p=4,5,6` total
`704,1560,2912`; the corrected independent audit matches every coefficient and selected rational
ranks; the symbolic certificate passes. The first audit implementation inserted forbidden offset
`8p-1`, is preserved as invalid non-evidence, and motivated an explicit endpoint clause in the
proof. HWB-043 is done. HWB-044 opens an in-place v0.17 manuscript and Zenodo gate. The next
research target is `beta_(3,7)` through the next canonical-idealization strand and comparison map.

HWB-044 is complete. The existing manuscript was expanded in place to v0.17 with the complete
colon theorem, canonical-idealization presentation, multigraded degree-six profile, integral
normal-form proof, evidence ledger, and explicit `beta_(3,7)` boundary. The DOI-bearing 40-page
PDF passed two clean LaTeX builds and complete rendered inspection. A visual defect in the first
theorem render was corrected before the final build and upload. Zenodo record `22030167`, DOI
`10.5281/zenodo.22030167`, is public and concept-latest under concept DOI
`10.5281/zenodo.21763582`; its fresh unauthenticated 714,021-byte download matches MD5
`4c7daffba7539f37ea4ecb6d52fad9d9` and SHA-256
`480f135b9ecf8dbcec0fb91e85491f8fcf11e1e3c7417f6415ebeda366b5d640`. HWB-046 owns the checked
research promotion and later scoped management-ledger reconciliation. No release tag is claimed
for this research-only round.

Research promotion is complete. PR #205 passed `guards` and `test` and merged the complete EXP-030
theorem, artifacts, manuscript v0.17, and verified Zenodo record to `develop` at
`5a1a645f7552585f75f6a9d4f5415cb731df46da`. PR #206 passed all required checks and promoted the
exact tested `develop` state to `main` at `4ec881a182b5ac2dc9fbb99d0bbab173c7ccaf69`.
Research work, `develop`, and `main` share payload tree
`33b044658401e9216705481ad627dea55dbdf754`. CAOS_MANAGE remains untouched on
`task/difusion-rename-all-explorations-20260820` with 397 unrelated staged entries; HWB-046 stays
open only for a later scoped ledger reconciliation after management safely returns to clean
`develop`.

## 2026-08-20 - EXP-031 final third-row vanishing

HWB-045 is redirected from computing another colon coefficient to an integral contraction of the
total-degree-seven relative complex. The decisive simplification is

```text
E_(p,5)=E_(p,4)=[0,24p-1],
E_(p,3)=[0,24p-1] minus {6p-1}.
```

Boolean matching on vertex `0` predicts that the only unmatched triangles have residual `6p-1`.
Every such triangle has a least positive low vertex outside it, and adjoining that vertex gives a
tetrahedron with that triangle as its unique unmatched face. EXP-031 tests whether these fillers
give a signed identity block, proving `beta_(3,7)=0` integrally for every `p>=4`. Complete small
profiles, a separately encoded filler audit, adversarial controls, and a written all-parameter
proof are mandatory. No result or manuscript v0.18 gate is claimed at declaration.

EXP-031 is CONFIRMED. The total-degree-seven relative complex admits an integral zero-vertex
matching. Its only critical triangles have residual `6p-1`; every one receives a same-offset
tetrahedral filler by adjoining a missing vertex from `{1,2,3,4}`. The filler has exactly one
critical face and unit boundary coefficient, so the reduced boundary onto critical triangles is
surjective over `Z`. Thus `beta_(3,7)=0` over every field and the third homological row is complete.

The exact profile campaign gives zero at every offset for `p=4` over `GF(2)` and `GF(1000003)` and
for `p=5` over `GF(2)`. Canonical and independently encoded filler audits agree for
`p=4,...,12`; arithmetic obligations pass through `p=300`. The first tuple-only filler key is
preserved as invalid non-evidence because it compared cells in different offset complexes.
HWB-045 is done and HWB-047 opens an in-place manuscript v0.18 and Zenodo gate. A separate
manuscript remains deferred; after publication, the next research route should use complete-row
data plus duality to derive whole diagonal recurrences before any raw full-resolution sweep.

Manuscript v0.18 is PUBLISHED and fresh-download verified at DOI
`10.5281/zenodo.22030743`. Its 42 pages passed the warning-free two-pass build and complete rendered
inspection; public metadata has one creator and the sole ORCID, record `22030743` is concept-latest,
and the public 725,554-byte PDF matches Git by MD5 and SHA-256. HWB-047 is done and HWB-048 opens
the separate-PR research promotion gate. The scoped CAOS_MANAGE ledger remains deferred while that
checkout contains unrelated staged work.

Research promotion is COMPLETE. PR #209 passed `guards` and `test` and merged the exact EXP-031
plus v0.18 state to `develop` at `ce2b79b0b2d1c98f4613946fb3482190de8fc722`. PR #210 passed
all required checks and promoted it to `main` at
`842371a02758eea2123391bacfde1265197f4e3b`. All three delivery branches shared payload tree
`8d37059beea83e662151fcdeb2ff1bef63d35c2c` before this handoff update. HWB-048 remains open only
for the later scoped CAOS_MANAGE ledger reconciliation.

## 2026-08-20 - EXP-032 complete cubic-colon resolution

HWB-049 opens a declaration-first test of a stronger consequence of EXP-030. Put `c=2p-2` and
`m=8p`. The low canonical idealization is two-dimensional Gorenstein with h-vector `(1,c,1)`, no
linear equations, and regularity two. Minimality and Gorenstein self-duality predict that its
resolution has only the linear strand

```text
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1),  1<=a<=c-1,
```

and the final entry `beta_(c,c+2)=1`. Tensoring with the `m` killed high variables predicts the
complete colon-quotient Betti polynomial

```text
(1+xz)^m(1+sum_a lambda_(c,a)x^a z^(a+1)+x^c z^(c+2)).
```

EXP-032 must independently reconstruct every coefficient, verify Hilbert and self-duality
identities through `p=300`, reject corrupted controls, and supply the all-parameter proof before
any result or manuscript v0.19 gate is claimed. This route determines the colon quotient, not the
still-open full resolution of `C_p`.

EXP-032 is CONFIRMED for the complete graded Betti polynomial and free-module shape. Minimality,
regularity two, and Gorenstein self-duality force the low resolution to have only one linear
strand and the terminal entry `beta_(c,c+2)=1`. The Hilbert numerator determines

```text
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1),
```

and the disjoint high-variable Koszul complex gives the displayed full product. All 297 canonical
rows through `p=300`, an independently reconstructed coefficient route, symbolic identities,
complete `p=4,5,6` tables, and corrupted controls pass. Two budget-limited attempts and two
representation/CAS defects were rejected and recorded before the final artifacts were generated.

HWB-049 is done and HWB-050 opens the existing-manuscript v0.19 and Zenodo new-version gate. The
scope is precise: every free-module rank and shift is proved, but explicit differential matrices
and the full resolution of `C_p` remain open. After publication, the strongest mathematical route
is the cubic mapping-cone comparison map against `P_p/Q_p`, using the now-complete colon table to
turn unknown higher Betti entries into comparison-map ranks.

## 2026-08-20 - manuscript v0.19 prepublication candidate validated

The EXP-032 theorem is incorporated in place rather than split into a third manuscript. The
43-page candidate passed its claim map, two consecutive warning-free LaTeX builds, text and PDF
metadata extraction, complete 150-DPI page inspection, full-size inspection of the new theorem
and boundary pages, sole-author/ORCID audit, content and structure guards, Ruff, all 60 tests, the
full registry pipeline, and manifest/artifact consistency.

The exact candidate is 741,461 bytes with MD5
`0ddc07fc56b07490e66a9b1967c6a0d0` and SHA-256
`ebd4d3294cf1dd6fdeccf8902e93399a6617d661dd7421d9dd260278670f3a15`. The pipeline also
reconciled 13 previously stale experiment-registry entries, including EXP-021--032. Reversible
Zenodo draft `22031481`, DOI `10.5281/zenodo.22031481`, remains empty and unpublished. The next
gate is to commit and push this exact payload before authenticated upload and draft validation.

The committed candidate was uploaded to draft `22031481` and the server reports exactly one
completed file with the expected filename, 741,461 bytes, and MD5
`0ddc07fc56b07490e66a9b1967c6a0d0`. Version, title, sole creator/ORCID, CC BY 4.0, open access,
and the v0.19 description also match. Publication remains deliberately pending until this
reversible checkpoint is committed and pushed.

Manuscript v0.19 is now PUBLISHED at DOI `10.5281/zenodo.22031481` under concept DOI
`10.5281/zenodo.21763582`. Public metadata and the sole file pass, record `22031481` is
concept-latest, and a fresh unauthenticated 741,461-byte download matches MD5
`0ddc07fc56b07490e66a9b1967c6a0d0` and SHA-256
`ebd4d3294cf1dd6fdeccf8902e93399a6617d661dd7421d9dd260278670f3a15`. HWB-050 is done;
HWB-051 opens the separate-PR research-promotion gate. No research release tag is implied.

Research promotion is complete. PR #213 passed `guards` and `test` and merged the full EXP-032,
registry reconciliation, manuscript v0.19, and verified Zenodo record to `develop` at
`0ded528712f18064a7483119bf57324edd8a3a2d`. PR #214 passed all required checks and promoted that
tested state to `main` at `e04660ead2afa68f7490f32a4bf837cd0eaa3533`. Work, `develop`, and
`main` shared payload tree `c2f9f58488c7a1fa7ccee181a75944f7209b795c` before this handoff
update. HWB-051 is done; the next mathematical gate is a declaration-first mapping-cone
comparison experiment, not an unsupported full-resolution claim.

## 2026-08-22 - EXP-033 minimal cubic mapping cone

The comparison-map target was redirected before matrix construction. Put `A_p=P_p/Q_p` and
`L_p=Q_p:f_p`. EXP-030 regularity of `f_p` modulo `L_p` gives the family-specific intersection

```text
Q_p=(Q_p,f_p) intersect L_p.
```

The pullback has a high-variable kernel `K_p` with

```text
H_(K_p)(z)=(8p z+10p z^2)/(1-z).
```

Since EXP-026 makes `X_0` regular on `C_p`, it is regular on `K_p`; hence `K_p` is
one-dimensional Cohen--Macaulay of regularity two. The exact sequence
`0 -> K_p -> A_p -> D_p -> 0` then forces

```text
depth(A_p)=1,   pd(A_p)=10p-1,   reg(A_p)=2.
```

EXP-033 is CONFIRMED. After the cubic shift, every source summand from `D_p(-3)` is in regularity
rows three through five, strictly above all target summands of `A_p`. The entire comparison map is
Tor-zero and the mapping cone is minimal:

```text
B_(C_p)(x,z)=B_(A_p)(x,z)+x z^3 B_(D_p)(x,z).
```

Consequently the complete regularity-three and regularity-four strands are

```text
beta_(i,i+3)=sum_(a=1)^(c-1)lambda_(c,a)binom(8p,i-1-a),
beta_(i,i+4)=binom(8p,i-1-c),             c=2p-2.
```

All 297 canonical rows, all 297 independent coefficient reconstructions, 25 structural kernel
audits, symbolic identities, prior Betti anchors, and adversarial controls pass. Three exact
attempts stopped at `p=102,209,267` under the 120-second cap and remain preserved as
`INCONCLUSIVE_BUDGET`; the final recurrence completes in 15.159 seconds with unchanged earlier
hashes.

HWB-052 is done. This material theorem opens HWB-053 for an in-place main-manuscript v0.20 and
Zenodo new-version gate. The remaining mathematical frontier is no longer the cubic comparison
map: it is the two lower strands of the regularity-two quadratic quotient, best approached through
`0 -> K_p -> A_p -> D_p -> 0` rather than a raw full-resolution sweep.

## 2026-08-22 - manuscript v0.20 publication and repository gates

The EXP-033 theorem is incorporated in the existing main manuscript rather than split into a new
paper. The 45-page v0.20 candidate passed its claim audit, two consecutive warning-free LaTeX
builds, PDF metadata and text extraction, complete 150-DPI page inspection, full-size inspection
of page one and pages 40--45, and sole-human-authorship/ORCID gates. The exact candidate is 774,246
bytes with MD5 `69f45597e879afc8fd91ca4157fb2cf3` and SHA-256
`163a3a2fc6a5d61b6ff97e3ed1089dc3b6e9b320aa9c68ed67d2f1155362d743`.

After the committed candidate and reversible draft checkpoint were pushed, Zenodo record
`22062161`, DOI `10.5281/zenodo.22062161`, was published under concept DOI
`10.5281/zenodo.21763582`. It is concept-latest at version `0.20`; the public title, sole creator
and ORCID, CC BY 4.0 license, filename, bytes, and MD5 agree. A fresh unauthenticated download
matches the committed PDF by MD5 and SHA-256. HWB-053 is done.

Repository gates also pass: template, content, and research-structure guards; Ruff over the CI
scope and EXP-033 scripts; all 60 tests; the full registry pipeline; and manifest/artifact
consistency. Regeneration reconciles EXP-033 plus three previously unbaked tau-conjecture records,
which are retained as repository-wide generated state. HWB-054 is active for the required
work-branch-to-`develop` PR followed by the `develop`-to-`main` PR. The next mathematical problem
remains the two lower strands of `A_p` via `0 -> K_p -> A_p -> D_p -> 0`.

Promotion is complete. PR #218 passed `guards` and `test` and merged the full EXP-033 theorem,
registry reconciliation, manuscript v0.20, and verified Zenodo record to `develop` at
`28bac50f70bd775d17e61d0526eed367e0772ba0`. PR #219 passed all required checks and promoted the
same tested state to `main` at `c1e6b20427d51781afeeb6ef1c5c2d57bf30c649`. Both remote branches
share payload tree `f51cb2845d20b4fbf7d43029a71af0392bc3d6d9`. HWB-054 is done. No release
tag belongs to this research-only round.

## 2026-08-27 - EXP-034 two-layer kernel route

EXP-034 is declared before implementation under HWB-055. It redirects the remaining lower-strand
problem from a raw resolution of `A_p=P_p/Q_p` to the Artinian reduction
`M_p=K_p/X_0K_p`. The proposed offset bases in degrees one and two make the resolution of `K_p`
an explicit family of signed incidence maps.

The first falsifiable target is the codomain cell labelled by

```text
b*=8p-1,   F*={1,...,p},   tau_p=8p-1+p(p+1)/2.
```

If its representation set is exactly `F*`, it has no incoming face and yields a primitive
characteristic-free class in `beta_(p,p+2)(K_p)`. This would refute a naive maximal-rank model of
the kernel. The stronger target is to prove that the same class survives the connecting map from
`D_p` and therefore gives a new lower-strand entry of `A_p`. These targets are intentionally
separate: the ordinary Betti polynomial of `D_p` cannot decide a multigraded connecting map.

The canonical campaign, independent reconstruction, symbolic proof, and corrupted controls are
specified in the experiment hypothesis. A proved kernel class is a relevant structural result;
manuscript v0.21 and Zenodo remain gated on a new theorem for `A_p`.

EXP-034 is CONFIRMED. The first missing degree-two offset `8p-1` and the minimum exterior set
`{1,...,p}` give a one-dimensional integral cokernel in total offset
`tau_p=8p-1+p(p+1)/2`. Every possible connecting-map contribution from `D_p` has a unique
nonzero low boundary coordinate, so no source cycle can hit this class. Since the row-two strand
of `D_p` starts at homological degree `2p-2`, the long exact Tor sequence gives

```text
beta_(p,(p+2,tau_p))(K_p)
=beta_(p,(p+2,tau_p))(A_p)
=beta_(p,(p+2,tau_p))(C_p)=1
```

over every field. Canonical rows pass for all `p=4,...,300`; exact finite-field ranks,
independent numerical-semigroup reconstruction, rational literal sources, symbolic inequalities,
and adversarial controls pass. HWB-055 is done. The theorem crosses the in-place main-manuscript
v0.21 gate under HWB-056, while a separate manuscript and a complete-lower-strand claim remain
deferred.

## 2026-08-27 - manuscript v0.21 publication and repository gates

The EXP-034 theorem is incorporated in the existing main manuscript rather than split into a new
paper. The 48-page v0.21 candidate passed its claim audit, two consecutive warning-free LaTeX
builds, PDF metadata and text extraction, complete 150-DPI page inspection, full-size inspection
of page one and pages 41--48, and sole-human-authorship/ORCID gates. The exact candidate is
792,863 bytes with MD5 `13b92773205a49977abb88cd7ab8dde1` and SHA-256
`c717fbb4d6d3178e0fb0786a8a61c9e2c109d97d77a7b9e1308a2274c0f97539`.

After the committed candidate and reversible draft checkpoint were pushed, Zenodo record
`22135689`, DOI `10.5281/zenodo.22135689`, was published under concept DOI
`10.5281/zenodo.21763582`. It is concept-latest at version `0.21`; the public title, date, sole
creator and ORCID, CC BY 4.0 license, filename, bytes, and MD5 agree. A fresh unauthenticated
download matches the committed PDF by MD5 and SHA-256. HWB-056 is done.

Repository gates also pass: template, content, and research-structure guards; Ruff over the CI
scope and EXP-034 scripts; all 60 tests; the full registry pipeline; and manifest/artifact
consistency. Regeneration adds EXP-034 to the public experiment registry. HWB-057 is active for
the required work-branch-to-`develop` PR followed by the `develop`-to-`main` PR. The next
mathematical route remains classification of the other incidence cokernel cells and their
connecting-map survival; a separate manuscript remains premature.

Promotion is complete. PR #222 passed `guards` and `test` and merged the full EXP-034 theorem,
registry update, manuscript v0.21, and verified Zenodo record to `develop` at
`0092685731eda7b692d5849c86f0c4da2352181e`. PR #223 passed all required checks and promoted the
same tested state to `main` at `4cde1856a0850df8c89cc0fa9473c19ccaaf2b58`. The work branch,
`develop`, and `main` shared payload tree `f571fb955560c29489c181a6ce542548619209e0` before the
documentation handoff. HWB-057 is done. No release tag belongs to this research-only round.

## 2026-08-30 - EXP-035 zero-row classification gate

HWB-058 is active. The invariant-first observation is that a codomain coordinate
`e_F tensor v_b` is an integral zero row exactly when the representation set
`R_b={g:b-g in H_p}` is contained in `F`. EXP-035 first classifies this canonical primitive
cokernel summand without building full incidence matrices.

The stronger target is the block `b=10p+t`, `2<=t<=p-2`, whose predicted representation set has
size `2p-t-1`. These cells would fill the consecutive homological interval
`p+1,...,2p-3` next to the EXP-034 class at `p`. Kernel existence and connecting-map survival are
separate gates. Manuscript v0.22 and Zenodo remain closed unless the all-parameter survival theorem
is proved and independently validated.

EXP-035 is CONFIRMED with its declared P3 mechanism refuted. The zero-row criterion
`R_b subset F` splits off an exact primitive free coordinate summand for every `p>=4`. The block
`b=10p+t`, `2<=t<=p-2`, supplies consecutive kernel classes in homological degrees
`p+1,...,2p-3`.

The first connecting smoke case has an integral cycle, so coordinatewise survival fails. The full
target quotient is stronger: at `(p,t)=(4,2)`, the multigraded Betti number of both `A_4` and
`C_4` is four over `GF(2)` and three over `GF(3)`. The kernel incidence cokernel is
`Z^4 direct-sum Z/2Z`. Complete exact matrices, a semigroup-derived independent reconstruction,
Smith form, four field ranks, and symbolic interval proofs pass. HWB-058 is done. HWB-059 opens
the in-place manuscript v0.22 gate; the next mathematical path is the all-parameter anatomy of
the discovered two-torsion, not another naive unit-pivot sweep.

## 2026-08-30 - manuscript v0.22 publication gate

The EXP-035 result remains in the coherent main manuscript rather than opening a separate paper.
The 51-page v0.22 candidate passed its claim/scope audit, two consecutive warning-free LaTeX
builds, metadata and text extraction, complete 150-DPI rendered inspection, full-size inspection
of page one and theorem pages 45--46, and sole-human-authorship/ORCID gates. The frozen candidate
is 810,905 bytes with MD5 `5ed2409d6688b30147963a7293598440` and SHA-256
`3868f511a047073c9d7bedf25e026f1aaf3a5ab2c05c45d03614675ef6bdf5c2`.

After the committed DOI-baked candidate and validated draft checkpoints were pushed, Zenodo
record `22177072`, DOI `10.5281/zenodo.22177072`, was published under concept DOI
`10.5281/zenodo.21763582`. It is concept-latest at version `0.22`; the public title, date, sole
creator and ORCID, CC BY 4.0 license, filename, bytes, and MD5 agree. A fresh unauthenticated
download matches the committed PDF by MD5 and SHA-256. Ruff, all 60 tests, full registry
regeneration, artifact consistency, and every repository guard pass. HWB-059 is done. HWB-060
opens separate-PR promotion to `develop` and then `main`; no release tag belongs to this
research-only round.

Promotion is complete. PR #226 passed `guards` and `test` and merged the full EXP-035 theorem,
regenerated registry, manuscript v0.22, and verified Zenodo record to `develop` at
`95b944273a34d636c0b256b3e7de455d6371c997`. PR #227 passed both required jobs and promoted the
same tested state to `main` at `10d524a9f9226a95f9d1d23341c54f8af6ce0812`. The work branch,
`develop`, and `main` shared payload tree `0847e35a7641ab5592afd136f42bcf09ffe514f3` before this
documentation handoff. HWB-060 is done. HWB-061 is pending for a freshly declared experiment on
the all-parameter anatomy of the observed factor-two torsion.

## 2026-08-30 - EXP-036 factor-two torsion anatomy gate

HWB-061 is active. EXP-036 first replaces literal combination enumeration by an exact-sum target
constructor and must reproduce the complete EXP-035 `(4,2)` target before larger parameters are
accepted. It then screens every declared family cell for `p=5`, followed by `p=6` only within the
checkpointed budget. The mod-two versus odd-prime rank defect is the invariant-first torsion test;
Smith form is reserved for positive cells.

The complementary recognition lens reduces the known integral matrix by unimodular unit pivots.
The declared strong prediction is a six-essential-variable core with the homology profile of the
minimal real-projective-plane triangulation. This comparison is motivated by the fresh primary
source sweep but is not a premise. A different residual support refutes the recognition clause
while preserving any exact Smith result. No manuscript or Zenodo update is open at declaration.

The canonical finite checkpoint passes. The bounded exact-sum constructor reproduces the complete
EXP-035 `(4,2)` target, then completes both `p=5` and all three `p=6` cells in 94.072 seconds.
Kernel even-rank defects occur at `(4,2)`, `(5,3)`, and `(6,3)`. The connecting quotient creates
additional characteristic dependence even when the kernel is independent: `A_(5,2)` has dimensions
`24` and `20`, while `A_(6,2)` has dimensions `95` and `86` over `GF(2)` and `GF(3)`;
`GF(1000003)` agrees with `GF(3)`.
Together with the EXP-035 gap at `p=4`, the `t=2` excess sequence is `1,4,9=(p-3)^2`. The next
gate is a targeted `p=7,8` test and interval-block derivation, not a raw full-resolution sweep.

EXP-036 is now CONFIRMED with structural propagation unresolved.  Targeted exact cells give
`t=2` characteristic-two excesses

```text
p=4,5,6,7,8,9: 1,4,9,18,31,49.
```

The `p=7` value refutes `(p-3)^2`; the `p=9` value refutes the quadratic that fits `p=5,...,8`.
For every tested `5<=p<=9`, the `t=2` kernel-cokernel dimensions agree over all three tested
fields and the
connecting-image rank creates the entire excess.  This is a second mechanism, distinct from the
kernel rank defects at `(4,2)`, `(5,3)`, and `(6,3)`.  Independent semigroup reconstruction,
dynamic exact sums, reverse pivots, and a third odd field reproduce the canonical targets.

The `(4,2)` unit reduction confirms a compact factor-two residual but traces it to seven low
variables, so the declared six-variable projective-plane recognition is not obtained.  A separate
symbolic argument closes the family-wide cubic question: its shifted source misses the target by
at least `3(p-1)^2`, hence `A_p=C_p` at every declared `(p,t)`.  This does not prove infinitely
many characteristic-dependent cells or a formula for their multiplicities.  HWB-061 remains
active only for that connecting-parity theorem.

## 2026-08-30 - manuscript v0.23 publication gate

HWB-062 opens an in-place update of the main manuscript.  The publication payload must include
the finite propagation table, the distinction between kernel and connecting mechanisms, the
compact integral localization, both refuted interpolations, the all-parameter cubic-source
inequality, and an explicit finite-only scope statement.  A separate paper remains premature.

The gate requires a fresh claim audit, two warning-free builds, PDF metadata and text checks,
complete 150-DPI rendered inspection, sole-human-authorship and ORCID checks, exact Zenodo draft
validation, publication, concept-latest verification, and a fresh public-download hash match.
HWB-063 opens only after that publication is frozen and owns separate PR promotion through
`develop` and `main`.

The publication gate is complete.  The 53-page v0.23 passed the claim and scope audit, two
warning-free stabilized builds, metadata and text extraction, complete 150-DPI rendered
inspection, sole-human-authorship and ORCID checks, all repository tests and guards, exact
one-file draft validation, publication, concept-latest verification, and a fresh unauthenticated
download.  Zenodo record `22181972`, DOI `10.5281/zenodo.22181972`, contains the exact 824,114-byte
PDF with MD5 `6bcacfa265e840f40e89dcdb87b75f7b` and SHA-256
`c77b08a3724db90b14039c2c88e98325403ef4f656f52137057a27eb6fa5072d`.  HWB-062 is done and
HWB-063 is active for separate-PR promotion to `develop` and then `main`.

The promotion gate is complete. PR #230 passed `guards` and `test` and merged the complete
EXP-036 theorem, regenerated registry, manuscript v0.23, and verified Zenodo publication to
`develop` at `fc40e74251c2b8c16e0875178742aeed45e25ce0`. PR #231 passed both required jobs and
promoted the exact state to `main` at `817cc01ea76074f4989e28f11511ddb8c2343ce2`. Before this
documentation handoff, work, `develop`, and `main` shared payload tree
`8ea3fbd0dfd136a7b91c508a31146be7d88eded1`. HWB-063 is done. The strongest remaining route is
HWB-061's infinite parity-sensitive connecting-quotient theorem; neither complete lower strand is
claimed.

## 2026-08-30 - EXP-037 connecting-parity quasipolynomial gate

HWB-064 is active under the still-open HWB-061 structural objective. A sequence lookup after two
failed interpolations exposes a new period-six cubic candidate with rational generating function

```text
(1+2x+x^2+x^3)/((1-x)^2(1-x^2)(1-x^3)).
```

This is a falsification target, not evidence. It predicts the new exact excesses `73` and `104`
at `p=10,11`. The invariant-first route computes `(10,2)` over `GF(2)` and `GF(3)` after exact
small-cell regressions. The structural route performs integral unit cancellation on the full
connecting presentation and seeks unmatched factor-two cells indexed by the lattice points of
the generating function. Finite agreement cannot confirm the all-parameter statement. No
manuscript or Zenodo update is open at declaration.

The first EXP-038 gate passes. The complete `(11,2)` block gives surviving dimensions `8688` over
`GF(2)` and `8586` over both `GF(3)` and `GF(5)`, hence `e_11=102`. Low-degree and canonical
orders agree on every exact rank. The denominator implies the order-seven recurrence

```text
e_n-2e_(n-1)+e_(n-3)+e_(n-4)-2e_(n-6)+e_(n-7)=0,
```

and `p=11` is its first nontrivial out-of-sample check. Measured primary/audit times of 330.533246
and 176.288232 seconds activate the already declared second prediction `e_12=138` under a
7,200-second, 40-GB cap. Even two finite passes do not prove the recurrence or its proposed
degree-six relation.

EXP-037 is now REFUTED at the first out-of-sample gate. The complete `(10,2)` presentation gives
surviving dimensions `4240` over `GF(2)` and `4168` over `GF(3)`, hence `e_10=72`, not 73. A
canonical residual order reproduces every `GF(2)` rank, while `GF(5)` reproduces every `GF(3)`
rank. The kernel cokernel and connecting boundary are field-independent; the 72-dimensional
defect is entirely in the connecting image. The proposed 73-point lattice indexing therefore
fails as well. HWB-064 is done. This finite refutation does not trigger manuscript v0.24 or a
Zenodo version.

## 2026-08-30 - EXP-038 degree-six relation gate

HWB-065 is active under HWB-061. The smallest structural correction to the rejected free-lattice
series is a first relation in degree six:

```text
(1+2x+x^2+x^3-x^6)/((1-x)^2(1-x^2)(1-x^3)).
```

This is fitted through `p=10`, not inferred as a theorem. It forces the new prediction `e_11=102`
and then `e_12=138`. The primary gate is the complete `(11,2)` rank over `GF(2)` and `GF(3)` under
3,600 seconds and 40 GB. A pass requires a canonical-order `GF(2)` and `GF(5)` audit before any
attempt to identify the proposed relation. A mismatch closes the formula immediately. No
manuscript or Zenodo update is open at declaration.

## 2026-08-30 - EXP-039 component-stabilization gate

Both declared EXP-038 finite predictions pass exactly: `e_11=102` and `e_12=138`, independently
audited by alternate residual order and `GF(5)`.  EXP-038 remains inconclusive because neither the
degree-six relation nor the order-seven recurrence is proved.  A third large coefficient is
therefore demoted behind a structural test.

EXP-039 applies the anatomy, topology, invariant, and two-sided lenses to the combined signed
presentation.  Exact unit peeling is followed by bipartite connected-component decomposition and
per-component ranks.  The strong finite prediction is that every defective component through
`p=9` is bounded by 5,000 vertices and contributes defect one, with recurring normalized signed
types.  A giant defective component refutes that model and redirects to a finer matched-block or
relative-homology decomposition.  The run is capped at 1,800 seconds and 20 GB with per-parameter
checkpoints.  No publication gate is open.

## 2026-08-30 - EXP-040 merged-sector relation gate

EXP-039 is refuted at `p=6`: defects are not one per bounded connected component.  Its exact
partitions nevertheless reveal four latent sectors with dimensions
`binom(p-2,3),p-4,p-4,p-5` for `p=6,7,8`.  At `p=9`, the first three merge in support and retain
combined defect `35+5+5=45`; the fourth remains four.  Erasing signs or flipping one sign changes
every defective odd rank, so support-only topology is insufficient.

EXP-040 is declared before computation.  At `p=10`, it predicts partition `67+5`: the merged free
value `56+6+6=68` loses exactly one relation while the fourth sector remains five.  On a pass, the
conditional `p=11` prediction is `96+6`, corresponding to two degree-one translates.  Both odd
fields must agree componentwise.  Only after both partitions pass may signed bridge extraction
begin.  No manuscript or Zenodo gate is open.

The first partition passes exactly. At `p=10`, the two defective components contribute `67+5`;
their ranks are `218451/218518/218518` and `2445/2450/2450` over `GF(2)/GF(3)/GF(5)`. Thus the
first correction from free total 73 to exact 72 is localized inside the large merged component.

The conditional second partition is refuted. At `p=11`, the exact split is `95+7`, not `96+6`,
while the aggregate remains 102 and both odd fields agree componentwise. This leaves
connected-component identity unresolved: the isolated component might switch from the latent
`p-5` sector to one of the `p-4` sectors, or might change rank internally. P3 bridge deletion is not attempted
because its P2 transport premise failed. HWB-067 is done; HWB-068 records semantic interval-tag
profiling as the next route. No manuscript or Zenodo gate opens.

## 2026-08-31 - EXP-041 semantic-sector gate

HWB-068 is active. EXP-041 is declared before implementation and replaces component size or rank
matching by exact semantic atoms: module side, affine coefficient interval, and exterior
interval-count vector. The `p=8` partition `20+4+4+3` supplies three named anchor types without
using component indices. The strong prediction is that the isolated components at `p=9,10`
retain the defect-three anchor's coefficient-tag support, while the isolated defect-seven
component at `p=11` switches to exactly one defect-four anchor.

The implementation must reproduce every frozen support hash and component partition before its
profiles count as evidence. It then stores exact defective-component histograms and an independent
sum/reversed-tag audit. A failure refutes component-level interval grading and redirects to chain
generators inside the merged support. The campaign is capped at 2,400 seconds and 36 GB with
atomic parameter checkpoints. No manuscript or Zenodo gate is open at declaration.

The completed profiles reproduce all frozen support hashes and partitions. P1 passes finitely:
at `p=8`, the defect-three anchor is the unique defective component omitting `H1/C1`. P2 is
refuted more strongly than a support-only failure. The isolated component keeps the same eight
coefficient tags and, after subtracting `p` from its `L0/L1` exterior counts, exactly the same
twelve semantic atoms for `p=8,...,11`. Its defect sequence is `3,4,5,7`; the last jump is an
internal signed-rank event, not an `R -> L` identity switch. P3 is refuted because the selected
EXP-035 row is absent from every defective profile; no particular peeling history is inferred.

HWB-068 is done and HWB-069 is active. The next gate is not another coefficient. It is an exact
signed normal form for the persistent twelve-atom family: extract the incidence blocks, cancel
unit/matched pairs integrally, and audit the residual over `GF(2)`, two odd primes, and, if small
enough, Smith normal form. A chain-level relative-homology or OI-module description is the proof
route only after explicit parameter maps are constructed. Toric gluing remains downstream until
an actual ideal or chain splitting exists. No manuscript or Zenodo gate opens from EXP-041.

## 2026-08-31 - EXP-042 Bockstein normal-form gate

The path audit ranks a matrix Bockstein plus integral matched-block reduction above another
coefficient computation. EXP-042 is declared before implementation. It independently extracts the
persistent isolated signed matrix and computes the first Bockstein
`ker(M mod 2) -> coker(M mod 2)` by lifting binary kernel vectors, dividing their even integer
boundaries by two, and reducing again modulo two. The exact prediction is Bockstein rank
`3,4,5,7` at `p=8,9,10,11`.

A pass proves finitely that the observed defects have independent order-exactly-two directions;
without a rational-rank upper bound it is not a complete Smith form. Forward/reverse reductions,
frozen multi-prime ranks, and an independent witness audit are mandatory. OI/FI stability,
relative homology, and toric gluing remain downstream until explicit chain maps or splittings are
constructed. No publication gate is open.

The full campaign passes all three predictions. Exact first-Bockstein ranks are `3,4,5,7`, equal
to the isolated odd-minus-two rank gaps. Independent high- and low-pivot implementations agree on
rank. They disagree on representative atom: high pivots place images in `D:B`, while low pivots
place them in `K:C0`. The rank therefore proves finite valuation-one Smith factors; neither atom
is a canonical torsion carrier.

HWB-070 is the next finite closure gate. Use a product of distinct primes whose logarithm exceeds
the Hadamard bound for every `(r+1)` minor. If every modular rank stays at `r=rank_GF(3)`, all such
minors vanish over the integers and `rank_Q=r`. Combined with EXP-042, this would prove that the
complete 2-primary torsion of each tested isolated cokernel is elementary. A uniform
matched-block/chain-map theorem remains necessary for an all-parameter result. No manuscript or
Zenodo gate opens from the finite Bockstein result.

## 2026-08-31 - EXP-043 Hadamard rational-rank gate

EXP-043 is declared before modular computation. For each isolated matrix, let `r` be the frozen
`GF(3)` rank and `d` its maximum column degree. Distinct verified 61-bit primes must all give rank
`r`; their exact product `Q` is accumulated until `Q^2>4*d^(r+1)`. Then every `(r+1)` minor is
divisible by `Q` and strictly bounded by `Q/2`, proving it is zero. The existing rank-`r` minor
modulo three supplies the matching lower bound.

The strong prediction is `rank_Q=1002,1607,2450,3586` for `p=8,9,10,11`. Combined with EXP-042,
this would completely identify the finite isolated 2-primary cokernels as elementary groups of
ranks `3,4,5,7`. Opposite-pivot modular recomputation and deterministic primality verification are
mandatory. No all-parameter or publication claim is opened.

All three predictions pass. The exact rational ranks are `1002,1607,2450,3586`, certified by
minimal prefixes of `31,52,83,125` distinct 61-bit primes. An independent low-pivot audit
recomputes all 291 ranks, verifies every prime and exact product, and confirms the Hadamard bounds.
Combined with EXP-042, the complete isolated 2-primary cokernels are
`(Z/2)^3,(Z/2)^4,(Z/2)^5,(Z/2)^7`.

HWB-070 is done. HWB-071 redirects from finite arithmetic to the chain mechanism: test exact row
projections involving `D:B` and `K:C0`, identify whether deleting either side kills or transfers
the Bockstein, and then build a parameterized integral matching. The representative dependence
found by EXP-042 forbids declaring either atom the canonical carrier. No manuscript or Zenodo gate
opens until a uniform theorem or comparably transferable result is proved.

## 2026-08-31 - EXP-044 row-projection bridge gate

EXP-044 is declared before projected ranks are read. It tests four exact presentations of every
isolated `p=8,...,11` matrix: delete `D:B`, delete `K:C0`, delete both, and retain only their union.
The strong two-sided-bridge hypothesis predicts that deleting either side kills the first
Bockstein, while retaining the union preserves ranks `3,4,5,7`. Forward/reverse Bocksteins and
three finite-field ranks are mandatory for every projection.

A pass would identify the smallest currently visible row-atom bridge candidate. A refutation would
be equally actionable: surviving torsion after a deletion or lost torsion in the union projection
would specify which larger atom set the integral matching must include. The computation does not
substitute for unimodular reduction or compatible maps in `p`, so it cannot establish the uniform
theorem or open a publication gate.

The full result passes P1 and P3 but refutes P2. Deleting `D:B`, deleting `K:C0`, or deleting both
gives equal ranks in all three fields and Bockstein zero for every `p=8,...,11`. Retaining only the
union also gives zero, so the two atoms are necessary interfaces but not a sufficient carrier.
The independent low-pivot audit passes all 158 checks.

HWB-071 therefore redirects to a bounded atom-lattice gate: enumerate all 64 subsets of the six
normalized row atoms, identify every inclusion-minimal subset preserving the full Bockstein, and
require the minimal carrier pattern to agree across all four parameters. Integral Morse matching
starts only after that carrier is known.

## 2026-08-31 - EXP-045 complete row-atom carrier lattice

EXP-045 is declared before any new subset ranks are read. It enumerates all 64 subsets of the six
normalized row atoms for each `p=8,...,11`. The strong prediction is six-way essentiality: every
proper subset has Bockstein zero and the full set alone carries ranks `3,4,5,7`. If refuted, the
runner must return the complete inclusion-minimal nonzero and full-carrier antichains rather than
select a favorable subset after computation.

All three fields and two genuinely opposite Bockstein conventions are required for every one of
the 256 projections. The finite carrier table is a map for integral Morse reduction, not a
replacement for it; no uniform theorem or publication gate is opened in advance.

All three predictions are refuted as declared, but the exhaustive table exposes a stronger useful
structure. For `p=8,9,10`, nonzero carriers are exactly the supersets of mask `58`; at `p=11` they
are exactly the supersets of mask `56`. Full carriers are exactly `59,62,63` for every parameter,
with stable minimal antichain `{59,62}`. The intersection core `58` has Bockstein sequence
`1,2,3,5`, and either alternative completion adds exactly two classes to give `3,4,5,7`.

The independent low-pivot audit passes all 2,855 checks. HWB-071 now targets relative integral
presentations for `58->59` and `58->62`, seeking a signed equivalence of their two-class
completion. The separate `56->58` quotient owns the new `p=11` threshold. More coefficients remain
lower priority until these relative blocks are understood.
