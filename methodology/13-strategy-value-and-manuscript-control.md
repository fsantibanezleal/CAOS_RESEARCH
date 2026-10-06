# 13 - Strategy, value, and manuscript control

Research may change direction, but it may not lose its declared purpose. This
document is binding for every long-running problem and complements the
experiment, exploration, and publication rules.

## The research-control record

Every problem that continues beyond its first coherent theorem keeps a
machine-readable `program/<slug>/research-governance.json` and a human-readable
`program/<slug>/manuscript-map.md`. They answer five questions without relying
on chat history:

1. What was the original purpose, and what is the verified external status of
   the original problem?
2. Which research focus is active now, and why is it valuable?
3. What exact theorem-sized success gate would close that focus?
4. What evidence would stop or redirect it?
5. Which manuscript owns every theorem, finite result, refutation, and open
   obligation?

The original problem and a derived research focus are different objects. A
settled conjecture may motivate valuable extension work, but the record must
never describe an extension as another attempt to settle the original
conjecture.

## Focus admission gate

A new focus is admitted only when all fields below are persisted before its
first experiment:

- `target`: one mathematical question, stated independently of a computation;
- `value`: why answering it matters beyond filling another table entry;
- `success_gate`: the theorem, classification, counterexample, or reusable
  method that would close the focus;
- `stop_conditions`: evidence that makes further work low value;
- `novelty_status`: primary sources searched and the remaining uncertainty;
- `manuscript_route`: the existing paper that would receive the result, or the
  precise trigger for creating a new coherent paper;
- `first_bounded_action`: the cheapest invariant-first step that can decide
  whether the focus deserves an experiment.

An exposed invariant, an unfinished sequence, or a technically difficult
calculation is not by itself a reason to continue.

## Stop and review cadence

A strategic review is mandatory at each of these boundaries:

1. the original objective is achieved or externally settled;
2. a manuscript reaches a coherent theorem;
3. three consecutive experiments are refuted, finite-only, or fail to improve
   the active success gate;
4. a route moves to a new mathematical object or a substantially narrower
   quotient, projection, or parameter family;
5. a new manuscript or Zenodo version would be triggered.

At the review, the session either retains the focus with a written reason,
redirects to a better focus, or marks it `gated`, `dormant`, or `closed`.
Repeated instructions to continue do not waive this review. The user must be
shown the changed target and its value before a materially different program
is treated as the continuation of the previous one.

## Result and manuscript routing

Every experiment receives one disposition:

- `primary-manuscript`: theorem or essential proof input included in a paper;
- `companion-manuscript`: coherent result separated into a focused paper;
- `research-record`: finite, negative, calibration, or supporting evidence that
  remains in the experiment archive;
- `superseded`: retained historically but not used as current evidence.

Not every experiment deserves a manuscript. Every validated theorem does need
a manuscript home. A large paper must split when its parts have different
central questions, proof toolkits, or intended audiences. A split does not
rewrite or delete an immutable published version. It produces focused future
submission papers with explicit dependency and overlap statements.

## Publication and novelty boundary

Repository validation proves internal correctness only to the extent of the
recorded checks. Zenodo proves public persistence, not peer review or worldwide
novelty. Each manuscript map therefore distinguishes:

- internally proved;
- primary-source overlap checked;
- external novelty not yet independently confirmed;
- expert reviewed or peer reviewed, when that actually occurs.

No negative literature search is described as proof of novelty.
