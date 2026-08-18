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
