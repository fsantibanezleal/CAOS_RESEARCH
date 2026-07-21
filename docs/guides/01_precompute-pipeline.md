# Guide: the export pipeline (precompute lane)

```bash
./scripts/precompute.sh       # bakes all registry artifacts (or: python -m researchlab.pipeline all)
```

The pipeline has one stage, `export_registry`: it reads `program/portfolio.yaml` and the
per-problem experiment records, transcribes the Jacobian payload from the exact verdicts, and
writes `data/derived/research/*.json` plus SHA-256 manifests and `manifests/index.json`
(CONTRACT 2). It is deterministic (no timestamps, sorted keys), stdlib + PyYAML only, and never
touches the experiment layer: the heavy engine of this repository is the experiment records
themselves, which run exactly once and persist their outputs under
`problems/<area>/<slug>/experiments/`.

The web app (`frontend/`) copies `data/derived` into `public/data` at build time
(`copy-data.mjs`) and replays it; it computes nothing at request time.
