"""EXP-011 canonical certificate: a barrier for linear refinements of the Hilbert-parity product.

Device: CPU. Deterministic Arb ball arithmetic (python-flint), 128 bits.

Stages:
  1. bind the declaration, the frozen file and this runner by SHA-256;
  2. Prediction A: certified Q(C1) - (2N + 3O - 4S) for the six-triple configuration;
  3. Prediction B: certified (Q(C2) - 2N)/O for the 10001-cell lattice, through the exact
     translation-invariant formula Q = sum_{a,b} m_a m_b sum_{|d|<=2M} (2M+1-|d|) K(x_a - x_b + d s)^2;
  4. Prediction C: h_beta(0.532) = (2 + beta kappa - (2 - c(0.532)))/4 < 0 for beta = 2.365 and the
     EXP-010 frozen detectors nu = 0.0199, 0.0299 (their canonical enclosures);
  5. Control D: the EXP-006 product on C1 and C2, and the formula against the direct double sum at M = 50;
  6. write the canonical result, receipt and log.

Kernel (Montgomery-Taylor window, K(0) = 1):
  K(xi) = [a sinc((b-c)a) + a sinc((b+c)a)] / (2 sin(ab)/b),  a = 1/2, b = sqrt2, c = 2 pi xi.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

from flint import acb, arb, ctx

PREC_BITS = 128
MAX_SECONDS = 900.0
HERE = Path(__file__).resolve().parent
FROZEN = HERE / "frozen-parameters.json"
DECLARATION = HERE / "hypothesis.md"
EXP010_RESULT = HERE.parent / "EXP-010-levinson-parity-transfer" / "artifacts" / "canonical" / "result.json"
THETA_C = Fraction(532, 1000)
DETECTORS_C = ("199/10000", "299/10000")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_identity(repo: Path) -> dict[str, object]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip()
    clean = subprocess.run(["git", "diff", "--quiet"], cwd=repo).returncode == 0 and subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=repo).returncode == 0
    return {"head": head, "tracked_tree_clean": clean}


def ball(text: str | Fraction) -> arb:
    q = Fraction(text)
    return arb(q.numerator) / q.denominator


class Kernel:
    def __init__(self) -> None:
        self.a = ball("1/2")
        self.b = arb(2).sqrt()
        self.norm = 2 * (self.a * self.b).sin() / self.b
        self.two_pi = 2 * arb.pi()

    def __call__(self, xi: acb) -> acb:
        c = self.two_pi * xi
        return (self.a * ((self.b - c) * self.a).sinc() + self.a * ((self.b + c) * self.a).sinc()) / self.norm


def interval(value: arb, digits: int = 25) -> dict[str, str]:
    return {"mid": value.mid().str(digits), "rad": value.rad().str(5), "arb": value.str(digits, radius=True)}


def upper(value: arb) -> Fraction:
    m, e = (value.mid() + value.rad()).man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def lower(value: arb) -> Fraction:
    m, e = (value.mid() - value.rad()).man_exp()
    return Fraction(int(m)) * Fraction(2) ** int(e)


def q_direct(points: list[acb], mult: list[int], kernel: Kernel) -> arb:
    total = acb(0)
    for i, zi in enumerate(points):
        for j, zj in enumerate(points):
            k = kernel(zi - zj)
            total += mult[i] * mult[j] * k * k
    return total.real


def c1_points(frozen: dict) -> tuple[list[acb], list[int]]:
    c1 = frozen["C1"]
    pts = [acb(ball(x)) for x in c1["real_triples"]]
    y = ball(c1["pair_imaginary_part"])
    x = ball(c1["pair_real_part"])
    pts += [acb(x, y), acb(x, -y)]
    return pts, [3] * len(c1["real_triples"]) + [1, 1]


def c2_cell(frozen: dict) -> tuple[arb, list[acb], list[int], int]:
    c2 = frozen["C2"]
    s = ball(c2["s"])
    cell = [acb(0)]
    mult = [3]
    for y, o in zip(c2["y"], c2["offsets"]):
        cell.append(acb(ball(o) * s, ball(y)))
    for y, o in zip(c2["y"], c2["offsets"]):
        cell.append(acb(ball(o) * s, -ball(y)))
    mult += [1] * (2 * len(c2["y"]))
    return s, cell, mult, int(c2["M"])


def q_lattice(s: arb, cell: list[acb], mult: list[int], m_half: int, kernel: Kernel, log=None) -> arb:
    total = acb(0)
    width = 2 * m_half + 1
    for ia, za in enumerate(cell):
        for ib, zb in enumerate(cell):
            base = za - zb
            weight = mult[ia] * mult[ib]
            acc = acb(0)
            for d in range(-2 * m_half, 2 * m_half + 1):
                k = kernel(base + d * s)
                acc += (width - abs(d)) * k * k
            total += weight * acc
        if log is not None:
            log(f"    cell row {ia + 1}/{len(cell)} done")
    return total.real


def lattice_points(s: arb, cell: list[acb], mult: list[int], m_half: int) -> tuple[list[acb], list[int]]:
    pts, mm = [], []
    for n in range(-m_half, m_half + 1):
        for z, m in zip(cell, mult):
            pts.append(z + n * s)
            mm.append(m)
    return pts, mm


def wang_c(theta: Fraction) -> arb:
    t = ball(theta)
    r2 = arb(2).sqrt()
    return 2 - t / 2 - (t / r2).cot() / r2


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only; never canonical")
    args = parser.parse_args()
    out = args.output_dir
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("output directory must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()
    lines: list[str] = []

    def log(message: str) -> None:
        line = f"[{time.time() - started:8.2f}s] {message}"
        lines.append(line)
        print(line, flush=True)
        if time.time() - started > MAX_SECONDS:
            raise TimeoutError("budget exceeded")

    ctx.prec = PREC_BITS
    repo = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=HERE, text=True).strip())
    identity = git_identity(repo)
    if not identity["tracked_tree_clean"] and not args.allow_dirty:
        raise RuntimeError("tracked repository files must be clean before canonical execution")
    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    thresholds = frozen["thresholds"]
    kernel = Kernel()
    log("stage 1/6: bind sources")
    bindings = {"hypothesis.md": sha256(DECLARATION), "frozen-parameters.json": sha256(FROZEN), "run.py": sha256(Path(__file__)), "exp010_result.json": sha256(EXP010_RESULT)}
    if abs(kernel(acb(0)).real - 1) > arb("1e-30"):
        raise AssertionError("K(0) != 1")

    log("stage 2/6: Prediction A (C1)")
    pts1, m1 = c1_points(frozen)
    q1 = q_direct(pts1, m1, kernel)
    n1, o1, s1 = sum(m1), len(frozen["C1"]["real_triples"]), 0
    slack1 = q1 - (2 * n1 + 3 * o1 - 4 * s1)
    pass_a = upper(slack1) < Fraction(thresholds["A_C1_slack_upper"])
    log(f"  Q(C1) = {q1.str(20, radius=True)}; slack = {slack1.str(15, radius=True)}; pass={pass_a}")

    log("stage 3/6: Prediction B (C2 lattice)")
    s, cell, mult, m_half = c2_cell(frozen)
    q2 = q_lattice(s, cell, mult, m_half, kernel, log)
    o2 = 2 * m_half + 1
    n2 = sum(mult) * o2
    ratio2 = (q2 - 2 * n2) / o2
    pass_b = upper(ratio2) < Fraction(thresholds["B_C2_ratio_upper"])
    log(f"  O = {o2}, N = {n2}; (Q-2N)/O = {ratio2.str(15, radius=True)}; pass={pass_b}")

    log("stage 4/6: Prediction C (onset cap with the EXP-010 detectors)")
    exp010 = json.loads(EXP010_RESULT.read_text(encoding="utf-8"))
    beta = ball(thresholds["C_onset_lower_for_beta"])
    c_theta = wang_c(THETA_C)
    rows_c = []
    for entry in exp010["detector_constants"]:
        if entry["nu"] not in DETECTORS_C:
            continue
        k_up = ball(entry["kappa"]["upper"])
        h = (2 + beta * k_up - (2 - c_theta)) / 4
        rows_c.append({"nu": entry["nu"], "kappa_upper_used": entry["kappa"]["upper"], "h_beta": interval(h), "negative": upper(h) < 0})
        log(f"  nu={entry['nu']}: h_beta(0.532) = {h.str(12, radius=True)}")
    pass_c = len(rows_c) == 2 and all(r["negative"] for r in rows_c)

    log("stage 5/6: Control D")
    prod1 = (q1 - s1) * (n1 - o1) - 2 * (n1 - s1) ** 2
    prod2 = (q2 - 0) * (n2 - o2) - 2 * n2**2
    small = 50
    q_formula = q_lattice(s, cell, mult, small, kernel)
    pts_small, m_small = lattice_points(s, cell, mult, small)
    q_dir = q_direct(pts_small, m_small, kernel)
    overlap = q_formula.overlaps(q_dir)
    pass_d = lower(prod1) > 0 and lower(prod2) > 0 and overlap
    log(f"  product slack C1 = {prod1.str(10, radius=True)}, C2 = {prod2.str(10, radius=True)}; formula vs direct at M=50 overlap={overlap}")

    checks = {"A": pass_a, "B": pass_b, "C": pass_c, "D": pass_d}
    result = {
        "experiment": "EXP-011",
        "schema": "exp011-canonical-v1",
        "precision_bits": PREC_BITS,
        "bindings_sha256": bindings,
        "C1": {"N": n1, "O": o1, "S": s1, "Q": interval(q1), "slack_L": interval(slack1), "product_slack": interval(prod1)},
        "C2": {"N": n2, "O": o2, "S": 0, "Q": interval(q2), "ratio_Q_minus_2N_over_O": interval(ratio2), "product_slack": interval(prod2)},
        "C_onset_cap": {"theta": str(THETA_C), "beta": thresholds["C_onset_lower_for_beta"], "wang_c": interval(c_theta), "rows": rows_c},
        "D_formula_check": {"M": small, "formula": interval(q_formula), "direct": interval(q_dir), "overlap": overlap},
        "checks": checks,
        "accepted": all(checks.values()),
    }
    log("stage 6/6: write canonical result")
    write_json(out / "result.json", result)
    receipt = {"experiment": "EXP-011", "git": identity, "python": sys.version.split()[0], "python_flint": __import__("flint").__version__, "result_sha256": sha256(out / "result.json"), "elapsed_seconds": round(time.time() - started, 2), "accepted": result["accepted"]}
    write_json(out / "execution-receipt.json", receipt)
    (out / "stdout.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    log(f"accepted={result['accepted']}")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
