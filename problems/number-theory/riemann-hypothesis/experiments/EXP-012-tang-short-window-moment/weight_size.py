"""EXP-012 step-3 value check: the size of Tang's dual weight G_{T,H}(1/2+it) (mpmath, 30 digits).

G_{T,H}(w) = int_0^inf exp(-(2 pi x - T)^2/H^2) x^(w-1) dx (Tang, arXiv:2608.14852v1, eq. (GTH)).
With x = (T + H y)/(2 pi), G(1/2+it) = (H/2pi) int e^(-y^2) ((T+Hy)/2pi)^(-1/2+it) dy, so
|G(1/2+it)| = (H/sqrt(T)) sqrt(1/2) exp(-(tH/2T)^2)(1 + o(1)) for |t| << T/H.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import mpmath as mp


def weight(t_value, big_t, h_value):
    def integrand(y):
        return mp.exp(-(y**2)) * ((big_t + h_value * y) / (2 * mp.pi)) ** (mp.mpf("-0.5") + 1j * t_value)

    return h_value / (2 * mp.pi) * mp.quad(integrand, [-12, 0, 12])


def main(out: Path) -> int:
    mp.mp.dps = 30
    rows = []
    ok = True
    for big_t_exp, theta in ((8, "0.6"), (10, "0.55"), (12, "0.7")):
        big_t = mp.mpf(10) ** big_t_exp
        h_value = big_t ** mp.mpf(theta)
        predicted = h_value / mp.sqrt(big_t) * mp.sqrt(mp.mpf(1) / 2)
        for frac in ("0", "0.25", "1"):
            t_value = mp.mpf(frac) * big_t / h_value
            g = abs(weight(t_value, big_t, h_value))
            model = predicted * mp.exp(-((t_value * h_value / (2 * big_t)) ** 2))
            rel = abs(g / model - 1)
            ok = ok and rel < mp.mpf("0.02")
            rows.append({"T": f"1e{big_t_exp}", "theta": theta, "t_over_T_over_H": frac, "abs_G": mp.nstr(g, 10), "model": mp.nstr(model, 10), "relative_difference": mp.nstr(rel, 3)})
    report = {"rows": rows, "model_within_2_percent": bool(ok)}
    out.mkdir(parents=True, exist_ok=True)
    (out / "weight-size.json").write_text(json.dumps(report, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("artifacts/canonical")))
