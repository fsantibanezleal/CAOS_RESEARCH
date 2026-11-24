# EXP-002 verdict: CONFIRMED. The closed forms agree with exhaustive counts for mu <= 4 and satisfy the inequality for mu <= 40

Date: 2026-11-24. Exact arithmetic, one instrument (`run.py`, standard library only).

- H1, H2, H3 confirmed in the nine cases (mu, j) with mu <= 4.
- H4 confirmed for mu = 2..40: equality at j = 1 only.

Limits. One instrument. The exhaustive part stops at mu = 4 (65,536 matrices); above it only the closed forms are
evaluated, so the experiment guards the algebra of the note, not the lemma itself for larger mu. The experiment adds
no statement: the theorem is proved in the note for every mu.
