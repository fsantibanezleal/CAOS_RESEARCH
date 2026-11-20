# EXP-005 results summary

Generated from `artifacts/results.json` by `make_summary.py`; never edited by hand. The hypothesis is `hypothesis.md` (frozen). Counts only: the verdict is written by the coordinating session.

## Gates

| Gate | Outcome | Counts |
|---|---|---|
| G1 | PASSED | `{"compared": 35, "degrees_compared": 19, "same_subspace_as_EXP003": 35, "failing_cases": []}` |
| G2 | PASSED | `{"compared": 160, "degrees": "0..12", "per_field": {"GF(2)": 40, "GF(2^2)": 40, "GF(2^4)": 40, "GF(32003)": 40}, "failing_cases": []}` |
| G3 | PASSED | `{"singular": "Singular for x86_64-Linux version 4.3.2 (4330, 64 bit) Apr  1 2024 04:44:00", "sample_cases": 75, "agree": 75, "per_sample": {"C2a|GF(2)|first 10": 10, "C2a|GF(2^2)|first 10": 10, "C2e|GF(2)|first 10": 10, "C2b|GF(2^4)|first 5": 5, "C3|GF(2^4)|first 40": 40}, "failing_cases": [], "singular_errors": [], "unfinished": [], "c4_modules": 24, "c4_failing": [], "c4_i1_i2_tables_agree": 13, "c4_i2_hilbert_consistent": 24}` |
| G4 | PASSED | `{"exit_code": 0, "last_line": ".............                                                            [100%]"}` |

## Totals per family and field

| Family | Field | Cases | Finite length | Eventually constant | By value | Growing | Unclassified | Unfinished |
|---|---|---|---|---|---|---|---|---|
| C1a | GF(2) | 35 | 0 | 29 | `{"2": 29}` | 6 | 0 | 0 |
| C1b | GF(2) | 651 | 0 | 530 | `{"4": 530}` | 121 | 0 | 0 |
| C1c | GF(2) | 63 | 0 | 0 | `{}` | 63 | 0 | 0 |
| C2a | GF(2) | 120 | 0 | 116 | `{"8": 116}` | 4 | 0 | 0 |
| C2a | GF(2^2) | 120 | 0 | 119 | `{"8": 119}` | 1 | 0 | 0 |
| C2a | GF(2^4) | 120 | 0 | 120 | `{"8": 120}` | 0 | 0 | 0 |
| C2b | GF(2) | 120 | 0 | 116 | `{"12": 116}` | 4 | 0 | 0 |
| C2b | GF(2^2) | 120 | 0 | 119 | `{"12": 119}` | 1 | 0 | 0 |
| C2b | GF(2^4) | 120 | 0 | 120 | `{"12": 120}` | 0 | 0 | 0 |
| C2c | GF(2^4) | 10 | 0 | 10 | `{"18": 10}` | 0 | 0 | 0 |
| C2d | GF(2^4) | 10 | 0 | 10 | `{"24": 10}` | 0 | 0 | 0 |
| C2e | GF(2) | 20 | 0 | 18 | `{"12": 18}` | 2 | 0 | 0 |
| C2e | GF(2^2) | 20 | 0 | 20 | `{"12": 20}` | 0 | 0 | 0 |
| C2e | GF(2^4) | 20 | 0 | 20 | `{"12": 20}` | 0 | 0 | 0 |
| C2f | GF(2^4) | 20 | 0 | 20 | `{"6": 20}` | 0 | 0 | 0 |
| C2g | GF(2^4) | 5 | 0 | 5 | `{"12": 5}` | 0 | 0 | 0 |
| C3 | GF(2^4) | 40 | 39 | 1 | `{"1": 1}` | 0 | 0 | 0 |

## C3 per shape (a, b, e)

