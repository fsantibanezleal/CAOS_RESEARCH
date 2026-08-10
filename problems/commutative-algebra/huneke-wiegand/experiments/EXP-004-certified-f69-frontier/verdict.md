# EXP-004 verdict - CONFIRMED

Run date: 2026-08-02. Phase HW-P3. Backlog HWB-004.

## Decision

CAOS independently reproduces the published `F<69` positive frontier for two-generated monomial
ideals over symmetric numerical semigroup rings. Two independent complete routes agree, and all
predeclared predictions P1-P6 pass.

This is a certified reproduction of García-Sánchez--Leamer Example 23, not an extension of its
mathematical boundary and not a new counterexample.

## Prediction table

| prediction | result | decisive evidence |
|---|---|---|
| P1 | PASS | Route A enumerates exactly six semigroups at `F=11`; none has a rigid gap |
| P2 | PASS | all 48,954 symmetric semigroups and 1,503,391 gaps for odd `F<=67` checked; zero rigid cases |
| P3 | PASS | the declared `F=11` mutation is rejected because closure fails at `(1,1)` |
| P4 | PASS | independent DIMACS at `(181,14)` is SAT; decoded model equals the public candidate and passes exact semantics |
| P5 | PASS | all 1,156 fixed `(F,s)` formulas below 69 are `UNSAT_VERIFIED`; every DRAT proof is accepted |
| P6 | PASS | routes agree; pinned tools, atomic checkpoints, per-file hashes and an independent full-manifest audit pass |

## Route A - theorem-complete tree

The direct Blanco--Rosales Theorem 9 implementation exhausted every odd Frobenius number from 1
through 67 in 529.60 seconds:

```text
symmetric semigroups: 48,954
gap cases:            1,503,391
rigid cases:          0
aggregate SHA-256:    5771bd998c4a80a79f8ba7e0621494231145a291bc7cbeee939dd3caa4a93d4a
```

Every node was independently checked for closure, symmetry, genus and the theorem parent, and
every nonrigid gap retained a first element of `D` missing from `E+E`. The largest tree contained
11,971 semigroups at `F=67`.

## Route B - proof-carrying Boolean obstruction

The independently written DIMACS route completed in 3,349.61 seconds:

```text
fixed formulas:        1,156
SAT:                   0
UNSAT_VERIFIED:        1,156
UNKNOWN:               0
CNF bytes:             142,745,039
DRAT proof bytes:       51,916,843
aggregate SHA-256:      47e1d9489581fd8be7fad5553af0c535acf7ffc31acc8a137f32c7e95dd2f57e
```

The slowest fixed query was `(F,s)=(39,19)` at 2.961 seconds, far below the 300-second cap. The
calibration formula at `(181,14)` was SAT and its extracted semigroup passed the independent exact
checker.

Pinned proof toolchain:

```text
CaDiCaL reported version: 1.7.3
Ubuntu package:           1.7.4-1
CaDiCaL SHA-256:          7b73df0a6d9cf3c751a1948300e5baff8e82c4d39bcd88f0c063b5f5cfb8b33e
DRAT-trim commit:         2e3b2dc0ecf938addbd779d42877b6ed69d9a985
DRAT-trim SHA-256:        92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a
```

## Independent manifest audit

`audit_route_b.py` rehashed every CNF, proof, solver log and checker log from the compact result
manifest:

```text
manifest entries:              1,156
external files rehashed:       4,624
external bytes:                211,671,241
missing files:                 0
hash mismatches:               0
bad solver/checker markers:    0
aggregate recomputation:       MATCH
route-b-results.json SHA-256:  74b43dc194d10dcdcbc25a6125e9f37e495d28692ca7545bdfb0a4912f364571
```

Heavy artifacts remain under
`E:/_Datos/caos-research/huneke-wiegand/EXP-004-certified-f69-frontier/route-b-full/`. Git contains
the deterministic code, full compact manifest/checkpoint and audit result.

## Instrumentation note

During the earlier `F<=11` smoke run, the command wrapper did not stream the child process output
and a wrapper termination request did not terminate the child. The experiment script itself kept
writing atomic checkpoints and safely completed all 36 queries. No proof, formula, status or
mathematical result was lost or inferred from the wrapper. The later full run used a hidden
background process with explicit logs and completed normally.

## Exact claim boundary

For every symmetric numerical semigroup with Frobenius number below 69 and every nonprincipal
two-generated monomial ideal, the finite rigidity equality required for a counterexample fails.
This follows independently from the complete enumeration theorem route and from checked Boolean
certificates.

EXP-004 does not prove anything for `F>=69`, does not prove the public `F=181` value minimal, does
not classify examples, and does not establish an infinite family. Reproduction alone does not
trigger a manuscript or Zenodo release. EXP-005 is now unblocked and owns the novel frontier.
