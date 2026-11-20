# EXP-013 results summary (generated from artifacts/results.json by make_summary.py)

Outcomes only: no statement about realizability or about the theorem. Betti entries b(i,j) = rank of the free module of homological degree i in degree j. d is the degree of the endomorphism; the scaled table sends b(i, j) to b(i, d j).

## Gates and predictions

- G1: passed {"passed": true, "failing_cases": []}
- G2: passed {"passed": true, "compared": 20, "failing_cases": [], "modules_without_two_instruments": [], "cases_not_run": []}
- G3: passed {"passed": true, "exit_code": 0, "last_line": ".........                                                                [100%]"}
- P1: {"holds": true, "cases_run": 10, "cases_expected": 10, "cases_not_run": [], "failing_cases": [], "cases_without_both_instruments": [], "lengths_S": {"S1": {"uhlib": 216, "singular": 216, "expected": 216}, "S2": {"uhlib": 512, "singular": 512, "expected": 512}, "S6": {"uhlib": 729, "singular": 729, "expected": 729}, "S4": {"uhlib": 1000, "singular": 1000, "expected": 1000}, "S3": {"uhlib": 1728, "singular": 1728, "expected": 1728}, "S5": {"uhlib": 4096, "singular": 4096, "expected": 4096}, "S7": {"uhlib": 13824, "singular": 13824, "expected": 13824}}}
- P2: {"holds": true, "N1_decided_by_a_table": true, "per_case": {"N1": {"pair_degree": 10, "tables": {"singular_phi": [[0, 0, 1], [1, 10, 2], [2, 20, 1]]}, "pure": {"singular_phi": false}, "uhlib_status": "module not finite within degree 42", "uhlib_dims": [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 34, 38, 41, 44, 46, 48, 49, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50], "singular_length": null, "compare_uhlib": {"table_is_scaled_table": null, "length_is_d3_times": null}, "compare_singular": {"table_is_scaled_table": false, "length_is_d3_times": null}}, "N2": {"pair_degree": 10, "tables": {"uhlib_phi": [[0, 0, 1], [1, 10, 2], [2, 33, 6], [2, 34, 3], [3, 34, 1], [3, 35, 6], [3, 36, 1]], "singular_phi": [[0, 0, 1], [1, 10, 2], [2, 33, 6], [2, 34, 3], [3, 34, 1], [3, 35, 6], [3, 36, 1]]}, "pure": {"uhlib_phi": false, "singular_phi": false}, "uhlib_status": "computed", "uhlib_dims": [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 34, 38, 41, 44, 46, 48, 49, 50, 50, 50, 49, 48, 46, 44, 41, 38, 34, 30, 25, 20, 14, 8, 1], "singular_length": 973, "compare_uhlib": {"table_is_scaled_table": false, "length_is_d3_times": false}, "compare_singular": {"table_is_scaled_table": false, "length_is_d3_times": false}}}, "note": "P2 concerns N1 only; N2 has no prediction"}

## Cases

