# petersen-coloring: RESUME (zero-loss handoff)

Updated 2026-09-03 at open. First read for any fresh session, per methodology 07. Derived view: on
conflict, experiment verdicts win.

## 1. State in one screen

The problem. `P` is the Petersen graph. A Petersen coloring of a cubic graph `G` is a map
$\sigma: E(G) \to E(P)$ such that for every vertex $v$ of $G$ there is a vertex $w$ of $P$ with
$\sigma(\partial_G(v)) = \partial_P(w)$. Jaeger 1988: every bridgeless cubic graph has one [V via
GJMMM]. Jaeger 1985: equivalent to a normal 5-edge-coloring, a proper 5-edge-coloring in which
every edge $uv$ satisfies $|c(\partial(u)) \cup c(\partial(v))| \in \{3, 5\}$ [V via GJMMM].
Implies Berge-Fulkerson (six perfect matchings covering every edge exactly twice) and the
5-cycle double cover conjecture [V, Open Problem Garden; primary derivation pinned in context].

Status 2026-09-03. FALSE. Putman (Zenodo 2026-08-06/08, arXiv:2608.10012): two nonisomorphic
112-vertex counterexamples, girth 5, connectivity 3, cyclically 4-edge-connected, automorphism
groups of order 1 and 6, CNF plus DRAT certificates [V, artifacts hash-verified locally]. Jooken
(arXiv:2608.10028): human-checkable proof via the P-coloring sets of the 4-poles [V summary].
Goedgebeur-Jooken-Macajova-Mattiolo-Mazzuoccolo (Zenodo 21933786, 2026-08-14): 52-vertex
cyclically 4-edge-connected girth-5 counterexample (edge list read), infinite cyclically
4-edge-connected families, smallest order in $[38, 52]$, Problem 5 (cyclic 5-connectivity),
Conjecture 6 (normal 6), strong normal 6 verified on one 112 graph only [V, read in full].
A 68-vertex example exists on X, not retrievable [U].

CAOS results: none yet. EXP-001 declared.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| `G112` | Putman's main graph, sorted-edge-list SHA-256 `dc16cc18...e8b`, 112 vertices, 168 edges | EXP-001 |
| `H112` | Putman's D3-symmetric graph, digest `0f2d8858...35c7` | EXP-001 |
| `G52` | GJMMM appendix graph, 52 vertices, 78 edges | EXP-001 |
| `F` | Petersen graph minus two adjacent vertices, an 8-vertex 4-pole | PCB-008 |
| `C` (claw six-pole) / `C` (GJMMM 4-cycle 4-pole) | connectors; the two papers use the letter for different poles | context dossier |
| `L` | `4F + C`, 36-vertex 4-pole | PCB-008 |
| `P-Col(M)` | set of boundary color tuples of P-colorings of a multipole `M` | PCB-008 |

## 3. Experiment index

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| 001 | Do our own encodings certify `G112`, `H112`, `G52` and accept controls? | declared | pending |

## 4. In flight

EXP-001 declared; no run yet. Tooling smoke test (Petersen graph, both encodings, proof
round-trip through drat-trim) is the first command.

## 5. Next actions, ordered

1. Smoke: `.\.venv\Scripts\python.exe problems\combinatorics\petersen-coloring\experiments\EXP-001-independent-certification\run.py --smoke`
2. Full EXP-001 run, verdict, history, wiki 03.
3. Declare EXP-002 (Berge-Fulkerson first), run, verdict.
4. EXP-003, EXP-004, EXP-005; manuscript v0.01; Zenodo.

## 6. Where everything lives

| what | path |
|---|---|
| problem tree | `problems/combinatorics/petersen-coloring/` |
| programme record | `program/petersen-coloring/` |
| scouting record | `program/scouting-2026-09/` |
| external evidence | `E:/_Datos/caos-research/petersen-coloring/` (sources, DRAT archives) |
| management mirror | `_CAOS_MANAGE/plans/caos-research/petersen-coloring/` |
| manuscript | `manuscripts/petersen-coloring/` (created with EXP-005) |

## 7. Gotchas

- Putman's Zenodo DOI in GJMMM's reference list is `10.5281/zenodo.21819153` (v1.0.0); the
  v1.1.0 record is `21845291`; the graphs are unchanged between versions [V, changelog].
- GJMMM's concept record `21933785` has no API entry; the version record is `21933786`.
- CaDiCaL in WSL is 1.7.3 (Putman used 3.0.1); drat-trim binary lives under the huneke-wiegand
  tools folder and is shared.
- Two different poles are both called `C` in the two papers (claw six-pole vs trimmed-K4
  4-pole); name them explicitly in every artifact.
- Solver UNSAT without a checked DRAT is not a theorem here.
