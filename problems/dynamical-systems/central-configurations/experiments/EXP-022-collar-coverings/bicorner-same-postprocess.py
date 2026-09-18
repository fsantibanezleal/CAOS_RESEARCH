"""Post-process bicorner-same's 20 failed boxes: locate + trap.

Same flow as band-postprocess.py, in bicorner-same chart coordinates
(rhoa, taua, rr, taub).
"""
import json
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent

def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

pl = _load("pipeline", "pipeline.py")
bs = _load("bs", "bicorner-same.py")

CERTS = Path("E:/_Datos/caos-research/central-configurations/EXP-022/"
             "bicorner-same-certificates.jsonl")

failed = []
for line in open(CERTS, encoding="utf-8"):
    r = json.loads(line)
    if r["by"] == "FAILED":
        failed.append(pl.dec_box(r["box"]))
print(f"{len(failed)} failed boxes")
for b in failed[:20]:
    mid = [float((ax[0] + ax[1]) / 2) for ax in b]
    wid = max(float(ax[1] - ax[0]) for ax in b)
    ra, ta, rr, tb = mid
    print(f"  rhoa={ra:.5f} taua={ta:.5f} rr={rr:.5f} taub={tb:.5f} w={wid:.1e}")

trapped = still = 0
results = []
for b in failed:
    got = pl.trap(bs.entry_factory("iv"), bs.entry_factory("dv"), b)
    if got is not None:
        trapped += 1
        results.append({"box": pl.enc_box(b), "by": got})
    else:
        still += 1
        results.append({"box": pl.enc_box(b), "by": "STILL-FAILED"})
print(f"trapped {trapped}/{len(failed)}, still failed {still}")
(HERE / "artifacts" / "bicorner-same-failed-postprocess.json").write_text(
    json.dumps({"failed": len(failed), "trapped": trapped,
                "still_failed": still, "results": results}, indent=1),
    encoding="utf-8")