| Shape | Cases | Finite length | Eventually constant | Growing | Unclassified | Unfinished |
|---|---|---|---|---|---|---|
| (1, 3, 2) | 10 | 10 | 0 | 0 | 0 | 0 |
| (1, 3, 3) | 10 | 10 | 0 | 0 | 0 | 0 |
| (1, 3, 4) | 10 | 9 | 1 | 0 | 0 | 0 |
| (2, 4, 2) | 10 | 10 | 0 | 0 | 0 | 0 |

## Predictions

- P1 (no case of C1 or C2 has finite length): holds. 0 finite length of 1574 done cases.
- P2 (b = a + 1 cases): value clause holds: 1372 eventually constant, 1372 with the S2 value, 0 with another value; no unclassified: holds (0); GF(16) share growing: holds (0 of 305, share 0.0); C1c all grow: holds (63 of 63).
  - growing by field over the b = a + 1 cases (growing, cases): `{"GF(2)": [137, 946], "GF(2^2)": [2, 260], "GF(2^4)": [0, 305]}`
  - GF(16) growing by family (growing, cases): `{"C2a": [0, 120], "C2b": [0, 120], "C2c": [0, 10], "C2d": [0, 10], "C2e": [0, 20], "C2f": [0, 20], "C2g": [0, 5]}`
- P3 (at least 8 of 10 finite length per shape): (1, 3, 2): 10 of 10 (holds); (1, 3, 3): 10 of 10 (holds); (1, 3, 4): 9 of 10 (holds); (2, 4, 2): 10 of 10 (holds).
- P4 (the Betti table of U/U(x^e, y^e)): holds; 24 modules, 0 on the wrong side [].

## P4 per module

| Module | Predicted pure | Finite length | Pure table (first instrument) | Pure table (Singular) | Hilbert function is the pure one | Tables agree |
|---|---|---|---|---|---|---|
| C4|GF(11)|e6 | False | False | False | False | False | None |
| C4|GF(11)|e7 | False | False | False | False | False | None |
| C4|GF(13)|e6 | True | True | True | True | True | True |
| C4|GF(13)|e7 | False | False | False | False | False | None |
| C4|GF(17)|e6 | True | True | True | True | True | True |
| C4|GF(17)|e7 | True | True | True | True | True | True |
| C4|GF(19)|e6 | True | True | True | True | True | True |
| C4|GF(19)|e7 | True | True | True | True | True | True |
| C4|GF(2)|e6 | False | False | False | False | False | None |
| C4|GF(2)|e7 | False | False | False | False | False | None |
| C4|GF(23)|e6 | True | True | True | True | True | True |
| C4|GF(23)|e7 | True | True | True | True | True | True |
| C4|GF(29)|e6 | True | True | True | True | True | True |
| C4|GF(29)|e7 | True | True | True | True | True | True |
| C4|GF(3)|e6 | False | False | False | False | False | None |
| C4|GF(3)|e7 | False | False | False | False | False | None |
| C4|GF(31)|e6 | True | True | True | True | True | True |
| C4|GF(31)|e7 | True | True | True | True | True | True |
| C4|GF(5)|e6 | False | False | False | False | False | None |
| C4|GF(5)|e7 | False | False | False | False | False | None |
| C4|GF(7)|e6 | False | False | False | False | False | None |
| C4|GF(7)|e7 | False | False | False | False | False | None |
| C4|QQ|e6 | True | True | True | True | True | True |
| C4|QQ|e7 | True | True | True | True | True | True |

## Reading notes

- The seed of a random case is 20261120 + its index within its (family, field) list (within C3: its index 0 to 39 in the order of the shapes).
- For a module that is not of finite length at the degree bound, the first instrument has no Betti table by Tor; the table is then judged by the Hilbert function (a module with the pure table has the pure Hilbert function) and by Singular's table.
- P2's 5 percent clause is evaluated over all GF(16) cases of C2 with b = a + 1 pooled; the per-family counts are listed above.
- Wall time of the commands (seconds): `[{"command": "gates", "seconds": 22.4}, {"command": "cases", "seconds": 20.5}]`; total 42.9.
