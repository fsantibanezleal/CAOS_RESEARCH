# EXP-061 verdict

Date: 2026-09-05. Status: **CONFIRMED: uniform nonzero order-two class.**

The corrected hypothesis was committed and pushed as `9169f23` before
computation. The all-parameter [proof](proof.md), independent full-source/D-kernel
audit, permanent tests, and independent paper review all pass. The original
coefficient presentation remains an explicit imported premise.

## Exact uniform result

The twelve-row functional has value one on eta, annihilates
every original K-source boundary, and annihilates the K image of every complete
D cycle. Its relative-functional contradiction proves eta
nonzero in the full original cokernel modulo two. Combined with EXP-060, its integral class and the
EXP-057-equivalent class of `b_A+b_B` then have exact order two for every
integer `p>=8`.

The proof includes all reachable high sectors, notably `h=10p-3`, and the
complete generalized-potential kernel with free `f_u(u)` coordinates at
`d=2`. Finite ranks are not its justification for completeness.

P1 is established by exhaustive original K-source classification. P2 follows
from the complete D-kernel reconstruction in every reachable high sector,
including the three large-high exceptions. P3 is the relative-functional
contradiction: a hypothetical original source for eta must have zero D boundary,
and hence pair to zero, contrary to its value one. No global D-row functional
or global matrix basis is required for this argument.

## Independent audit and finite campaign

The producer checks 2,123 potential chains over the 14 declared parameters
`p=8,...,16,25,32,50,64,100`. At `p<=12` it checks every basis coordinate
in every generalized-potential sector, including `d=2` free diagonal
coordinates. Larger cases use the frozen endpoint/midpoint selection. Complete
original K incidence and all specified producer controls pass at `p=8,...,12`.

The separate auditor reconstructs the functional without importing producer
mathematics. At each of `p=8,...,12` it independently enumerates every
incident K source and every original S source in every reachable high sector.
It keeps all original D rows and certifies that the induced K functional lies
in their row span using exact `F_2` elimination. Its retained certificates
therefore apply to the full D kernel, not only to producer potential chains.

| Independent audit quantity | Total |
|---|---:|
| Parameters | 5 |
| Complete high-sector certificates | 65 |
| Original S columns | 23,695 |
| Complete D rows | 108,261 |
| D incidences | 231,986 |
| Labelled D-row dual terms | 1,070 |
| Adverse controls | 20 |

The independently computed full kernel dimensions agree with every producer
potential dimension at all five small parameters, including `d=2`. This
exceeds the declared two-parameter completeness comparison, but the uniform
completeness claim still rests on the written reconstruction proof.

Controls include removing the odd eta-pairing row, a support-index mutation,
the previously omitted `10p-3` sector, and a candidate passing a proper local
subset but failing an added original source. The omitted-sector witness has
nonzero D boundary: it exposes an incomplete sector list, not a refutation of
the complete relative-functional claim.

Both processes finish within the declared 120-second and 1-GiB caps. All 21
new tests and focused Ruff checks pass. The independent audit also reproduces
its complete certificate byte-for-byte in a temporary replay. Tests use
temporary output paths. No dense global ambient matrix, HNF/SNF, or old
`p=11` HNF-source label is used; this is not an untouched-holdout campaign.

## Certificate identity

| File | SHA-256 |
|---|---|
| `run.py` | `767b34ffe8dcd880ece54743bfff400a59f3c91471483afc5a76350d8de60968` |
| `artifacts/results.json` | `0dbff45a4da41912b5d0857f7fea7d3b22b45cfc1ff955f14a008d47a1a1dc7c` |
| `audit.py` | `2808798097a4c257c640e864ad73ffc23981197d4f422ee3e8472c14f7ab3ab5` |
| `artifacts/audit-results.json` | `0d891037c2dd007d3f0cd2c971a4be7529d789c4317307355b711e1afc882b07` |

Producer internal hash:
`14192d0977aad7b876a94f3c8bcb91c93c67b2997ebe65e28023a983548cf2df`.
Independent certificate internal hash:
`42e3014f0c08c65374ec8d9ab95d092ef90dccf28b7f87aa1ed49081d43a80c5`.

After the first result commit, a Git-blob comparison caught Windows CRLF in the
audit receipt while the repository enforces LF. The writer now explicitly emits
LF; a complete rerun reproduces every mathematical certificate and count. The
hashes above identify this portable replay, not the earlier platform-dependent
serialization. No hypothesis, source formula, or proof changed.

## Research and publication boundary

Uniform nonvanishing of the tracked class is now proved, closing the next
gate after EXP-060. The result justifies upgrading the unpublished focused
complementary manuscript from annihilation to one exact order-two class.
Independent paper review found no remaining defect in the complete source,
kernel, endpoint, or exceptional-sector arguments.

A second independent class, a full-quotient upper bound, and a recurrence remain
outside this experiment's claim. A later family generalization requires its own
declared proof and audit; finite earlier isolated ranks are not an identification
of the full original cokernel with any smaller completion quotient. The original
coefficient model is not rederived by these checks. Normal manuscript claim,
build, rendering, metadata, and fresh public-download gates still apply. No
new Zenodo publication is claimed by this verdict.
