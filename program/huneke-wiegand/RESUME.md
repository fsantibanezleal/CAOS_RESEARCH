# Huneke-Wiegand extensions - session handoff

Updated: 2026-08-10. Lifecycle: published. EXP-009 proves an infinite family, manuscript v0.03
is published, PR #145 promoted the research round to `develop`, and release v0.63.000 promoted
the tested state through PRs #146 and #147 to tag `v0.63.000` on `main`.

## 1. State in one screen

Son Pham has priority for the first public counterexample, independently verified by Professor
Craig Huneke. CAOS does not claim that discovery. Its validated extensions are:

1. an independent Singular/4ti2 reproduction of the decisive colon equality (EXP-001);
2. exact endomorphism-overring anatomy and the Ext/Tor escape mechanism (EXP-002);
3. certified Frobenius minimality `F_min=181` in the symmetric numerical-semigroup,
   two-generated monomial-ideal class (EXP-004/005);
4. uniqueness of the normalized pair at that minimum (EXP-007); and
5. an explicit infinite family of counterexamples in the same class (EXP-009).

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

## 4. In flight

- v0.01 DOI `10.5281/zenodo.21763583`: Frobenius minimality.
- v0.02 DOI `10.5281/zenodo.21764868`: minimum-layer uniqueness. Public PDF SHA-256
  `93a07d124c7b3f2cf144a5343d31ca40e312a80d99308b3ef567c7065f126bb9`.
- v0.03 DOI `10.5281/zenodo.21873911`: explicit infinite family. The public 399,272-byte PDF has
  MD5 `bd9767de4a530150073f654c76ba84a0` and SHA-256
  `f2edff24e924a8d38bc7becd380a69f30fa6b2466c3f584802b829f14d1393cf`.
- concept DOI `10.5281/zenodo.21763582`.
- The concept latest resolves to record `21873911`; title, version, sole author/ORCID, licence,
  filename, bytes and both hashes were checked from a fresh public download.

## 5. Next actions

1. Resume the surviving-variants matrix and optional classification of the EXP-009 family or
   nearby Kunz faces as a separately declared research round.
2. Keep EXP-010 inactive: its old conditional gate was superseded when EXP-009 succeeded.
3. Treat release `v0.63.000` as the frozen public repository baseline for subsequent work.

## 7. Gotchas

- The broad Huneke-Wiegand conjecture is already false by the public seed. CAOS's new theorem is
  an infinite family in numerical semigroup rings with two-generated monomial ideals; it is not a
  classification of arbitrary modules or arbitrary one-dimensional Gorenstein domains.
- Son Pham retains discovery priority for the first public counterexample.
- Expert verification is not journal peer review.
- Never import or execute upstream verifier code as independent CAOS evidence.
- A finite sweep is not the infinite-family proof; the affine interval argument is load-bearing.
- Solver SAT needs independent semantics; UNSAT needs accepted certificates or another complete
  route. Equality in a finite window needs a proved tail.
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
