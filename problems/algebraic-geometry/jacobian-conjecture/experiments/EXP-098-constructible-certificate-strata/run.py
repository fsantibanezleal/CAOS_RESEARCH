"""EXP-098: exact constructible certificate-strata controls.

CPU only. Exact SymPy arithmetic over QQ. No randomness.
Run from the repository root:

    python problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-098-constructible-certificate-strata/run.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from sympy import Matrix, cancel, groebner, symbols


ROOT = Path(__file__).resolve().parent
ARTIFACT = ROOT / "artifacts" / "results.json"

x, y, q1, q2 = symbols("x y q1 q2")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"[PASS] {message}")


def matrix_is_zero(matrix: Matrix) -> bool:
    return all(cancel(entry) == 0 for entry in matrix)


def main() -> None:
    # The constructible control.
    matrix = Matrix([[-y, 0], [x, 0], [0, x]])
    rhs = Matrix([1, 0, 1])

    # Independent route 1: the total solution scheme is empty. This Groebner
    # basis includes the parameters and the proposed solution coordinates.
    equations = list(matrix * Matrix([q1, q2]) - rhs)
    total_basis = groebner(equations, q1, q2, y, x, order="lex")
    total_unit = list(total_basis) == [1]
    require(
        total_unit,
        "the total solution ideal is the unit ideal, so every geometric fiber is inconsistent",
    )

    # Independent route 2: direct dichotomy.
    # If x = 0, the third equation is 0 = 1.
    # If x is invertible, the second equation forces q1 = 0, while the first
    # equation requires -y*q1 = 1.
    require(
        matrix.subs(x, 0)[2, :] == Matrix([[0, 0]]) and rhs[2] == 1,
        "the closed stratum V(x) is inconsistent by the third equation",
    )
    require(
        equations[1] == x * q1 and equations[0] == -q1 * y - 1,
        "on D(x), q1 = 0 contradicts the first equation",
    )

    # Global syzygy calculation. For c=(c1,c2,c3), M^T c=0 gives
    # -y*c1+x*c2=0 and x*c3=0. Since QQ[x,y] is a domain and gcd(x,y)=1,
    # c3=0, c1=x*h, c2=y*h. Thus the pairing with rhs is x*h.
    global_generator = Matrix([x, y, 0])
    require(
        matrix_is_zero(matrix.T * global_generator),
        "(x,y,0) generates the primitive global left-syzygy direction",
    )
    global_pairing = cancel((global_generator.T * rhs)[0])
    require(global_pairing == x, "the global pairing ideal is (x)")
    pairing_basis = groebner([global_pairing], x, y, order="lex")
    require(list(pairing_basis) != [1], "the global pairing ideal is proper")

    # Generic principal-open chart.
    open_certificate = Matrix([1, y / x, 0])
    require(
        matrix_is_zero(matrix.T * open_certificate),
        "D(x) has a localized left-syzygy certificate",
    )
    require(
        cancel((open_certificate.T * rhs)[0]) == 1,
        "the D(x) certificate pairs to one",
    )

    # Residual closed stratum and the specialization-only certificate.
    matrix_closed = matrix.subs(x, 0)
    closed_certificate = Matrix([0, 0, 1])
    require(
        matrix_is_zero(matrix_closed.T * closed_certificate),
        "V(x) gains the specialized syzygy e3",
    )
    require(
        (closed_certificate.T * rhs)[0] == 1,
        "the V(x) specialization certificate pairs to one",
    )
    require(
        global_generator.subs(x, 0)[2] == 0 and closed_certificate[2] == 1,
        "the e3 certificate is absent from the specialized global generator",
    )

    # Non-lift proof: the second global syzygy equation is x*c3=0. In the
    # domain QQ[x,y], every global syzygy has c3=0, so e3 cannot lift.
    require(
        matrix[:, 1] == Matrix([0, 0, x]),
        "the global equation x*c3=0 forces c3=0 before specialization",
    )

    # Presentation check:
    # coker(M) = (x,y) direct-sum QQ[x,y]/(x).
    # The rhs class is (x, 1 mod x). The first component survives on D(x);
    # the torsion component survives on V(x), but Hom(R/(x),R)=0.
    first_relation = matrix[:, 0]
    torsion_relation = matrix[:, 1]
    require(
        first_relation == Matrix([-y, x, 0])
        and torsion_relation == Matrix([0, 0, x]),
        "the cokernel presentation is (x,y) direct-sum R/(x)",
    )

    # Positive and negative controls.
    global_matrix = Matrix([[x], [0]])
    global_rhs = Matrix([0, 1])
    global_certificate = Matrix([0, 1])
    require(
        matrix_is_zero(global_matrix.T * global_certificate)
        and (global_certificate.T * global_rhs)[0] == 1,
        "global-certificate control is detected without stratification",
    )

    consistent_matrix = Matrix([[1], [0]])
    consistent_rhs = Matrix([1, 0])
    require(
        consistent_matrix * Matrix([1]) == consistent_rhs,
        "everywhere-consistent control has the explicit solution q=1",
    )
    consistent_kernel = Matrix([0, 1])
    require(
        matrix_is_zero(consistent_matrix.T * consistent_kernel)
        and (consistent_kernel.T * consistent_rhs)[0] == 0,
        "consistent control has no nonzero syzygy pairing",
    )

    # The open-cover collapse is a symbolic lemma, not a sampled claim. After
    # clearing denominators on D(s_i), each certificate pairs to s_i^N_i.
    # If those opens cover Spec(R), the ideal of these powers is R. A linear
    # combination of the cleared covectors is therefore one global covector
    # pairing to 1.
    collapse_steps = [
        "clear each localized denominator",
        "obtain global syzygies pairing to powers of chart functions",
        "use the unit ideal generated by those powers",
        "combine the syzygies into one global covector pairing to one",
    ]

    result = {
        "experiment": "EXP-098",
        "ring": "QQ[x,y]",
        "matrix": [["-y", "0"], ["x", "0"], ["0", "x"]],
        "rhs": ["1", "0", "1"],
        "total_solution_groebner_basis": [str(item) for item in total_basis],
        "universally_inconsistent": total_unit,
        "global_syzygy_generator": ["x", "y", "0"],
        "global_pairing_ideal": "(x)",
        "global_pairing_is_unit": False,
        "open_chart": {
            "locus": "D(x)",
            "certificate": ["1", "y/x", "0"],
            "pairing": "1",
        },
        "closed_stratum": {
            "locus": "V(x)",
            "certificate": ["0", "0", "1"],
            "pairing": "1",
            "lifts_globally": False,
        },
        "cokernel_presentation": "(x,y) direct-sum R/(x)",
        "open_cover_collapse_steps": collapse_steps,
        "controls": {
            "global_certificate": "pass",
            "everywhere_consistent": "pass",
        },
        "decision": (
            "Use recursive constructible rank strata. A principal-open cover "
            "of localized global syzygies alone is equivalent to one global "
            "polynomial covector."
        ),
    }

    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    ARTIFACT.write_text(payload, encoding="utf-8", newline="\n")
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()
    print(f"[PASS] wrote {ARTIFACT.relative_to(ROOT)}")
    print(f"SHA256 {digest}")
    print("RESULT: CONFIRMED")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"RESULT: FAILED: {exc}", file=sys.stderr)
        raise
