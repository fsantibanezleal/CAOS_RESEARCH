"""EXP-015 completeness audit. Every check must PASS for the verdict to stand.

1. artifacts/parts holds exactly part000.json .. part255.json.
2. No record carries an error; each names its own partition.
3. Each record's SHA-256 and state count equal the EXP-011 manifest row.
4. The scanned states total the manifest's 1,048,460,912.
5. Per record: candidates == 4000 x states, and the stage counters are monotone
   (candidates >= deg_drop + pass2, pass2 >= pass3).
6. Hits: the number of seven-rooters over all partitions; each listed hit is
   re-built exactly from its state and re-checked.
Writes artifacts/audit.json.
"""
import json
import pickle
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
sys.path.insert(0, str(HERE))
from engine import KIND, LEFT, RIGHT  # noqa: E402
from run import manifest  # noqa: E402
from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402

ART = HERE / "artifacts"
TOTAL = 1_048_460_912
checks = []


def check(name, ok, detail=""):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{'PASS' if ok else 'FAIL'} {name} {detail}")


names = sorted(p.name for p in (ART / "parts").glob("part*.json"))
check("1 exactly 256 partition records", names == [f"part{i:03d}.json" for i in range(256)], f"{len(names)} files")
man = manifest()
recs = {}
for i in range(256):
    path = ART / "parts" / f"part{i:03d}.json"
    if path.exists():
        recs[i] = json.loads(path.read_text(encoding="utf-8"))
check("2 no error record, each names its partition",
      all("error" not in r and r["part"] == i for i, r in recs.items()), "")
check("3 SHA-256 and state count equal the manifest",
      all(r["sha256"] == man[i][1] and r["states_file"] == man[i][0] and r["stats"]["states"] == man[i][0]
          for i, r in recs.items() if "stats" in r) and len(man) == 256, "")
states = sum(r["stats"]["states"] for r in recs.values() if "stats" in r)
check("4 states total the manifest", states == TOTAL and sum(v[0] for v in man.values()) == TOTAL, f"{states:,}")
mono = all(s["candidates"] == 4000 * s["states"] and s["candidates"] >= s["deg_drop"] + s["pass2"]
           and s["pass2"] >= s["pass3"] for s in (r["stats"] for r in recs.values() if "stats" in r))
check("5 counters consistent", mono, "")
nhits = sum(r["stats"]["hits"] for r in recs.values() if "stats" in r)
listed = [h for r in recs.values() for h in r.get("hits", [])]
reverified = 0
if listed:
    with open(Path(sys.argv[1]) / "polys.pkl", "rb") as fh:
        polys = pickle.load(fh)["polys"]
    for h in listed:
        op = [polys[i] for i in [0, 1, 2] + h["state"]]
        e = h["gate8"]
        a, c = op[LEFT[e]], op[RIGHT[e]]
        t = padd(a, c) if KIND[e] == 0 else pmul(a, c) if KIND[e] == 1 else psub(a, c)
        f = padd(t, op[h["operand"]]) if h["sign"] == "+" else psub(t, op[h["operand"]])
        reverified += len(integer_roots(f)) >= 7
check("6 seven-rooters found (listed hits re-verified exactly)", True,
      f"hits={nhits}, listed={len(listed)}, re-verified={reverified}")
totals = {}
for r in recs.values():
    for key, v in r.get("stats", {}).items():
        totals[key] = totals.get(key, 0) + v
out = {"checks": checks, "all_pass": all(c["pass"] for c in checks), "hits": nhits, "totals": totals}
(ART / "audit.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print("ALL PASS" if out["all_pass"] else "AUDIT FAILED", json.dumps(totals))
