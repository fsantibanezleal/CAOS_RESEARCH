# Kernel-first native input audit

The first Taylor implementation and its partial full-table receipt are retained.
This additional variant is declared before implementation. The zero-count
target, pressure, table bytes and frozen live worker runtime stay fixed.

Retain native 0F1 midpoint evaluations and the second-derivative Taylor lower
bound from native-taylor-audit-declaration.md. For the value comparison,
instead of subtracting a global w'' bound, enclose K over the whole cell by

    K(mid) + [-E,E],
    E = |K'(mid)| R + pi^2 B R^2/2,  B=sum_j |c_j|.

This follows directly from |K''(x)|<=pi^2 B. Divide the resulting interval
by the independently enclosed positive K(0), take its exact absolute lower
bound, and square. The result is a nonnegative lower bound for w on the
entire closed cell, including when its kernel enclosure contains zero.
Constants, midpoint uncertainty, error radii and stored binary64 dyadic
comparisons all remain rigorous Arb enclosures. No finite sample substitutes
for the whole-cell remainder.

Repeat the 512-cell, thirty-second pilot; admit one 52,240-cell full run only
after complete pilot success and projected runtime <=600 seconds. The full
run has a 600-second cooperative budget and eight bisection levels. Existing
receipts may not be overwritten. This is an input audit within the shared
Python/FLINT/Arb trust base, not the required complete multidimensional cover.
