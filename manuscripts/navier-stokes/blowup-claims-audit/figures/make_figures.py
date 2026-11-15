"""Build the figures of the paper from the result files they report.

Every plotted number is read from a `result*.json` under
`problems/analysis-pde/navier-stokes/experiments/`, or computed by the library
`problems/analysis-pde/navier-stokes/code/nslib` that the design bounds of the paper quote;
nothing is typed in except the acceptance thresholds, which are the ones committed in each
experiment's hypothesis and coded in `run_exp00N.py`. Run from any directory:

    python make_figures.py

It writes fig-damping, fig-localization, fig-ceiling, fig-horizon, fig-cycle, fig-rt,
fig-handoff and fig-design (all `.pdf`) next to itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[3] / "problems/analysis-pde/navier-stokes/experiments"
sys.path.insert(0, str(HERE.parents[3] / "problems/analysis-pde/navier-stokes/code"))

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


def fig_horizon() -> None:
    """Finite-horizon gap of the cascade model against the number of stages, EXP-003."""
    d = load("EXP-003-threshold-sweep/result.json")["H1"]
    hc = d["horizon_convergence"]
    q = [r["stages"] for r in hc]
    gap = [r["max_gap_to_closed_form"] for r in hc]
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.plot(q, gap, ls="none", marker="o", ms=5.5, color=BLUE, label="bisection on the model")
    xs = [q[0] * 0.8, q[-1] * 1.25]
    ax.plot(xs, [gap[0] * q[0] / x for x in xs], color=GREY, lw=0.9, ls="--", label=r"$\propto 1/Q$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks(q, [str(v) for v in q])
    ax.minorticks_off()
    ax.set_xlabel("stages $Q$ inspected by the run")
    ax.set_ylabel(r"largest gap to $1/(4p)$")
    ax.legend(fontsize=7.5)
    fig.savefig(HERE / "fig-horizon.pdf")
    plt.close(fig)


def fig_cycle() -> None:
    """Landing, steering gain and hold drift on two backgrounds and at the committed parameters, EXP-005 B."""
    sine = load("EXP-005-steered-cycle/result-B-sine.json")
    flat = load("EXP-005-steered-cycle/result-B-flattened.json")
    committed = load("EXP-005-steered-cycle/result-B-committed-parameters-REFUTED.json")
    # thresholds: B1 landing < 2e-2, B1 gain < 2e-2, B3 hold drift < 1e-2 (run_exp005.py, part_b)
    keys = [("landing_pde", "landing", 2e-2), ("gain_relative_error", "steering gain", 2e-2),
            ("hold_theta_relative_drift", "hold drift", 1e-2)]
    labels = ["flattened background, repaired schedule", "sine background, repaired schedule",
              "sine background, committed parameters"]
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    w = 0.26
    for j, (key, label, thr) in enumerate(keys):
        vals = [flat["main"][key], sine["main"][key], committed["main"][key]]
        for i, (v, col, hatch) in enumerate(zip(vals, [BLUE, ORANGE, GREY], ["", "//", "xx"])):
            ax.bar(j + (i - 1) * w, v, width=w, color=col, hatch=hatch, edgecolor="white", lw=0.4,
                   label=labels[i] if j == 0 else None)
        ax.plot([j - 1.6 * w, j + 1.6 * w], [thr, thr], color="black", lw=1.0, ls=":")
    ax.set_yscale("log")
    ax.set_ylim(1e-6, 2e3)
    ax.set_xticks(range(len(keys)), [k[1] for k in keys])
    ax.set_ylabel("measured value (log scale)")
    ax.plot([], [], color="black", lw=1.0, ls=":", label="acceptance threshold")
    ax.legend(fontsize=7, loc="upper left")
    fig.tight_layout()
    fig.savefig(HERE / "fig-cycle.pdf")
    plt.close(fig)


def fig_rt() -> None:
    """Growth of the neighbouring modes and of the field maximum in the refuted run, EXP-005 B.1."""
    d = load("EXP-005-steered-cycle/result-diagnosis-hold.json")
    t = [s["t"] for s in d["series"]]
    hor = [s["neighbour_horizontal_max"] for s in d["series"]]
    wave = [abs(s["mode_Theta"]) for s in d["series"]]
    mx = [s["max_abs_theta"] for s in d["series"]]
    t1, tb = d["t1"], d["t_b"]
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(6.4, 2.8))
    tp = [x for x, h in zip(t, hor) if h > 0]
    hp = [h for h in hor if h > 0]
    ax.plot(t, wave, color=BLUE, lw=1.1, label=r"steered layer, $|\Theta|$")
    ax.plot(tp, hp, color=ORANGE, lw=1.1, marker="o", ms=2.5, label="largest horizontal neighbour")
    rate = d["predicted_rates"]["worst_horizontal_neighbour_rate_in_hold"]
    ts = [tb, t[-1]]
    i0 = min(range(len(tp)), key=lambda i: abs(tp[i] - tb))
    ax.plot(ts, [hp[i0] * 2.718281828 ** (rate * (x - tb)) for x in ts], color=GREY, ls="--", lw=0.9,
            label=rf"$e^{{{rate:.2f}\,t}}$, predicted neighbour rate")
    for x in (t1, tb):
        ax.axvline(x, color=GREY, lw=0.6, ls=":")
    ax.set_yscale("log"); ax.set_ylim(1e-6, 2e2)
    ax.set_xlabel("time"); ax.set_ylabel("amplitude")
    ax.legend(fontsize=6.3, loc="upper left")
    ax2.plot(t, mx, color=BLUE, lw=1.1)
    ax2.axhline(4.0, color=GREY, lw=0.8, ls="--")
    ax2.text(t[0], 4.2, r"background value $4.0$", fontsize=7, va="bottom")
    for x in (t1, tb):
        ax2.axvline(x, color=GREY, lw=0.6, ls=":")
    ax2.set_xlabel("time"); ax2.set_ylabel(r"$\max|\theta|$")
    fig.tight_layout()
    fig.savefig(HERE / "fig-rt.pdf")
    plt.close(fig)


def fig_handoff() -> None:
    """Correlation and slope of the measured local rate against the two predictions."""
    froz = load("EXP-004-multilayer-handoff/result-frozen.json")
    dyn = load("EXP-004-multilayer-handoff/result-dynamical.json")
    runs = [("window 1.5", "EXP-005-steered-cycle/result-D-window-1.5.json"),
            ("window 3", "EXP-005-steered-cycle/result-D-window-3.0.json"),
            ("window 4.5", "EXP-005-steered-cycle/result-D-window-4.5.json"),
            (r"$\lambda_2=360$", "EXP-005-steered-cycle/result-D-handoff.json"),
            (r"$\lambda_2=512$", "EXP-005-steered-cycle/result-D-separation-512.json")]
    rows = [("frozen", froz["H1_full_two_scale_gradient"], froz["H2_control_base_only"]),
            ("dynamical", dyn["H1_lowpass_including_layer1"], dyn["H2_control_stratification_only"])]
    for lab, rel in runs:
        r = load(rel)
        rows.append((lab, r["H1_total_gradient"], r["H2_control_base_only"]))
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.0), gridspec_kw={"width_ratios": [1.7, 1]})
    x = list(range(len(rows)))
    ax.plot(x, [r[1]["corr"] for r in rows], ls="none", marker="o", ms=5.5, color=BLUE, label="total gradient")
    ax.plot(x, [r[2]["corr"] for r in rows], ls="none", marker="s", ms=5, color=ORANGE, mfc="none",
            label="base stratification only")
    ax.axhline(0.9, color="black", lw=1.0, ls=":")
    ax.text(len(rows) - 0.6, 0.915, "criterion 0.9", ha="right", fontsize=7)
    ax.axvline(1.5, color=GREY, lw=0.6)
    ax.text(0.5, 0.03, "EXP-004", ha="center", fontsize=7)
    ax.text(5.0, 0.03, "EXP-005 part D", ha="center", fontsize=7)
    ax.set_xticks(x, [r[0] for r in rows], rotation=35, ha="right", fontsize=7)
    ax.set_ylabel("correlation with the measured rate")
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=7, loc="center left")
    ax2.plot(x, [r[1]["slope"] for r in rows], ls="none", marker="o", ms=5.5, color=BLUE)
    ax2.axhspan(0.85, 1.15, color=GREY, alpha=0.2, lw=0)
    ax2.text(2.5, 0.9, r"criterion $1\pm0.15$", ha="center", fontsize=7)
    ax2.set_xticks(x, [r[0] for r in rows], rotation=35, ha="right", fontsize=7)
    ax2.set_ylabel("slope of measured on predicted rate")
    fig.tight_layout()
    fig.savefig(HERE / "fig-handoff.pdf")
    plt.close(fig)


def fig_design() -> None:
    """Design ceilings against the number of controlled force derivatives, from nslib."""
    from nslib import ab_force_budget as F
    from nslib import cascade as C

    fig, ax = plt.subplots(figsize=(3.8, 2.9))
    style = [("published choices", F.PUBLISHED, "o", BLUE), ("every free choice released", F.RELAXED, "s", ORANGE),
             ("scale at the previous wavelength", F.OPTIMISTIC, "^", GREY)]
    for name, arch, mk, col in style:
        rows = arch.ceiling(20)["rows"]
        ax.plot([r["d"] for r in rows], [r["alpha"] for r in rows], marker=mk, ms=3.5, lw=0.9, color=col,
                label=name)
    thr = C.ALPHA0_CMZ / 2.0
    ax.axhline(thr, color="black", lw=1.0, ls=":")
    ax.text(20, thr * 1.08, "proved threshold", ha="right", fontsize=7)
    ax.set_yscale("log")
    ax.set_ylim(1e-5, 0.1)
    ax.set_xlabel("controlled derivatives of the force, $d$")
    ax.set_ylabel(r"largest certified exponent $\alpha$")
    ax.legend(fontsize=6.5, loc="lower left")
    fig.savefig(HERE / "fig-design.pdf")
    plt.close(fig)


if __name__ == "__main__":
    fig_damping()
    fig_localization()
    fig_ceiling()
    fig_horizon()
    fig_cycle()
    fig_rt()
    fig_handoff()
    fig_design()
    print("wrote eight figures")
