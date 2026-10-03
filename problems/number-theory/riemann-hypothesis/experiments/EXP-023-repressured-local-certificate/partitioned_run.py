"""Separate changed-pressure certificate; single pilot runs in this process."""

import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import multiprocessing
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"code"))
from partitioned_pressure_replay import prepare, worker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--baseline-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--shard", type=int)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--exp020-complete-receipt", type=Path)
    args = parser.parse_args()
    if not 1 <= args.workers <= 24 or (args.shard is not None and not 0 <= args.shard < 96):
        parser.error("invalid worker or shard count")
    if args.workers > 4:
        if args.exp020_complete_receipt is None:
            parser.error("more than four workers requires complete EXP020 audit")
        receipt = json.loads(args.exp020_complete_receipt.read_bytes())
        if (receipt.get("passed") is not True or receipt.get("experiment") != "EXP-020"
                or len(receipt.get("reports_sha256", {})) != 96):
            parser.error("invalid EXP020 complete-audit resource gate")
    bound = prepare(args.output_dir, args.baseline_dir)
    print(f"prepared pressure={bound['pressure']} target={bound['target']} cells={bound['cells']}", flush=True)
    if args.prepare_only:
        return
    if args.shard is not None:
        result = worker((args.shard, str(args.output_dir), bound))
        print(f"pressure COMPLETE shard={args.shard} nodes={result['report']['nodes']}", flush=True)
        return
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as executor:
        pending = {executor.submit(worker, (s, str(args.output_dir), bound)) for s in range(96)}
        complete = 0
        while pending:
            done, pending = wait(pending, timeout=30, return_when=FIRST_COMPLETED)
            for future in done:
                result = future.result()
                print(f"pressure COMPLETE shard={result['shard']} nodes={result['report']['nodes']}", flush=True)
                complete += 1
            print(f"pressure cover completed={complete}/96 pending={len(pending)}", flush=True)


if __name__ == "__main__":
    main()
