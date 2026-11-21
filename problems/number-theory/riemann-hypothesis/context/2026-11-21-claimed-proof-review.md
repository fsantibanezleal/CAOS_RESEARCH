# The formal proof of the Riemann hypothesis released on 2026-11-20: review, state of verification, and what stays open

Date: 2026-11-21 (readings between 08:00 and 12:00 UTC). Written by the coordinating session on Felipe's order of
2026-11-21 ("review last claim from Anthropic, that they solved Riemann hypothesis, read and research online in
max depth for all the new works on that problem, and verify if any space of research is open"). Evidence marks:
[P] read by this session on the primary source; [T] a third party's published check, read on its own page; [R] a
delegated research report of 2026-11-21 (coordination repository, `wip/caos-research/rh-claim-reception`,
`rh-literature-refresh`, `rh-open-space`, each accepted with its open items); [D] a derivation of this programme.
This dossier reports who has shown what. It does not itself establish that the hypothesis is proved, and the
programme's own theorems do not depend on it.

## 1. The claim, on its primary source

- [P] A four-page unsigned note, `https://alpo.ge/remark.pdf` (245,114 bytes, SHA-256
  `3fc97784b71ddd44ff8aa0a177e99622a1c61b13cfa843a0989ee4a7a0cfeb8d`), on the site of Levent Alpoge (Anthropic;
  Society of Fellows, Harvard). Its words: "I believe I have, working with Claude, discovered a proof of the Riemann
  Hypothesis. In fact, the method easily extends much further, resolving the so-called Generalized Riemann
  Hypothesis, and I expect, with more time, the Extended Riemann Hypothesis too. Claude and I have also formalized
  the arguments without assumptions." The only artifact is Lean code, `https://alpo.ge/lean.tar.gz.part01` to
  `part14`. There is no written proof: "It being obviously inappropriate to attempt to post some massive
  unreadable travesty [...], I decided to only present Lean"; a generated text had "250,000+ pages".
- [P] The mathematics, as the note sketches it: "This argument is a descendant of Stepanov's"; multiplicity over
  the integers is obtained by "chaining theta lifts", "for the von Mangoldt sum of length X, Claude's suggested
  length of chain of theta lifts [...] was sqrt(X)"; a timeline of twenty steps dated 2026-10-06 to 2026-11-16
  names a Stepanov determinant, positivity of Weil's functional through determinants, Gan-Gross-Prasad and Bessel
  periods, iterated theta lifts between totally definite unitary groups, a Bost slope inequality, an Iwasawa tower,
  a relative trace formula, Chowla-Selberg, a weakening of Vandiver, and "11/16/26: GRH". The author states that
  parts of this description paraphrase a summary he cannot yet vouch for and that he expects simplifications.
- [R] The same author with R. Furman posted arXiv:2608.13637 in August 2026 (at least two thirds of the zeros simple
  and on the line, unconditionally; argument found by Claude; the baseline of this programme). The November proof
  is a different method; no source links the two. No official statement of Anthropic, of the Clay Mathematics
  Institute or of the Lean FRO was found on 2026-11-21.

## 2. What is formally stated

- [P] `src/Main.lean` of the archive (read on the mirror `leanprover-community/riemann-hypothesis`, commit 23aebbb3)
  has five theorems: `riemannHypothesis : RiemannHypothesis`; the same written out; and three statements on
  Dirichlet L-functions: no zero with real part above 1/2 for every modulus and every character (except the pole of
  the trivial character), every zero in the open critical strip on the line, and the same for primitive characters
  (`src/Statements.lean`, 16 lines, imports only Mathlib). "GRH" in the code means Dirichlet L-functions only.
  Dedekind zeta functions, Hecke, Artin and automorphic L-functions are not covered.
- [P] Statement check by this session, on Mathlib at the pinned commit `0df444a360eaa60ab8c11dca51a86af692955474`
  (file `Mathlib/NumberTheory/LSeries/RiemannZeta.lean`, SHA-256 `db9f37f0...2a1a9`): `riemannZeta` is defined as
  `hurwitzZetaEven 0` (line 121); `differentiableAt_riemannZeta` (line 139) gives differentiability at every
  s other than 1; `zeta_eq_tsum_one_div_nat_cpow` (line 207) gives riemannZeta s = sum of 1/n^s for Re s > 1. A
  function analytic on the plane minus the point 1 that equals the Dirichlet series on Re s > 1 is the zeta
  function, by uniqueness of analytic continuation. `RiemannHypothesis` (line 185) says: every zero other than
  the points -2(n + 1) and other than s = 1 has real part 1/2. That is the Riemann hypothesis. For characters,
  `DirichletCharacter.LFunction` equals the L-series for Re s > 1 (`LFunction_eq_LSeries`, line 75 of
  `DirichletContinuation.lean`) and is differentiable away from the pole (line 92), so it is the Dirichlet
  L-function.
- [T] The same comparison was made by hand by the verifiers (verification notes of the mirror; an independent
  reader, ishaan2006) and mechanically: Comparator's statement matching and `con-leche --compare` find the five
  theorems of the archive equal to the five of a challenge file that imports only Mathlib.

## 3. What has been checked, by whom (as of 2026-11-21 08:33 UTC)

Source for every line unless said: `https://math.mit.edu/~drew/grh/` (A. Sutherland, MIT; last updated 2026-11-20
22:05 UTC; unchanged at 08:33 UTC on the 21st) [T], and the verification notes of the mirror [T].

| Check | Result |
|---|---|
| All 175,187 modules compile (Lean v4.33.1, Mathlib tag v4.33.1) | pass, zero errors |
| `#print axioms` of the five theorems | `propext`, `Classical.choice`, `Quot.sound` only |
| Static scan of the 17,374,215 lines | no `axiom`, `sorry`, `native_decide`, `unsafe`, `implemented_by`, `opaque`; two tactics (`kexactB`, `kcopy`) assign terms without elaborator type checking, so the kernel is the only check of those proofs |
| `leanchecker` replay of every module | 175,187 of 175,187 |
| nanoda (independent kernel, Rust) on the full export (61,570,595,788 bytes, SHA-256 `5ea74b91...be244e`) | accepts |
| con-leche (independent kernel), plain and `--compare` against the challenge | accepts; the five theorems "justified by the solution" |
| lean4lean (third kernel design) on the compiled modules | 175,187 of 175,187 (five with a raised step limit) |
| A second, independent build (ishaan2006, 94 cores, 401 minutes) [R] | its export is byte-identical to the first |
| Lean default kernel and hardened kernel on the export; `lake comparator` end to end | still running; no verdict published |
| A sandboxed build with the protocol of the mirror | not reported |
| Any rejection, crash or discrepancy of a kernel | none found in any source read |

Limits recorded by the verifiers themselves [T]: the builds were not sandboxed; Lean v4.33.1 predates runtime fixes
of v4.34.1 (issues 15241 and 15289, which could in principle be turned into a proof of False in the official kernel
with constructed input), which is why the judging uses independent kernels; "a passing check shows that the formal
statements, as written in Lean against Mathlib's definitions, follow from the three standard axioms according to
the kernels used". The Lean Zulip thread could not be read without an account [R].

This session could not replay a kernel: the published route needs 50 to 100 GB of memory and this device has 47.7.
What it checked itself is Section 2 and Section 5.

## 4. The proof as third parties have mapped it

[R], from issues 3, 5 and 12 of the mirror, a reader's guide on Zenodo (10.5281/zenodo.24410057) and reader
repositories; all are unofficial readings, several made with AI assistance, none by the author.

- Chain: the Riemann hypothesis is deduced from the nonvanishing of every Dirichlet L-function to the right of 1/2;
  that from a one-sided bound of square-root quality for weighted sums over primes, on windows, through a window
  form of Landau's theorem; the bound from Arakelov geometry (families of Hermitian lattices indexed by a code, a
  slope inequality of Bost type, near-orthogonality of period maps, a Chebyshev-type count of prime powers compared
  with a Chowla-Selberg period), with arithmetic inputs proved inside the archive (Galois representations through
  theta lifts, bounds for Tate-Shafarevich groups of Tate twists).
