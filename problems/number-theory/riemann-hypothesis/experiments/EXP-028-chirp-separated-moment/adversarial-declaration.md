# Exact exponent and window-loss refutation controls

Declared 2026-10-04 before this extension is computed. This remains EXP-028,
RH-F4; no optimization or new detector is introduced. The independent Mellin
route replaces the original unproved differentiated-Hankel assumptions.

Freeze theta=5339/10000, nu=349/10000, eta=1/100000 and tail increment A=4.
Reconstruct every dyadic exponent from gamma normalization, the actual three
l2 norms, the two attributed Bettin-Chandee monomials and its parameter
factor. Cover an exact rational grid in g,p,q with p,q<=nu-g and the break
points r=0,max(0,N0 exponent),p+q and far-tail scales. Check both monomials
against the proposed global bound at theta-eta. The analytic piecewise
linear argument, rather than this finite grid alone, supplies universality.
Derive signs of all N slopes before/after the contour change separately.
Check the corrected compact-window exponents exactly. Reject zero margin,
an overlarge smoothing loss, omitted separation cost, reversed parameter
factor, and an unconvergent tail. Thirty CPU seconds, stdlib Fraction only.

PASS is an exponent-accounting control, not a proof of zeta asymptotics or
external review. Preserve all receipts including failures. Commit the code
before execution; preserve earlier conditional receipts and their original
analytic_moment_theorem_proved=false flags.