| Case | p | d | Module | Table of M' (uhlib) | Table of M' (Singular) | Scaled table of M' | Table of phi^*M' (uhlib) | Table of phi^*M' (Singular) | Comparison (uhlib) | Comparison (Singular) | Time |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | 3 | 3 | U/(U(x^2 + y^2 + yx) + U(x^2 + yx - z)) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.5s] | b0,0=1; b1,6=2; b2,18=2; b3,24=1 | b0,0=1; b1,6=2; b2,18=2; b3,24=1; length 216 [0.12s] | b0,0=1; b1,6=2; b2,18=2; b3,24=1; length 216 [0.3s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.1 s |
| S2 | 3 | 4 | U/(U(x^2 + y^2 + yx) + U(x^2 + yx - z)) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.4s] | b0,0=1; b1,8=2; b2,24=2; b3,32=1 | b0,0=1; b1,8=2; b2,24=2; b3,32=1; length 512 [0.29s] | b0,0=1; b1,8=2; b2,24=2; b3,32=1; length 512 [0.6s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.3 s |
| S3 | 5 | 6 | U/(U x^2 + U y^2) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.4s] | b0,0=1; b1,12=2; b2,36=2; b3,48=1 | b0,0=1; b1,12=2; b2,36=2; b3,48=1; length 1728 [2.07s] | b0,0=1; b1,12=2; b2,36=2; b3,48=1; length 1728 [1.1s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 2.1 s |
| S4 | 5 | 5 | U/(U x^2 + U y^2) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.4s] | b0,0=1; b1,10=2; b2,30=2; b3,40=1 | b0,0=1; b1,10=2; b2,30=2; b3,40=1; length 1000 [0.62s] | b0,0=1; b1,10=2; b2,30=2; b3,40=1; length 1000 [0.3s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.6 s |
| S5 | 7 | 8 | U/(U x^2 + U y^2) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.4s] | b0,0=1; b1,16=2; b2,48=2; b3,64=1 | b0,0=1; b1,16=2; b2,48=2; b3,64=1; length 4096 [34.21s] | b0,0=1; b1,16=2; b2,48=2; b3,64=1; length 4096 [1.2s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 34.2 s |
| S6 | 3 | 3 | U/(U(x^3 + y z) + U(y^3 + x z)) | b0,0=1; b1,3=2; b2,9=2; b3,12=1; length 27 [0.01s] | b0,0=1; b1,3=2; b2,9=2; b3,12=1; length 27 [0.5s] | b0,0=1; b1,9=2; b2,27=2; b3,36=1 | b0,0=1; b1,9=2; b2,27=2; b3,36=1; length 729 [0.31s] | b0,0=1; b1,9=2; b2,27=2; b3,36=1; length 729 [0.3s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.3 s |
| S7 | 7 | 8 | U/(U x^3 + U y^3) | b0,0=1; b1,3=2; b2,9=2; b3,12=1; length 27 [0.01s] | b0,0=1; b1,3=2; b2,9=2; b3,12=1; length 27 [0.3s] | b0,0=1; b1,24=2; b2,72=2; b3,96=1 | b0,0=1; b1,24=2; b2,72=2; b3,96=1; length 13824 [1080.26s] | b0,0=1; b1,24=2; b2,72=2; b3,96=1; length 13824 [388.9s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 1080.3 s |
| T1 | 3 | 3 | U/(U x + U y^2) | b0,0=1; b1,1=1; b1,2=1; b2,4=1; b2,5=1; b3,6=1; length 3 [0.0s] | b0,0=1; b1,1=1; b1,2=1; b2,4=1; b2,5=1; b3,6=1; length 3 [0.4s] | b0,0=1; b1,3=1; b1,6=1; b2,12=1; b2,15=1; b3,18=1 | b0,0=1; b1,3=1; b1,6=1; b2,12=1; b2,15=1; b3,18=1; length 81 [0.02s] | b0,0=1; b1,3=1; b1,6=1; b2,12=1; b2,15=1; b3,18=1; length 81 [0.3s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.0 s |
| T2 | 5 | 6 | U/(U x + U y^2) | b0,0=1; b1,1=1; b1,2=1; b2,4=1; b2,5=1; b3,6=1; length 3 [0.0s] | b0,0=1; b1,1=1; b1,2=1; b2,4=1; b2,5=1; b3,6=1; length 3 [0.5s] | b0,0=1; b1,6=1; b1,12=1; b2,24=1; b2,30=1; b3,36=1 | b0,0=1; b1,6=1; b1,12=1; b2,24=1; b2,30=1; b3,36=1; length 648 [0.32s] | b0,0=1; b1,6=1; b1,12=1; b2,24=1; b2,30=1; b3,36=1; length 648 [0.3s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.3 s |
| T3 | 3 | 4 | U/(U x^2 + U x y + U y^2 + U z) | b0,0=1; b1,2=4; b2,3=2; b2,4=3; b3,5=2; length 3 [0.0s] | b0,0=1; b1,2=4; b2,3=2; b2,4=3; b3,5=2; length 3 [0.5s] | b0,0=1; b1,8=4; b2,12=2; b2,16=3; b3,20=2 | b0,0=1; b1,8=4; b2,12=2; b2,16=3; b3,20=2; length 192 [0.05s] | b0,0=1; b1,8=4; b2,12=2; b2,16=3; b3,20=2; length 192 [0.3s] | table is the scaled table, length is d^3 times | table is the scaled table, length is d^3 times | 0.1 s |
| N1 | 5 | 5 | U/(U x^2 + U y^2) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.4s] | b0,0=1; b1,10=2; b2,30=2; b3,40=1 | no table: module not finite within degree 42 (dimensions found: [1, 2, 4, 6, 9, 12, 16, 20, 25, 30, 34, 38, 41, 44, 46, 48, 49, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]) [0.22s] | b0,0=1; b1,10=2; b2,20=1; length None [0.3s] | table not decided, length not decided | table is NOT the scaled table, length not decided | 0.2 s |
| N2 | 7 | 5 | U/(U x^2 + U y^2) | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.0s] | b0,0=1; b1,2=2; b2,6=2; b3,8=1; length 8 [0.4s] | b0,0=1; b1,10=2; b2,30=2; b3,40=1 | b0,0=1; b1,10=2; b2,33=6; b2,34=3; b3,34=1; b3,35=6; b3,36=1; length 973 [0.58s] | b0,0=1; b1,10=2; b2,33=6; b2,34=3; b3,34=1; b3,35=6; b3,36=1; length 973 [1.5s] | table is NOT the scaled table, length is NOT d^3 times | table is NOT the scaled table, length is NOT d^3 times | 0.6 s |

## Per case: endomorphism and generators

### S1 (pair of degree 6)

- phi(x) = `y*z + x^3`; phi(y) = `y^3 + x*z`; phi(z) = `2*z^3` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `2*z + y^2 + x*y + x^2` ; `z + x*y + x^2`
- generators of the ideal of phi^*M' (the images of those generators): `y^2*z^2 + y^4*z + y^6 + x*y*z^2 + 2*x*y^3*z + x^2*z^2 + 2*x^3*y*z + x^3*y^3 + x^4*z + x^6` ; `z^3 + y^2*z^2 + y^4*z + x*y*z^2 + 2*x^3*y*z + x^3*y^3 + x^4*z + x^6`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 216

### S2 (pair of degree 8)

- phi(x) = `z^2 + x^4`; phi(y) = `z^2 + y^4`; phi(z) = `x^3*y^3*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `2*z + y^2 + x*y + x^2` ; `z + x*y + x^2`
- generators of the ideal of phi^*M' (the images of those generators): `y^8 + 2*x^3*y^3*z + x^4*y^4 + x^8` ; `2*z^4 + y^4*z^2 + x^3*y^3*z + x^4*y^4 + x^8`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 512

### S3 (pair of degree 12)

- phi(x) = `z^3 + x^6`; phi(y) = `z^3 + y^6`; phi(z) = `x^5*y^5*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^2` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `z^6 + 2*x^6*z^3 + x^12` ; `z^6 + 2*y^6*z^3 + y^12`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 1728

### S4 (pair of degree 10)

- phi(x) = `y*z^2 + x^5`; phi(y) = `y^5 + x*z^2`; phi(z) = `4*z^5` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^2` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `y^2*z^4 + 2*x^5*y*z^2 + x^10` ; `y^10 + 2*x*y^5*z^2 + x^2*z^4`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 1000

### S5 (pair of degree 16)

- phi(x) = `z^4 + x^8`; phi(y) = `z^4 + y^8`; phi(z) = `x^7*y^7*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^2` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `z^8 + 2*x^8*z^4 + x^16` ; `z^8 + 2*y^8*z^4 + y^16`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 4096

### S6 (pair of degree 9)

- phi(x) = `y*z + x^3`; phi(y) = `y^3 + x*z`; phi(z) = `2*z^3` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `y*z + x^3` ; `y^3 + x*z`
- generators of the ideal of phi^*M' (the images of those generators): `2*x*z^4 + x^9` ; `2*y*z^4 + y^9`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 729

### S7 (pair of degree 24)

- phi(x) = `z^4 + x^8`; phi(y) = `z^4 + y^8`; phi(z) = `x^7*y^7*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^3` ; `y^3`
- generators of the ideal of phi^*M' (the images of those generators): `z^12 + 3*x^8*z^8 + 3*x^16*z^4 + x^24` ; `z^12 + 3*y^8*z^8 + 3*y^16*z^4 + y^24`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): 13824

### T1 (table not pure, degrees multiplied by 3)

- phi(x) = `y*z + x^3`; phi(y) = `y^3 + x*z`; phi(z) = `2*z^3` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `y*z + x^3` ; `y^6 + 2*x*y^3*z + x^2*z^2`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): None

### T2 (same, multiplied by 6)

- phi(x) = `z^3 + x^6`; phi(y) = `z^3 + y^6`; phi(z) = `x^5*y^5*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `z^3 + x^6` ; `z^6 + 2*y^6*z^3 + y^12`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): None

### T3 (same for T, multiplied by 4)

- phi(x) = `z^2 + x^4`; phi(y) = `z^2 + y^4`; phi(z) = `x^3*y^3*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^2` ; `x*y` ; `y^2` ; `z`
- generators of the ideal of phi^*M' (the images of those generators): `z^4 + 2*x^4*z^2 + x^8` ; `z^4 + y^4*z^2 + x^4*z^2 + x^4*y^4` ; `z^4 + 2*y^4*z^2 + y^8` ; `x^3*y^3*z`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): None

### N1 (phi(z) = 0, outside the hypotheses)

- phi(x) = `x^5`; phi(y) = `y^5`; phi(z) = `0` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^2` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `x^10` ; `y^10`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): None

### N2 (commutator not central, outside the hypotheses)

- phi(x) = `y^3*z + x^5`; phi(y) = `y^5 + x^3*z`; phi(z) = `2*z^5 + 6*x*y*z^4 + 3*x^2*y^2*z^3 + 3*x^3*y^3*z^2 + 4*x^4*y^4*z` (computed as phi(x) phi(y) - phi(y) phi(x))
- generators of the ideal of M' (PBW): `x^2` ; `y^2`
- generators of the ideal of phi^*M' (the images of those generators): `y^6*z^2 + 3*x^2*z^4 + 4*x^3*y*z^3 + 6*x^4*y^2*z^2 + 2*x^5*y^3*z + x^10` ; `3*y^2*z^4 + y^10 + 4*x*y^3*z^3 + 6*x^2*y^4*z^2 + 2*x^3*y^5*z + x^6*z^2`
- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): None
