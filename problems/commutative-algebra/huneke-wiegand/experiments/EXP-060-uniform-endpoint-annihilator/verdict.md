# EXP-060 verdict

Date: 2026-09-05. Status: **CONFIRMED: uniform original-map 2-annihilation.**
The hypothesis was committed and pushed as `db3642d` before computation.
The all-parameter signed proof and the independent full-boundary audit pass.

## Exact result

For every integer `p>=8`, the explicitly generated integral source

```text
V_p=P(F_2+2F_1-4delta_03-4delta_02)+4Q_3-4Q_2
```

satisfies `M V_p=2eta_p` in the complete original presentation of EXP-036.
No D row, K row, or high-variable face is projected away. From EXP-057's
corrected identity `M(s+q)=b_A+b_B+eta`, it follows that

```text
M(2s+2q-V_p)=2(b_A+b_B).
```

Therefore both tracked classes have order dividing two in the full integral
cokernel. When two is invertible in the coefficient ring, these particular
classes vanish by the explicit half-source identities. Uniform nonvanishing
in characteristic two is not established.

The result rests on the all-parameter [proof](proof.md): complete signed D
equations with truncation endpoints, an exhaustive K-face table,
reflection-symmetric interval telescoping, and both short kernel-domain
corrections. Independent paper review checked these arguments, including the
`p=8` endpoint inequalities. Finite agreement is not extrapolated into a theorem.

## Declared predictions and audit

| Prediction | Verdict | Basis |
|---|---|---|
| P1: zero complete D boundary and the stated surviving K faces | PROVED for every `p>=8` for the constructed potentials | Shifted A/B equations, truncation checks, and all low/high products |
| P2: `M P(F_j)=2x_0j`, `j=1,2` | PROVED for every `p>=8` | C0 reflection and three signed interval endpoint identities |
| P3: B/D identities and `M V_p=2eta_p` | PROVED for every `p>=8` | Exact Q2/Q3 signs, admissibility, and original target-vector equality |
| Independent finite campaign | PASS, all 18 declared parameters | Independent sources, complete differentials, archive verification, and mutation controls |
| Uniform nonzero order-two class | NOT ESTABLISHED | Requires a full-relation annihilating functional or another nonvanishing proof |
| Second class and complete quotient upper bound | NOT ESTABLISHED | Separate research obligations |

The fixed campaign checks `p=8,...,20,25,32,50,64,100`. At every parameter:

- The producer's two original differential encodings agree on the component
  chains and the complete `V_p` boundary.
- The independent auditor reconstructs every `V_p` source coefficient and
  exterior label using its own potential parametrization, then applies a
  separately encoded bitset differential.
- P1/P2 and both B/D identities pass; the final original boundary has exactly
  zero D rows and four K rows, equal to `2eta_p`.
- Wrong-sign and single-coefficient controls produce nonzero discrepancies.
- Both distinct pre-declaration rejected proposals fail, with their exact
  residual vectors reproduced independently.

The auditor additionally runs 25 literal EXP-054 full-differential crosschecks:
the five sources `P(F_1)`, `P(F_2)`, `P(delta_03)`, `P(delta_02)`, and `V_p`
at each `p=8,...,12`. No independent full-matrix rank or lattice calculation
is claimed or needed.

Observed `V_p` support is 110 at `p=8` and 3054 at `p=100`; its coefficient
height is five at every declared parameter. The support observations do not
constitute an all-parameter counting theorem. The complete labelled sources
are retained losslessly, not replaced by these summaries.

All 20 new tests and the focused Ruff check pass. The tests include the original
`b_A+b_B` source transfer at `p=8` and use temporary output paths. Producer
and auditor complete within the declared per-process 60-second and 1-GiB caps.
There is no HNF, Smith form, global basis, or old HNF-source input. The new
formula is tested at `p=11`, but the old `p=11` labelled source holdout remains
unread and no holdout novelty claim is made.

## Both rejected formulas remain visible

Let `D=P(delta_02)+Q_2`. Merely omitting this correction from the final source
gives `V_omit=V_p+4D`, whose discrepancy is

