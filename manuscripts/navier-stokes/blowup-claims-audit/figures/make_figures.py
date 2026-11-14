"""Build the three figures of the paper from the result files they report.

Every plotted number is read from a `result*.json` under
`problems/analysis-pde/navier-stokes/experiments/`; nothing is typed in. Run from any directory:

    python make_figures.py

It writes `fig-damping.pdf`, `fig-localization.pdf` and `fig-ceiling.pdf` next to itself.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[3] / "problems/analysis-pde/navier-stokes/experiments"

# colour-blind-safe pair plus black; markers carry the same distinction as colour
BLUE, ORANGE, GREY = "#1f5fa8", "#d1601b", "#555555"

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.linewidth": 0.7,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "savefig.bbox": "tight",
})


def load(rel: str) -> dict:
    return json.loads((EXP / rel).read_text(encoding="utf-8"))


def fig_damping() -> None:
    """Measured against predicted decrement of the peak growth rate, EXP-002."""
    res = load("EXP-002-reduction-control/result.json")["cases"]
    base = res["P1_inviscid"]["peak_measured"]
    rows = res["P1_viscous"]
    pred = [r["damp"] for r in rows]
    meas = [base - r["peak_measured"] for r in rows]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(6.4, 2.6), gridspec_kw={"width_ratios": [1.15, 1]})
    lo, hi = min(pred) * 0.5, max(pred) * 2.0
    ax.plot([lo, hi], [lo, hi], color=GREY, lw=0.9, label="measured = predicted")
    for a in sorted({r["alpha"] for r in rows}):
        sel = [(p, m) for r, p, m in zip(rows, pred, meas) if r["alpha"] == a]
        ax.plot(*zip(*sel), ls="none", marker={0.25: "o", 0.5: "s", 1.0: "^"}[a], ms=5,
                color=BLUE, mfc="none" if a == 0.5 else BLUE, label=rf"$\alpha={a}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"predicted damping $\nu(\lambda|\zeta|)^{2\alpha}$")
    ax.set_ylabel("measured decrement of the peak rate")
    ax.legend(fontsize=7.5, loc="upper left")
    err = [abs(r["peak_measured"] - r["peak_predicted"]) for r in rows]
    labels = [rf"{r['alpha']}, {r['nu']:.0e}".replace("e-0", "e-") for r in rows]
    ax2.bar(range(len(rows)), [e * 1e4 for e in err], color=ORANGE, width=0.6)
    ax2.set_xticks(range(len(rows)), labels, rotation=45, ha="right", fontsize=7)
    ax2.set_ylabel(r"absolute error of the rate ($10^{-4}$)")
    ax2.set_xlabel(r"$\alpha,\ \nu$")
    fig.tight_layout()
    fig.savefig(HERE / "fig-damping.pdf")
    plt.close(fig)


def fig_localization() -> None:
    """Relative error of the plane-wave damping law against the bandwidth ratio, EXP-007."""
    d = load("EXP-007-localized-dissipation/result.json")
    scan = d["scan"]
    alpha = scan[0]["alpha"]
    coef = d["H2_coefficient_max"] / 1.0   # coefficient at alpha = 1.0, the largest in the scan
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    lams = sorted({c["lambda"] for c in scan})
    marks = dict(zip(lams, ["o", "s", "^", "D"]))
    for lam in lams:
        sel = sorted((c["ell_times_lambda"], c["relative_error"]) for c in scan if c["lambda"] == lam)
        ax.plot(*zip(*sel), ls="none", marker=marks[lam], ms=4.5, color=BLUE,
                mfc="none", label=rf"$\lambda={lam:g}$")
    ctrl = d["H3_control_wide_envelope"]
    ax.plot([ctrl["ell_times_lambda"]], [ctrl["relative_error"]], ls="none", marker="x", ms=7,
            color=ORANGE, label=r"narrow envelope")
    xs = [20, 1000]
    ax.plot(xs, [coef * alpha / x for x in xs], color=GREY, lw=0.9,
            label=rf"${coef:.1f}\,\alpha/(\ell\lambda)$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel(r"bandwidth ratio $\ell\lambda$")
    ax.set_ylabel("relative error of the damping law")
    ax.legend(fontsize=7, loc="lower left")
    fig.savefig(HERE / "fig-localization.pdf")
    plt.close(fig)


def fig_ceiling() -> None:
    """Critical exponent against the frequency exponent p for both growth laws, EXP-008."""
    d = load("EXP-008-growth-law-ceiling/result.json")
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    style = {0.5: ("o", BLUE, r"pendulum, $\gamma=1/2$"), 1.0: ("s", ORANGE, r"stretching, $\gamma=1$")}
    ps = [1.4 + 0.05 * i for i in range(0, 75)]
    for gamma, (mk, col, lab) in style.items():
        rows = [r for r in d["rows"] if r["gamma"] == gamma]
        ax.plot(ps, [gamma / (2 * p) for p in ps], color=col, lw=0.9, ls="--")
        ax.plot([r["p"] for r in rows], [r["measured_alpha_c"] for r in rows], ls="none",
                marker=mk, ms=5, color=col, label=lab)
    ax.set_xlabel(r"frequency exponent $p$ in $\lambda=A^{p}$")
    ax.set_ylabel(r"critical exponent $\alpha_c$ (ours)")
    ax.legend(fontsize=7.5)
    fig.savefig(HERE / "fig-ceiling.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig_damping()
    fig_localization()
    fig_ceiling()
    print("wrote fig-damping.pdf, fig-localization.pdf, fig-ceiling.pdf")
