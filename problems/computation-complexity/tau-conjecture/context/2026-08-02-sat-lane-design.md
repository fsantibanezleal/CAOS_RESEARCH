# RL-7 design note: deciding the residual [8,9] case by SAT/SMT

Dated 2026-08-02 (round 7). Design only; no run. Companion to EXP-006,
whose case-split reduces the 8-gate question to: does an 8-gate 6-rooter
exist whose FINAL gate is $+$ or $-$ (the $\times$ case being decided
exactly by the co-occurrence scan)?

## The residual statement (assuming EXP-006 part 1 returns empty)

Exists a normalized SLP with gates $g_1, \dots, g_8$ over inputs
$\{-1, 1, x\}$, ops in $\{+, -, \times\}$, with $g_8 \in \{+, -\}$ and at
least one operand of $g_8$ equal to $g_7$'s value, whose output has 6
distinct integer roots. (Final-gate structure by the EXP-006 claim 1;
$g_8 = \times$ excluded by the scan.)

## Encoding options, with soundness classes

1. **QF_NIA (Z3/cvc5), fully sound both ways.** Unknowns: for each gate,
   a one-hot op selector and operand selectors over earlier indices
   (structure variables, finite); six unknown integer roots
   $r_1 < r_2 < \dots < r_6$ (symmetry-broken by ordering); for each
   root, evaluation variables $e_{i,j}$ = value of gate $j$ at $x = r_i$,
   with the gate semantics as equalities
   ($e_{i,j} = e_{i,l(j)} \pm e_{i,r(j)}$ or product per the selector)
   and $e_{i,8} = 0$. No coefficient variables at all: evaluation avoids
   representing the polynomial. UNSAT would prove the residual case
   empty OVER ALL of $\mathbb{Z}$; SAT gives a witness program + roots.
   Risk: nonlinear integer arithmetic is undecidable in general; the
   solver may return unknown or diverge. Structure space is small
   ($\le 3 \cdot \binom{10}{2}$-ish per gate), so the combinatorial part
   is easy; the products over unbounded $r_i$ are the hard part.
2. **Bounded-root variant, sound as a partial decision.** Add
   $|r_i| \le R$ (say $R = 32$). SAT closes the window; UNSAT proves
   only "no 8-gate 6-rooter with all roots in $[-R, R]$ ending in
   $\pm$": a window-exact statement to report honestly, mirroring the
   EXP-006 part 2 framing. All census evidence has record roots in
   $[-3, 3]$, so this variant carries real evidential weight while
   remaining labeled partial.
3. **Bit-blasted SAT (Fuhs--Schneider-Kamp style).** Fixed-width
   integers with overflow flags forced false: sound for UNSAT within
   the width, same partiality caveat as (2), likely fastest in
   practice; needs a careful width argument for the evaluation chain
   ($|e_{i,j}| \le (R + 2)^{2^{j}}$-scale, so width $\sim 2^8 \log R$:
   large but bit-blastable at $R \le 8$; at $R = 32$ prefer (1)/(2)
   via SMT).

## Plan for EXP-007 (when actioned)

1. Implement encoding (1) in Z3 (python bindings; add `z3-solver` to
   the repo requirements-dev if absent: isolated venv rule).
   Symmetry-break: gate operand ordering for commutative ops; root
   ordering; optionally force gate 7 used by gate 8 (the claim-1
   normalization) and forbid recomputing inputs/earlier values
   (normalization lemmas) to shrink the space.
2. Run (2) first at $R = 32$ with a 2 h budget (expected fast); then
   attempt (1) unbounded with a 12 h budget and `unknown` as an
   acceptable recorded outcome.
3. Any SAT hit is replayed through tclib exactly (the witness is an
   explicit program) before being believed; an UNSAT from (1) closes
   min-$\tau$(6 roots) = 9 and ships as a Zenodo new version of the
   census paper together with EXP-006.

## Why not just canonicalize and run depth 8 (TCB-005)?

The depth-8 frontier is ~$10^9$ states; even with a 4x orbit quotient
and a compiled backend this is days-scale and memory-hostile, while the
residual question after EXP-006 is far narrower than the full census
(it fixes the final two gates' shape). SAT attacks exactly the narrowed
question. The full depth-8 census (which would also give $z_{\max}(8)$,
not just the 6-rooter threshold) remains TCB-005's larger goal.
