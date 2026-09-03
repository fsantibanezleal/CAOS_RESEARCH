"""pcclib: exact tooling for the Petersen coloring counterexample record.

Standard library only. Graphs are simple cubic graphs given as sorted edge lists on vertices
0..n-1. Every decision is made through a CNF written by `encoders`, solved by CaDiCaL inside WSL
with a DRAT proof (`solver`), and every positive answer is decoded and re-verified by a checker in
`checkers` that never reads the CNF.
"""

from . import checkers, cnf, encoders, graphs, invariants, solver

__all__ = ["checkers", "cnf", "encoders", "graphs", "invariants", "solver"]
