"""Re-run ONLY band's residual boxes, at a deeper cap.

Same measurement as fa2b: all 44 of band's failures share one box width,
the width the seed reaches at the depth cap of 44, so none of them failed
before the cap. This re-seeds band's own loop with just those boxes at
depth 0, which gives them 44 further halvings, and writes to a SEPARATE
artifact so the original band run stays on the record unchanged.
"""
import json
import sys
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("band", HERE / "band.py")
band = importlib.util.module_from_spec(_s)
_s.loader.exec_module(band)

ORIG_CERTS = band.CERTS
band.CKPT = HERE / "artifacts" / "band-residue-checkpoint.json"
band.CERTS = ORIG_CERTS.parent / "band-residue-certificates.jsonl"
band.BUDGET = 21600


def main():
    if not band.CKPT.exists():
        seen, boxes = set(), []
        for line in ORIG_CERTS.open(encoding="utf-8"):
            if "FAILED" not in line:
                continue
            b = json.dumps(json.loads(line)["box"])
            if b in seen:
                continue
            seen.add(b)
            boxes.append(json.loads(b))
        print(f"seeding with {len(boxes)} residual boxes", flush=True)
        band.CKPT.write_text(json.dumps(
            {"stack": [[b, 0] for b in boxes],
             "counters": {"processed": 0, "certified": 0, "mv_certified": 0,
                          "core_discard": 0, "tube_discard": 0,
                          "failed": 0}}), encoding="utf-8")
        band.CERTS.write_text("", encoding="utf-8")
    sys.argv = [sys.argv[0], "--resume"]
    band.main()


if __name__ == "__main__":
    main()