- Weaknesses flagged, none of which is a kernel failure: two classical inputs are present in a weaker form than the
  published theorems they are named after; ten statements on the chain have no reference in the literature (they
  are the new mathematics a referee would read); one clause is satisfied for a degenerate reason and is not used
  downstream; many declarations are off the path of the final theorems; the semantics of the archive's own
  definitions of classical objects has not been audited by experts.
- Reception [R]: T. Tao (blog, 2026-11-20): "has generated an (enormous) Lean-only proof of the Generalized Riemann
  Hypothesis"; "I imagine the digestion process will take some time". A. Sutherland: "This is indeed an historic
  moment"; "There is much work to be done to understand the mathematical details of the proof". J. Maynard: "If
  this fully checks out, it is clearly a historic milestone in mathematics". A. Granville: "What he released is
  garbled". M. Radziwill: the note contains "nonsensical statements". B. Conrey: "I really did not see this coming
  at all". Nothing was found from the persons named in the note's acknowledgements other than Radziwill.

## 5. The last step, checked on paper by this programme

[D] `2026-11-21-windowed-landau-endgame.md`: with G(x) = sum over n <= x of Lambda(n)(x/n - 1) - x log x +
(1 + gamma) x, a bound G(x) <= Y^eta x^theta on windows [Y, Y^(1 + delta)] for arbitrarily large Y and every
eta > 0 implies that zeta has no zero to the right of theta; the same for positive combinations over Dirichlet
characters. The proof was written from the Lean statements (`Formalism.Gz`, `Deduction.landau_window`,
`Deduction.zeroFree_of_rpow_window`), not from the proof terms. The explicit formula gives the converse size:
under the hypothesis, |G(x) - log 2 pi| <= 0.0461915 sqrt(x) + 0.31/x^2. EXP-029 is the numerical control of the
normalization (PASS on 2026-11-21: the explicit formula agrees at 460 points, and up to 10^8 the sum stays within
0.0247 sqrt(x) of log 2 pi, with both signs). This is the one piece of the formal proof this programme has verified independently of a kernel;
it is the easy end, and all the depth is upstream of it.

