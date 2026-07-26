# Graded Keller maps: source reconciliation (2026-07-25)

## Source and provenance

- T. Shaska, *Graded Keller maps and the Jacobian Conjecture*,
  [arXiv:2607.20210v1](https://arxiv.org/abs/2607.20210), submitted 2026-07-22.
- Primary source read in full from the arXiv TeX bundle on 2026-07-25.
- Local verification copy:
  `E:\_Temp\jc-round-2026-07-25\arxiv-2607.20210\sh-131.tex`.
- SHA-256 of the TeX source:
  `2B9228F067875C0C97007C7822803449CA64D49C8D841A4D44798E27A3028AC0`.
- The local copy is not committed. The arXiv identifier and hash are the durable
  provenance record.

## Statement relevant to this program

Shaska's Theorem 3.3 gives the full classification of Keller maps
$G:\mathbb{C}^2\to\mathbb{C}^2$ equivariant for a nontrivial algebraic
$\mathbb{G}_m$ action, after polynomially linearizing the source and target
actions:

1. same-sign source weights give triangular automorphisms, possibly nonlinear;
2. one zero weight gives affine automorphisms;
3. opposite-sign weights give diagonal or coordinate-swapped linear
   automorphisms.

The proof is independent of our experiment record. In the opposite-sign case it
uses the invariant $m=x^q y^p$ and the degree identity
$$
\frac{d}{dm}\bigl(mA(m)^qB(m)^p\bigr)
 = A(m)^{q-1}B(m)^{p-1}\det JG,
$$
which forces $\deg A+\deg B=0$.

The source contains no `sl2`, Lie-algebra, or weight-module formulation of the
corrector ladder. It therefore changes the positioning of EXP-010 but does not
decide EXP-080.

## Reconciliation against EXP-010

EXP-010 was declared on 2026-07-21 and its theorem and proof are explicitly
restricted to weights $(w_1,-w_2)$ with $w_1\geq1$ and $w_2\geq0$. Its exact
certificate and its mixed-sign/zero-weight conclusion remain valid.

Two derived claims had drifted beyond that evidence:

- "for arbitrary weights, every equivariant Keller map is linear";
- "every $\mathbb{G}_m$-equivariant Keller map of $\mathbb{C}^2$ is linear".

Those statements are false for same-sign weights. For example, triangular
automorphisms can be equivariant and nonlinear. The correct global conclusion is
that every such equivariant planar Keller map is an automorphism; linearity is
the sharper mixed-sign/zero-weight conclusion proved by EXP-010.

## Novelty and chronology

The 2026-07-22 literature dossier honestly reported that no mixed-sign planar
statement was found at that time. Shaska's v1 was submitted later that same day
and is now a directly overlapping independent result. The durable record must
therefore say:

- EXP-010 predates the arXiv submission by one day;
- the two derivations are independent as far as the available chronology and
  proofs show;
- no priority or novelty claim is made;
- current readers are directed to Shaska's full all-signature classification.

## Consequences for the current round

1. Preserve EXP-010 unchanged as the primary experiment record.
2. Correct scope drift in the wiki, manuscripts, routes, handoff, backlog, and
   management mirror.
3. Publish corrected manuscript versions because the current Zenodo PDFs contain
   the overbroad derived wording and an obsolete "not found" novelty statement.
4. EXP-080 follow-through (completed later the same day): its preflight separated
   raw torus shifts from a claimed `sl2` action on the pinned corrector operators.
   The invariant gate refuted the declared natural triple, so commutators were not
   run; see the experiment verdict for the scoped null.
