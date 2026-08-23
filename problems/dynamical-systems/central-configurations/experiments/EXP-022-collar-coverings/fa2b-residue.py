"""Re-run ONLY fa2b's residual boxes, at a deeper cap.

Every one of fa2b's failures sits at the shared depth cap of 44: the boxes
all have widths 1/2048, 1/2048, 1/1536, 1/1024, which is 11 + 12 + 10 + 11
halvings of the seed. 188 of 200 touch no face at all, so they are not a
face phenomenon; they tile a curve in the interior at ratio r = 0.9375, a
dyadic value, which is where the chart's grid crosses the locus rather
than a feature of the locus itself.

So the question this run asks is simple: does the residue DISCHARGE under
more bisection, or does it survive and mark something real? Seeding with
the failed boxes and raising the cap answers it without redoing the 1.3
million boxes the chart already certified.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("fa2b", HERE / "fa2b.py")
fa2b = importlib.util.module_from_spec(_s)
_s.loader.exec_module(fa2b)
pl = fa2b.pl

CERT = Path("E:/_Datos/caos-research/central-configurations/EXP-022"
            "/fa2b-certificates.jsonl")


def failed_boxes():
    seen, out = set(), []
    for line in CERT.open(encoding="utf-8"):
        if "FAILED" not in line:
            continue
        b = tuple(tuple(F(x) for x in ax) for ax in json.loads(line)["box"])
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out


def main():
    boxes = failed_boxes()
    print(f"seeding with {len(boxes)} residual boxes", flush=True)
    if not boxes:
        return
    depth = 44 + int(sys.argv[1]) if len(sys.argv) > 1 else 76
    print(f"depth cap {depth}", flush=True)
    pl.run_covering(
        "fa2b-residue", boxes,
        fa2b.entry_factory("iv"), fa2b.entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=fa2b.discard, depth=depth, budget=21600,
        resume="--resume" in sys.argv)


if __name__ == "__main__":
    main()
