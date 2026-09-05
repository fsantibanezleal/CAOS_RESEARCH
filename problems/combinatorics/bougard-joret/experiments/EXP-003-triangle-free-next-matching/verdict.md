# EXP-003 verdict: the next triangle-free matching level

Date: 2026-09-05. Status: **PASS, uniform derivation [D] and independent finite validation [MV]**. Hypothesis commit `f3fdda6` was pushed before computation. The primary mathematical statement is the [complete proof](proof.md); finite checks do not replace it.

## Derived result

For every integer $d\ge7$,

$$T(d,d+1)=d^2+d+2,$$

where $T(d,m)$ maximizes the number of edges in an arbitrary finite simple triangle-free graph with maximum degree at most $d$ and matching number at most $m$. The fixed-order maximum on $2d+3$ vertices has the same value. A shortest-odd-cycle deficit bound leaves one possible extra edge; an exhaustive symbolic five-type argument rules out its equality case. Tutte-Berge then reduces arbitrary order to small even and odd components. A separate route through AEY Corollary 3.5 confirms the reduction.

The attaining graph is **Banak-Ekim-Taskin's known construction**, Proposition 4.1, not a new construction. Their Table 3 already determines this slice through $d=12$ and records $184\le T(13,14)\le185$. The uniform upper bound proves $T(13,14)=184$ and all subsequent degrees. This solves the $m=d+1$ slice of AEY Conjecture 6.1, not the entire conjecture. Source versions, direct passages, access limits and the twenty-row portfolio review are in the [source dossier](../../context/2026-09-05-next-matching-review.md).

The secondary result is only the one-edge bracket

$$d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2.$$

The lower endpoint exceeds the degree-sum prediction by $\lfloor d/2\rfloor-2$, an unbounded strict-interior discrepancy. The exact Bougard endpoint is unresolved. The known triangle-free maximizer cannot establish attainment: its complement has connectivity $d+1$, one below the requirement. A subdivided crown gives the upper endpoint with connectivity exactly $d+2$.

## Exact evidence

| Route | Declared scope | Result |
|---|---|---|
| Main stdlib certificate | $d=7,\ldots,30$, two graphs per degree | 48 graphs pass degree, triangle, matching and complement controls; 24 direct flow checks for $d\le18$ |
| Equality obstruction control | 287,564 positive five-type tuples with a designated singleton | No equality candidate survives |
| Independent NetworkX 3.4.1 reconstruction | All 48 saved graphs, no CAOS graph imports | Exact maximum matching, clique number and full vertex connectivity agree |
| Independent five-type enumeration | All 17,040 positive five-part compositions for $d=7,\ldots,10$ | No singleton-containing equality candidate survives; all-large case excluded symbolically |
| Rejected shortcut | 24 supplied complement cuts | All disconnect; independent connectivity is $d+1$ |
| Boundary control | Balanced $C_5$ blowup at $d=6$ | 45 edges exceeds proposed extension 44; range cannot simply include six |
| Corruption control | Add an edge inside a forbidden crown side | Triangle detected by both implementations |

The [main certificate](artifacts/certificate.json) binds its source and reused graph routines. The [independent receipt](artifacts/independent-audit.json) binds the certificate, proof, main implementation and independent implementation with LF-normalized SHA-256. Rerunning the pytest regression reproduces the entire main certificate in a temporary directory. The complete repository suite passed **101 tests**; focused Ruff checks passed.

Independent internal mathematical review read all eleven proof sections and found no gap, specifically checking odd degrees, equality implications without assuming complete blowups, all singleton arrangements, Tutte-Berge signs and component accounting, both connectivity arguments and the bracket algebra. It is an internal review, not external peer review or formal proof-assistant verification.

## Reproduction and residual risks

Run from the repository root using Python 3.11 or later:

```sh
python problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/run.py
python -m pip install -r problems/combinatorics/bougard-joret/experiments/EXP-002-next-shell/requirements-audit.txt
python problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching/audit.py
python -m pytest -q tests/test_bougard_joret_next_matching.py
```

The independent audit uses the existing adjacent NetworkX 3.4.1 pin. No long-running process remains. The main finite search took about two seconds and the independent audit about six seconds, inside the predeclared budget. Arbitrary-order graph enumeration was unnecessary once the distinguishing deficit invariant and Tutte-Berge formula closed the proof.

How this could be wrong: a missed equality configuration or a misapplied matching reduction would invalidate the universal theorem even if all finite checks passed; both were independently audited. A prior publication may already contain the same uniform theorem; targeted searches reduce but cannot eliminate this bibliographic risk. Complete extremal classification, higher matching levels and the exact Bougard bracket endpoint remain further work. EXP-001/002 and the published first-shell v0.02 are unchanged. A separate next-matching manuscript carries this coherent new block.
