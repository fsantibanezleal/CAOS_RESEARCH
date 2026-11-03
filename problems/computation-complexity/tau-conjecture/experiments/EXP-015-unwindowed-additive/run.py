"""EXP-015 production: scan every depth-7 partition with the window-free engine.

Each partition is first hashed and compared with the EXP-011 manifest (SHA-256
and state count); a mismatch stops that partition with an error record. Results:
artifacts/parts/partNNN.json, one per partition, written atomically; a partition
whose record exists is skipped (restartable). The aggregate is artifacts/final.json.

Usage: python run.py <assets dir> [--nproc N] [--k 7] [--parts a b ...]
"""
import argparse
import hashlib
import json
import pickle
import re
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
sys.path.insert(0, str(HERE))
ART = HERE / "artifacts"
MANIFEST = HERE.parent / "EXP-011-depth8-pipeline" / "artifacts" / "frontier7.manifest.md"
BATCH = 256
T0 = time.time()


def manifest():
    rows = {}
    for m in re.finditer(r"\| uniq(\d{3})\.bin \| ([\d,]+) \| ([\d,]+) \| `([0-9a-f]{64})` \|",
                         MANIFEST.read_text(encoding="utf-8")):
        rows[int(m.group(1))] = (int(m.group(3).replace(",", "")), m.group(4))
    return rows


_G = {}


def _init(assets, k):
    from engine import Engine, load_tables
    with open(Path(assets) / "polys.pkl", "rb") as fh:
        polys = pickle.load(fh)["polys"]
    _G["engine"] = Engine(polys, load_tables(Path(assets)), k)
    _G["assets"] = Path(assets)
    _G["manifest"] = manifest()


def worker(part):
    out = ART / "parts" / f"part{part:03d}.json"
    if out.exists():
        return part, "skipped"
    eng = _G["engine"]
    f = _G["assets"] / "frontier7" / f"uniq{part:03d}.bin"
    raw = f.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    want_states, want_sha = _G["manifest"][part]
    arr = np.frombuffer(raw, dtype=np.int32).reshape(-1, 7)
    rec = {"part": part, "sha256": digest, "states_file": int(arr.shape[0])}
    if digest != want_sha or arr.shape[0] != want_states:
        rec["error"] = f"manifest mismatch: want {want_sha} / {want_states} states"
    else:
        before = dict(eng.stats)
        t0 = time.time()
        hits = []
        for s in range(0, arr.shape[0], BATCH):
            hits.extend(eng.scan(arr[s:s + BATCH]))
        rec["stats"] = {key: eng.stats[key] - before[key] for key in eng.stats}
        rec["hits"] = hits[:50]
        rec["seconds"] = round(time.time() - t0, 1)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(rec), encoding="utf-8")
    tmp.replace(out)
    return part, rec.get("error") or f"hits={rec['stats']['hits']} exact={rec['stats']['exact']} {rec['seconds']}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("assets")
    ap.add_argument("--nproc", type=int, default=22)
    ap.add_argument("--k", type=int, default=7)
    ap.add_argument("--parts", type=int, nargs="*")
    a = ap.parse_args()
    parts = a.parts if a.parts else list(range(256))
    done = 0
    with Pool(processes=a.nproc, initializer=_init, initargs=(a.assets, a.k)) as pool:
        for part, msg in pool.imap_unordered(worker, parts):
            done += 1
            print(f"[{time.time()-T0:8.0f}s] part {part:03d} {msg} ({done}/{len(parts)})", flush=True)
    if a.parts:
        return 0
    total = {}
    hits, errors = [], []
    for p in range(256):
        rec = json.loads((ART / "parts" / f"part{p:03d}.json").read_text(encoding="utf-8"))
        if "error" in rec:
            errors.append(p)
            continue
        for key, v in rec["stats"].items():
            total[key] = total.get(key, 0) + v
        hits.extend(rec["hits"])
    final = {"k": a.k, "partitions": 256, "errors": errors, "totals": total, "hits": hits[:50]}
    (ART / "final.json").write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(final, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
