# Counterexample-ready conjecture radar

Use this lens when selecting or reprioritizing open problems. It complements the lifecycle and
feasibility fields; it does not weaken source, novelty, or publication gates.

## Score before committing a research round

Score each item 0, 1, or 2. A strong counterexample-search target normally scores at least 12/18
and has no zero in the first four rows.

| criterion | 0 | 1 | 2 |
|---|---|---|---|
| exact verifier | judgment only | partial exact checks | finite exact certificate with a small trusted checker |
| bounded search | no usable bound | heuristic cap | theorem-backed exhaustive bound or certificate |
| construction language | no parametrization | ad hoc families | compact generative grammar or normal form |
| independent route | same derivation repeated | implementation diversity | mathematically independent theorem/tool route |
| adversarial controls | none | positive controls only | known-positive and deliberately corrupted controls |
| source completeness | secondary summaries | key papers | primary statement, hypotheses, corrections, latest status |
| novelty window | saturated/closed | unclear | recent claim or unsearched extension with attributable priority |
| compute fit | unavailable/opaque | expensive | resumable, checkpointed, commodity exact computation |
| extension value | isolated reproduction | one refinement | minimality, family, mechanism, or surviving-variant programme |

## Mandatory routing rules

1. Reproduce a public candidate independently before extending it.
2. Credit discovery priority explicitly; replication is not rediscovery.
3. Commit a falsifiable hypothesis before computation.
4. Prefer a distinguishing invariant before a sweep.
5. Require negative controls that can falsify the verifier itself.
6. Separate SAT/solver scouting from certified results; an UNSAT claim needs a checkable proof or
   an independent exhaustive verifier.
7. A manuscript/Zenodo update requires validated novel material, not merely a successful rerun.

## Current application: Huneke-Wiegand

The public candidate has an exact finite certificate, independent expert verification, a compact
numerical-semigroup construction, and immediate extension questions. The strongest CAOS targets
are minimality, an infinite family, the endomorphism-ring escape mechanism, and the boundary of
surviving positive variants. A duplicate Python verifier is low value because the public package
already contains several.
