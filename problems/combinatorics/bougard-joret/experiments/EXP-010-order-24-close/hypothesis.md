# EXP-010 preflight: the two edge counts left open at order 24 (BJB-021)

Date: 2026-11-10. Status: frozen before any computation. CPU only.

## Question

EXP-009 left (24,7,3) and (24,3,7) open, each at its last edge count below the conjectured value: is there a graph
on 24 vertices with 40 edges, minimum degree 3, independence number 7 and connectivity at least 3, and is there one
with 94 edges, minimum degree 7, independence number 3 and connectivity at least 7? If not, f(24,7,3) = 41 and
f(24,3,7) = 95, the conjectured values.

## Method

EXP-009's pipeline unchanged (`run_enum.py`, `geng_a7` and `geng_a3` gated in EXP-006, `filter2`), one edge count
per triple: `run_enum.py ... 24 7 3 40 40` and `run_enum.py ... 24 3 7 94 94`, run at the same time on 14 processes
each, split into 56 disjoint parts.

## Prediction

No graph is found at either edge count, so both values equal the conjectured ones (MODERATE).

## Budget

At most 20 hours of wall-clock time per edge count; a cap leaves the triple open with the bound from EXP-009.
