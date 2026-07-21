# 06 - Web publication gates

The web app (`frontend/`, GitHub Pages) is the public showcase. It replays baked artifacts only;
it never computes and never claims beyond the record.

## What a problem page shows (fixed structure)

1. **Summary**: the problem in one screen, current global status, our contribution one-liner.
2. **Context and history**: statement, timeline, the known-results ladder.
3. **References and approaches**: primary sources + the map of known attack routes.
4. **Our strategy**: the current plan (mirrors `program/<slug>/plan.md`).
5. **Experiments and results**: the analysis sequence as a timeline; each step links its EXP-NNN
   and shows its verdict; interactive visualizations replay baked artifacts.
6. **Open questions**: what is genuinely open, including our null results.

## Gates

- A problem appears on the web ONLY in `published` state (see 01): wiki complete, every shown
  claim adversarially validated or explicitly labeled as conjecture/UNVERIFIED, SVGs authored,
  i18n (EN/ES) complete, light and dark themes screenshot-verified for every tab.
- Experiment entries surface verbatim verdicts (`confirmed / refuted / null / inconclusive`);
  the web never upgrades a verdict's language.
- Baked web artifacts are produced by the `data-pipeline/` from committed experiment artifacts;
  the manifest records the source EXP and hashes, so every visualization is traceable to a run.
