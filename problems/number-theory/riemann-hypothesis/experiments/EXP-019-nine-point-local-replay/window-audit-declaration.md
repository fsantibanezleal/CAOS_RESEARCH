# Additional EXP-019 input obligation: window normalization

Declared 2026-10-03 before this audit computation. The full local cover is
already running, with frozen code and unchanged bindings. In parallel with
it, verify the other numerical input of EXP-018: H(v)>=3362285207/5000000000
and admissibility of the exact seven-term window.

Use an independently expressed 256-bit Arb evaluation of the closed
integrals I1=integral v, I2=integral v^2 and J=double integral |s-t|v(s)v(t).
Derive the J formula from the second-order ODE for integral |s-t|cos(as) ds;
cross-check symmetry of the resulting bilinear form. Use Arb's native sinc
for this scalar audit, separately from the imported sinc derivative series.
Evaluate positivity and v'(s)/s on 4096 closed cells of [0,1/2], with exact
rational endpoints. The computation budget is ten CPU minutes. Retain any
failed sign/enclosure; do not replace it with a float check.

PASS establishes the numerical window input with explicit Arb trust. It
does not by itself validate the unconditional pair-correlation theorem or
the operator construction. The manuscript must cite and describe those
analytic dependencies. This audit cannot upgrade incomplete local coverage.
