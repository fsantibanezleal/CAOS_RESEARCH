# EXP-001 verdict: CONFIRMED. Every finite fact used by the note holds for mu = 2, 3, 4

Date: 2026-11-24. Exact arithmetic, one instrument (the script `run.py`, standard library only). The hypothesis file
was written after the run and says so.

- H1 confirmed: the maximum of p_mu(B)/p_1(B) is at rank one and equals 3/2, 7/4, 15/8 = 2 - 2^(1-mu).
- H2 confirmed: the Fourier sum is positive at B of rank 2 (mu = 2, 3, 4) and of rank 4 (mu = 4).
- H3 confirmed: all three spanning statements, with full dimension mu^2.
- H4 confirmed: six maximal cliques of four vertices.
- H5 confirmed: connected, with a triangle.

Limits. One instrument; the counts for mu = 2 were also obtained by hand before the run. Nothing here is a proof for
general mu. The experiment adds no statement of its own: it guards the finite steps of Propositions 5.2 and 5.4 of
the note `context/2026-11-24-boolean-ladder-and-the-two-cases.md`.
