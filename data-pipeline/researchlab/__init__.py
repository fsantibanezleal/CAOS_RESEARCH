"""researchlab: the CAOS Research engine package.

The real engine of this repository is the experiment layer under problems/ (exact, hypothesis-
declared sympy runs); this package holds the offline export pipeline that bakes the program
registry and per-problem payloads into the JSON artifacts the static web app replays (ADR-0057
precompute lane), plus the generic io/core base.
"""

__version__ = "0.38.000"  # display X.XX.XXX; PEP 440 form in pyproject.toml
