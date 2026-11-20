"""Second instrument of EXP-008: Singular 4.3.2 (Plural) in WSL, one script per stored pure space.

The generator, the output parser and the WSL runner are those of EXP-005 (`exp005_singular`, which imports nothing from
`uhlib` and nothing from the first instrument), reached through EXP-006's thin layer; the scripts are generated from the
stored bases of results.json.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIBLING = HERE.parent / "EXP-006-odd-characteristic-below-2e"
if str(SIBLING) not in sys.path:
    sys.path.insert(0, str(SIBLING))

import exp006_singular as Sg6  # noqa: E402

build_script = Sg6.build_script
parse_output = Sg6.parse_output
relations_of = Sg6.relations_of


def run_space(name, field_record, basis, script_dir, timeout=1800):
    """Singular's Betti table {(i, j): rank} of U / (U f + U g) for a stored basis; (table, seconds, error)."""
    return Sg6.run_space(name, field_record, basis, script_dir, timeout=timeout)
