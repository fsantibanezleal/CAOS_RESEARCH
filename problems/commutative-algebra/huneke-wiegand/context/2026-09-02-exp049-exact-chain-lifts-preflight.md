# EXP-049 preflight - exact completion-chain lifts and parity duals

Date: 2026-09-02. Scope: HWB-075, the two stable relative inclusions `58->59` and
`58->62` in the isolated `(p,2)` presentation.

## Source-complete check

The fresh primary-source sweep found no theorem that supplies the required parameter-dependent
cycles or parity characters for the CAOS matrices.

- Kozlov, *Discrete Morse Theory for free chain complexes*,
  <https://arxiv.org/abs/cs/0504090>, proves that an acyclic matching splits a free chain complex
  into a Morse complex and an acyclic summand. This validates a future relative-Morse reduction,
  but only after the matching and its boundary paths are constructed.
- Jollenbeck and Welker, *Resolution of the residue class field via algebraic discrete Morse
  theory*, <https://arxiv.org/abs/math/0501179>, extends the matching construction to chain
  complexes of free modules over a ring. It does not identify a matching for this family.
- Stanley, *Smith Normal Form in Combinatorics*, <https://arxiv.org/abs/1602.00166>, records the
  lattice and cokernel interpretation of Smith factors. It supports testing exact lattice
  membership of twice a proposed class instead of inferring integral order from field ranks.
- Autry, Graves, Loucks, O'Neill, Ponomarenko, and Yih, *Squarefree divisor complexes of certain
  numerical semigroup elements*, <https://arxiv.org/abs/1804.06632>, supplies the
  numerical-semigroup to simplicial-complex dictionary. It does not settle the connecting block
  or its factor-two torsion.

The sources support the tools and the reformulation, not the desired all-parameter result. The
four chains remain post-EXP-048 conjectural formulas outside `p=8,...,11`.

## Premise and artifact check

1. EXP-042 freezes the exact signed isolated matrices and their semantic atom tables.
2. EXP-045 identifies masks `59` and `62` as the stable minimal full carriers, with intersection
   mask `58`.
3. EXP-047 proves that both tested relative cokernels have torsion exactly `(Z/2)^2` and stores the
   compact relative matrices.
4. EXP-048 independently reconstructs every added-row label and verifies the four displayed
   `alpha/beta` support formulas at `p=8,...,11`.
5. No verdict proves that the displayed zero-one chains themselves, rather than representatives
   differing by an even correction, have exact order two. That is the new hypothesis.

Every reused executable and artifact is SHA-256 pinned by the runner before arithmetic begins.

## Invariant-first and tooling decision

The cheapest decisive invariant is column-lattice membership:

```text
2 a in im_Z(R).
```

Here `a` is one displayed `alpha` or `beta` chain and `R` is the compact relative matrix. This
single test decides whether the chain itself is an exact order-two candidate. It is strictly
stronger than another Bockstein or finite-field rank and much cheaper than transforming the full
isolated presentation.

Row Hermite form of `R^T`, with its unimodular transformation, gives both a membership decision
and an exact coefficient vector `y` satisfying `R y=2a`. Mapping `y` through the already defined
saturated source kernel gives a source-domain cycle. Binary left-nullspace solving gives parity
characters that annihilate every column of `R` and pair with the two chains.

## Adversarial route and cost gate

The primary route uses transformed row Hermite membership. The independent audit will multiply
the sparse matrix by every stored witness, recompute source annihilation directly, and recompute
the parity pairings with an independent high-pivot binary elimination. It will not trust the HNF
membership flag or the primary low-pivot dual solver.

- Smoke: `p=8`, at most 300 seconds and 10 GiB, with a checkpoint after each inclusion.
- Full finite range: `p=8,...,11`, at most 2,400 seconds and 24 GiB.
- Stop on any frozen hash mismatch, semantic formula mismatch, nonintegral HNF division, failed
  exact multiplication, or disagreement between the two parity solvers.
- A budget stop is `INCONCLUSIVE_RESOURCE_BUDGET` and proves nothing about the formulas.

## Exploration moment and path ranking

The new viewpoint is to separate three logically different obligations that the phrase
"construct a torsion class" had conflated:

1. exact order at most two, certified by `R y=2a`;
2. nontriviality and independence, certified by parity characters;
3. the all-parameter upper bound, which still needs a uniform complement or relative-Morse
   reduction.

This decomposition makes the first two obligations finite, explicit, and independently auditable.
If exact membership fails, the stable-chain route is redirected immediately to corrected integral
representatives. If it passes but the witnesses remain arithmetically opaque, their semantic
support becomes the next extraction target. Relative Morse theory remains the best fallback for
the nonuniform `56->58` threshold and for the eventual upper bound.

No manuscript or Zenodo update is opened by this preflight. A uniform construction or a comparably
transferable theorem remains the publication trigger.
