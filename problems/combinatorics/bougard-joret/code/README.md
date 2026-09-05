# Code ownership

The self-contained exact checker is currently `../experiments/EXP-001-tree-strip/run.py`.
No reusable package has been created for one experiment. A regression replay lives in `tests/test_bougard_joret_tree_strip.py` and writes only to temporary paths. Promote shared logic here when a second experiment reuses it.
