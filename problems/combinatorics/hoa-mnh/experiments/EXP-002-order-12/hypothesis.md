# EXP-002 preflight: maximal non-Hamiltonian graphs of order 12 by the maximum-degree split

Date: 2026-11-06. Status: frozen before the production run. CPU only. Follows EXP-001 (order <= 11) and HMB-005.

## Question

Same questions as EXP-001 at order n = 12: every MNH graph of order 12, every longest cycle, Hoa's conjecture,
Zhan's Questions 2-4, and A185306(12).

## Method (exact)

Goedgebeur, Neyt and Zamfirescu (Appl. Math. Comput. 386 (2020), Corollary 12, [V] in the archived PDF): an MNH
graph of order n has maximum degree n - 1 or at most n - 4. Two disjoint cases:

- **Case A, a universal vertex:** G = K_1 join H for a graph H on n - 1 = 11 vertices. Every such G arises from
  exactly one H up to isomorphism (deleting a universal vertex is well defined up to isomorphism: two universal
  vertices are swapped by an automorphism). Generate every graph H on 11 vertices (`geng -q 11`, all
  1,018,997,864), join a universal vertex (`join6.c`), test with `mnh.c` (EXP-001's exact filter).
- **Case B, maximum degree at most 8:** every connected graph on 12 vertices with maximum degree <= 8
  (`geng -c -D8 12`), built with EXP-001's degree-sum PRUNE hook (sound: degrees only grow under geng's vertex
  extensions, so a nonadjacent pair whose degree sum exceeds n - 1 stays so, and no completion is MNH), tested
  with `mnh.c`.

A(12) = (number of MNH graphs in A) + (number in B).

## Gates (before production)

1. The split reproduces EXP-001 at orders 10 and 11: case A on graphs of order 9 (resp. 10) plus case B with
   maximum degree <= 6 (resp. 7) gives 31 (resp. 67).
2. The pruned generator alone already reproduced 18, 31, 67 at orders 9, 10, 11 (EXP-001 artifacts and this
   session's run).
3. Every MNH graph of order 12 is re-checked by EXP-001's independent `verify.py`.

## Prediction

No counterexample at order 12 (confidence MODERATE); A(12) roughly doubles, between 100 and 200 (LOW).

## Cost and stop condition

Probe: one 1/2000 slice of case B took 195 s on one core, so case B is about 3.9 hours on 28 processes; case A
is dominated by the filter, under an hour. Stop if the measured case B rate projects past 12 hours.
