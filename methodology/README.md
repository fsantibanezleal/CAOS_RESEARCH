# methodology/ - the research operating system

Every problem in this repository is worked under one fixed operating system. It exists so that the
record stays honest, reproducible and adversarially validated, independent of who (or what) runs a
given session. The twelve documents below are binding where applicable for every problem folder.

| Doc | Governs |
|---|---|
| [01-lifecycle.md](01-lifecycle.md) | The states a problem moves through and the gates between them. |
| [02-experiment-standard.md](02-experiment-standard.md) | The EXP-NNN record: hypothesis before run, deterministic entry point, artifacts, verdict. |
| [03-adversarial-validation.md](03-adversarial-validation.md) | The validation ladder every positive finding must climb before it is believed. |
| [04-code-standards.md](04-code-standards.md) | Environments, exact-vs-float policy, GPU usage, tests, CI guards. |
| [05-writing-standards.md](05-writing-standards.md) | Markdown/KaTeX/SVG/reference rules for context, history and wiki content. |
| [06-web-publication.md](06-web-publication.md) | What may appear on the web app, and when (the `published` gate). |
| [07-session-handoff.md](07-session-handoff.md) | The resume contract: `program/<problem>/RESUME.md`, updated every session, so a new session resumes with zero loss. |
| [08-parallel-sessions.md](08-parallel-sessions.md) | Per-problem isolation, shared-surface ownership, and the serialized release step. |
| [09-manuscripts-and-publication.md](09-manuscripts-and-publication.md) | Manuscript triggers, Zenodo publication, and immutable version updates. |
| [10-research-lenses.md](10-research-lenses.md) | The systematic spine plus complementary lenses and the invariant-first rule. |
| [11-exploration-cadence.md](11-exploration-cadence.md) | The required new-viewpoint or honest-null exploration moment in every round. |
| [12-preflight-and-cost-discipline.md](12-preflight-and-cost-discipline.md) | Source, premise, tooling, one-sidedness, invariant, and compute-budget checks. |

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
