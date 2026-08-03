# EXP-007 verdict: CONFIRMED: no 8-gate seven-rooter via multiplication; the digit ladders measured; prediction 2 refuted

Run 2026-08-02, 3 h 07 min (budget 3.5 h), all 25,844,905 depth-6 states,
exact arithmetic; internal anchor: the hit count at union $\ge 6$
re-derived EXACTLY as EXP-006's 408. Raw output: `artifacts/union7.json`.

## Question 1 (TCB-025): DECIDED: max union = 6

Every one of the 408 final-multiplication hits has union size exactly 6
(histogram: $\{6: 408\}$). Hence **no 8-gate polynomial with final gate
$\times$ has 7 distinct integer roots**; combined with EXP-006:
$z_{\max}(8) = 6$ OR a 7-plus-rooter at 8 gates ends in $\pm$ (the SAT
lane's residual shape). The seven-root threshold currently sits in
$[8, 10]$: 8 only via a final $\pm$; upper witness at 10 gates (append
$\times (x - 4)$ to the 8-gate six-rooter, whose state already contains
the constant 4: one subtraction + one multiplication).
Prediction 1 CONFIRMED (our first emptiness-style prediction to survive,
stated after three refutals with explicitly moderate confidence).

## Question 2 (V9): the digit ladders, exact through $\tau = 7$

$$z^{(2,1)}_{\max}(\tau) = 1, 2, 2, 2, 2, 3, 4 \qquad
  z^{(3,1)}_{\max}(\tau) = 1, 1, 1, 2, 2, 3, 3 \quad (\tau = 1..7).$$

**Prediction 2 REFUTED** (fourth refutation of a structural judgment):
we predicted odd-root maximum 3 at $\tau \le 7$; the census returns 4.
The mechanism, reconstructed as an explicit witness [D]:
$(x^2-1)(x^2-9)$ at exactly 7 gates ($x^2$; $x^2{-}1$; $2$; $4$; $8$;
$x^2{-}9 = (x^2{-}1) - 8$; product), roots $\{\pm 1, \pm 3\}$: ALL FOUR
odd. The digit-restricted world has its own record mechanism: symmetric
products $\prod (x^2 - (2k+1)^2)$ whose roots are all odd: the digit
census is NOT simply a shadow of the full census (the full-record
polynomials, with roots crowding $\{0,\pm1,\pm2\}$, are digit-poor; the
digit records are different polynomials).
Reading: the SUFFICIENT form of the conjecture (Rojas digit form) has,
at the bottom, slower growth (4 vs 6 at $\tau \le 7$... precisely:
$z_{\max}(7) = 5$ vs $z^{(2,1)}_{\max}(7) = 4$) but its own extremal
family; measuring both ladders per depth is now standard
instrumentation.

## Question 3 (TCB-026): the punctured five-rooter anatomy

All 67 five-rooter polynomials saved and factored. The two punctured
patterns are realized by ONE mechanism family (up to sign/reflection):
$$\pm x^2 (x^2 - 1)(x - 2)(x - 4) \quad \text{roots } \{-1, 0, 1, 2, 4\}
\text{ (and its reflection } \{-4, -2, -1, 0, 1\}).$$
Structure: a product of TWO split quadratics with DIFFERENT centers:
$(x^2 - 1)$ (DOS at center 0) and $(x-2)(x-4) = (x-3)^2 - 1$ (DOS at
center 3), times $x^2$. The hole at 3 is the center of the second
quadratic: punctured sets are two-center DOS products, and the missing
point is a center. This closes TCB-026 with a clean mechanism statement
[D from the factored witnesses].

## Adversarial validation record

- Internal anchor: 408 hits reproduced exactly (EXP-006 agreement).
- Frontier gates: all depth 1-6 state counts exact.
- The odd-ladder witness $(x^2-1)(x^2-9)$ verified by direct gate count
  and exact evaluation [D]; the ladder VALUES come from the census
  catalog (decision-complete by EXP-001..004 premises).
- Smoke: zero hits one depth down (known answer), digit pass exercised.

## How could this be wrong?

Same soundness base as EXP-006 (last-gate lemma + census anchors), plus
the digit pass being a pure function of stored root sets. The single
new risk: the union histogram depends on the same root-set memo as the
hit detection: hedged by the 408 anchor agreement and the round-3 sympy
cross-check of the root-counting layer.

## Consequences for the strategy

- $z_{\max}(8)$ is pinned to: 6, unless a final-$\pm$ 8-gate 7-rooter
  exists: the SAT lane's residual question, now sharper (encode final
  gate $\pm$, 7 roots).
- The digit census (V9) has its first surprise and its own record
  family; TCB-027 (mod-p Frobenius-ceiling instrumentation) gains
  motivation: the odd-record family IS the reduction mod 2 of the
  $\{\pm1,\pm3\}$ pattern.
- Paper v0.03 material accumulated (seven-rooter exclusion, digit
  ladders + refuted prediction, punctured anatomy, V10 narrative):
  publish DELIBERATELY: queued to ship together with the $z_{\max}(8)$
  resolution rather than immediately (R3 discipline).
