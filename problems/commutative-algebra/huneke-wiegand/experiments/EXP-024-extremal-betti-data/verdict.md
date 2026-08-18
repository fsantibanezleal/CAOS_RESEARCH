# EXP-024 - verdict

Run date: 2026-08-18. Backlog HWB-027.

Status: **CONFIRMED**.

## Result

For every `p>=4`, let `C_p=P_p/J_p` be the conductor special fiber, where `P_p` has `10p`
degree-one variables and put `c=10p-1`. The symbolic proof establishes

```text
pd_(P_p)(C_p)=10p-1,
reg_(P_p)(C_p)=4,
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(c,c+2)=10p,
beta_(c,c+4)=1,
beta_(c,j)=0 otherwise,
beta_(c-1,c+3)=8p.
```

The full alternating Betti polynomial is `(1-z)^c h_p(z)`, with
`h_p=(1,10p-1,12p,2p-1,1)`. The canonical module has `10p` minimal generators in degree `-1`
and one in degree `-3`.

This is a genuine partial resolution theorem: it determines the first linear-syzygy count and
the extremal right edge, but does not claim the unresolved interior Betti table.

## Why the verdict is theorem-level

- Auslander--Buchsbaum and Cohen--Macaulayness give the exact projective dimension.
- The degree-four h-polynomial gives presentation-ring regularity four, correcting a stale v0.12
  open-question phrase.
- Hilbert-numerator coefficient extraction and an independent degree-three dimension count give
  the same closed `beta_(2,3)` formula.
- Regular linear reduction preserves the minimal Betti numbers; top Koszul homology identifies
  the complete last row with the already proved Artinian socle.
- Regularity, the vanishing middle socle degree, and the `z^(c+3)` coefficient isolate the
  penultimate extremal entry.
- Dualizing the last free module gives the canonical-module generator degrees.

## Computational evidence

- Mandatory smoke: `p=4`, PASS by both routes.
- Campaign: every `p=4,...,300`, 297/297 PASS.
- Independent audit: all 297 rows rehashed and rebuilt; selected source reconstructions at
  `p=4,5,17,73,151,300`; all twenty EXP-023 campaign first rows cross-checked.
- Adversarial controls: false regularity, false projective dimension, perturbed linear syzygy,
  deleted last-row contribution, perturbed penultimate entry, corrupted premise hash, and a false
  full-table claim are all rejected.

Deterministic aggregates:

```text
campaign = baf6200a442be9476cd083fde753bbdd9e623c06aa2528f3a7f138ee825637eb
audit    = b6035f615f2b2092351b5a42e5a734c72ba4783adf82943ed41b38fe07ef17e2
```

Artifact manifest:

| file | bytes | SHA-256 |
|---|---:|---|
| `smoke-p4.json` | 3,387 | `492f6f8171412efa040e77d887168a098b634d7d4e083052d0a98a41e91563d0` |
| `smoke-p4-checkpoint.json` | 242 | `a4dee7cbf8cf8556e7377727fe15efcad71b5401dacbc197970666023807ff06` |
| `results.json` | 659,539 | `30cefcb20edaeca931f471a781db9f7fb2da5796ed77dce61f6a8dfb609807e9` |
| `checkpoint.json` | 21,558 | `fb7e7dab64f47832f8d065469e9dba815c4439d18b2b05ec68b1be45549ffd3f` |
| `audit.json` | 6,345 | `4f39aa61b11c05c3ab73e58265f988196ffefa602b1512d5d9aefa76aacb20a9` |

## Trust and scope boundary

EXP-024 imports only frozen, hash-verified EXP-021/023 premises. A defect in those mathematical
premises would propagate even though the present arithmetic routes agree. In particular, the
EXP-023 all-parameter component proof retains its disclosed solver/encoding boundary. No finite
campaign proves the theorem, and no claim is made for arbitrary fiber cones or for the full Betti
table of `C_p`.

## Manuscript decision and next path

This theorem directly extends the same conductor special-fiber presentation studied in v0.12.
It is material enough for manuscript v0.13 and a new Zenodo version after claim/build/render QA,
but not for a split manuscript.

The strongest next research route after publication is a separately declared explicit quadratic
or Groebner-basis experiment. A complementary manuscript becomes justified only if that route
produces a standalone uniform basis, substantial interior resolution data, or a primary-
decomposition theorem.

