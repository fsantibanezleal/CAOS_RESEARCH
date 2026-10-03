"""CPU-only exact interval cover for the EXP-020 stronger candidate."""

import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import multiprocessing
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"code"))
from quadratic_replay import prepare, worker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--baseline-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--shard", type=int)
    args = parser.parse_args()
    if not 1 <= args.workers <= 24 or (args.shard is not None and not 0 <= args.shard < 96):
        parser.error("invalid worker or shard count")
    bound = prepare(args.output_dir, args.baseline_dir)
    targets = [args.shard] if args.shard is not None else list(range(96))
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as executor:
        pending = {executor.submit(worker, (s, str(args.output_dir), bound)) for s in targets}
        complete = 0
        while pending:
            done, pending = wait(pending, timeout=30, return_when=FIRST_COMPLETED)
            for future in done:
                result = future.result()
                print(f"quadratic COMPLETE shard={result['shard']} nodes={result['report']['nodes']}", flush=True)
                complete += 1
            print(f"quadratic cover completed={complete}/{len(targets)} pending={len(pending)}", flush=True)
    # Full mathematical disposition requires the separately audited final cover.


if __name__ == "__main__":
    main()
