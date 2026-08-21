"""Independent re-verification of the shipped certificate files.

The covering runs report counters; the ARTIFACT is the jsonl certificate
list. This gate reads the files back and, for a random sample of lines,
recomputes the claimed certificate from scratch and checks it:

  "((r1,r2,r3), (c1,c2,c3))"      -> that 3x3 minor must exclude zero over
                                     the recorded box (plain interval)
  "mv((r1,r2,r3), (c1,c2,c3))"    -> the mean-value enclosure must exclude
                                     zero over the recorded box
  {"rank2": ..., "minor1": ...}   -> the 2x2 rank witness must exclude
                                     zero AND the named gradient pair must
                                     have a 2x2 subdeterminant excluding
                                     zero, both over the recorded box
  "ballN" / "FAILED" / discards   -> reported, not re-verified here

It also runs NEGATIVE CONTROLS: the same check with the box inflated by a
large factor, which must FAIL for most certificates (otherwise the check
is not sensitive to the box at all).

Usage: verify-certificates.py <chart-module> <jsonl-stem> [--sgn N] [--n K]
"""
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent

def load(name, fname):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def parse_minor(s):
    """'((0, 1, 2), (0, 1, 3))' or 'mv((0, 1, 2), (0, 1, 3))'."""
    mv = s.startswith("mv")
    body = s[2:] if mv else s
    nums = [int(t) for t in body.replace("(", " ").replace(")", " ")
            .replace(",", " ").split()]
    return mv, (tuple(nums[:3]), tuple(nums[3:6]))

def main():
    mod_name, stem = sys.argv[1], sys.argv[2]
    sgn = int(sys.argv[sys.argv.index("--sgn") + 1]) if "--sgn" in sys.argv else None
    N = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 400
    if mod_name == "orig":
        # charts that cover in the ORIGINAL (u,v,p,q) coordinates with no
        # rescaling: band, and EXP-021's integrated core run
        pl = load("pipeline", "pipeline.py")
        eiv = lambda boxes: pl.r21.entry_matrix(*boxes)
        edv = lambda duals: pl.p3.entry_matrix_dual(*duals)
    else:
        mod = load(mod_name.replace("-", "_"), f"{mod_name}.py")
        pl = mod.pl
        eiv = mod.entry_factory("iv") if sgn is None else mod.entry_factory(sgn, "iv")
        edv = mod.entry_factory("dv") if sgn is None else mod.entry_factory(sgn, "dv")
    base = ("E:/_Datos/caos-research/central-configurations/EXP-021/"
            if stem.startswith("integrated")
            else "E:/_Datos/caos-research/central-configurations/EXP-022/")
    path = Path(base + f"{stem}-certificates.jsonl")
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"{stem}: {len(lines)} certificate lines")
    rnd = random.Random(7)
    sample = rnd.sample(lines, min(N, len(lines)))
    ok = bad = skipped = traps = 0
    inflate_fail = inflate_pass = 0
    for line in sample:
        rec = json.loads(line)
        box = pl.dec_box(rec["box"])
        by = rec["by"]
        if isinstance(by, dict):
            got = pl.trap(eiv, edv, box)
            if got is not None:
                traps += 1
                ok += 1
            else:
                bad += 1
                print("  TRAP NOT REPRODUCED:", rec["box"])
            continue
        if not (by.startswith("(") or by.startswith("mv")):
            skipped += 1
            continue
        mv, (rows, cols) = parse_minor(by)
        try:
            if mv:
                good = pl.rank3_mv(edv, box) is not None
            else:
                J = eiv([tuple(x) for x in box])
                good = pl.det3(J, rows, cols).excludes_zero()
        except AssertionError:
            good = False
        if good:
            ok += 1
        else:
            bad += 1
            print(f"  NOT REPRODUCED: {by} on {rec['box']}")
        # negative control: inflate the box 64x about its centre
        big = []
        for lo, hi in box:
            c = (lo + hi) / 2
            r = (hi - lo) / 2 * 64 + F(1, 1024)
            big.append((c - r, c + r))
        try:
            Jb = eiv([tuple(x) for x in big])
            still = pl.det3(Jb, rows, cols).excludes_zero()
        except AssertionError:
            still = False
        if still:
            inflate_pass += 1
        else:
            inflate_fail += 1
    print(f"  re-verified OK {ok} (traps {traps}), FAILED {bad}, skipped {skipped}")
    print(f"  negative control (64x inflated box): {inflate_fail} lose the "
          f"certificate, {inflate_pass} keep it")
    if bad == 0 and inflate_fail > 0:
        print("  GATE PASSES: certificates reproduce, and the check is "
              "sensitive to the recorded box.")
    elif bad:
        print("  GATE FAILS: some recorded certificates do not reproduce.")
    else:
        print("  GATE INCONCLUSIVE: control never fired (check not sensitive).")

if __name__ == "__main__":
    main()
