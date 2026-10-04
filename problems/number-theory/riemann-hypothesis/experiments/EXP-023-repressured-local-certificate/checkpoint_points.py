"""Declared bounded midpoint diagnostic; never modifies the worker's files."""

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
CODE = HERE.parents[1] / "code"
sys.path.insert(0, str(CODE))
from local_replay import PACKET, encoded  # noqa: E402
from partitioned_pressure_replay import spec  # noqa: E402
from rh019_vendor.kernel import (  # noqa: E402
    kernel_k0,
    squared_kernel_derivatives,
)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(checkpoint, output):
    started = time.monotonic()
    raw = Path(checkpoint).read_bytes()
    wrapper = json.loads(raw)
    data = wrapper["data"]
    if sha(encoded(data)) != wrapper["sha256"]:
        raise ValueError("checkpoint wrapper checksum mismatch")
    binding = data["binding"]
    if (data["schema"] != "exp023-partitioned-checkpoint-v1"
            or data["complete"] or data["shard"] != 0
            or binding["grid"] != 4000 or binding["target"] != "52231/5000000"
            or binding["pressure"] != "1/1250"):
        raise ValueError("unexpected checkpoint domain")
    packet_raw = PACKET.read_bytes()
    if sha(packet_raw) != binding["packet_sha256"]:
        raise ValueError("packet binding mismatch")
    kernel_sha = sha((CODE / "rh019_vendor/kernel.py").read_bytes())
    if kernel_sha != binding["baseline_source"]["code"]["rh019_vendor\\kernel.py"]:
        raise ValueError("frozen kernel binding mismatch")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output / "checkpoint-snapshot.json").write_bytes(raw)
    ctx.prec = 256
    current = spec()
    packet = json.loads(packet_raw)
    pi = arb.pi()
    coefficients = [arb(fmpq(n, packet["window_coefficient_denominator"]))
                    for n in packet["window_coefficient_numerators"]]
    omegas = [arb(2).sqrt()] + [2 * j * pi for j in range(1, 7)]

    def sinc(z):
        return (-z * z / 4).hypgeom_0f1(arb(fmpq(3, 2)))

    k0_native = sum((c * sinc(w / 2) for c, w in zip(coefficients, omegas)), arb(0))
    k0_derivative = kernel_k0(current.kernel)
    if not k0_native > 0 or not (k0_native - k0_derivative).contains(0):
        raise ValueError("normalization disagreement")

    def native_w(x):
        k = sum((c * (sinc(w / 2 - pi * x) + sinc(w / 2 + pi * x)) / 2
                 for c, w in zip(coefficients, omegas)), arb(0))
        return (k / k0_native) ** 2

    points = []
    selected = data["state"]["stack"][-32:]
    for ordinal, (box, depth) in enumerate(selected):
        if time.monotonic() - started >= 60:
            break
        if len(box) != 8 or any(not isinstance(lo, int) or not isinstance(hi, int)
                                or lo < 0 or hi < lo for lo, hi in box):
            raise ValueError("invalid pending box")
        gaps = [fmpq(lo + hi + 1, 8000) for lo, hi in box]
        pressure = arb(current.pressure * sum(gaps, fmpq(0)))
        direct, independent = pressure, pressure
        for (i, j), weight in current.weights.items():
            x = arb(sum(gaps[i:j], fmpq(0)))
            w, _, _ = squared_kernel_derivatives(x, current.kernel, k0_derivative ** 2)
            other = native_w(x)
            if not (w - other).contains(0):
                raise ValueError("kernel point-path disagreement")
            direct += arb(weight) * w
            independent += arb(weight) * other
        if not (direct - independent).contains(0):
            raise ValueError("energy disagreement")
        target = arb(current.target)
        points.append({"ordinal": ordinal, "depth": depth, "box": box,
                       "gaps": [str(x) for x in gaps], "energy_derivative": str(direct),
                       "energy_native": str(independent), "slack_native": str(independent - target),
                       "point_above_target": bool(independent >= target),
                       "candidate_counterexample": bool(independent < target)})
    receipt = {"schema": "exp023-pending-point-diagnostic-v1", "precision_bits": 256,
               "snapshot_sha256": sha(raw), "packet_sha256": sha(packet_raw),
               "script_sha256": sha(Path(__file__).read_bytes()),
               "source_kernel_sha256": kernel_sha,
               "snapshot_nodes": data["state"]["nodes"], "pending_boxes": len(data["state"]["stack"]),
               "inspected_points": len(points), "budget_expired": len(points) < len(selected),
               "elapsed_seconds": time.monotonic() - started, "points": points,
               "counterexample_candidates": sum(p["candidate_counterexample"] for p in points),
               "scope": "Finite exact midpoint diagnostic only; no universal certificate. Shared FLINT/Arb."}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run(args.checkpoint, args.output)
    print(json.dumps({k: v for k, v in result.items() if k != "points"}, indent=2))
