# EXP-002 results

Run: `python -I run.py` (CPython, standard library only), 2026-11-24. Output: `artifacts/run-output.txt`.

- mu = 2, 3, 4, every rank j of B: the counted p_1, the counted character sum over the invertible matrices and the
  counted p_mu equal the closed forms (nine cases, all agree).
- mu = 2..40, closed forms: the ratio at j = 1 is exactly 2 - 2^(1-mu), and every ratio at j >= 2 is strictly
  smaller. Largest ratio at j >= 2: 0.5, 0.9722, 1.1607, 1.2486, 1.2913 for mu = 2..6; the difference to the value at
  j = 1 stays above 2/3 up to mu = 40.