[P] The link above it was read in the Lean source itself (`src/Formalism/GammaFactorNonvanishing/CritLine.lean`, 30
lines). `Formalism.VW.critLine` takes a zero s of a primitive L(chi, s) with 0 < Re s < 1/2, uses Mathlib's
functional equation (`IsPrimitive.completedLFunction_one_sub`) and the nonvanishing of the gamma factor to produce
a zero of L(chi^-1, 1 - s) with real part above 1/2, against the half-plane statement; `Formalism.VW.rh_of_every`
applies the half-plane statement to the character of modulus 1, whose L-function is the zeta function
(`LFunction_modOne_eq`), and concludes through `rh_of_right`. This is the classical deduction of the line from the
half-plane, written with Mathlib's lemmas; nothing in it depends on the archive's own definitions. So the chain
reads, from the top: the hypothesis, from the half-plane statement for every Dirichlet character (functional
equation; read); the half-plane statement, from a one-sided bound on windows (Landau's theorem on windows; proved
on paper in the note); the one-sided bound, from the arithmetic geometry of the archive (not read by this
programme).

## 6. Assessment

- The evidence that the five formal statements are theorems of Lean with Mathlib is strong and of a new kind:
  three independent kernel designs accept the proof, two independent builds give the same export, the statements
  are Mathlib's own, and no axiom beyond the standard three is used. What remains pending is confirmatory (the
  reference kernel on the export, the end-to-end Comparator run, a sandboxed build).
- What is absent is understanding. No written proof exists, the author says he has not mastered parts of the
  argument, the experts quoted reserve judgment on the mathematics, and the new statements of the chain have not
  been read by referees. The rules of the Clay Mathematics Institute require publication in a refereed outlet, two
  years, and general acceptance, and say nothing about formal proofs [R].
- For this programme the working position is: treat the Riemann hypothesis and the generalized hypothesis for
  Dirichlet L-functions as formally verified statements whose acceptance is in progress; state every new result
  either unconditionally or explicitly "under the Riemann hypothesis" (which is correct mathematics whatever the
  outcome); never describe a result of this programme as part of, or progress toward, that proof.

## 7. What stays open, and where this programme can still prove something

From [R] `rh-open-space` (rows marked UNVERIFIED there are not used here):

- Not covered by the five theorems: every result "under GRH" that needs Dedekind, Hecke, Artin or automorphic
  L-functions (Artin's primitive root conjecture after Hooley, generators of class groups after Bach, effective
  Chebotarev, ranks of elliptic curves). The note itself says the extended hypothesis needs more time.
- Not implied by any form of the hypothesis: simplicity of all zeros; Montgomery's pair correlation conjecture and
  the GUE statistics; linear independence of the ordinates; the true order of zeta on the line and of S(t); the
  moment conjectures; Cramer's conjecture.
