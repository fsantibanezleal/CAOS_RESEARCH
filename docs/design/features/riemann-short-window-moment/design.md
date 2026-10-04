# Preimplementation design review

An optional `short_window_moment` object with schema `riemann-short-window-moment-v1` is added to replay v9. Existing helpers and frozen evidence remain unchanged. The offline stage reads all required committed EXP-028 proof/control sources and v0.02 publication files, validates SHA-256 bindings and exact rational margins/density floor, then exports a compact typed record. It never searches or attempts to prove the analytic theorem computationally.

The final `proof-review.json` is separate from historical conditional receipts: its internal analytic review admits the theorem, while those receipts still say that arithmetic alone does not prove it. Native and independent interval controls share the frozen EXP-010 detector premise. All attributed dependencies remain explicit.

A bilingual component presents the current short-window result in each existing tab. Historical EXP-010 content is labeled earlier. A separate typed browser selector checks recorded flags and matching provenance. A small proof-stage control may explain signed representation, exact dual transformation, separated multiplier and counting transfer without adding online scientific computation.

Mutation tests alter actual recorded sources/receipts and verify rejection. Full EN/ES, light/dark and desktop/mobile rendered QA follows the existing pointer-driven harness, with explicit new-result/source-link checks. This chat owns the serialized release on `work/riemann-hypothesis/moment-release-20261004`; protected concurrent checkouts and frozen source/PDF bytes are preserved.

Review verdict: accepted before implementation. Each claim has an evidence gate, every requirement has a measurable release check, and the contribution has one existing manuscript home. No research coordination is moved.
