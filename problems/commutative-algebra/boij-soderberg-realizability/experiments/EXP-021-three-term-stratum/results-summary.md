# EXP-021 results summary (generated from artifacts/results.json by make_summary.py; do not edit)

Counts and members only. No statement about realizability is made here.

## Gates

- G3 (unit tests): passed (11 passed in 13.42s)
- G1 (controls): passed
- G2 (second instrument, Singular for x86_64-Linux version 4.3.2 (4330, 64 bit) Apr  1 2024 04:44:00): passed; 9 members, 9 agree and are pure in both instruments; errors none; failing none

### G1, every control count against the hypothesis

| Case | Item | Got | Hypothesis | Equal |
|---|---|---|---|---|
| K|5|3 | stages | [44175, 7526, 5684, 1664] | [44175, 7526, 5684, 1664] | yes |
| K|5|3 | found | 1664 | 1664 | yes |
| K|5|3 | tables | 1664 | 1664 | yes |
| K|5|3 | pure | 400 | 400 | yes |
| K|5|3 | pure_delta0 | 58 | 58 | yes |
| K|5|3 | pure_gamma_delta0 | 0 | 0 | yes |
| K|5|3 | first_pure | [866, 919] | [866, 919] | yes |
| K|5|3 | plain | 1736 | 1736 | yes |
| K|5|3 | stage3_delta0 | 180 | 180 | yes |
| K|5|3 | stage3_gamma_delta0 | 22 | 22 | yes |
| K|7|5 | stages | [316708, 64914, 18166, 212] | [316708, 64914, 18166, 212] | yes |
| K|7|5 | found | 212 | 212 | yes |
| K|7|5 | tables | 212 | 212 | yes |
| K|7|5 | pure | 64 | 64 | yes |
| K|11|7 | stages | [196061, 3249, 690, 0] | [196061, 3249, 690, 0] | yes |
| K|11|7 | found | 0 | 0 | yes |
| K|11|7 | tables | 0 | 0 | yes |
| K|11|7 | pure | 0 | 0 | yes |
| non-monic (5, 3) | members | 73447 | 73447 | yes |
| non-monic (5, 3) | stages | [60933, 3942, 8572, 0] | [60933, 3942, 8572, 0] | yes |
| non-monic (5, 3) | plain | 0 | 0 | yes |

## Cases

| Case | Members done / planned | Stages 0, 1, 2, 3 | Stage 3 | Tables | Pure | Status |
|---|---|---|---|---|---|---|
| (5, 3) complete | 59,049 / 59,049 | 44,175; 7,526; 5,684; 1,664 | 1,664 | 1664 | 400 | complete |
| (7, 5) random | 400,000 / 400,000 | 316,708; 64,914; 18,166; 212 | 212 | 212 | 64 | complete |
| (11, 7) random | 200,000 / 200,000 | 196,061; 3,249; 690; 0 | 0 | 0 | 0 | complete |
| (11, 3) complete | 43,046,721 / 43,046,721 | 35,798,729; 5,710,940; 1,494,122; 42,930 | 42,930 | 16 | 5 | complete |

### Case K|5|3: (e, p) = (5, 3), complete

- Members done: 59,049 of 59,049 planned (list of 59,049); blocks 3 of 3 of 20000 members; status complete.
- Syzygy classes (s1, s2) = (0, 1), block order [0, 1].
- Counts by stage 0, 1, 2, 3: 44,175, 7,526, 5,684, 1,664.
- Members with delta = 0 (index below 6561), stages 0 to 3: [5089, 654, 638, 180]; with gamma = delta = 0 (index below 729): [561, 82, 64, 22].
- Members with the pure Hilbert function by the plain staged test (no pattern): 1736.
- Members of stage 3: 1664 (1664 kept with their data).
- Betti tables computed: 1664 (rule: all); pure: 400; pure with delta = 0: 58; with gamma = delta = 0: 0.
- Tables that are not pure: 1264 members in 11 distinct tables; the most frequent: [[0, 0, 1], [1, 5, 2], [2, 15, 2], [2, 16, 1], [3, 16, 1], [3, 20, 1]], length 125 x 420; [[0, 0, 1], [1, 5, 2], [2, 15, 2], [2, 19, 1], [3, 19, 1], [3, 20, 1]], length 125 x 164; [[0, 0, 1], [1, 5, 2], [2, 15, 2], [2, 16, 1], [2, 17, 1], [3, 16, 1], [3, 17, 1], [3, 20, 1]], length 125 x 152.
- First pure indices: [866, 919, 2944, 2953, 2962, 2972, 2981, 2990].
- Throughput: 1.014 ms per member per worker (counting only); 1278 members per second of wall time (with the tables); 141.6 s of workers, 46.2 s of wall time; block seconds min and max [19.324, 20.457].

Pure member, index 866, digits [0, 0, 0, 1, 0, 1, 2, 0, 0, 2]:

    f = y^3*z - x*z^2 + x^2*y*z + x^5
    g = -y*z^2 + y^5