- Zeros of zeta under the hypothesis, best known: at least 19/27 simple (Bui and Heath-Brown, arXiv:1302.5018,
  under RH alone); at least 0.8477 distinct (Chirre, Goncalves and de Laat, arXiv:1810.08843); multiplicity at most
  (1/2 + o(1)) log t/log log t (Goldston and Gonek). These dominate, once the hypothesis is a theorem, every
  global unconditional proportion of 2026, including the 0.6725 and 0.8362 of the programme's baseline, the
  0.67353 and 0.83900 of Knausgard (arXiv:2610.08965, 2026-10-06) and the programme's own distinct-zero constants.
- Short intervals: no theorem was found, with or without the hypothesis, giving a positive proportion of simple
  zeros in (T, T + T^theta] for theta at or below 0.5501 (Wang, arXiv:2609.07918v2; before, Steuding, 0.552),
  except this programme's unconditional 0.534 (`short-interval-levinson` v0.02, unrefereed).
- [D, a reading of this programme, to be written out and reviewed as the first unit of focus RH-F17] The pair
  correlation method should not pass that point even under the hypothesis: on a window of length H = T^theta the
  mean value theorem for Dirichlet polynomials controls lengths up to about H, so the form factor is available for
  |alpha| < theta only, and the resulting bound for the sum of the multiplicities carries information only for
  theta above about 0.55 (with the Fejer kernel of that band, simple zeros at least 2 - 1/theta - theta/3,
  positive exactly for theta > 3 - sqrt(6) = 0.5505; Wang's 0.5501 is the same barrier with the optimal kernel).
  Mollified discrete moments of zeta'(rho) (Conrey, Ghosh and Gonek; Bui and Heath-Brown) give a positive
  proportion for a mollifier of any positive length, so with the programme's short-window twisted moments
  (mollifier T^nu, nu < theta - 1/2; EXP-010, EXP-028) they are the natural route to every theta > 1/2 under the
  hypothesis. This is the research space the plan of 2026-11-21 opens (focus RH-F17).
  The computation is written out in `2026-11-21-pair-correlation-band-barrier.md`: on a band lambda the method
  gives simple zeros at least 2 - lambda/2 - cot(lambda/sqrt 2)/sqrt 2, which vanishes at 0.550194 and equals
  0.41908 at 3/4, the two numbers of Wang's theorem.

## 8. New works since the last pass (2026-10-04), from [R] `rh-literature-refresh`

- Knausgard, arXiv:2610.08965 (2026-10-06): distinct zeros at least 1645064/1960733 = 0.83900..., simple and
  critical at least 0.67353..., Lean 4 proofs with three axioms that record search-program results. It supersedes
  as a record the 0.8371747... and 0.8373797... of `distinct-zero-gram` v0.01 (which stay true statements).
- Wang, arXiv:2609.24167: withdrawn by its author (confirmed); arXiv:2609.07918 v2 unchanged at onset 0.5501.
- Lamzouri, arXiv:2611.14486 (small gaps, 0.7892) and arXiv:2610.26841 (isolated zeros, 13/20); Cobeli and
  Zaharescu, arXiv:2610.23467 (simple or on the line, more than 8/9); Arias de Reyna, arXiv:2610.24612 (a human
  exposition of the 0.6725 theorem); Goulden, arXiv:2611.23332 (Gram's law for moving targets, threshold
  0.5339..., the same decimals as this programme's internal onset for a different statement: to be examined).
- The zero-free half-plane of OpenAI (2026-10-06, Re s > 7/8, unrefereed) and five preprints that refine or use it
  (Liu, arXiv:2610.12234 and 2610.26835; Xu and Sang, 2610.15291; Ji, 2611.16665; one more); a conditional and an
  unconditional bound for the de Bruijn-Newman constant.
- No arXiv paper presents or reviews the proof of 2026-11-20.

## 9. Sources kept

Copies with SHA-256 under the data root, `caos-research/riemann-hypothesis/claim-2026-11-20/`: `coordinator/` (the
note, the MIT page as text, the mirror's README, notes, issues 2, 3, 5, 12, the statement and main files, the Lean
files of the last step, the two Mathlib files at the pinned commit) and one folder per research report. Manifest:
`source-manifest-claim-20261121.json`.

## How could this be wrong?

- A defect shared by the kernels that accepted the proof, or a flaw in Mathlib's definitions of the functions
  involved, would not be seen by any check listed; the second is unlikely for definitions with the analytic
  continuation and the Dirichlet series both proved in the library, the first is what the pending runs and the
  different kernel designs address.
- Sections 4, 7 and 8 rest on delegated reports with open items; their statements are marked [R] and the rows
  those reports call UNVERIFIED were left out.
- The state of verification changes by the hour. The watch list of the plan fixes when it is read again.
