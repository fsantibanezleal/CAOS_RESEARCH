# EXP-006 verdict: confirmed Hilbert-parity threshold improvement

Date: 2026-09-20. The declaration commit
`b1febcf8a6d5830218e1df386af1e8a92c3037be` was pushed before implementation
or computation. The audit then strengthened the declared target, committed the
amended runner, and executed the canonical certificate from clean commit
`0d736fa22ce7e833200381a32e8cc89f77c660e8`.

**Verdict: confirmed.** This is a new internally reviewed deduction from
attributed analytic inputs. It does not establish external peer acceptance,
absolute novelty priority, an end-to-end formal proof, or the Riemann
hypothesis.

## Confirmed finite theorem

[D] For a nonempty conjugation-invariant finite multiset, let `N` count copies,
`S` count simple real support points, `O` count distinct odd-multiplicity real
support points, and let `Q` be Lamzouri's squared-kernel pair sum. Then

$$
\boxed{(Q-S)(N-O)\ge2(N-S)^2.} \tag{1}
$$

The coefficient two is sharp: a single real point of multiplicity two or
three gives equality. The proof starts with Lamzouri's attributed
arbitrary-parameter Hilbert inequality, retains its simple-real term, and uses
parity to prove `2(r+k)<=N-O`. The exact product (1), rather than the
arbitrary-parameter premise, is the proposed finite deduction.

## Confirmed short-interval theorem

[D] Let `S(T,H)` count simple critical zeros, `O(T,H)` count distinct
odd-multiplicity critical zeros, and `N(T,H)` count all nontrivial zero copies
in `(T,T+H]`. Put

$$
c(\theta)=2-\frac\theta2-
\frac1{\sqrt2}\cot\!\left(\frac\theta{\sqrt2}\right),
\qquad
k_3(\theta)=\frac{\theta-1/2}{4eC_3},
$$

where `C_3` is Pearce-Crump's reproducible rank-three constant, and define

$$
h_3(\theta)=
\frac{3+k_3(\theta)-
\sqrt{(1-k_3(\theta))(9-k_3(\theta)-8c(\theta))}}4.
$$

For every fixed `1/2<theta<1`,

$$
\boxed{
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge
\max\left\{0,c(\theta),
\frac{c(\theta)+2k_3(\theta)}3,
h_3(\theta)
\right\}.} \tag{2}
$$

The new fourth term is positive exactly when

$$
F(\theta)=c(\theta)+(2-c(\theta))k_3(\theta)>0.
$$

Since

$$
F'(\theta)=c'(\theta)(1-k_3(\theta))
+(2-c(\theta))k_3'(\theta)>0,
$$

it has a unique root. The exact certificate proves

$$
\boxed{0.545884<\theta_{\rm HP}<0.545885.} \tag{3}
$$

This strictly lowers the EXP-005 threshold bracket
`0.5459<theta_Sel<0.546`. At `theta=0.5459`, the previous linear parity term
is still negative, with upper bound

$$
-0.0000107367174936433552040195369,
$$

while the strengthened term proves

$$
\boxed{
\liminf_{T\to\infty}
\frac{S(T,T^{0.5459})}{N(T,T^{0.5459})}
>0.0000168381638551244569880374399.} \tag{4}
$$

The first passed finite transfer would have given only
`0.0000126556179972388281537305037`. Retaining the simple-real term improves
the frozen lower bound by more than 33 percent. No analytic constant or target
point changed.

## Why the result is structurally new within the program

[D+MV] At `theta=0.5459`, the published scalar conclusions in Lamzouri's
Proposition 2.1 and the EXP-004 scalar relaxation still admit a normalized
mixture of real triple and double points with `S=0`. The exact certificate
checks that witness. Inequality (1) rejects the scalar witness at the available
pair level because it retains the first-subspace dimension before compression
and couples it to odd support.

Pearce-Crump's printed rank-six constant would raise the lower bound in (4) to
more than `0.0000177645181613023236390595079`, but its full profile is not
printed. That value is recorded only as sensitivity and is not a premise of
the confirmed theorem.

## Exact evidence

[MV] The canonical result is
[`artifacts/canonical/result.json`](artifacts/canonical/result.json), schema
`riemann-exp006-results-v2`, SHA-256
`82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.
It was generated from clean commit
`0d736fa22ce7e833200381a32e8cc89f77c660e8` and records PASS in 0.953
seconds.

The runner checked 18,479 multiplicity profiles, exact endpoint signs, the
scalar zero-simple witness, source hashes, and containment of an independent
100-digit interval replay. Seven focused EXP-006 tests pass; the combined
EXP-004, EXP-005, and EXP-006 suite has 48 passing tests.

Replay into a fresh directory from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/run.py --output-dir tmp/riemann-exp006-replay --budget-seconds 120
pytest tests/test_riemann_hilbert_parity.py
```

The [complete proof](mathematical-proof.md),
[adversarial audit](adversarial-audit.md), and
[`proof-review.json`](proof-review.json) provide the claim boundary.

## Scope

The theorem imports recent analytic preprints and EXP-005's internally audited
localization. It has not received external peer review, and the bounded search
cannot guarantee priority. It is asymptotic and gives no effective height.
It does not improve any global simple-zero percentage, and the Riemann
hypothesis remains open.
