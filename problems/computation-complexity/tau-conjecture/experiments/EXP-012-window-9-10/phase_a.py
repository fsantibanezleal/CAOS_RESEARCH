"""EXP-012 phase A: the (6,1) sub-case on stored 8-gate 6-rooter witnesses."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import integer_roots, padd, pmul, psub

INPUTS = [(-1,), (1,), (0, 1)]
src = HERE.parent / "EXP-006-window-89" / "artifacts" / "window.json"
d = json.loads(src.read_text("utf-8"))
hits = d["times_case_hits"]
print(f"stored 8-gate 6-rooter witnesses: {len(hits)}")

found = []
for h in hits:
    state = [tuple(p) for p in h["state"]]
    v, b = tuple(h["v"]), tuple(h["b"])
    f8 = pmul(v, b)
    R8 = set(integer_roots(f8))
    assert len(R8) >= 6
    # operands available for a 9th gate over the depth-8 state
    operands = INPUTS + state + [v, f8]
    for o in operands:
        Ro = set(integer_roots(o)) if o else set()
        outside = Ro - R8
        if outside:
            found.append({"f8": list(f8), "R8": sorted(R8),
                          "operand": list(o), "outside": sorted(outside),
                          "union": sorted(R8 | Ro)})
print(f"operands with a root OUTSIDE R(f8): {len(found)}")
for x in found[:5]:
    print(" ", x)
(HERE / "artifacts").mkdir(exist_ok=True)
(HERE / "artifacts" / "phase_a.json").write_text(
    json.dumps({"witnesses_checked": len(hits), "found": found}, indent=1), "utf-8")
print("PHASE A:", "HIT" if found else "EMPTY (prediction 1 holds on stored data)")
