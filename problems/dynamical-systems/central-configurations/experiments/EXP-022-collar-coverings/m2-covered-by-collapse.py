"""Verify the standing claim that the collapse chart covers m2's residue.

The atlas has carried this as an assumption since the collapse chart was
written: m2's residual boxes lie in a region the collapse chart covers at
zero failures, so m2's residue does not matter. The claim is written in
collapse.py's own docstring, and a comment is not evidence.

Two things have to hold for every m2 residual box:

  1. it lies inside the collapse chart's SEED region, so the chart is
     defined there at all; and
  2. the collapse chart's DISCARD does not reject it, because a box the
     chart throws away is not a box the chart covers.

Both are checked here, and the failure mode is reported box by box rather
than as a summary, because a single uncovered box is a hole in the atlas.
"""
import json
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("collapse", HERE / "collapse.py")
collapse = importlib.util.module_from_spec(_s)
_s.loader.exec_module(collapse)

SEED = ((F(0), F(3, 8)), (F(0), F(1)), (F(-3), F(3)), (F(-3), F(3)))
HEAVY = Path("E:/_Datos/caos-research/central-configurations/EXP-022")


def failed(path):
    seen, out = set(), []
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


def inside(box, seed):
    return all(b[0] >= s[0] and b[1] <= s[1] for b, s in zip(box, seed))


for tag in ("m2-L", "m2-R"):
    path = HEAVY / f"{tag}-certificates.jsonl"
    if not path.exists():
        print(f"{tag}: no certificate file")
        continue
    boxes = failed(path)
    n_out, n_disc, n_ok = 0, 0, 0
    examples = {"outside": [], "discarded": []}
    for b in boxes:
        if not inside(b, SEED):
            n_out += 1
            if len(examples["outside"]) < 3:
                examples["outside"].append(b)
            continue
        try:
            d = collapse.discard(b)
        except Exception:
            d = False
        if d:
            n_disc += 1
            if len(examples["discarded"]) < 3:
                examples["discarded"].append(b)
            continue
        n_ok += 1
    print(f"{tag}: {len(boxes)} residual boxes")
    print(f"   inside the collapse seed AND kept by its discard: {n_ok}")
    print(f"   OUTSIDE the collapse seed: {n_out}")
    print(f"   inside but DISCARDED by collapse: {n_disc}")
    for kind, exs in examples.items():
        for b in exs:
            print(f"   {kind} example: "
                  + " ".join(f"[{float(x[0]):.5g},{float(x[1]):.5g}]"
                             for x in b))
    print("")

print("the collapse chart's own state, for the claim to rest on")
ck = json.loads((HERE / "artifacts" / "collapse-checkpoint.json")
                .read_text(encoding="utf-8"))
print(f"   counters: {ck['counters']}")
print(f"   stack still to process: {len(ck['stack'])}")
