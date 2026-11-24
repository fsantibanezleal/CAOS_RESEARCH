# P versus NP: from the algebraic lower bound towards Boolean circuits

Whether every problem whose solutions can be checked quickly can also be solved quickly is the P versus NP problem.
It is stated for Turing machines, and it is open. A weaker model, the arithmetic circuit, computes polynomials by
additions and multiplications and must be right for every value of the variables; its version of the problem asks
whether the permanent and the Hamiltonian cycle polynomial need circuits of more than polynomial size. On
2026-11-23 two proofs of that were announced, both written by AI systems and checked in Lean, neither yet read by a
human mathematician. They do not settle P versus NP, because a Boolean circuit only has to be right on the inputs 0
and 1.

Status of this program: opened 2026-11-24. It studies the statements that lie between the two models (circuits that
are right on 0 and 1 and whose polynomial has bounded degree in each variable) and a question the first proof leaves
open. Records: [RESUME](../../../../program/p-vs-np/RESUME.md), [plan](../../../../program/p-vs-np/plan.md),
[path map](../../../../program/p-vs-np/research-lines-2026-11-24.md),
[first note](../context/2026-11-24-boolean-ladder-and-the-two-cases.md).
