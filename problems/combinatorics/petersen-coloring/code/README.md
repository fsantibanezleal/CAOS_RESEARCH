# pcclib

Standard-library Python package for the Petersen coloring record.

| module | what |
|---|---|
| `graphs.py` | `Graph` container, edge-list loader, Putman digest convention, Petersen graph, `K4`, prism, flower snarks, the 4-pole `F` |
| `invariants.py` | connectivity, girth, exact edge connectivity (unit max-flow), exhaustive cycle-separating cuts below a bound |
| `cnf.py` | CNF builder with named variables, exactly-one, at-least/at-most-two, sequential-counter at-most-k |
| `encoders.py` | Petersen coloring, normal k-edge-coloring (plain, strong, with defect bound), Berge-Fulkerson, Berge covers, Fan-Raspaud, cycle double covers, nowhere-zero flows, proper colorings |
| `checkers.py` | independent witness checkers that read only the graph and the decoded witness |
| `solver.py` | CaDiCaL in WSL with DRAT proofs, drat-trim verification, hashes and timings |

Tests: `.\.venv\Scripts\python.exe -m pytest problems\combinatorics\petersen-coloring\code\tests -q`
(the solver test needs WSL with `/usr/bin/cadical` and the shared drat-trim binary).
