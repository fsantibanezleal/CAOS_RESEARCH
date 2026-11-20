"""Second instrument of EXP-007: Singular 4.3.2 (Plural) in WSL, one script per stored space.

The script generator, the output parser and the WSL runner are those of EXP-005 (`exp005_singular`, which imports nothing from
`uhlib` and nothing from the first instrument); this file only turns a stored basis of W (coefficients "n/d" strings over the
rationals) into the relations of the cyclic module U / (U f + U g).  The Hilbert function of the module is rebuilt from
Singular's Betti table (alternating sum, its own dim U_n formula).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "EXP-005-characteristic-two-machine-checks"
if str(SIBLING) not in sys.path:
    sys.path.append(str(SIBLING))

import exp005_singular as Sg  # noqa: E402

build_script = Sg.build_script
parse_output = Sg.parse_output
hilbert_from_table = Sg.hilbert_from_table
dim_u = Sg.dim_u

QQ_RECORD = {"name": "QQ", "uhlib_name": "QQ", "char": 0, "degree": 1, "modulus": None}


def relations_of(basis):
    """Relations [[component, [i, j, k], coefficient], ...] of the two forms of a stored basis (component 0)."""
    return [[[0, list(m), c] for m, c in poly] for poly in basis]


def run_space(name, basis, script_dir, timeout=1200):
    """Singular's Betti table {(i, j): rank} of U / (U f + U g) over the rationals; (table, seconds, error)."""
    return Sg.run_case(name, QQ_RECORD, 1, relations_of(basis), script_dir, timeout=timeout)
