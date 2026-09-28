"""EXP-011 independent audit (different kernel evaluation, different code path).

1. C1 with mpmath at 30 digits and the kernel evaluated by numerical quadrature of its definition
   K(xi) = int eta^2(u) exp(-2 pi i xi u) du / int eta^2, eta^2 = cos(sqrt2 u) on (-1/2, 1/2), not by the
   closed form used in run.py.
2. C2 with numpy float64 and the closed form, summed directly over the lattice difference weights;
   the canonical Arb value must agree to 1e-9 relative.
3. A quadrature-kernel mpmath evaluation of the C2 cell at M = 5 (subdivided panels) against the float sum.

Run 1 used M = 30 with an unsubdivided quadrature, which is inaccurate for |xi| near 360; its failed
report is kept as artifacts/audit/audit-run1-failed.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp
import numpy as np

HERE = Path(__file__).resolve().parent


def mid_value(text: str) -> str:
    """Midpoint string of an Arb rendering such as '[-0.0582 +/- 3e-17]' or '2.35886'."""
    return text.strip().lstrip("[").split(" +/-")[0].rstrip("]").strip()


def k_quad(xi):
    # Subdivide so that each panel holds about one oscillation even for |Re xi| near 70.
    panels = max(8, int(abs(mp.re(xi))) * 2 + 8)
    nodes = [mp.mpf(-1) / 2 + mp.mpf(j) / panels for j in range(panels + 1)]
    num = mp.quad(lambda u: mp.cos(mp.sqrt(2) * u) * mp.exp(-2j * mp.pi * xi * u), nodes)
    den = mp.quad(lambda u: mp.cos(mp.sqrt(2) * u), [-0.5, 0.5])
    return num / den


def k_float(xi: np.ndarray) -> np.ndarray:
    a, b = 0.5, np.sqrt(2.0)
    c = 2 * np.pi * xi
    return (a * np.sinc((b - c) * a / np.pi) + a * np.sinc((b + c) * a / np.pi)) / (2 * np.sin(a * b) / b)


def cell(frozen: dict):
    c2 = frozen["C2"]
    s = float(c2["s"])
    pts = [0j] + [float(o) * s + 1j * float(y) for y, o in zip(c2["y"], c2["offsets"])] + [float(o) * s - 1j * float(y) for y, o in zip(c2["y"], c2["offsets"])]
    return s, np.array(pts), np.array([3.0] + [1.0] * (2 * len(c2["y"]))), int(c2["M"])


def lattice_float(s, pts, m, m_half):
    d = np.arange(-2 * m_half, 2 * m_half + 1)
    w = (2 * m_half + 1 - np.abs(d)).astype(float)
    kk = k_float((pts[:, None] - pts[None, :])[:, :, None] + d[None, None, :] * s)
    return float(np.real(np.sum(m[:, None, None] * m[None, :, None] * w[None, None, :] * kk * kk)))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frozen = json.loads((HERE / "frozen-parameters.json").read_text(encoding="utf-8"))
    canonical = json.loads((HERE / "artifacts" / "canonical" / "result.json").read_text(encoding="utf-8"))
    mp.mp.dps = 30
    c1 = frozen["C1"]
    pts = [mp.mpc(mp.mpf(x)) for x in c1["real_triples"]] + [mp.mpc(0, mp.mpf(c1["pair_imaginary_part"])), mp.mpc(0, -mp.mpf(c1["pair_imaginary_part"]))]
    mult = [3] * 6 + [1, 1]
    q1 = mp.re(mp.fsum(mult[i] * mult[j] * k_quad(pts[i] - pts[j]) ** 2 for i in range(8) for j in range(8)))
    slack1 = q1 - 58
    c1_ok = slack1 < mp.mpf(frozen["thresholds"]["A_C1_slack_upper"]) and abs(slack1 - mp.mpf(mid_value(canonical["C1"]["slack_L"]["mid"]))) < mp.mpf("1e-20")
    s, cpts, cm, m_half = cell(frozen)
    q2 = lattice_float(s, cpts, cm, m_half)
    o2 = 2 * m_half + 1
    n2 = cm.sum() * o2
    ratio_float = (q2 - 2 * n2) / o2
    ratio_can = float(mid_value(canonical["C2"]["ratio_Q_minus_2N_over_O"]["mid"]))
    c2_ok = abs(ratio_float - ratio_can) < 1e-9 * abs(ratio_can) and ratio_float < float(frozen["thresholds"]["B_C2_ratio_upper"])
    small = 5
    mp.mp.dps = 20
    d_vals = range(-2 * small, 2 * small + 1)
    cpts_mp = [mp.mpc(complex(z)) for z in cpts]
    q_small = mp.mpf(0)
    kcache = {}
    for ia, za in enumerate(cpts_mp):
        for ib, zb in enumerate(cpts_mp):
            acc = mp.mpf(0)
            for d in d_vals:
                key = (ia, ib, d)
                k = kcache.setdefault(key, k_quad(za - zb + d * mp.mpf(frozen["C2"]["s"])))
                acc += (2 * small + 1 - abs(d)) * mp.re(k * k)
            q_small += cm[ia] * cm[ib] * acc
    q_small_float = lattice_float(s, cpts, cm, small)
    small_ok = abs(q_small - q_small_float) < mp.mpf("1e-8") * abs(q_small)
    report = {
        "C1_quadrature_kernel": {"Q": mp.nstr(q1, 25), "slack": mp.nstr(slack1, 20), "pass": bool(c1_ok)},
        "C2_float_closed_form": {"ratio": repr(ratio_float), "canonical_mid": canonical["C2"]["ratio_Q_minus_2N_over_O"]["mid"], "pass": bool(c2_ok)},
        "C2_M5_quadrature_vs_float": {"quadrature": mp.nstr(q_small, 18), "float": repr(q_small_float), "pass": bool(small_ok)},
        "accepted": bool(c1_ok and c2_ok and small_ok),
    }
    (args.output_dir / "audit.json").write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
