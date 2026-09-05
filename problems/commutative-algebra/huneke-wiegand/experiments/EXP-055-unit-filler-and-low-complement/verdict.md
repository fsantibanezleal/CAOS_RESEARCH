# EXP-055 verdict

Status: **P1 PROVED FOR THE UNIFORM FILLER; P2 CONFIRMED FINITELY; P3 PASSED**.

The explicit column `c_p=[K,(L_p minus {2,3p}) union {7p};6p]` satisfies `M_pc_p=-e_p`
for every `p>=4` by the interval and sign argument in [proof.md](proof.md). Exact regressions
pass for all 97 parameters `p=4,...,100`.

Adding `2(-1)^p c_p` repairs each full EXP-053 source at `p=8,9,10`, without changing its
mod-two cycle. Their corrected supports are `126,179,239`. The independent checker passes
456 checks plus 1,793 exterior-complement sign identities and their negative controls.

The fixed-high S slice has only `7,8,9` terms, all even, and exactly the desired D boundary.
Its equally small K boundary is retained explicitly. This is the useful new research direction:
divide this slice by two and work with three missing low indices, not 78 HNF skeletons.

## How could this be wrong?

The uniform filler is only one cancelled coordinate; it is not a generic formula for the
entire source. The fixed-high slice is a finite observation here; EXP-056 owns its later formula
and proof. A nonzero K boundary must not be silently discarded. No all-parameter torsion order,
nontriviality, second class, or upper bound has been established. The elementary filler does not
meet the stronger manuscript-split trigger, and no Zenodo publication is claimed.
