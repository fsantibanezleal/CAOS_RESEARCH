# EXP-146: archived independent checks and certificate inputs (addendum of 2026-11-16)

## Third-prime recomputation (`third-prime/`)

The adversarial review of 2026-11-15 recomputed leaves of both branch trees at third primes with its own scripts, which do
not import `chaincert.py`: plus branch at p3 = 268435399, r3 = 174414054 (all three leaves: `recompute_plus.py` for t.z.nz and
t.z.z, `recompute_plus_tnz.py` for t.nz); minus branch at p3 = 399999949, r3 = 61040865 (the two leaves below the second
split, `recompute_minus.py`). The review's scratch folder was deleted on 2026-11-16 in a cleanup; the scripts were rebuilt
by replaying their recorded edits, and each rebuilt file has the SHA-256 printed in the review report
(`recompute_plus.py` 98a8e047...5932, `recompute_plus_tnz.py` 3431d049...50c0, `recompute_minus.py` 3855eed2...b081). The
outputs here come from a rerun on 2026-11-16 with the review's commands on the first-record SLPs (99ebd728), and agree with
the review's recorded outputs:

- plus: t.nz 2 of 2 constants nonzero (105243149, 212674548), t.z.nz 3 of 4, t.z.z 6 of 6 (`plus/out-tnz-p3.txt`, `plus/out-p3.txt`);
- minus: t.z.nz 3 of 4, t.z.z 6 of 6 nonzero at p3, constants at p1 equal to the record, 0 problems (`minus/run4.txt`).

Commands, from a folder holding a copy of the experiment files (`exp/` for plus, `src/` for minus) and the data root inputs:

    python -I recompute_plus.py exp/artifacts/slp-plus.json <data root>/jacobian-conjecture/exp142-143-branch-plus/eqs.json 268435399 174414054 t.z.nz t.z.z
    python -I recompute_plus_tnz.py exp/artifacts/slp-plus.json <data root>/jacobian-conjecture/exp142-143-branch-plus/eqs.json 268435399 174414054
    python -I recompute_minus.py src/artifacts/slp-minus.json <data root>/jacobian-conjecture/exp142-143-branch-minus/eqs.json

## Certificate inputs (`../inputs/`)

`eqs-plus.json` and `eqs-minus.json` are the two branch systems of EXP-142 (nine equations each over L), with the SHA-256
G0 checks: bd227b53...849424a and 0a3a3905...aae76e9. They are committed so the certificate reproduces from the repository;
`gates.py` reads them from the data root (`BRANCH`), and G0 regenerates them from EXP-141's `eqs.json` with EXP-142's
`branches.py`. To rerun on a device without that data root, copy them to the paths `gates.py` names.
