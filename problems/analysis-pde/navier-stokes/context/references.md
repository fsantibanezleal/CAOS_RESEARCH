# navier-stokes: references

Status marks: `[V]` read in the primary source; `[P]` partial read (abstract, introduction, or the
specific theorem only); `[U]` cited only through another source.

All files below were downloaded on 2026-09-11 and hashed. Third-party PDFs are NOT redistributed in
this repository (same rule the bougard-joret and petersen-coloring dossiers follow); the local mirror
lives outside git at `E:/_Temp/ns-research/pdfs/`. The SHA-256 column is what makes a later re-download
checkable.

## The September 2026 claims

- OpenAI, *Finite time blowup for Navier-Stokes*, 2026-09-08.
  <https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf>
  `[V]` introduction, Section 2 (physical description); `[P]` Sections 3 to 10 and appendices.
  2,959,204 bytes, sha256 `0e779481c4da40bd28d1e642e1d8ca57447d129610df28dfa5a11e9af8ae228f`.
- OpenAI, *Finite time blowup for the Euler equation*, 2026-09-08.
  <https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf>
  `[V]` introduction and Theorem 1.1; `[P]` Sections 2 to 6.
  535,142 bytes, sha256 `a0c234518e6c489e16996805023eb2e75c00b7c03455f7a3a5be2c124954bfdd`.
- OpenAI, *On the Navier-Stokes Millennium Prize Problem* (announcement page), 2026-09-08, with a
  Concurrent-work update dated 2026-09-10. <https://openai.com/index/navier-stokes-solution/> `[V]`
- OpenAI, `openai/NavierStokesAndEuler`, Lean 4 certificates, Apache-2.0.
  <https://github.com/openai/NavierStokesAndEuler> `[V]` repository metadata, README,
  `formalization.yaml`, `ComparatorChallenges/NavierStokes.lean`, `NavierStokes/ComparatorSolution.lean`.
  Created 2026-09-08T10:53:38Z, last push 2026-09-10T15:14:13Z at audit time; 2,659 Lean files,
  641,332 lines.

## The Alpoge-Buckmaster release (one day earlier)

- L. Alpoge, T. Buckmaster, *Blowup for the Boussinesq equations with smooth forcing*, 2026-09-07.
  <https://cims.nyu.edu/~tristanb/boussinesq.pdf> `[V]` Section 1 (problem, construction, growth
  mechanism, related work); `[P]` Sections 3 to 10.
  846,615 bytes, sha256 `895a628d1783bcb039374686f50b895b5f450f53b8ef8aa173523487a7a4a21b`.
- L. Alpoge, T. Buckmaster, *Blowup for the Euler equations with smooth forcing*, 2026-09-07.
  <https://cims.nyu.edu/~tristanb/euler.pdf> `[P]` abstract and contents.
  1,105,306 bytes, sha256 `97ef408bff09b4f6ed9f3867734d1eb2245f3f34e6334b28136c84c02d0ae8d8`.
- L. Alpoge, T. Buckmaster, M. P. Coiculescu, *Extending the Cordoba-Martinez-Zoroa IPM blow-up to
  uniformly space-time smooth forcing*, 2026-09-07. <https://cims.nyu.edu/~tristanb/ipm.pdf>
  `[P]` abstract and introduction.
  704,785 bytes, sha256 `b3ebdbb8d9a93dcca5f3b3f8796e63f7f28b48e0b0e258b909110a4b69c72a12`.
- T. Buckmaster, public statement on priority, credit and the OpenAI contacts, 2026-09-07.
  <https://cims.nyu.edu/~tristanb/statement.pdf> `[V]` full text.
  53,497 bytes, sha256 `8d7723941bcda2fa55c1e74faa6298e04c706d17ff8abd2ad01878039c621f9d`.
- T. Buckmaster, announcement post, Mastodon, 2026-09-08T03:58:50Z.
  <https://mastodon.social/@tristanbuckmaster/117233413705701198> `[V]` (carries the four PDF links
  and the Lean repository link <https://github.com/tristanbuckmaster/fluid_lean>).
- T. Tao, *Finite time blowup with smooth forcing term for the incompressible porous medium,
  Boussinesq, and incompressible Euler equations*, What's new, 2026-09-07.
  <https://terrytao.wordpress.com/2026/09/07/finite-time-blowup-with-smooth-forcing-term-for-the-incompressible-porous-medium-boussinesq-and-incompressible-euler-equations/>
  `[V]` (expert exposition of the low-frequency plus high-frequency scheme).

## The program these results extend

- D. Cordoba, L. Martinez-Zoroa, *Finite time singularities to the 3D incompressible Euler equations
  for solutions in C-infinity(R3 minus origin) intersect C-1,alpha intersect L2*, arXiv:2410.22920v3.
  <https://arxiv.org/abs/2410.22920v3> `[P]`.
  549,167 bytes, sha256 `14c3a2423cbcec2d6ca5c54258ae4bd978f66631165fdb6217248bda280d45e8`.