```text
M V_omit-2eta=4(x_01+e(2;0,1)).
```

The literal earliest proposal also had the wrong `F_1` sign. It equals
`V_early=V_omit-4P(F_1)` and has discrepancy

```text
M V_early-2eta=4(e(2;0,1)-x_01).
```

Both are nonzero because `x_01=e(1;0,1)` and `e(2;0,1)` are different
original target rows. The errors were found on paper before the hypothesis
was declared; the final experiment was not silently repaired after a failure.

## Certificate identity and full-source persistence

| File | SHA-256 |
|---|---|
| `run.py` | `ad24a493584834217b760eb3d11b4bc49db3775aacd056e986ad3e7632b667eb` |
| `artifacts/results.json` | `f57fa704d045a8a87d77497e0a18c198fa24585ce754ab043acc11e6d9671bc4` |
| `artifacts/results-sources.json.gz` | `85f8ea0800f0e8b65dbc5bcad226477bd00b9d64b3d80b50909e8c9f0753c5c6` |
| `audit.py` | `daa4b8bf019b09374f5be0d69b43ae235065c905f37ce3316d9d937c7c9b58be` |
| `artifacts/audit-results.json` | `3bcf3cabe5b0330fa48bdc206d2220e4165508937a42cd63cd21ee636d90fa1e` |

The producer internal hash is
`18ce08cfb55e9b1db947c80855e050e2947576aa47cecda26c52e63d7fb11fa0`;
the audit internal hash is
`2fee6ecec9ee8716e3c151dc4cb909bb8580008dcb57f9af91836611166a0b5a`.

The full-source JSON is 4,508,227 bytes before lossless compression and 80,250
bytes after deterministic gzip compression. The archive has zero timestamp
and empty embedded filename. Its raw SHA-256 is
`d70c6ce4d7b331ef305862747ed7d5b1f4d817f2a8213e18f9d95c6ae6f5786e`.
The auditor verifies raw and compressed bytes, hashes, all 18 parameter records,
and every original source label against its independent reconstruction.

## Research and manuscript decision

The uniform twice-source gate for the tracked endpoint class is now closed
positively. The strongest next mathematical gate is nonvanishing: construct a
functional annihilating every original relation and taking a nonzero value on
eta. The local EXP-058 dual does not supply such a functional, because it
annihilates only the declared radius-two columns. Neither the new source nor
its odd coefficients establish nonvanishing. A second independent class and
a full-quotient upper bound remain separate requirements.

This result meets the existing complementary-manuscript trigger in its narrow
all-parameter annihilation sense. Unlike a representative change or another
finite rank table, it supplies a full-cokernel homological consequence across
the S and K source components. The proof also gives a general signed
triangle-interval construction; the classical potential/complement methods
themselves are not claimed as new.

Accordingly, open a focused complementary manuscript candidate combining the
EXP-059 potential connecting maps with the EXP-060 uniform integral
annihilator. Its theorem and title must say annihilation or order dividing
two, not nonzero torsion, the complete parity quotient, or a solved conjecture.
This assessment does not weaken the separate nonvanishing, normal-form,
recurrence, or full-quotient goals. The current curvilinear companion concerns
a different object and is not the appropriate destination for this result.

The manuscript still requires a focused novelty/dependency audit, claim map,
build and rendered QA, and normal Zenodo metadata and fresh-download checks.
No new published manuscript or Zenodo record is asserted by this verdict.

## How could this be wrong?

- The original coefficient presentation remains an imported premise. Several
  agreeing differentials do not independently derive that presentation.
- The uniform claim depends on the written signs, interval boundaries, and
  truncation proof, not on the eighteen numerical instances.
- The auditor independently reconstructs sources and differentials but shares
  the stated original algebra and frozen target definitions.
- A nonzero target vector can represent zero in the full cokernel. Thus even
  a correct `M V=2eta` identity cannot establish order exactly two.
- No retraction or quotient-wide upper bound is constructed. Extending the
  result from the tracked classes to the entire connecting quotient would
  require a separate proof.
