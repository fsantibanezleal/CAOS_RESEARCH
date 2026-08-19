"""Post-process the band's 44 failed boxes.

1. Locate them (midpoints, extents, f and u-p values): do they cluster?
2. Attempt the trap certificate (rank-2 witness + gradient pair) on each,
   using the ORIGINAL entry matrix: a trapped box contributes at most a
   2-dim piece to R_2 and nothing to R_1, same ladder value as certified.
3. Anything neither certified nor trapped stays FAILED and is investigated
   as a potential rank-degeneracy discovery.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)

CERTS = Path("E:/_Datos/caos-research/central-configurations/EXP-022/band-certificates.jsonl")

failed = []
for line in open(CERTS, encoding="utf-8"):
    r = json.loads(line)
    if r["by"] == "FAILED":
        failed.append(pl.dec_box(r["box"]))
print(f"{len(failed)} failed boxes")

for b in failed[:8]:
    mid = [float((ax[0] + ax[1]) / 2) for ax in b]
    wid = max(float(ax[1] - ax[0]) for ax in b)
    u, v, p, q = mid
    print(f"  mid u={u:.6f} v={v:.6f} p={p:.6f} q={q:.6f} "
          f"f={v-q:.6f} u-p={u-p:.6f} width={wid:.2e}")

# cluster summary
us = sorted(float((b[0][0] + b[0][1]) / 2) for b in failed)
vs = sorted(float((b[1][0] + b[1][1]) / 2) for b in failed)
ps = sorted(float((b[2][0] + b[2][1]) / 2) for b in failed)
qs = sorted(float((b[3][0] + b[3][1]) / 2) for b in failed)
print(f"u range [{us[0]:.4f},{us[-1]:.4f}] v [{vs[0]:.4f},{vs[-1]:.4f}] "
      f"p [{ps[0]:.4f},{ps[-1]:.4f}] q [{qs[0]:.4f},{qs[-1]:.4f}]")

def entry_iv(boxes):
    return pl.r21.entry_matrix(*boxes)

def entry_dv(duals):
    return pl.p3.entry_matrix_dual(*duals)

trapped = still = 0
results = []
for b in failed:
    got = pl.trap(entry_iv, entry_dv, b)
    if got is not None:
        trapped += 1
        results.append({"box": pl.enc_box(b), "by": got})
    else:
        still += 1
        results.append({"box": pl.enc_box(b), "by": "STILL-FAILED"})
print(f"trapped {trapped}/{len(failed)}, still failed {still}")
(HERE / "artifacts" / "band-failed-postprocess.json").write_text(
    json.dumps({"failed": len(failed), "trapped": trapped,
                "still_failed": still, "results": results}, indent=1),
    encoding="utf-8")
