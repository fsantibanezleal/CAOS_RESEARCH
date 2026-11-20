"""EXP-006: reduce artifacts/results.json to what the repository keeps, and record where the full file is.

The run stores, for every space with rank of mu_3e at most the target, its basis and Hilbert function (13.5 MB). Every
space is rebuilt from its seed (20261120 + index, families A2, B1, B2, B3, C) or from its enumeration index (family
A1), so the repository keeps:
  - every count per chunk (unchanged), the gates, the totals and the predictions;
  - every pure space, with its basis;
  - every space with the pure Hilbert function and another Betti table, with its index, seed and table, without basis;
and drops the per-space records of the other spaces (they stay in the per-chunk histograms).

The full file is copied to <data root>/caos-research/boij-soderberg-realizability/EXP-006/results-full.json first;
its byte count and SHA-256 are written into the reduced file (key "full_results").

Usage, from the repository root:
    python <this file> --data-root <data root>        (or the environment variable CAOS_RESEARCH_DATA)
Writes nothing if the file is already reduced. The summary generated from the reduced file must equal the one
generated from the full file: the script checks it and stops otherwise.
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RESULTS = HERE / "artifacts" / "results.json"
SUMMARY = HERE / "results-summary.md"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--data-root", default=os.environ.get("CAOS_RESEARCH_DATA"))
    args = ap.parse_args(argv)
    if not args.data_root:
        ap.error("give --data-root or set CAOS_RESEARCH_DATA")
    raw = RESULTS.read_bytes()
    res = json.loads(raw.decode("utf-8"))
    if "full_results" in res:
        print("already reduced:", res["full_results"])
        return 0
    import make_summary

    before = SUMMARY.read_text(encoding="utf-8")
    full_dir = Path(args.data_root) / "caos-research" / "boij-soderberg-realizability" / "EXP-006"
    full_dir.mkdir(parents=True, exist_ok=True)
    full = full_dir / "results-full.json"
    full.write_bytes(raw)
    assert full.read_bytes() == raw
    kept = dropped = 0
    for chunk in res["chunks"].values():
        spaces = []
        for sp in chunk["spaces"]:
            if sp.get("pure"):
                spaces.append(sp)
            elif sp.get("pure_hilbert"):
                spaces.append({k: v for k, v in sp.items() if k != "basis"})
            else:
                dropped += 1
                continue
            kept += 1
        chunk["spaces"] = spaces
    res["full_results"] = {"file": "caos-research/boij-soderberg-realizability/EXP-006/results-full.json (under the data root)",
                           "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
                           "space_records_kept": kept, "space_records_dropped": dropped,
                           "rule": "pure spaces with basis; pure Hilbert function with another table without basis; others dropped"}
    tmp = HERE / "artifacts" / "results.reduced.tmp.md"
    make_summary.write_summary(res, tmp)
    after = tmp.read_text(encoding="utf-8")
    tmp.unlink()
    if after != before:
        print("the summary generated from the reduced file differs from results-summary.md: nothing is written")
        return 1
    RESULTS.write_text(json.dumps(res, separators=(",", ":"), ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"reduced: {len(raw)} bytes to {RESULTS.stat().st_size}; kept {kept} space records, dropped {dropped}; full file {full.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
