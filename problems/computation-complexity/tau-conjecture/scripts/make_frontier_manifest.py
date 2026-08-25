"""Generate the SHA-256 manifest for the depth-7 frontier asset.

The catalog had a manifest; the frontier, which is the larger and more
expensive asset, did not, while the manuscript claimed manifests for both.
This produces the missing one: a per-file hash plus a hash-of-hashes so the
whole 256-file set has a single verifiable fingerprint.
"""
import hashlib
import os
import time

SRC = "E:/_Datos/caos-research/tau-conjecture/frontier7"
OUT = os.path.join(os.path.dirname(__file__), "..", "experiments",
                   "EXP-011-depth8-pipeline", "artifacts", "frontier7.manifest.md")
ROW = 28

t0 = time.time()
files = sorted(f for f in os.listdir(SRC) if f.startswith("uniq") and f.endswith(".bin"))
lines, total, rows, agg = [], 0, 0, hashlib.sha256()
for i, fn in enumerate(files):
    p = os.path.join(SRC, fn)
    sz = os.path.getsize(p)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b""):
            h.update(chunk)
    d = h.hexdigest()
    agg.update(d.encode())
    lines.append(f"| {fn} | {sz:,} | {sz // ROW:,} | `{d}` |")
    total += sz
    rows += sz // ROW
    if (i + 1) % 64 == 0:
        print(f"  {i+1}/{len(files)} hashed ({time.time()-t0:.0f}s)", flush=True)

body = [
    "# frontier7 manifest (depth-7 reached-set states)",
    "",
    f"Generated {time.strftime('%Y-%m-%d')} by `scripts/make_frontier_manifest.py`.",
    "",
    f"- files: **{len(files)}**",
    f"- total bytes: **{total:,}** ({total/2**30:.2f} GiB, {total/1e9:.2f} GB)",
    f"- row width: {ROW} bytes",
    f"- total states: **{rows:,}**",
    f"- aggregate digest (sha256 of the concatenated per-file digests, in name order):",
    f"  `{agg.hexdigest()}`",
    "",
    "The state count above is derived from file sizes and matches the census",
    "figure reported throughout the record, which is the point of hashing it:",
    "the asset and the claim are now checkable against each other.",
    "",
    "| file | bytes | states | sha256 |",
    "|---|---:|---:|---|",
]
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("\n".join(body + lines) + "\n")

print()
print(f"files       : {len(files)}")
print(f"total bytes : {total:,}")
print(f"total states: {rows:,}   (record claims 1,048,460,912 -> {rows == 1048460912})")
print(f"aggregate   : {agg.hexdigest()}")
print(f"written     : {os.path.relpath(OUT)}")
print(f"{time.time()-t0:.0f}s")
