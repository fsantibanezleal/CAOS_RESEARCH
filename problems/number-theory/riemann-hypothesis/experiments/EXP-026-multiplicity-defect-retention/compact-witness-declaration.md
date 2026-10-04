# Stronger adversarial check: isolation within the pressure budget

Declared after the original controls and before this computation, 2026-10-04.
The original hypothesis and receipt remain unchanged.

The large-gap witness does not rule out a pressure-constrained lower bound.
Test one seven-point configuration: a doubled point at zero and six simple
points at distinct positive zeros of the pinned Fourier kernel. Seek six
disjoint sign-changing intervals on [1/2,8], with a fixed grid spacing 1/16;
bisect each interval to width at most 2^-40 using certified Arb signs.
IVT then supplies actual zero locations, not sampled near-zero points.

For all locations inside the six intervals, certify unit and weighted Gram
Gershgorin upper bounds below 1+tau and c respectively, certify strictly
positive simple-block energy, and check that the source's actual vector
pressure sum is below delta. At the exact roots the doubled row of U-I
vanishes, so the retained remainder is zero even with bounded pressure.

PASS proves a compact isolation obstruction to a positive remainder bound
depending only on multiplicity count, including that pressure budget. It
does not refute a joint bound using both the baseline local slack and the
retained remainder. FAIL means an unresolved sign, insufficient roots,
excess pressure or an uncertified spectral/energy bound. Twenty seconds CPU,
one worker, one fixed configuration; no gap/weight optimization. A budget
hit is inconclusive. No manuscript or zero-bound upgrade follows.
