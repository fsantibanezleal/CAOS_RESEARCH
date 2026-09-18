# EXP-013 completeness audit of the production scan (threshold 7). CPU only; stdlib only; deterministic.
# Run from the repo root:
#   python problems/computation-complexity/tau-conjecture/experiments/EXP-013-additive-residual/audit.py
#
# Checks, each against an independent record:
#   1. artifacts/parts_final holds exactly part000.json .. part255.json, one per frontier partition;
#   2. every file is well formed (part, states, hit_count, hits, promoted) and names its own partition;
#   3. each partition's scanned state count equals the state count of the frontier file uniqNNN.bin in
#      EXP-011's frontier7 SHA-256 manifest (size / 28-byte rows), so no partition was scanned partially;
#   4. the totals reproduce the manifest's 1,048,460,912 states;
#   5. no partition reports a hit (hit_count == 0 == len(hits));
#   6. partitions 0 and 1 equal the exact regression records of the batched engine (parts_regress).
# Writes artifacts/audit.json; exits 1 if any check fails.
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = HERE / "artifacts" / "parts_final"
MANIFEST = HERE.parent / "EXP-011-depth8-pipeline" / "artifacts" / "frontier7.manifest.md"
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def manifest_states():
    text = MANIFEST.read_text(encoding="utf-8")
    rows = {int(m.group(1)): int(m.group(2).replace(",", ""))
            for m in re.finditer(r"^\| uniq(\d{3})\.bin \| [\d,]+ \| ([\d,]+) \|", text, re.M)}
    total = int(re.search(r"total states: \*\*([\d,]+)\*\*", text).group(1).replace(",", ""))
    return rows, total


def main():
    frontier, frontier_total = manifest_states()
    check("M: the frontier7 manifest lists 256 partitions whose states sum to its stated total",
          sorted(frontier) == list(range(256)) and sum(frontier.values()) == frontier_total,
          f"{len(frontier)} rows, {sum(frontier.values()):,} states")

    names = sorted(p.name for p in PARTS.glob("*.json"))
    expected = [f"part{k:03d}.json" for k in range(256)]
    check("1: exactly part000..part255, no gap, no extra file", names == expected,
          f"{len(names)} files; missing {sorted(set(expected) - set(names))[:5]}; extra {sorted(set(names) - set(expected))[:5]}")

    rows, bad_shape, bad_states, hits, promoted = [], [], [], 0, 0
    for k in range(256):
        f = PARTS / f"part{k:03d}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        if set(d) != {"part", "states", "hit_count", "hits", "promoted"} or d["part"] != k:
            bad_shape.append(k)
            continue
        if d["states"] != frontier.get(k):
            bad_states.append((k, d["states"], frontier.get(k)))
        hits += d["hit_count"] + len(d["hits"])
        promoted += d["promoted"]
        rows.append({"part": k, "states": d["states"], "hit_count": d["hit_count"], "promoted": d["promoted"]})
    check("2: every file is well formed and names its own partition", not bad_shape, f"bad {bad_shape[:5]}")
    check("3: every partition's scanned states equal its frontier file's states (manifest)", not bad_states,
          f"mismatches {bad_states[:3]}")
    scanned = sum(r["states"] for r in rows)
    check("4: the scanned states total the frontier's 1,048,460,912", scanned == frontier_total == 1_048_460_912,
          f"{scanned:,}")
    check("5: no partition reports a hit at threshold 7", hits == 0, f"hits {hits}; promoted {promoted:,}")

    regress = {}
    for f in sorted((HERE / "artifacts" / "parts_regress").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        regress[int(d["part"])] = d
    same = all(regress.get(k, {}).get(key) == next(r for r in rows if r["part"] == k)[key]
               for k in (0, 1) for key in ("states", "hit_count", "promoted"))
    check("6: partitions 0 and 1 equal the batched engine's exact regression records", same and len(regress) == 2)

    out = {"experiment": "EXP-013", "threshold": 7, "window": [-32, 32], "partitions": len(rows),
           "states": scanned, "frontier_total": frontier_total, "hits": hits, "promoted": promoted,
           "promoted_per_partition": {"min": min(r["promoted"] for r in rows), "max": max(r["promoted"] for r in rows)},
           "manifest": MANIFEST.relative_to(HERE.parent.parent).as_posix(), "failures": failures}
    (HERE / "artifacts" / "audit.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n",
                                                   encoding="utf-8", newline="\n")
    print(f"written artifacts/audit.json; {len(failures)} failed check(s)")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