- D. Cordoba, L. Martinez-Zoroa, forced IPM blowup with spatially smooth source. `[U]`, cited as [6]
  by the Alpoge-Buckmaster Boussinesq paper; the obligation to read it in the primary source is open.
- D. Cordoba, A. Lain-Sanclemente, L. Martinez-Zoroa, Boussinesq multi-layer pendulum construction.
  `[U]`, cited as [5] by the Alpoge-Buckmaster Boussinesq paper; open obligation.

## Problem statement and background

- C. L. Fefferman, *Existence and smoothness of the Navier-Stokes equation*, official Clay Millennium
  Prize problem description. <https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf>
  `[V]` full text of the statement, conditions (1) to (11) and alternatives (A) to (D).
- J. Leray (1934), global finite-energy weak solutions. `[U]` (via Fefferman and the OpenAI paper).
- L. Caffarelli, R. Kohn, L. Nirenberg, partial regularity of suitable weak solutions. `[U]`.
- J. T. Beale, T. Kato, A. Majda, continuation criterion. `[U]` (stated in Fefferman `[V]` and in the
  OpenAI Euler paper `[V]`).
- T. Tao, *Finite time blowup for an averaged three-dimensional Navier-Stokes equation*,
  arXiv:1402.0290. <https://arxiv.org/abs/1402.0290> `[P]`.
  1,052,688 bytes, sha256 `743c802bd9ecf90ec8d022292885f886a321ab1f7c2dfb601b3c860b98b3f07d`.
- T. Buckmaster, V. Vicol, nonuniqueness of weak solutions via convex integration. `[U]` (cited as [4]
  by the OpenAI Navier-Stokes paper).
- D. Albritton, E. Brue, M. Colombo, *Non-uniqueness of Leray solutions of the forced Navier-Stokes
  equations*, arXiv:2112.03116. <https://arxiv.org/abs/2112.03116> `[P]`.
  426,725 bytes, sha256 `b2dcf166c3832a4ba627ecf634ad9d8aa1dd6f693c4cc8ca33e6e37f53fd0329`.
- T. M. Elgindi, *Finite-time singularity formation for C-1,alpha solutions to the incompressible
  Euler equations on R3*, arXiv:1904.04795. <https://arxiv.org/abs/1904.04795> `[P]`.
  664,080 bytes, sha256 `139d50284b491ee1e68e66f4b0690f8e0b0770fd2989a797c4909bf46a9d79ee`.
- J. Chen, T. Y. Hou, *Stable nearly self-similar blowup of the 2D Boussinesq and 3D Euler equations
  with smooth data*, arXiv:2210.07191. <https://arxiv.org/abs/2210.07191> `[P]`.
  5,181,971 bytes, sha256 `2714863f3fe0f5411a297945f678a87a463c4b5e194a1fa233bd42c4b0455697`.
- T. Y. Hou, Y. Wang, Y. Yang, computer-assisted nonuniqueness of unforced 3D suitable Leray-Hopf
  solutions, arXiv:2509.25116. <https://arxiv.org/abs/2509.25116> `[P]` (already recorded in the
  2026-09-05 portfolio refresh under bougard-joret).
  2,148,337 bytes, sha256 `2d369eade29bd0d5e8dfc6d7def7ed19b8282ab4450860978f3691176d9f8318`.
- Y. Wang, C.-Y. Lai, J. Gomez-Serrano, T. Buckmaster, *Discovery of unstable singularities*,
  arXiv:2509.14185. <https://arxiv.org/abs/2509.14185> `[P]`.
  2,225,069 bytes, sha256 `ade2c449cbbc9314504fcf715f91f33d706960c93dea5cb2c6133cf8a5772613`.

## Formalization tooling

- Google DeepMind, Formal Conjectures, `FormalConjectures/Millenium/NavierStokes.lean`.
  <https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/Millenium/NavierStokes.lean>
  `[U]` at the upstream source; `[V]` in the adapted copy shipped as
  `ComparatorChallenges/NavierStokes.lean` in the OpenAI repository. This is the independent
  statement of alternatives (C) and (D) that the OpenAI Comparator challenge is checked against.
- Comparator, <https://github.com/leanprover/comparator>, with `lean4export` and `nanoda_bin` as the
  external kernel re-checkers. `[U]`.

## Access limits recorded honestly

- The OpenAI Navier-Stokes paper is 165 pages plus appendices. Sections 3 to 10 and Appendices A to C
  have not been read line by line. No claim in this dossier depends on them beyond what the
  introduction and Section 2 state.
- The two Cordoba-Martinez-Zoroa sources that the whole program rests on ([5] and [6] of the
  Alpoge-Buckmaster Boussinesq paper) have not been obtained in the primary source yet. That is the
  first gap to close before any novelty claim is made.
- No independent expert verification of either the OpenAI or the Alpoge-Buckmaster proofs existed at
  the time of writing. The Clay Mathematics Institute had not commented.
