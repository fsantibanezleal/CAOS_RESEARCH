# EXP-026: retain the multiplicity term in the mixed-Gram completion

Declared 2026-10-04 before code or computation. This is a bounded alternative
within the zero-proportion investigation. RH-F4 remains the primary analytic
focus; neither repository management nor the scientific mission changes.

Let U be a positive semidefinite unit-diagonal m-point Gram matrix and D be
diagonal with entries in {1,2}. Put X=U-I, C=min(X,tau), M=D^(-1/2) C D^(-1/2),
P=D^(1/2) U D^(1/2), and let J mark the diagonal entries equal to two.
For c>=max(1+tau,2+tau/2), test the retained completion inequality

    tr(phi_c(P))-tr(D^2)
      >= tr(Psi_tau(U)) + tr(C^2)-tr(M^2)
      >= tr(Psi_tau(U)) + (1/2)*tr(J*C^2).

The expression comes from EXP-025's source-attributed mixed completion; its
noncommutative proof is already recorded. This experiment does not claim that
the retained algebra or matrix method has new priority. The question is whether
this positive term admits a usable zero-counting lower bound.

First adversarial target: can it guarantee

    tr(phi_c(P))-tr(D^2) >= (1 + number_of_twos/(10*m))*tr(Psi_tau(U))

uniformly for actual Fourier-window point Grams? Test an isolated doubled
point at -R and two simple points at 0 and 1/2, using EXP-025's pinned positive
window. Establish the R->infinity family analytically, not from sampled zeros.

P1/P3: EXP-025 proof and its pinned window are the premises; EXP-016's trace
refinement already exists and is not rediscovered here. The local formal theorem
does not supply a multiplicity-dependent lower bound on the retained term.
P5: a decaying Fourier kernel can isolate a doubled point while a simple block
retains positive energy. This invariant is checked before any larger certificate.

PASS proves the complete retained inequality and resolves the adversarial
uniform-gain prediction by a proof plus exact/enclosed normalization controls.
A numerical pass alone proves no uniform inequality or proportion improvement.
If the proposed uniform factor is refuted, stop that factor-only route; a
pressure-paid geometric lower bound would be a separate future hypothesis.
FAIL is an algebra, sign, normalization or enclosure mismatch; retain it before
repair. Thirty seconds CPU, one worker, flushed receipt; a budget hit is
inconclusive. No parameter sweep or GPU work is justified.

No manuscript or stopping condition follows from a retained classical term or
an applicability obstruction. A new companion version requires a proved,
certified proportion gain with all analytic and counting inputs retained.