Betti table by uhlib (degree-wise rank): (0,0):1 (1,5):2 (2,15):2 (3,20):1; length 125.
Betti table by Singular: (0,0):1 (1,5):2 (2,15):2 (3,20):1; agree: True.

Pure member, index 919, digits [0, 0, 0, 1, 0, 2, 1, 0, 0, 1]:

    f = y^3*z + x*z^2 - x^2*y*z + x^5
    g = y*z^2 + y^5

Betti table by uhlib (degree-wise rank): (0,0):1 (1,5):2 (2,15):2 (3,20):1; length 125.
Betti table by Singular: (0,0):1 (1,5):2 (2,15):2 (3,20):1; agree: True.

Pure member, index 2944, digits [0, 0, 1, 1, 0, 0, 1, 0, 0, 1]:

    f = y^3*z + x*z^2 + x*y^4 + x^5
    g = y*z^2 + y^5

Betti table by uhlib (degree-wise rank): (0,0):1 (1,5):2 (2,15):2 (3,20):1; length 125.
Betti table by Singular: (0,0):1 (1,5):2 (2,15):2 (3,20):1; agree: True.

### Case K|7|5: (e, p) = (7, 5), random

- Members done: 400,000 of 400,000 planned (list of 244,140,625); blocks 20 of 20 of 20000 members; status complete.
- Syzygy classes (s1, s2) = (1, 2), block order [1, 2, 0].
- Counts by stage 0, 1, 2, 3: 316,708, 64,914, 18,166, 212.
- Members of stage 3: 212 (212 kept with their data).
- Betti tables computed: 212 (rule: all); pure: 64; pure with delta = 0: 64; with gamma = delta = 0: 63.
- Tables that are not pure: 148 members in 20 distinct tables; the most frequent: [[0, 0, 1], [1, 7, 2], [2, 21, 2], [2, 22, 1], [3, 22, 1], [3, 28, 1]], length 343 x 44; [[0, 0, 1], [1, 7, 2], [2, 21, 2], [2, 23, 1], [3, 23, 1], [3, 28, 1]], length 343 x 21; [[0, 0, 1], [1, 7, 2], [2, 21, 2], [2, 27, 1], [3, 27, 1], [3, 28, 1]], length 343 x 12.
- First pure indices: [4043, 4845, 8039, 17420, 20435, 29559, 31740, 41449].
- Throughput: 0.622 ms per member per worker (counting only); 13114 members per second of wall time (with the tables); 294.3 s of workers, 30.5 s of wall time; block seconds min and max [11.115, 13.52].

Pure member, index 4043, digits [1, 2, 4, 0, 3, 3, 0, 2, 3, 0, 4, 4]:

    f = 2*x*z^3 - x*y^6 - 2*x^3*y^2*z - 2*x^4*y^3 + x^7
    g = -y*z^3 + y^7 - x*y^2*z^2 - 2*x^3*y^4 + 2*x^5*z + x^6*y

Betti table by uhlib (degree-wise rank): (0,0):1 (1,7):2 (2,21):2 (3,28):1; length 343.
Betti table by Singular: (0,0):1 (1,7):2 (2,21):2 (3,28):1; agree: True.

Pure member, index 4845, digits [4, 4, 2, 1, 1, 1, 3, 3, 1, 2, 4, 3]:

    f = y^5*z - 2*x*z^3 + 2*x*y^6 - 2*x^2*y*z^2 + x^3*y^2*z + x^4*y^3 + x^7
    g = -2*y*z^3 + y^7 - x*y^2*z^2 + 2*x^2*y^3*z + x^3*y^4 - x^5*z - x^6*y

Betti table by uhlib (degree-wise rank): (0,0):1 (1,7):2 (2,21):2 (3,28):1; length 343.
Betti table by Singular: (0,0):1 (1,7):2 (2,21):2 (3,28):1; agree: True.

Pure member, index 8039, digits [3, 1, 0, 0, 1, 4, 2, 2, 2, 4, 4, 4]:

    f = 2*x*z^3 + 2*x^2*y*z^2 - x^3*y^2*z + x^4*y^3 + x^7
    g = -y*z^3 + y^7 - x*y^2*z^2 - x^2*y^3*z + 2*x^3*y^4 + x^5*z - 2*x^6*y

Betti table by uhlib (degree-wise rank): (0,0):1 (1,7):2 (2,21):2 (3,28):1; length 343.
Betti table by Singular: (0,0):1 (1,7):2 (2,21):2 (3,28):1; agree: True.

### Case K|11|7: (e, p) = (11, 7), random

- Members done: 200,000 of 200,000 planned (list of 33,232,930,569,601); blocks 10 of 10 of 20000 members; status complete.
- Syzygy classes (s1, s2) = (1, 2), block order [1, 2, 0, 3, 4].
- Counts by stage 0, 1, 2, 3: 196,061, 3,249, 690, 0.
- Members of stage 3: 0 (0 kept with their data).
- Betti tables computed: 0 (rule: all); pure: 0; pure with delta = 0: 0; with gamma = delta = 0: 0.
- First pure indices: none.
- Throughput: 0.829 ms per member per worker (counting only); 11904 members per second of wall time (with the tables); 165.9 s of workers, 16.8 s of wall time; block seconds min and max [16.418, 16.705].

