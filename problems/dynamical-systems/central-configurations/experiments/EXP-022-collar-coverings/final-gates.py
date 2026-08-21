"""Run every verification gate in sequence and print one verdict block.

The four gates, each of which has already caught a real defect:

  1. SEAM      atlas-audit.py       is any stratum point claimed by no chart?
                                    (with negative controls: dropping a chart
                                    must open a gap)
  2. FACE-RANK face-rank-gate.py    does each chart keep rank >= 3 ON its face,
                                    or is it one of the three closed by a lemma?
  3. ARTIFACT  verify-certificates  do the SHIPPED certificates recompute,
                                    and does inflating the box lose them?
  4. RESIDUE   residue-audit.py     does every uncertified box touch a
                                    collision, which the stratum excludes?

Run this before declaring the chain complete. It is deliberately slow.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable

CHARTS = [
    ("cb1", "cb1", None), ("cb1f", "cb1f", None), ("fa1", "fa1", None),
    ("bicorner-opp", "bicorner-opp", None), ("ulow", "ulow", None),
    ("uplow", "uplow", None), ("fa2b", "fa2b", None),
    ("tube", "tube-R", "1"), ("tube", "tube-L", "-1"),
    ("tube", "tubeext-R", "1"), ("tube", "tubeext-L", "-1"),
    ("orig", "band", None), ("orig", "integrated", None),
    ("m1chart", "m1", None), ("bicorner-same", "bicorner-same", None),
    ("fartube", "fartube", None), ("collapse", "collapse", None),
    ("deep", "deep-R", "1"), ("deep", "deep-L", "-1"),
    ("m2chart", "m2-R", "1"), ("m2chart", "m2-L", "-1"),
]

def run(cmd, label):
    print(f"\n{'=' * 70}\n{label}\n{'=' * 70}", flush=True)
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    print(out[-4000:], flush=True)
    return out

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else "all"
    if only in ("all", "seam"):
        run([PY, "atlas-audit.py"], "GATE 1: SEAM (with negative controls)")
    if only in ("all", "face"):
        run([PY, "face-rank-gate.py"], "GATE 2: FACE RANK")
    if only in ("all", "artifact"):
        print(f"\n{'=' * 70}\nGATE 3: ARTIFACT (recompute shipped certificates)"
              f"\n{'=' * 70}", flush=True)
        for mod, stem, sgn in CHARTS:
            cert = Path("E:/_Datos/caos-research/central-configurations")
            p1 = cert / "EXP-022" / f"{stem}-certificates.jsonl"
            p2 = cert / "EXP-021" / f"{stem}-certificates.jsonl"
            if not p1.exists() and not p2.exists():
                continue
            cmd = [PY, "verify-certificates.py", mod, stem, "--n", "120"]
            if sgn:
                cmd += ["--sgn", sgn]
            r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
            tail = [l for l in (r.stdout or "").splitlines()
                    if "GATE" in l or "re-verified" in l or "control" in l]
            print(f"  {stem:16s} " + " | ".join(t.strip() for t in tail[-3:]),
                  flush=True)
    if only in ("all", "residue"):
        stems = [s for _, s, _ in CHARTS]
        run([PY, "residue-audit.py"] + stems, "GATE 4: RESIDUE")

if __name__ == "__main__":
    main()
