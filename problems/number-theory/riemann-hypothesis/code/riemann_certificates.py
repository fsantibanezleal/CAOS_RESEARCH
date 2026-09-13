"""CPU-only Arb certificates for the declared Riemann experiments.

All geometric endpoints and thresholds are rational. Floating point is used only
for elapsed-time budgets; it never makes a mathematical acceptance decision.
"""

from __future__ import annotations

import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx


def ball(q: Fraction | str | int) -> arb:
    q = Fraction(q)
    return arb(q.numerator) / q.denominator


def bracket(x: arb) -> dict[str, str]:
    if not x.is_finite():
        raise ValueError("Nonfinite interval")
    return {"lower": str(x.lower().fmpq()), "upper": str(x.upper().fmpq()),
            "display": x.str(45)}


def c_value(theta: Fraction | str) -> arb:
    t = ball(theta)
    a = t / arb(2).sqrt()
    return 2 - t / 2 - a.cos() / (arb(2).sqrt() * a.sin())


def sinc_series(x: arb, terms: int = 96) -> arb:
    """Independent entire-sinc Taylor evaluation with a real Taylor remainder."""
    term = arb(1)
    total = term
    for j in range(1, terms):
        term = -term * x * x / ((2 * j) * (2 * j + 1))
        total += term
    maximum = max(abs(x.lower()), abs(x.upper()))
    remainder = maximum ** (2 * terms) / arb.fac_ui(2 * terms + 1)
    return total + arb(0, remainder.upper())


def kernel(theta: Fraction, x: Fraction, independent: bool = False) -> arb:
    t = ball(theta)
    a = t / arb(2).sqrt()
    X = arb.pi() * t * ball(x)
    sinc = sinc_series if independent else lambda y: y.sinc()
    return (sinc(X - a) + sinc(X + a)) / (2 * sinc(a))


def energy_lower(theta: Fraction, box: tuple[Fraction, ...], independent: bool = False) -> arb:
    """Lipschitz bounds: |k'| <= pi*theta because f is a probability density."""
    u0, u1, v0, v1 = box
    pairs = ((u0, u1), (v0, v1), (u0 + v0, u1 + v1))
    result = arb(0)
    lip = arb.pi() * ball(theta)
    for lo, hi in pairs:
        center, radius = (lo + hi) / 2, (hi - lo) / 2
        value = kernel(theta, center, independent)
        lower = abs(value).lower() - lip * ball(radius)
        if lower > 0:
            result += 2 * lower * lower
    return result


def split(box: tuple[Fraction, ...]) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    u0, u1, v0, v1 = box
    if u1 - u0 >= v1 - v0:
        mid = (u0 + u1) / 2
        return (u0, mid, v0, v1), (mid, u1, v0, v1)
    mid = (v0 + v1) / 2
    return (u0, u1, v0, mid), (u0, u1, mid, v1)


def certify_triangle(theta: Fraction, radius: Fraction, threshold: Fraction, *,
                     budget: float = 600, max_nodes: int = 2_000_000,
                     checkpoint: Path | None = None, resume: bool = False,
                     progress_every: int = 1000) -> dict:
    """Preorder B/E/O partition: branch, accepted energy box, outside triangle.

    Checkpoints contain the exact pending boxes and completed preorder prefix.
    A budget termination raises; no certificate is returned with pending boxes.
    """
    if not (0 < theta < 1 and radius > 0 and 0 < threshold <= 1):
        raise ValueError("Invalid domain or threshold")
    spec = {"theta": str(theta), "radius": str(radius), "threshold": str(threshold)}
    stack = [(Fraction(0), radius, Fraction(0), radius)]
    tree: list[str] = []
    counts = {"nodes": 0, "energy_leaves": 0, "outside_leaves": 0}
    if resume:
        if checkpoint is None:
            raise ValueError("Resume needs a checkpoint")
        saved = json.loads(checkpoint.read_text())
        if saved["spec"] != spec:
            raise ValueError("Checkpoint parameters differ")
        stack = [tuple(map(Fraction, b)) for b in saved["pending"]]
        tree, counts = list(saved["tree"]), saved["counts"]
    start = time.monotonic()

    def save() -> None:
        if checkpoint is not None:
            checkpoint.parent.mkdir(parents=True, exist_ok=True)
            checkpoint.write_text(json.dumps({"spec": spec, "tree": "".join(tree),
                "pending": [[str(q) for q in b] for b in stack], "counts": counts}, indent=2) + "\n",
                encoding="utf-8", newline="\n")

    print(json.dumps({"event": "start", **spec, "pending": len(stack)}), flush=True)
    save()
    while stack:
        if counts["nodes"] >= max_nodes or time.monotonic() - start > budget:
            save()
            raise TimeoutError("Budget reached with unresolved boxes; checkpoint saved")
        box = stack.pop()
        counts["nodes"] += 1
        if box[0] + box[2] > radius:
            tree.append("O")
            counts["outside_leaves"] += 1
        elif energy_lower(theta, box) >= ball(threshold):
            tree.append("E")
            counts["energy_leaves"] += 1
        else:
            tree.append("B")
            left, right = split(box)
            stack.extend((right, left))
        if counts["nodes"] % progress_every == 0:
            print(json.dumps({"event": "progress", **counts, "pending": len(stack)}), flush=True)
            save()
    save()
    encoded = "".join(tree)
    return {"schema": "riemann-triangle-v1", "arithmetic": "python-flint==0.9.0",
            "precision_bits": ctx.prec, **spec, **counts, "unresolved_boxes": 0,
            "tree": encoded, "tree_sha256": hashlib.sha256(encoded.encode()).hexdigest()}


def verify_triangle(certificate: dict, *, independent: bool = True) -> dict:
    """Reconstruct the complete partition and re-evaluate every accepted box."""
    theta = Fraction(certificate["theta"])
    radius = Fraction(certificate["radius"])
    threshold = Fraction(certificate["threshold"])
    if not (0 < theta < 1 and radius > 0 and 0 < threshold <= 1):
        raise ValueError("Invalid certificate parameters")
    tree = certificate["tree"]
    if hashlib.sha256(tree.encode()).hexdigest() != certificate["tree_sha256"]:
        raise ValueError("Partition hash mismatch")
    stack = [(Fraction(0), radius, Fraction(0), radius)]
    counts = {"nodes": 0, "energy_leaves": 0, "outside_leaves": 0}
    for token in tree:
        if not stack:
            raise ValueError("Trailing partition data")
        box = stack.pop()
        counts["nodes"] += 1
        if token == "B":
            left, right = split(box)
            stack.extend((right, left))
        elif token == "O":
            if box[0] + box[2] <= radius:
                raise ValueError("Discarded box intersects the domain")
            counts["outside_leaves"] += 1
        elif token == "E":
            if not energy_lower(theta, box, independent) >= ball(threshold):
                raise ValueError(f"Uncertified energy box {box}")
            counts["energy_leaves"] += 1
        else:
            raise ValueError("Unknown partition token")
    if stack or certificate.get("unresolved_boxes") != 0:
        raise ValueError("Incomplete partition")
    if any(certificate.get(k) != v for k, v in counts.items()):
        raise ValueError("Partition count mismatch")
    return {"verified": True, "independent_sinc_taylor": independent,
            "precision_bits": ctx.prec, **counts}


def improved_bound(theta: Fraction, radius: Fraction, delta: Fraction) -> arb:
    if not (0 < delta < 3 and radius > 0):
        raise ValueError("Invalid stability parameters")
    return (3 * c_value(theta) - 2 * ball(delta) / ball(radius)) / (3 - ball(delta))
