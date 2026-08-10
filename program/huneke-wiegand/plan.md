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
endomorphism/reflexivity row of the surviving-variants matrix. The next gate is manuscript v0.04
and immutable publication, followed by a separately declared classification question rather than
an automatic return to EXP-010.