### Case X|11|3: (e, p) = (11, 3), complete

- Members done: 43,046,721 of 43,046,721 planned (list of 43,046,721); blocks 2153 of 2153 of 20000 members; status complete.
- Syzygy classes (s1, s2) = (1, 2), block order [1, 2, 0, 3, 4].
- Counts by stage 0, 1, 2, 3: 35,798,729, 5,710,940, 1,494,122, 42,930.
- Members with delta = 0 (index below 4782969), stages 0 to 3: [3921713, 677192, 180080, 3984]; with gamma = delta = 0 (index below 531441): [423293, 84262, 23842, 44].
- Members of stage 3: 42930 (20000 kept with their data, the first in index order).
- Betti tables computed: 16 (rule: early); pure: 5; pure with delta = 0: 5; with gamma = delta = 0: 5.
- Tables that are not pure: 11 members in 2 distinct tables; the most frequent: [[0, 0, 1], [1, 11, 2], [2, 33, 2], [2, 34, 1], [2, 43, 1], [3, 34, 1], [3, 43, 1], [3, 44, 1]], length 1331 x 10; [[0, 0, 1], [1, 11, 2], [2, 33, 2], [2, 34, 1], [3, 34, 1], [3, 44, 1]], length 1331 x 1.
- First pure indices: [106184, 107155, 112979, 113464, 145685].
- Throughput: 1.525 ms per member per worker (counting only); 7719 members per second of wall time (with the tables); 65678.6 s of workers, 5576.6 s of wall time; block seconds min and max [14.652, 264.862].

Pure member, index 106184, digits [0, 0, 0, 0, 0, 1, 2, 1, 0, 1, 1, 2, 2, 2, 0, 2]:

    f = x*z^5 + x^3*y^2*z^3 - x^4*y^3*z^2 + x^5*y^4*z + x^11
    g = -y*z^5 + y^11 - x^2*y^3*z^3 - x^3*y^4*z^2 - x^4*y^5*z + x^5*y^6

Betti table by uhlib (degree-wise rank): (0,0):1 (1,11):2 (2,33):2 (3,44):1; length 1331.
Betti table by Singular: (0,0):1 (1,11):2 (2,33):2 (3,44):1; agree: True.

Pure member, index 107155, digits [0, 0, 0, 0, 0, 1, 2, 1, 0, 2, 2, 2, 2, 2, 0, 1]:

    f = -x*z^5 + x^3*y^2*z^3 - x^4*y^3*z^2 + x^5*y^4*z + x^11
    g = y*z^5 + y^11 - x^2*y^3*z^3 - x^3*y^4*z^2 - x^4*y^5*z - x^5*y^6

Betti table by uhlib (degree-wise rank): (0,0):1 (1,11):2 (2,33):2 (3,44):1; length 1331.
Betti table by Singular: (0,0):1 (1,11):2 (2,33):2 (3,44):1; agree: True.

Pure member, index 112979, digits [0, 0, 0, 0, 0, 1, 2, 2, 0, 1, 2, 2, 2, 1, 0, 2]:

    f = x*z^5 - x^3*y^2*z^3 - x^4*y^3*z^2 + x^5*y^4*z + x^11
    g = -y*z^5 + y^11 + x^2*y^3*z^3 - x^3*y^4*z^2 - x^4*y^5*z - x^5*y^6

Betti table by uhlib (degree-wise rank): (0,0):1 (1,11):2 (2,33):2 (3,44):1; length 1331.
Betti table by Singular: (0,0):1 (1,11):2 (2,33):2 (3,44):1; agree: True.

### Non-monic members at (5, 3)

Of the 132,496 normalized members of S(2; 0, 1), 59,049 have both leading coefficients nonzero and 73,447 do not; stages of the latter 0 to 3: [60933, 3942, 8572, 0]; with the pure Hilbert function by the plain staged test: 0.

## Predictions

- P1 (a pure pair at (11, 3), confirmed by both instruments): holds, 5 pure members, 3 confirmed by both instruments.
- P2 (the number of members of stage 3 is between 200 and 4000): does not hold, 42930 members of stage 3.
- P3 (the members with delta = 0 (index below 4782969) hold a pure pair): holds, 5 pure members with delta = 0 (first index 106184).
- P4 (no pure pair among the members with gamma = delta = 0 (index below 531441)): does not hold, 5 pure members with gamma = delta = 0 (first index 106184).
- P5 (of the Betti tables computed, between one tenth and six tenths are pure (given P1)): holds, 5 of 16 tables are pure (0.312).

## Time

- Wall time by family: {'K': 102.0, 'X': 4909.6}; total 5121.6 s.
