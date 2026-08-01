# tau-conjecture: RESUME (zero-loss handoff)

Updated 2026-08-01 (opening round close). First read for any fresh session,
per methodology 07. Derived view: on conflict, experiment verdicts win.

## 1. State in one screen

The problem: for $f \in \mathbb{Z}[x]$ computed by a constant-free SLP
(gates $+,-,\times$, free constants $-1,0,1$, input $x$, length $\tau(f)$ =
gate count), Shub-Smale (1995) conjecture
$$z(f) \le (1+\tau(f))^c \quad (z = \#\text{distinct integer roots})$$
for universal $c$. OPEN. [V: statement via Buergisser 2024 survey eq. 4.5.]

Verified ladder [V, dossier section 2]: conjecture $\Rightarrow$
$P_{\mathbb{C}} \ne NP_{\mathbb{C}}$ (SS95, via: every $(m_n n!)$ hard to
compute); conjecture $\Rightarrow VP^0 \ne VNP^0$, and $(n!)$ hard alone
$\Rightarrow VP^0 \ne VNP^0$ (Buergisser 2009); permanent easy
$\Rightarrow \tau(n!)$ polylog (TR06-113); with division $n!$ IS easy
(Shamir 1979); real-zeros analogue FALSE; no nontrivial lower bound on
$\tau(n!)$ known.

OUR results (all exact, EXP-001, [D] machine-verified):
$$z_{\max}(1)=1,\ z_{\max}(2)=2,\ z_{\max}(3)=3,\ z_{\max}(4)=3.$$
$z_{\max}(\tau) := \max\{z(f) : \tau(f) \le \tau\}$ decision-complete to
$\tau = 4$; enumerator anchored to Markstroem's published integer census
(exact match, depths 1-7).

## 2. Objects table

| Object | Definition | Owner |
|---|---|---|
| $\tau(f)$ | min gates, constant-free SLP, inputs $\{-1,1,x\}$ (free-0 elim lemma) | EXP-001 hypothesis lemmas |
| $z_{\max}(\tau)$ | max distinct integer roots at $\tau(f) \le \tau$ | EXP-001 |
| Reached-set state | frozen set of computed values; BFS by length with set dedup | EXP-001 run.py |
| Markstroem anchors | Figure 1 of arXiv:1306.3091v4 (reached sizes + intervals, k<=9) | context dossier section 5 |
| Record witnesses | 37 polys with z=3 at depth 4 (e.g. $-x(x+1)(x+2)$) | artifacts/census.json |

## 3. Experiment index

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| 001 | $z_{\max}(\tau \le 4)$ exact + integer regression gate | CONFIRMED | $z_{\max}(4) = 3$; gate PASS on all 7 anchors |

## 4. In flight

Nothing running. No mid-derivation mathematics pending beyond the minted
question: minimal $\tau$ with $z_{\max}(\tau) = 4$. Candidate upper bounds
to test at declaration time of EXP-002: separated-pair products like
$(x^2-1)(x^2-4)$ (roots $\{\pm1,\pm2\}$; naive cost: $x^2$ (1), $-1$ tail
(1), the constant 4 and second factor cost more; count carefully), and
shifted-triple extensions $x(x-1)(x+1)(x-2)$-type. The census at $\tau=5$
decides; naive state count est. ~1M states (Python feasible, minutes), with
TCB-005 canonicalization the safer route.

## 5. Next actions, ordered

1. EXP-002: extend the census to $\tau = 5$ (declare hypothesis: value of
   $z_{\max}(5)$, decide the minimal-$\tau$-for-4-roots question if <= 5).
   Command: venv python `problems/computation-complexity/tau-conjecture/experiments/EXP-002-*/run.py`
   patterned on EXP-001 (BFS depth 5; budget ~1 h; checkpoint per depth).
2. TCB-005: prove the canonicalization lemmas (sign symmetry
   $f(x) \mapsto \pm f(\pm x)$ orbit reduction; dominated-state pruning)
   BEFORE using them to shrink the $\tau = 6$ search; add sympy cross-check
   of the polynomial arithmetic layer.
3. TCB-002: fetch and read Shub-Smale 1995 (Duke) in full; upgrade the
   dossier tags.
4. TCB-006: integer census extension toward Markstroem's length-11
   frontier (checkpointed DFS with his squaring-reach pruning).
5. Wiki pages 01-03 transcription from the dossier + EXP-001 verdict.

## 6. Where everything lives

- Dossier + references: `problems/computation-complexity/tau-conjecture/context/`
- Experiments: `problems/computation-complexity/tau-conjecture/experiments/EXP-001-small-tau-census/`
  (hypothesis, run.py, artifacts/census.json, verdict)
- History: `problems/computation-complexity/tau-conjecture/history/log.md`
- Wiki: `problems/computation-complexity/tau-conjecture/wiki/README.md`
- Program: `program/tau-conjecture/` (plan, backlog, state, lenses, this file)
- Mirror: `<CAOS_MANAGE>/plans/caos-research/tau-conjecture/`
- Heavy artifacts: none yet (census.json is small and in-repo); future long
  runs write `E:\_Datos\caos-research\tau-conjecture\EXP-NNN\` + manifests.

## 7. Gotchas

- Run with the MAIN checkout venv:
  `D:\_Repos\Research_Caos\CAOS_RESEARCH\.venv\Scripts\python.exe`
  (worktrees carry no venv). Pure stdlib so far; no GPU used yet.
- Markstroem's integer model starts from 1 ONLY with POSITIVE normalized
  values; our polynomial model has inputs $\{-1,1,x\}$ and allows negative
  values; do not mix the two normalizations (Stage A vs Stage B in
  EXP-001).
- Markstroem Figure 1 "reached at k" counts values computable at length
  <= k INCLUDING 1 (fixed interpretation, matched on 14 numbers).
- $\tau'$ (ultimate complexity, min over multiples) vs $\tau$: his
  factorial tables are mostly $\tau'$; keep the distinction in any
  comparison.
- The free-0 elimination lemma (hypothesis lemma 1) is reasoning-verified,
  not machine-tested: revisit within TCB-005.

## Lenses ledger

| Round | Spine | Other lenses | Exploration yield |
|---|---|---|---|
| 2026-08-01 | Census decided $\tau \le 4$ | Anatomy (record mechanisms: consecutive triples, shift-for-one-gate), invariant (degree cap decides nothing at these depths; recorded), dictionary (Markstroem method import), audit (regression gate) | The $z_{\max}$ niche (apparently unpublished); minimal-$\tau$-for-4-roots question minted |
