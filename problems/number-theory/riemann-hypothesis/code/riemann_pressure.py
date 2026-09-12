"""Exact two-gap pressure certificates for EXP-003.

The legacy EXP-002 certificate format and verifier are unchanged. This adapter
shares their kernel, Lipschitz energy enclosure, and closed-box subdivision.
Construction checkpoints are candidate proof state; final replay is mandatory.
Replay checkpoints never authorize skipping arithmetic: a resumed replay checks
the prefix again, then continues, within its caller's remaining time budget.
"""

from __future__ import annotations

import hashlib
import json
import time
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from riemann_certificates import ball, c_value, energy_lower, split

SCHEMA = "riemann-triangle-pressure-v1"
CHECKPOINT_SCHEMA = "riemann-pressure-checkpoint-v1"


def exact(value: Fraction | str | int) -> Fraction:
    if isinstance(value, (float, bool)):
        raise ValueError("Parameters must be exact rationals")
    return Fraction(value)


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(value: dict) -> str:
    return hashlib.sha256(json_bytes(value)).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def source_identity() -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
            (Path(__file__), Path(__file__).with_name("riemann_certificates.py"))}


def parameters(theta, pressure, epsilon) -> dict[str, str]:
    theta, pressure, epsilon = map(exact, (theta, pressure, epsilon))
    if not (0 < theta < 1 and pressure > 0 and 0 < epsilon <= Fraction(1, 2)):
        raise ValueError("Invalid pressure certificate parameters")
    cutoff = epsilon / pressure
    if cutoff > 12:
        raise ValueError("Cutoff exceeds declared domain")
    return {"theta": str(theta), "pressure": str(pressure),
            "epsilon": str(epsilon), "cutoff": str(cutoff)}


def pressure_lower(theta: Fraction, pressure: Fraction, box: tuple[Fraction, ...],
                   independent: bool = False) -> arb:
    return energy_lower(theta, box, independent) + ball(pressure * (box[0] + box[2]))


def _counts() -> dict[str, int]:
    return {"nodes": 0, "validated_leaves": 0, "pressure_leaves": 0}


def _root(spec: dict) -> tuple[Fraction, ...]:
    cutoff = exact(spec["cutoff"])
    return (Fraction(0), cutoff, Fraction(0), cutoff)


def _advance(token: str, stack: list, counts: dict) -> tuple[Fraction, ...]:
    if not stack:
        raise ValueError("Trailing partition data")
    box = stack.pop()
    counts["nodes"] += 1
    if token == "B":
        left, right = split(box)
        stack.extend((right, left))
    elif token == "V":
        counts["validated_leaves"] += 1
    elif token == "P":
        counts["pressure_leaves"] += 1
    else:
        raise ValueError("Unknown pressure partition token")
    return box


def _restore(saved: dict, spec: dict, phase: str, evaluator: str,
             deadline: float | None = None) -> tuple[list, list, dict]:
    if saved.get("schema") != CHECKPOINT_SCHEMA or saved.get("phase") != phase:
        raise ValueError("Checkpoint schema or phase differs")
    if saved.get("spec") != spec:
        raise ValueError("Checkpoint parameters differ")
    if saved.get("precision_bits") != ctx.prec or saved.get("evaluator") != evaluator:
        raise ValueError("Checkpoint precision or evaluator differs")
    if saved.get("source_identity") != source_identity():
        raise ValueError("Checkpoint source identity differs")
    tree = saved["tree"]
    if hashlib.sha256(tree.encode()).hexdigest() != saved.get("tree_sha256"):
        raise ValueError("Checkpoint prefix hash mismatch")
    stack, counts = [_root(spec)], _counts()
    for token in tree:
        if deadline is not None and time.monotonic() >= deadline:
            raise TimeoutError("Checkpoint restoration budget exhausted")
        _advance(token, stack, counts)
    expected = [[str(q) for q in box] for box in stack]
    if expected != saved.get("pending") or counts != saved.get("counts"):
        raise ValueError("Checkpoint pending coverage or counts differ")
    return list(tree), stack, counts


def _save(path, spec, phase, evaluator, tree, stack, counts, extra=None) -> None:
    if path is None:
        return
    encoded = "".join(tree)
    write_json(path, {"schema": CHECKPOINT_SCHEMA, "phase": phase, "spec": spec,
        "precision_bits": ctx.prec, "evaluator": evaluator,
        "source_identity": source_identity(), "tree": encoded,
        "tree_sha256": hashlib.sha256(encoded.encode()).hexdigest(),
        "pending": [[str(q) for q in box] for box in stack],
        "counts": counts, **(extra or {})})


def _progress(phase: str, counts: dict, stack: list) -> None:
    print(json.dumps({"event": "progress", "phase": phase, **counts,
                      "pending": len(stack)}), flush=True)


