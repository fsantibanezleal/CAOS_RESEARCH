"""Generic failed-box post-processor: locate + trap.

Usage: postprocess.py <chart-module> <jsonl-name> [entry-args...]
  chart-module: python file providing entry_factory (mode) or
                entry_factory(sgn/hemi, mode) via --sgn N
Examples:
  postprocess.py cb1 cb1
  postprocess.py deep deep-R --sgn 1
"""
import json
import sys
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

def main():
    mod_name = sys.argv[1]
    jsonl = sys.argv[2]
    sgn = None
    if "--sgn" in sys.argv:
        sgn = int(sys.argv[sys.argv.index("--sgn") + 1])
    mod = _load(mod_name.replace("-", "_"), f"{mod_name}.py")
    # use the CHART's own pipeline instance (same IV/DV classes)
    global pl
    pl = mod.pl
    if sgn is None:
        eiv = mod.entry_factory("iv")
        edv = mod.entry_factory("dv")
    else:
        eiv = mod.entry_factory(sgn, "iv")
        edv = mod.entry_factory(sgn, "dv")
    certs = Path(f"E:/_Datos/caos-research/central-configurations/EXP-022/"
                 f"{jsonl}-certificates.jsonl")
    failed = []
    for line in open(certs, encoding="utf-8"):
        r = json.loads(line)
        if r["by"] == "FAILED":
            failed.append(pl.dec_box(r["box"]))
    print(f"{len(failed)} failed boxes")
    for b in failed[:12]:
        mid = [float((ax[0] + ax[1]) / 2) for ax in b]
        wid = max(float(ax[1] - ax[0]) for ax in b)
        print("  mid", [f"{x:.5f}" for x in mid], f"w={wid:.1e}")
    trapped = still = 0
    results = []
    for b in failed:
        got = pl.trap(eiv, edv, b)
        if got is not None:
            trapped += 1
            results.append({"box": pl.enc_box(b), "by": got})
        else:
            still += 1
            results.append({"box": pl.enc_box(b), "by": "STILL-FAILED"})
    print(f"trapped {trapped}/{len(failed)}, still failed {still}")
    (HERE / "artifacts" / f"{jsonl}-failed-postprocess.json").write_text(
        json.dumps({"failed": len(failed), "trapped": trapped,
                    "still_failed": still, "results": results}, indent=1),
        encoding="utf-8")

if __name__ == "__main__":
    main()
