"""EXP-146: does the rerun reproduce the certificate? Compares artifacts/slp-plus.json and slp-minus.json with the ones
committed at a baseline commit (default 99ebd728), field by field: node ids, parents, kinds, orders, statuses, splits
(variable, pivot, a, b, root), pivots, formal degrees, member digests (terms, degrees, values at two points), L values,
univariate degrees and orders, final pairs and constants at (p1, r1), and the replay constants at (p2, r2).
Fields that exist only in the new files (the V digests of the final members) are listed, not compared.
Run from the repository root; writes artifacts/rerun-comparison.json and exits 0 only if both certificates are identical.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
REL = HERE.relative_to(Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                                           cwd=HERE).stdout.strip())).as_posix()


def old_file(ref, name):
    r = subprocess.run(["git", "show", f"{ref}:{REL}/artifacts/{name}"], capture_output=True, text=True, cwd=HERE,
                       encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"cannot read {name} at {ref}: {r.stderr[-200:]}")
    return json.loads(r.stdout)


def strip_new(node):
    """Drop fields that exist only in the new records (V digests of the final members, new gate fields)."""
    node = json.loads(json.dumps(node))
    last = node.get("last")
    if last:
        for u in last.get("members", []):
            u.pop("digest", None)
    node.pop("seconds", None)   # wall time is not part of the certificate
    return node


def diff(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{path}/{k}: present in only one file")
            else:
                out += diff(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append(f"{path}: length {len(a)} vs {len(b)}")
        for i, (x, y) in enumerate(zip(a, b)):
            out += diff(x, y, f"{path}[{i}]")
    elif a != b:
        out.append(f"{path}: {a!r} vs {b!r}")
    return out


def main(ref="99ebd728"):
    res = {"baseline_ref": ref, "branches": {}}
    for tag in ("plus", "minus"):
        old, new = old_file(ref, f"slp-{tag}.json"), json.loads((ART / f"slp-{tag}.json").read_text(encoding="utf-8"))
        d = []
        for key in ("prime_tree", "prime_replay", "order", "inputs"):
            d += diff(old[key], new[key], key)
        on = {n["id"]: strip_new(n) for n in old["nodes"]}
        nn = {n["id"]: strip_new(n) for n in new["nodes"]}
        if list(on) != list(nn):
            d.append(f"node ids differ: {list(on)} vs {list(nn)}")
        for nid in on:
            if nid in nn:
                d += diff(on[nid], nn[nid], f"nodes/{nid}")
        d += diff(old["replay"], new["replay"], "replay")
        only_new = [f"{n['id']}/last/members/{u['id']}/digest" for n in new["nodes"] if n.get("last")
                    for u in n["last"]["members"] if "digest" in u]
        consts = {n["id"]: [(q["i"], q["c"]) for q in n["last"]["pairs"]] for n in new["nodes"] if n.get("last")}
        res["branches"][tag] = {"nodes": list(nn), "statuses": {k: v["status"] for k, v in nn.items()},
                                "differences": d, "identical": not d, "fields_only_in_new_files": len(only_new),
                                "final_constants_at_p1": consts,
                                "replay_constants_at_p2": {k: [(c.get("i"), c.get("c")) for c in v["constants"]]
                                                           for k, v in new["replay"].items()}}
    res["identical"] = all(b["identical"] for b in res["branches"].values())
    (ART / "rerun-comparison.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    for tag, b in res["branches"].items():
        print(tag, "identical:", b["identical"], "differences:", len(b["differences"]), b["differences"][:5])
    return 0 if res["identical"] else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:2]))
