# methodology/ - the research operating system

Every problem in this repository is worked under one fixed operating system. It exists so that the
record stays honest, reproducible and adversarially validated, independent of who (or what) runs a
given session. The six documents below are binding for every problem folder.

| Doc | Governs |
|---|---|
| [01-lifecycle.md](01-lifecycle.md) | The states a problem moves through and the gates between them. |
| [02-experiment-standard.md](02-experiment-standard.md) | The EXP-NNN record: hypothesis before run, deterministic entry point, artifacts, verdict. |
| [03-adversarial-validation.md](03-adversarial-validation.md) | The validation ladder every positive finding must climb before it is believed. |
| [04-code-standards.md](04-code-standards.md) | Environments, exact-vs-float policy, GPU usage, tests, CI guards. |
| [05-writing-standards.md](05-writing-standards.md) | Markdown/KaTeX/SVG/reference rules for context, history and wiki content. |
| [06-web-publication.md](06-web-publication.md) | What may appear on the web app, and when (the `published` gate). |
| [07-session-handoff.md](07-session-handoff.md) | The resume contract: `program/<problem>/RESUME.md`, updated every session, so a new session resumes with zero loss. |

## Principles (non-negotiable)

1. **Exact over floating wherever decidable.** A claim verified in rational/symbolic arithmetic or
   with certified numerics counts as verified; a float-only check never does. Floats explore and
   visualize; they do not certify.
2. **Adversarial validation before belief.** Every positive finding gets a persisted refutation
   attempt (independent route, stress family, or certificate) BEFORE it enters the wiki or web.
3. **The history is the product.** Experiments are append-only, numbered, dated. Wrong turns are
   documented, never deleted. Null results are first-class outcomes.
4. **Self-containment per problem.** Everything a problem needs to be read and reproduced lives
   under its `problems/<area>/<slug>/` folder.
5. **Offline compute, static web.** All computation is offline (local CPU/GPU); the web app only
   replays persisted, versioned artifacts.
6. **Primary sources only in claims.** Every transcribed claim cites DOI/arXiv/official URL, or is
   flagged UNVERIFIED until it does. Secondary sources may guide, never certify.
- [08 - Parallel sessions and per-problem isolation](08-parallel-sessions.md): the binding rules that let multiple sessions drive different problems concurrently (release ownership, bake ownership, start ritual).
- [09 - Manuscripts and publication](09-manuscripts-and-publication.md): the trigger rule (enough validated + novel material = manuscript created/expanded THAT round, transcribed from verdicts), the Zenodo upload rule (CC-BY, API flow, autonomous publish with post-review), and the update strategy (new versions, never edits; concept vs version DOIs).
- [10 - Research lenses](10-research-lenses.md): the reusable toolkit of complementary approaches (exclusion, anatomy, recognition, invariant, symmetry, two-sided, reformulation, dimension-ladder, at-infinity, adversarial, external-dialogue) for EVERY problem; the systematic exclusion path is the spine, always complemented by >=2 other lenses.
