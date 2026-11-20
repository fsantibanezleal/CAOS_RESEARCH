# EXP-011 results summary (generated from artifacts/results.json by make_summary.py)

Outcomes only: no statement about realizability or about the theorem. Betti entries b(i,j) = rank of the free module of homological degree i in degree j; pure means (1, 2, 2, 1) on (0, e, 3e, 4e).

## Gates and predictions

- G1: passed {"passed": true, "failing_cases": []}
- G2: passed {"passed": true, "compared": 16, "failing_cases": [], "singular_not_computed": [], "single_instrument_cases": []}
- G3: passed {"passed": true, "exit_code": 0, "last_line": "......                                                                   [100%]"}
- P1: {"holds": true, "cases_run": 16, "cases_expected": 16, "failing_cases": [], "cases_with_a_single_Betti_instrument": []}
- P2: {"holds": true, "per_case": {"N1": {"not_pure": true, "decided_by": "Betti table"}, "N2": {"not_pure": true, "decided_by": "Betti table"}, "N5": {"not_pure": true, "decided_by": "Betti table"}, "N3": {"hilbert_not_pure": true}, "N4": {"hilbert_not_pure": true}}}

## Cases

| Case | Family | (e, p) | f ; g | lambda | Identities | Hilbert function | Length | Betti (uhlib) | Betti (Singular) | Time (identities, Hilbert, uhlib Betti) |
|---|---|---|---|---|---|---|---|---|---|---|
| T1 | T | (3, 3) | `y*z + x^3` ; `y^3 + x*z` | 1 | all hold | equals h_e | 27 (e^3 = 27) | b0,0=1; b1,3=2; b2,9=2; b3,12=1 (pure) [0.01s] | b0,0=1; b1,3=2; b2,9=2; b3,12=1 (pure) [1.2s] | 0.0 s |
| T2 | T | (3, 3) | `y*z + x*z + x^3` ; `2*y*z + y^3 + x*z` | 2 | all hold | equals h_e | 27 (e^3 = 27) | b0,0=1; b1,3=2; b2,9=2; b3,12=1 (pure) [0.01s] | b0,0=1; b1,3=2; b2,9=2; b3,12=1 (pure) [1.1s] | 0.0 s |
| T3 | T | (5, 5) | `y*z^2 + x^5` ; `y^5 + x*z^2` | 1 | all hold | equals h_e | 125 (e^3 = 125) | b0,0=1; b1,5=2; b2,15=2; b3,20=1 (pure) [0.04s] | b0,0=1; b1,5=2; b2,15=2; b3,20=1 (pure) [5.1s] | 0.1 s |
| T4 | T | (5, 5) | `2*y*z^2 + x^5` ; `y^5 + 3*x*z^2` | 1 | all hold | equals h_e | 125 (e^3 = 125) | b0,0=1; b1,5=2; b2,15=2; b3,20=1 (pure) [0.05s] | b0,0=1; b1,5=2; b2,15=2; b3,20=1 (pure) [4.8s] | 0.1 s |
| T5 | T | (7, 7) | `y*z^3 + x^7` ; `y^7 + x*z^3` | 1 | all hold | equals h_e | 343 (e^3 = 343) | b0,0=1; b1,7=2; b2,21=2; b3,28=1 (pure) [0.14s] | b0,0=1; b1,7=2; b2,21=2; b3,28=1 (pure) [6.2s] | 0.2 s |
| T6 | T | (7, 7) | `3*y*z^3 + x^7` ; `y^7 + 5*x*z^3` | 1 | all hold | equals h_e | 343 (e^3 = 343) | b0,0=1; b1,7=2; b2,21=2; b3,28=1 (pure) [0.18s] | b0,0=1; b1,7=2; b2,21=2; b3,28=1 (pure) [7.2s] | 0.3 s |
| T7 | T | (7, 7) | `x*z^3 + x^7` ; `y*z^3 + y^7` | 6 | all hold | equals h_e | 343 (e^3 = 343) | b0,0=1; b1,7=2; b2,21=2; b3,28=1 (pure) [0.19s] | b0,0=1; b1,7=2; b2,21=2; b3,28=1 (pure) [4.5s] | 0.3 s |
| T8 | T | (9, 3) | `y*z^4 + x^9` ; `y^9 + x*z^4` | 1 | all hold | equals h_e | 729 (e^3 = 729) | b0,0=1; b1,9=2; b2,27=2; b3,36=1 (pure) [0.38s] | b0,0=1; b1,9=2; b2,27=2; b3,36=1 (pure) [7.6s] | 0.7 s |
| T9 | T | (9, 3) | `y*z^4 + x*z^4 + x^9` ; `y*z^4 + y^9` | 2 | all hold | equals h_e | 729 (e^3 = 729) | b0,0=1; b1,9=2; b2,27=2; b3,36=1 (pure) [0.49s] | b0,0=1; b1,9=2; b2,27=2; b3,36=1 (pure) [7.5s] | 0.9 s |
| T10 | T | (11, 11) | `y*z^5 + x^11` ; `y^11 + x*z^5` | 1 | all hold | equals h_e | 1331 (e^3 = 1331) | b0,0=1; b1,11=2; b2,33=2; b3,44=1 (pure) [0.75s] | b0,0=1; b1,11=2; b2,33=2; b3,44=1 (pure) [6.0s] | 0.9 s |
| T11 | T | (13, 13) | `y*z^6 + x^13` ; `y^13 + x*z^6` | 1 | all hold | equals h_e | 2197 (e^3 = 2197) | b0,0=1; b1,13=2; b2,39=2; b3,52=1 (pure) [1.61s] | b0,0=1; b1,13=2; b2,39=2; b3,52=1 (pure) [5.1s] | 1.8 s |
| T12 | T | (15, 3) | `y*z^7 + x^15` ; `y^15 + x*z^7` | 1 | all hold | equals h_e | 3375 (e^3 = 3375) | b0,0=1; b1,15=2; b2,45=2; b3,60=1 (pure) [3.59s] | b0,0=1; b1,15=2; b2,45=2; b3,60=1 (pure) [0.6s] | 4.7 s |
| T13 | T | (15, 5) | `y*z^7 + x^15` ; `y^15 + x*z^7` | 1 | all hold | equals h_e | 3375 (e^3 = 3375) | b0,0=1; b1,15=2; b2,45=2; b3,60=1 (pure) [3.84s] | b0,0=1; b1,15=2; b2,45=2; b3,60=1 (pure) [0.5s] | 5.8 s |
| G1 | G | (9, 3) | `y*z^4 + x^3*y^6 + x^9` ; `y^9 + x*z^4 + x^6*y^3 + x^9` | 1 | all hold | equals h_e | 729 (e^3 = 729) | b0,0=1; b1,9=2; b2,27=2; b3,36=1 (pure) [0.36s] | b0,0=1; b1,9=2; b2,27=2; b3,36=1 (pure) [8.4s] | 0.6 s |
| G2 | G | (5, 5) | `y*z^2 + 2*y^5 + x^5` ; `2*y^5 + x*z^2 + 3*x^5` | 1 | all hold | equals h_e | 125 (e^3 = 125) | b0,0=1; b1,5=2; b2,15=2; b3,20=1 (pure) [0.03s] | b0,0=1; b1,5=2; b2,15=2; b3,20=1 (pure) [1.7s] | 0.1 s |
| G3 | G | (15, 5) | `y*z^7 + x^10*y^5 + x^15` ; `y^15 + x*z^7 + 2*x^5*y^10 + x^15` | 1 | all hold | equals h_e | 3375 (e^3 = 3375) | b0,0=1; b1,15=2; b2,45=2; b3,60=1 (pure) [25.72s] | b0,0=1; b1,15=2; b2,45=2; b3,60=1 (pure) [0.6s] | 2.5 s |
| N1 | N | (5, 5) | `x^5` ; `y^5 + x*z^2` | not a multiple of z^e | FAILED: commutator_is_lambda_z_e | differs from h_e; dims [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12] | not finite within degree 25 | module not finite within degree 5e; no table | b0,0=1; b1,5=2; b2,10=1 [1.7s] | 0.0 s |
| N2 | N | (5, 5) | `y*z^2 + x^5` ; `y*z^2 + y^5` | not a multiple of z^e | FAILED: commutator_is_lambda_z_e | differs from h_e; dims [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13, 12] | not finite within degree 25 | module not finite within degree 5e; no table | b0,0=1; b1,5=2; b2,10=1 [1.7s] | 0.0 s |
| N3 | N | (5, 7) | `y*z^2 + x^5` ; `y^5 + x*z^2` | not a multiple of z^e | FAILED: A_B_central, commutator_is_lambda_z_e, syzygy_s1, syzygy_s2, third_relation | differs from h_e; dims [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 10, 9, 6, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3] | not finite within degree 25 | module not finite within degree 5e; no table | b0,0=1; b1,5=2; b2,15=3; b2,16=1; b3,17=3 [1.9s] | 0.0 s |
| N4 | N | (5, 3) | `y*z^2 + x^5` ; `y^5 + x*z^2` | not a multiple of z^e | FAILED: A_B_central, commutator_is_lambda_z_e, syzygy_s1, syzygy_s2, third_relation | differs from h_e; dims [1, 2, 4, 6, 9, 10, 12, 12, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12] | not finite within degree 25 | module not finite within degree 5e; no table | b0,0=1; b1,5=2; b2,11=2; b3,12=1 [4.6s] | 0.0 s |
| N5 | N | (9, 3) | `y*z^4 + x^9` ; `x*z^4 + x^6*y^3` | 1 | all hold | differs from h_e; dims [1, 2, 4, 6, 9, 12, 16, 20, 25, 28, 32, 34, 37, 38, 40, 40, 41, 40, 40, 38, 37, 34, 33, 30, 29, 26, 25, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24] | not finite within degree 45 | module not finite within degree 5e; no table | b0,0=1; b1,9=2; b2,22=1; b2,27=2; b3,28=1; b3,30=1 [7.7s] | 0.6 s |

Replacements of a non-coprime pair (G1, G3): {}
