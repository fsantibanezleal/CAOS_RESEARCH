from __future__ import annotations

import functools
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

pytest.importorskip("flint")
mp = pytest.importorskip("mpmath")

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = (
    ROOT / "problems/number-theory/riemann-hypothesis/experiments" / "EXP-010-levinson-parity-transfer"
)


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENT / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUN = _load("riemann_exp010_run", "run.py")
CONTROLS = _load("riemann_exp010_controls", "controls.py")


@functools.lru_cache(maxsize=1)
def certified() -> dict[Fraction, dict[str, object]]:
    RUN.ctx.prec = RUN.PREC_BITS
    frozen = json.loads(RUN.FROZEN.read_text(encoding="utf-8"))
    return {Fraction(entry["nu"]): RUN.certify_set(entry) for entry in frozen["parameter_sets"]}


def test_frozen_operator_polynomials_are_exactly_admissible() -> None:
    for record in certified().values():
        assert record["degree_Q"] == 201
        constraints = record["constraints"]
        assert (constraints["P(0)"], constraints["P(1)"], constraints["Q(0)"]) == ("0", "1", "1")
        assert constraints["Q(y)+Q(1-y)"] == "1"


def test_every_frozen_kappa_exceeds_the_declared_slope() -> None:
    for nu, record in certified().items():
        assert record["prediction_c_kappa_gt_0_717_nu"] is True
        assert Fraction(record["kappa_lower_rational"]) > Fraction(7170, 10000) * nu
    assert Fraction(certified()[Fraction(339, 10000)]["kappa_lower_rational"]) > Fraction(243, 10000)


def test_published_anchors_are_reproduced() -> None:
    RUN.ctx.prec = RUN.PREC_BITS
    record = RUN.anchors()
    young = record["young_2010"]["c"]
    assert Fraction(young["lower"]) > Fraction("2.3500677")
    assert Fraction(young["upper"]) < Fraction("2.3500678")
    assert Fraction(record["conrey_1989_note"]["kappa"]["lower"]) > Fraction("0.4088")


def test_exact_moment_reduction_matches_direct_quadrature() -> None:
    p, q = RUN.fmpq_poly([0, 1]), RUN.fmpq_poly([1, -1])
    big, small = RUN.conrey_constant_exact(p, q, RUN.fq("13/10"), RUN.fq("1/2"))
    exact = float(RUN.to_fraction(big)) * mp.exp(2 * mp.mpf("1.3")) + float(RUN.to_fraction(small))

    def integrand(u, v):
        w = mp.exp(mp.mpf("1.3") * v) * (1 - v)
        dw = mp.exp(mp.mpf("1.3") * v) * (mp.mpf("1.3") * (1 - v) - 1)
        return (w * 1 + mp.mpf("0.5") * dw * u) ** 2

    direct = 1 + 2 * mp.quad(integrand, [0, 1], [0, 1])
    assert abs(exact - direct) < 1e-12


def test_onset_rows_and_exp008_ratio_pass() -> None:
    RUN.ctx.prec = RUN.PREC_BITS
    onset = RUN.onset_and_curve(certified())
    assert all(row["pass"] for row in onset["rows"])
    first = next(row for row in onset["rows"] if row["theta"] == "267/500")
    assert Fraction(first["h_L"]["lower"]) > Fraction(1, 10**5)
    assert onset["exp008_comparison"]["pass"] is True
    assert Fraction(onset["exp008_comparison"]["ratio_h_L_over_h6_lower"]) > 900


def test_counting_identities_hold_at_one_point() -> None:
    mp.mp.dps = 30
    beta, q = CONTROLS.get_q("Q3")
    t = mp.mpf("10000.137")
    s = mp.mpc("0.5", t)
    L = mp.log(mp.mpf(10000))
    c = CONTROLS.f_taylor(s, len(q) - 1)
    lam = CONTROLS.lambda_taylor(s, len(q) - 1)
    v, chi_v1, e, vt = CONTROLS.levinson_parts(c, lam, q, L, beta)
    direct = CONTROLS.chi(s) * sum(q[k] * (-1 / L) ** k * mp.zeta(1 - s, 1, k) for k in range(len(q)))
    omega = mp.expj(mp.siegeltheta(t))
    assert abs(chi_v1 - direct) / abs(direct) < 1e-20
    assert abs(mp.im(omega * e)) / abs(e) < 1e-15
    assert abs(beta * mp.siegelz(t) - 2 * mp.re(omega * vt)) / abs(mp.siegelz(t)) < 1e-20


def test_execution_contracts_are_cpu_bounded() -> None:
    assert RUN.MAX_SECONDS == 900.0
    assert CONTROLS.MAX_SECONDS == 1800.0
    assert RUN.KAPPA_OVER_NU == Fraction(7170, 10000)


def test_canonical_artifacts_bind_clean_passes() -> None:
    result_path = EXPERIMENT / "artifacts/canonical/result.json"
    receipt = json.loads((EXPERIMENT / "artifacts/canonical/execution-receipt.json").read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert result["accepted"] is True and all(result["checks"].values())
    assert receipt["accepted"] is True
    assert receipt["git"]["tracked_tree_clean"] is True
    assert receipt["result_sha256"] == hashlib.sha256(result_path.read_bytes()).hexdigest()
    audit = json.loads((EXPERIMENT / "artifacts/audit/audit.json").read_text(encoding="utf-8"))
    assert audit["accepted"] is True and all(audit["checks"].values())
    assert audit["canonical_result_sha256"] == receipt["result_sha256"]
    controls = json.loads((EXPERIMENT / "artifacts/controls/controls.json").read_text(encoding="utf-8"))
    assert controls["accepted"] is True and all(controls["checks"].values())
