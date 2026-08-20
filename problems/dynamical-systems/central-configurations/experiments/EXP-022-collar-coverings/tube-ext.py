"""EXP-022 part (d2b): tube extension, w in [1/8, 7/32].

Reuses tube.py's verified chart (entries analytic for w > rho/2; here
w >= 1/8 > 3/64 >= rho/2) with the seed extended DOWN to w = 1/8, closing
the collision band {|u-p| <= 1/16, |f| <= 1/16} of A_uplow for w >= 1/8.
The w < 1/8 remainder is the deep-tube chart (declared pending). Both
angle charts run, same budgets and criteria as the original tube runs.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("tube", HERE / "tube.py")
tube = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tube)
pl = tube.pl

def main():
    resume = "--resume" in sys.argv
    seed = [((F(1, 8), F(7, 32)), (F(-3), F(3)), (F(-1), F(1)), (F(0), F(3, 32)))]
    for sgn in (1, -1):
        nm = f"tubeext-{'R' if sgn == 1 else 'L'}"
        pl.run_covering(
            nm, seed,
            tube.entry_factory(sgn, "iv"),
            tube.entry_factory(sgn, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
