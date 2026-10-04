"""Declared conditional nine-point transfer, 30-second CPU budget."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
CODE=HERE.parents[1]/"code"
sys.path.insert(0,str(CODE))


def main():
    from nine_point_distinct import certificate

    parser=argparse.ArgumentParser()
    parser.add_argument("--output-dir",type=Path,required=True)
    args=parser.parse_args()
    started=time.monotonic()
    data=certificate()
    paths=[HERE/"hypothesis.md",HERE/"proof.md",HERE/"run.py",CODE/"nine_point_distinct.py",
           CODE/"energy_envelope.py",CODE/"mixed_gram_parameters.py",HERE/"artifacts/input/nine-point-final.json",
           HERE/"artifacts/input/LICENSE",HERE.parents[1]/"context/source-manifest-exp018.json"]
    data["bindings"]={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    if time.monotonic()-started>30:
        raise TimeoutError("budget exceeded; inconclusive")
    raw=(json.dumps(data,indent=2,sort_keys=True)+"\n").encode()
    args.output_dir.mkdir(parents=True,exist_ok=True)
    (args.output_dir/"result.json").write_bytes(raw)
    print("EXP-018 passed conditional arithmetic: "+hashlib.sha256(raw).hexdigest(),flush=True)
    print(json.dumps(data["candidate"]["q_enclosure"]),flush=True)


if __name__=="__main__":
    main()
