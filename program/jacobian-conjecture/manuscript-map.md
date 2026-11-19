# Jacobian conjecture: result and manuscript map

Updated 2026-11-16 (methodology 13 adopted at the strategic review that EXP-146 triggers). This map separates
mathematical evidence, strategic value, manuscript coverage and external novelty. Experiment verdicts remain the
authority for proofs and refutations; the machine-readable record is `research-governance.json`.

## Status boundary

The Jacobian conjecture is false in every dimension n >= 3 since the counterexample announced by Alpoge on 2026-07-20
(question posed by Akhil, map produced with Claude Fable 5). The planar case JC(2) is open. The CAOS program validates the
public counterexample, states the consequence cascade at the level of dimension indices, and proves exact results about
the plane. It does not claim the counterexample and does not decide JC(2).

The planar degree floor is Guccione, Guccione, Horruitiner and Valqui's (arXiv:2204.14178, Theorem 2.1): a counterexample
to JC(2) has max deg >= 125 or degrees (72,108) or (108,72). Their Proposition 4.3 reduces the open case to two coefficient
systems (Cases 1 and 2). Helali (Zenodo 10.5281/zenodo.21479814, 2026-07-21) claimed first that both are empty,
conditional on that proposition and on his transcription; Guo claimed it second (2026-08-10). EXP-137 (Case 2) and
EXP-146 (Case 1) are an independent proof of both cases, with the same conditions (Proposition 4.3 exhaustive; the
encoding of its polygons, EXP-137). Priority for the exclusion stays Helali's.

Internal exact validation and Zenodo persistence do not establish peer review or worldwide novelty; no negative
literature search is described as proof of novelty.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Validation of the counterexample, seed family, degree laws, non-properness, char-p reductions | EXP-001 to EXP-012 | machine-verified and derived; validation is replication | trusted baseline and structure | `foundational` |
| Image of the announced map and its fibers over C = 0 | EXP-145 | CONFIRMED: image is C^3 minus the curve Gamma; corrects foundational v0.14 | correction with exact proof | `foundational` v0.15 |
| Two-dimensional equivariant rigidity | EXP-005, EXP-006, EXP-010 | proved (affine with one zero weight) | separates the mechanism from the plane | `foundational` |
| Consequence cascade at the level of indices | EXP-016, EXP-018, EXP-041, EXP-136, EXP-138, EXP-144 | located in primary sources (Mathieu 1997 not located); explicit objects checked exactly | prevents overclaiming the cascade | `cascade` v0.10 |
| Planar machine and weight-class exclusions | EXP-013 to EXP-049 (cited ones) | four theorems proved; the fifth on six certified shapes, a conjecture beyond | uniform planar exclusions | `planar`, Section `sec:theory` |
| Truncation ladder for a simultaneous covector | EXP-055, EXP-064, EXP-067, EXP-068, EXP-071 to EXP-075, EXP-078, EXP-080 | degrees 1 to 3 excluded modulo primes; ceiling and sl2 premise refuted | negative, bounded | `planar`, Section `sec:ladder` |
| Frontier recalibrated against primary sources | EXP-082, EXP-083, EXP-094 | the floor table with sources; twenty-three configurations in [125,150] undecided by the sources | the map of what is open | `planar`, Section `sec:frontier` |
| Chart atlas of the Case 1 system | EXP-050 to EXP-135 (cited ones) | exact closures of three- and four-coefficient restrictions and boundary sections | partial; superseded as a route by EXP-146 | `planar`, Section `sec:atlas` |
| Independent checks of Helali's Cases 1 and 2 | EXP-137 | Case 2 empty (Singular std in 3 s); Case 1 identities verified, unit at five primes | half of an independent proof | `planar`, Section `sec:helali` |
| Cost of exact and multi-modular Case 1 certificates | EXP-139 to EXP-143 | UNKNOWN at their budgets; heights above about 94,000 digits | measured cost; motivates EXP-146 | `planar`, Table `tab:cost` |
| Case 1 certified empty | EXP-146 | CONFIRMED: both branches certified by three-leaf resultant-chain trees at one prime, replayed at a second, Singular digests, third primes in the review | completes the independent proof (conditional) | `planar` v0.38 (drafted; publication waits for Felipe's validation of the phrasing) |
| The (9,24) case of the floor | EXP-147 | CONFIRMED: Theorem 5.1 of GGHV 2022 applies to the three classes of their Proposition 4.2 as printed (no unprinted bridge) | removes the gap the floor 125 inherited | `planar` v0.38 after its fix pass (the draft at c9874c70 still discloses the gap) |

Experiments outside these blocks are research records (calibration, superseded routes, finite or negative probes);
EXP-060, EXP-070 and EXP-076 are superseded (`research-governance.json`, `experiment_dispositions`).

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `foundational` | v0.16 | [10.5281/zenodo.24358311](https://doi.org/10.5281/zenodo.24358311) | [10.5281/zenodo.21503365](https://doi.org/10.5281/zenodo.21503365) | what the three-dimensional counterexample is: validation, structure, image, rigidity |
| `planar` | v0.38 | [10.5281/zenodo.24358296](https://doi.org/10.5281/zenodo.24358296) | [10.5281/zenodo.21503367](https://doi.org/10.5281/zenodo.21503367) | what can be proved about planar Keller maps, and where the degree floor stands |
| `cascade` | v0.10 | [10.5281/zenodo.24269044](https://doi.org/10.5281/zenodo.24269044) | [10.5281/zenodo.21503371](https://doi.org/10.5281/zenodo.21503371) | which implied and equivalent conjectures the counterexample settles, at which indices |

Split decision (2026-11-16 review): the three papers have different central questions and toolkits (exact validation
and real geometry; Newton polygons, certificates and elimination; located implications), so they stay separate. A
methods paper for the certificate method splits off only under focus JC-F6 (a second system certified by the same
method).

## Focus record

- Closed: JC-F0 (validation and structure), JC-F1 (cascade), JC-F3 (chart atlas; parked by JCB-098 on 2026-11-02 and made
  unnecessary for the exclusion by EXP-146).
- Dormant: JC-F2 (planar exclusions; the extension beyond the certified grid and a terminating covector ladder have no
  route).
- Active: **JC-F4**, the independent proof that Case 1 is empty. Its success gate was met on 2026-11-16 by EXP-146; it
  stays active until the planar paper carries the result (v0.38), whose publication waits for Felipe's validation of
  the closure phrasing (`72108-closure-statement.md`, "Proposed next steps (Felipe decides)").
- Proposed, for Felipe at this review (methodology 13: a changed target is shown before it is treated as the
  continuation): JC-F5, the twenty-three configurations of maximal degree in [125,150] left undecided by the sources
  (the next gap of the floor); JC-F6, the certificate method on a second system and a methods paper.

## Open obligations

- `planar`: v0.38 with EXP-146 and EXP-147 (brief `jc-planar-v038-2026-11-16` in CAOS_MANAGE); the fifth exclusion beyond its grid
  stays a conjecture; the twenty-three configurations in [125,150].
- `foundational`: v0.16, one sentence pointing to the planar certificate, released with planar v0.38.
- `cascade`: Mathieu for 3 <= N <= 14 (JCB-096); Wilson's GMC(2) proof (JCB-097).
