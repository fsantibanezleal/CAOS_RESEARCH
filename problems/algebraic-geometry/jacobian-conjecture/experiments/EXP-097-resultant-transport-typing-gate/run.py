"""EXP-097: exact typing gate for transporting the resultant invariant."""

from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


x, y = sp.symbols("x y")


def laurent_bounds(expression: sp.Expr) -> tuple[int, int]:
    """Return the minimum and maximum x exponents of a Laurent polynomial."""

    expanded = sp.expand(expression)
    exponents: list[int] = []
    for term in sp.Add.make_args(expanded):
        exponent = term.as_powers_dict().get(x, sp.Integer(0))
        if not exponent.is_Integer:
            raise ValueError(f"nonintegral exponent in {term}")
        exponents.append(int(exponent))
    return min(exponents), max(exponents)


def width(bounds: tuple[int, int]) -> int:
    return bounds[1] - bounds[0]


def main() -> None:
    # Nontrivial exact control pair over Q[x,y].
    f = y**2 + (x + 1) * y + x**2 + 1
    g = y + x**3 + x
    p = sp.degree(f, y)
    q = sp.degree(g, y)
    resultant = sp.factor(sp.resultant(f, g, y))

    # A common Laurent translation is an automorphism over Q(x).
    h = x**-2 + 2 * x**-1
    translated_f = sp.cancel(f.subs(y, y + h))
    translated_g = sp.cancel(g.subs(y, y + h))
    translated_resultant = sp.factor(
        sp.resultant(translated_f, translated_g, y)
    )
    translation_residual = sp.cancel(translated_resultant - resultant)
    assert translation_residual == 0

    # Exact monomial inversion/scaling law.
    c = 4
    inverted_f = sp.cancel(
        f.subs({x: x**-1, y: x**c * y}, simultaneous=True)
    )
    inverted_g = sp.cancel(
        g.subs({x: x**-1, y: x**c * y}, simultaneous=True)
    )
    inverted_resultant = sp.factor(
        sp.resultant(inverted_f, inverted_g, y)
    )
    expected_inverted = sp.factor(
        x ** (c * p * q) * resultant.subs(x, x**-1)
    )
    inversion_residual = sp.cancel(
        inverted_resultant - expected_inverted
    )
    assert inversion_residual == 0

    # Laurent units shift the absolute exponent interval, not its width.
    unit_power = 5
    unit_shifted_resultant = sp.factor(
        sp.resultant(x**unit_power * f, g, y)
    )
    expected_unit_shift = sp.factor(x ** (unit_power * q) * resultant)
    assert sp.cancel(unit_shifted_resultant - expected_unit_shift) == 0
    original_bounds = laurent_bounds(resultant)
    unit_bounds = laurent_bounds(unit_shifted_resultant)
    assert unit_bounds == (
        original_bounds[0] + unit_power * q,
        original_bounds[1] + unit_power * q,
    )
    assert width(unit_bounds) == width(original_bounds)

    # Boundary control: x is nonconstant in Q[x] but a unit after localizing x.
    boundary_f = x * y + 1
    boundary_g = x
    boundary_resultant = sp.resultant(boundary_f, boundary_g, y)
    assert boundary_resultant == x
    localized_normal_form = sp.cancel(boundary_resultant / x)
    assert localized_normal_form == 1

    # Swap control: the selected coordinate eliminant can lose that boundary
    # degree. Res_y(F(y,x),G(y,x)) equals Res_x(F,G), not Res_y(F,G).
    swapped_f = boundary_f.subs({x: y, y: x}, simultaneous=True)
    swapped_g = boundary_g.subs({x: y, y: x}, simultaneous=True)
    swapped_resultant_y = sp.resultant(swapped_f, swapped_g, y)
    other_coordinate_resultant = sp.resultant(
        boundary_f, boundary_g, x
    )
    assert swapped_resultant_y == other_coordinate_resultant == -1
    assert sp.degree(boundary_resultant, x) == 1
    assert sp.degree(swapped_resultant_y, x) == 0

    # Actual GGHV final-inversion arithmetic.
    reduced_p = 16
    reduced_q = 24
    reduced_c = 4
    reflection_constant = reduced_c * reduced_p * reduced_q
    original_degree = 21
    possible_orders = list(range(original_degree + 1))
    transported_intervals = [
        {
            "input_order": order,
            "input_interval": [order, original_degree],
            "output_interval": [
                reflection_constant - original_degree,
                reflection_constant - order,
            ],
            "width": original_degree - order,
        }
        for order in possible_orders
    ]
    assert reflection_constant == 1536
    assert transported_intervals[0]["output_interval"] == [1515, 1536]
    assert transported_intervals[-1]["width"] == 0

    result = {
        "experiment": "EXP-097",
        "arithmetic": "exact SymPy polynomial and rational-function algebra",
        "controls": {
            "base_resultant": str(resultant),
            "base_resultant_bounds": list(original_bounds),
            "translation_residual": str(translation_residual),
            "inversion_residual": str(inversion_residual),
            "unit_shift_power": unit_power,
            "unit_shifted_bounds": list(unit_bounds),
            "width_preserved_under_unit_shift": (
                width(unit_bounds) == width(original_bounds)
            ),
            "boundary_resultant_before_localization": str(
                boundary_resultant
            ),
            "boundary_resultant_modulo_laurent_unit": str(
                localized_normal_form
            ),
            "degree_before_swap": 1,
            "degree_after_selected_eliminant_swap": 0,
        },
        "gghv_final_inversion": {
            "y_degrees": [reduced_p, reduced_q],
            "c": reduced_c,
            "reflection_constant_cpq": reflection_constant,
            "original_resultant_degree": original_degree,
            "unknown_original_x_order": [0, original_degree],
            "possible_transported_intervals": transported_intervals,
            "unconditional_width_range": [0, original_degree],
            "width_equals_21_only_if_original_x_order_is_zero": True,
        },
        "decision": {
            "direct_absolute_degree_transport": False,
            "reason": (
                "The GGHV reduction enters a Laurent category in which x is "
                "a unit, then swaps and inverts boundary divisors. Absolute "
                "resultant degree requires boundary valuation data that the "
                "51 reduced coefficients do not carry by themselves."
            ),
            "conditional_typed_candidate": (
                "Laurent resultant exponent width, conditional on proving "
                "the missing original boundary order and swap compatibility."
            ),
        },
        "next_route": (
            "Do not build a degree-21 resultant equation in the 51 reduced "
            "coefficients. Either reconstruct a boundary-divisor ledger for "
            "the full GGHV map, or proceed to the declared small "
            "certificate-module/chart-cover experiment."
        ),
        "non_claims": [
            "The open (72,108) chain is not excluded.",
            "No seven-point inner vertex is proved realizable.",
            "No counterexample is constructed.",
            "The planar degree floor is not raised.",
        ],
    }

    output = json.dumps(result, indent=2, sort_keys=True)
    print(output, flush=True)
    artifact = Path(__file__).with_name("artifacts") / "results.json"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(output + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
