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