def certify_pressure_triangle(theta, pressure, epsilon, *, budget: float = 600,
        max_nodes: int = 2_000_000, checkpoint: Path | None = None,
        resume: bool = False, progress_every: int = 1000) -> dict:
    start = last_progress = time.monotonic()
    spec = parameters(theta, pressure, epsilon)
    theta, pressure, epsilon = map(exact, (theta, pressure, epsilon))
    if progress_every <= 0 or max_nodes < 0 or budget < 0:
        raise ValueError("Invalid execution limits")
    tree, stack, counts = [], [_root(spec)], _counts()
    if resume:
        if checkpoint is None:
            raise ValueError("Resume requires checkpoint")
        tree, stack, counts = _restore(json.loads(checkpoint.read_text(encoding="utf-8")),
                                      spec, "construction", "native-sinc", start + budget)
    print(json.dumps({"event": "start", "phase": "construction", **spec}), flush=True)

    def save():
        _save(checkpoint, spec, "construction", "native-sinc", tree, stack, counts)

    save()
    while stack:
        if counts["nodes"] >= max_nodes or time.monotonic() - start >= budget:
            save()
            raise TimeoutError("Construction budget reached with unresolved boxes")
        box = stack[-1]
        if pressure * (box[0] + box[2]) >= epsilon:
            token = "P"
        elif pressure_lower(theta, pressure, box) >= ball(epsilon):
            token = "V"
        else:
            token = "B"
        _advance(token, stack, counts)
        tree.append(token)
        if counts["nodes"] % progress_every == 0 or time.monotonic() - last_progress >= 10:
            _progress("construction", counts, stack)
            save()
            last_progress = time.monotonic()
    save()
    encoded = "".join(tree)
    return {"schema": SCHEMA, "inequality": "E3(theta,u,v)+pressure*(u+v)>=epsilon",
        "domain": "u>=0,v>=0; outside cutoff square covered by pressure",
        "arithmetic": "python-flint==0.9.0", "precision_bits": ctx.prec,
        **spec, **counts, "unresolved_boxes": 0, "tree": encoded,
        "tree_sha256": hashlib.sha256(encoded.encode()).hexdigest()}


def verify_pressure_triangle(certificate: dict, *, independent: bool = True,
        budget: float = 600, checkpoint: Path | None = None, resume: bool = False,
        progress_every: int = 1000, max_nodes: int = 2_000_000) -> dict:
    start = last_progress = time.monotonic()
    if certificate.get("schema") != SCHEMA:
        raise ValueError("Wrong pressure certificate schema")
    spec = parameters(certificate["theta"], certificate["pressure"], certificate["epsilon"])
    if certificate.get("cutoff") != spec["cutoff"]:
        raise ValueError("Certificate cutoff differs from epsilon/pressure")
    tree = certificate["tree"]
    if len(tree) > max_nodes:
        raise ValueError("Partition exceeds declared node cap")
    if hashlib.sha256(tree.encode()).hexdigest() != certificate.get("tree_sha256"):
        raise ValueError("Partition hash mismatch")
    if progress_every <= 0 or budget < 0:
        raise ValueError("Invalid replay execution limits")
    evaluator = "sinc-taylor-96" if independent else "native-sinc"
    certificate_sha256 = digest(certificate)
    if resume:
        if checkpoint is None:
            raise ValueError("Resume requires checkpoint")
        saved = json.loads(checkpoint.read_text(encoding="utf-8"))
        prefix, _, _ = _restore(saved, spec, "replay", evaluator, start + budget)
        if saved.get("certificate_sha256") != certificate_sha256 or not tree.startswith("".join(prefix)):
            raise ValueError("Replay checkpoint certificate differs")
        print(json.dumps({"event": "resume", "prefix_nodes_to_recheck": len(prefix)}), flush=True)
    theta, pressure, epsilon = (exact(spec[k]) for k in ("theta", "pressure", "epsilon"))
    stack, counts, checked = [_root(spec)], _counts(), []

    def save():
        _save(checkpoint, spec, "replay", evaluator, checked, stack, counts,
              {"certificate_sha256": certificate_sha256})

    print(json.dumps({"event": "start", "phase": "replay", "evaluator": evaluator}), flush=True)
    save()
    for token in tree:
        if time.monotonic() - start >= budget:
            save()
            raise TimeoutError("Replay budget reached with unchecked partition nodes")
        if not stack:
            raise ValueError("Trailing partition data")
        box = stack[-1]
        if token == "P" and pressure * (box[0] + box[2]) < epsilon:
            raise ValueError("Invalid pressure-only leaf")
        if token == "V" and not pressure_lower(theta, pressure, box, independent) >= ball(epsilon):
            raise ValueError(f"Uncertified pressure-energy box {box}")
        _advance(token, stack, counts)
        checked.append(token)
        if counts["nodes"] % progress_every == 0 or time.monotonic() - last_progress >= 10:
            _progress("replay", counts, stack)
            save()
            last_progress = time.monotonic()
    save()
    if stack or certificate.get("unresolved_boxes") != 0:
        raise ValueError("Incomplete pressure partition")
    if any(certificate.get(key) != value for key, value in counts.items()):
        raise ValueError("Partition count mismatch")
    return {"verified": True, "independent_sinc_taylor": independent,
            "precision_bits": ctx.prec, "certificate_sha256": certificate_sha256, **counts}


def frame_coefficients(epsilon, pressure, k: int) -> tuple[Fraction, Fraction]:
    epsilon, pressure = map(exact, (epsilon, pressure))
    if isinstance(k, bool) or not isinstance(k, int) or k < 1 or epsilon <= 0 or pressure <= 0 or k * epsilon > 1:
        raise ValueError("Invalid odd-frame parameters or unit cap")
    size = 2 * k + 1
    return k * epsilon / size, 2 * k * pressure / size


def pressure_frame_bound(theta, pressure, epsilon, k: int) -> arb:
    alpha, beta = frame_coefficients(epsilon, pressure, k)
    return (c_value(exact(theta)) - ball(beta)) / ball(1 - alpha)


def gain_comparison(theta, pressure, epsilon, k: int) -> arb:
    """Positive iff candidate gain is strictly >5/4 of the declared Stage A gain."""
    alpha, beta = frame_coefficients(epsilon, pressure, k)
    old_d, old_radius = Fraction(1, 7000), Fraction(21, 4)
    reference = Fraction(5, 4) * old_d / 2
    slope = alpha / (1 - alpha) - reference
    intercept = -beta / (1 - alpha) + reference * 2 / old_radius
    return ball(slope) * c_value(exact(theta)) + ball(intercept)
