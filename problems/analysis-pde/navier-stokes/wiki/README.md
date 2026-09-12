# navier-stokes wiki

Stub at open time, 2026-09-11. Pages are authored per unit as the units land, never bolted on at the
end, per ADR-0056 and methodology 05. Nothing is written yet because no experiment has run.

Planned pages, each to be transcribed from the context dossiers at the moment its unit is built, never
recalled from memory:

1. **The problem as Fefferman states it.** The four alternatives, the side conditions (4) to (11), and
   why (C) and (D) permit a forcing term while (A) and (B) do not. This page is the one that keeps our
   own language honest: a forced breakdown is not the statement a non-specialist hears in the words
   "the equations develop a singularity".
2. **The two September 2026 constructions.** The Alpoge-Buckmaster layer cascade and the OpenAI
   self-similar vortex core, with the comparison table from the source dossier and the shared
   low-frequency plus high-frequency scheme they both instantiate.
3. **The modulation system.** The exact wave, its three amplitude equations, the growth, steering and
   holding cycle, and the identity that makes the whole program work: a short wave carries a small
   amplitude and a large gradient, so frequency buys gradient but not growth.
4. **Dissipation and the frequency cap.** The derived extension, the cap, the upper bound, and the two
   omissions that keep it from being a threshold.
5. **What machine verification does and does not establish.** The statement audit, why a third-party
   reference statement is the strongest fact in a formalization repository, and why a compiling
   certificate is not a verified theorem.

Every page carries KaTeX equations, inline citations with real DOIs or arXiv identifiers, an
assumptions block, and theme-aware SVG figures in `assets/`. Attribution to Cordoba and
Martinez-Zoroa is a standing requirement on pages 2, 3 and 4.
