# 8. Smoothness of the force against dissipation

Two September 2026 results sit at opposite corners of the same budget. Alpoge and Buckmaster prove
blowup for 2D Boussinesq with a **smooth** force and no viscosity. Cordoba, Martinez-Zoroa and Zheng
prove it with a **rough** force, $C^{1,\epsilon}$, and hypodissipation up to
$\alpha_0=0.0463$ in our convention. This page asks what our dissipative extension
([page 4](04-dissipation-and-the-frequency-cap.md)) says about the first schedule, and the answer is
that the two goods are bought from the same budget.

Everything here is exponent bookkeeping on published constants; the prediction at the end is ours and
is dated and falsifiable. Full derivation:
[`context/2026-09-16-smoothness-versus-dissipation.md`](../context/2026-09-16-smoothness-versus-dissipation.md).

> **Correction, 2026-09-17.** The rule `120 k <= Q` used below is a sufficient simplification
> in the published design, not a structural exchange rate. Transcribing the full force budget
> ([`2026-09-17-force-estimates-exponent-content.md`](../context/2026-09-17-force-estimates-exponent-content.md)) shows that
> the ratio floor the estimates actually force is `Q >= 9d + 42`, from the derivative range of the
> coefficient bounds, and that the margin is capped near `1/2` by the remainder and near `1/4` by the
> leading phase means at the published target. The bound `1/480` below therefore holds for the
> design as published, but not for every retuning: at one derivative the most favourable reading of
> the architecture reaches `3.69e-03` (ours). The conclusion, that the design stays at least ten
> times below the proved threshold, is unchanged and now rests on the full budget. The text below is
> kept as written.

## What their schedule fixes

From Alpoge-Buckmaster (3.7) and (3.8):

$$\lambda_q=\lambda_{q-1}^{\,Q_q},\qquad Q_q=Q^\ast+q,\qquad Q^\ast\ge200,\qquad
120\,k_q\le Q_q,$$

with $k_q$ the number of derivatives of the force controlled uniformly, and the amplitude rule whose
exact consequence they state,

$$|\Theta^{\rm seed}_q|\,e^{L_q}=\lambda_q^{-7/8}.$$

So a layer stops at $\lambda_q^{-7/8}$ and, by the amplification identity
$\nabla\vartheta(0)=\lambda\Theta\zeta$, deposits a gradient $A_{q+1}=\lambda_q^{1/8}$. Call the
exponent the **amplitude margin**, $\delta=1/8$.

The rule $120k_q\le Q_q$ is the price list: **each further derivative of the force costs another 120
in the frequency ratio**, and a $C^{\infty}$ force needs $k_q\to\infty$, which is why $Q_q$ grows with
the stage.

## What dissipation would charge

Our damping term $\nu(\lambda|\zeta|)^{2\alpha}$ against their growth rate $\sqrt A\sin\varphi$ gives,
at stage $q$,

$$\boxed{\;\alpha<\frac{\delta}{4Q_q}\;}$$

with an insertion angle of order one, and a factor $Q_{q-1}$ tighter with their own angle (3.10). In
our cascade notation this is just C2, $\alpha p<1/4$, with $p=Q_q/\delta$.

**$Q_q$ is unbounded, so no positive $\alpha$ survives every stage.** The cascade runs finitely many
stages and stops, and a finite cascade gives a finite gradient.

| with the published constants | |
|---|---|
| largest $\alpha$ the first stage carries | $1.55\times10^{-4}$ |
| the same with their own insertion angle | $7.70\times10^{-7}$ |
| stages before stalling at $\alpha=10^{-4}$ | 113 |
| frequency ratio compatible with $\alpha=0.0463$ | $0.675$, that is, below 1 |
| derivatives of the force affordable there | $0.006$, that is, none |

## Read the other way: what one derivative costs

Their rule $120k\le Q$ and the constraint $\alpha<\delta/(4Q)$ combine into

$$\alpha<\frac{\delta}{480\,k},$$

so even with the most generous margin the amplification identity allows, $\delta\to1$, **controlling a
single derivative of the force caps the exponent at $1/480=0.00208$**: twenty-two times below the
threshold already proved for a $C^{1,\epsilon}$ force, and one hundred and seventy-eight times below
it at their own $\delta=1/8$.

The obstruction is therefore not the published constants, which are design choices, but the exchange
rate of 120 units of frequency ratio per derivative. Changing it means changing the correction
hierarchy, not retuning around it.

## The corner our own cap sits in

The trade-off in one line is $\alpha<\delta/(4Q)$. [Page 4](04-dissipation-and-the-frequency-cap.md)'s
cap of $1/4$ is the corner $\delta\to1$, $Q\to1$: a layer that stops just below $\lambda^{-1}$ and a
frequency that barely grows. The smooth-forcing design sits at $\delta=1/8$, $Q\ge200$, seven orders
of magnitude away, because both budgets were spent on the smoothness of the force. And
[page 6](06-where-the-published-threshold-comes-from.md) shows the other end is not free either: the
force budget of the hypodissipative construction forbids $Q=1$ outright.

## The prediction

A hypodissipative version of this mechanism must **bound the frequency ratio** (hence control only
finitely many derivatives, so a force of finite regularity), or **raise the amplitude margin** toward
1, or **change the growth law** to one whose rate is the background gradient itself rather than its
square root, as the vortex-layer construction does. Its threshold should scale like $\delta/(4Q)$.

It is wrong if a hypodissipative result appears with a positive threshold, an unbounded stage-dependent
$Q_q$, a margin near $1/8$ and the same square-root growth law. Recorded 2026-09-16, before that paper
appeared, and guarded in CI.

## Next

Back to the [index](README.md).
