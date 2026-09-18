"""Re-run ONLY m2's residual boxes, at a deeper cap.

m2's residue is the last open region of the (2,2) atlas. Three things are
already known about it:

  * it is at the shared depth cap of 44 (every failing box has the same
    width), so nothing failed BEFORE the cap;
  * it cannot be closed in the original coordinates, because m2's blow-up
    maps a tiny chart box to a 1.2e-3-wide original box straddling u = 0,
    where the matrix is not evaluable. That is precisely why the blow-up
    chart exists;
  * m2's own loop already tries pipeline's trap and it does not fire.

So the only untried lever is depth, and it is the lever that fully
discharged fa2b's residue (1544 boxes, zero failures at 76). Re-seeding
with just the failing boxes makes that affordable: tens of thousands of
boxes instead of the region's full covering.

Writes to a separate artifact so the original m2 runs stay on the record.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("m2", HERE / "m2chart.py")
m2 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(m2)
pl = m2.pl

HEAVY = "E:/_Datos/caos-research/central-configurations/EXP-022"


def failed_boxes(tag):
    path = Path(HEAVY) / f"{tag}-certificates.jsonl"
    seen, out = set(), []
    if not path.exists():
        return out
    for line in path.open(encoding="utf-8"):
        if "FAILED" not in line:
            continue
        raw = json.loads(line)["box"]
        k = json.dumps(raw)
        if k in seen:
            continue
        seen.add(k)
        out.append(tuple(tuple(F(x) for x in ax) for ax in raw))
    return out


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "R"
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 84
    sgn = 1 if which == "R" else -1
    tag = f"m2-{which}"
    boxes = failed_boxes(tag)
    print(f"{tag}: seeding with {len(boxes)} residual boxes, depth cap "
          f"{depth}", flush=True)
    if not boxes:
        return
    pl.run_covering(
        f"{tag}-residue", boxes,
        m2.entry_factory(sgn, "iv"), m2.entry_factory(sgn, "dv"),
        HERE / "artifacts", HEAVY,
        discard=m2.make_discard(sgn), depth=depth, budget=28800,
        resume="--resume" in sys.argv)


if __name__ == "__main__":
    main()
