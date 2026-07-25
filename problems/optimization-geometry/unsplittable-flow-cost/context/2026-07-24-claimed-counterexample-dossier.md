# The 2026 claimed counterexample: provenance, exact data, and the verification programme

Dated 2026-07-24. Companion to `2026-07-24-literature-status-dossier.md`. This dossier
records WHAT is claimed, WHERE it came from, and the exact object that must be decided.
It decides nothing: the adjudication is EXP-002, run by our own code.

Status of everything in section 2 below: **[CLAIMED]** until EXP-002 reports.

## 1. Provenance chain

| Date | Event | Evidence we hold | Tag |
|---|---|---|---|
| 2026-07-22/23 | Public announcement that the "Dinitz-Garg-Goemans conjecture is false" (meaning the Goemans COST conjecture, Conj 1.2; the DGG theorem itself is not in question), attributed to Dmitry Rybin with GPT-5.6 Pro | thread mirror threadnavigator.com/thread/2079904005652893709; secondary write-ups on mathlab.drummerduck.com, vibemathed.com, windowsnews.ai, digg.com, officechai.com | [CLAIMED] |
| 2026-07-23 | Reports that Grok 4.5 produced a comparable object independently | secondary coverage only (biggo.com, windowsnews.ai) | [CLAIMED], and note that "independently produced the same instance" is itself an unverified assertion |
| 2026-07-23 | A 3-parameter generalisation on the same 7 nodes posted publicly by a third party, with Rybin's instance reported as $(b,m,g) = (10,5,1)$ with costs scaled by $1/5$ | search-result text of x.com/basedjensen/status/2080020575968543230; the post itself was not retrievable (HTTP 402) | [CLAIMED], transcription incomplete, must not be relied on |
| 2026-07-24 | Felipe supplied the proposer's artifact bundle directly to this programme | the files themselves, archived and hashed below | [VERIFIED] that we hold them |
| 2026-07-24 | Search for peer-reviewed or preprint confirmation, or any response from the authors of the positive results (Traub, Vargas Koch, Zenklusen, Skutella, Warode, Morell, Majthoub Almoghrabi) | none found | [VERIFIED] as a negative search result |

**Archived bundle** (heavy data policy, methodology/04: files live on E:, in-repo only
this manifest), at `E:\_Datos\caos-research\unsplittable-flow-cost\claimed-counterexample\`:

| File | SHA-256 |
|---|---|
| `dgg_counterexample_instance.json` | `1fd5252d2554c1cc883ea97edf32f459582b2e5f1491362b2ef906428310cce5` |
| `dgg_counterexample_verify.py` | `70fc92a8bacb95ffa8a12073e1da398d3857886010d621603ffcc4f948ce3a73` |
| `dgg_counterexample_certificate.tex` | `f31effb363265f5c50ab071cdef7a36ca38d92458e5fbdb796b9e191d5c2a315` |
| `dgg_counterexample_certificate.pdf` | `b025cdcfae7519353b2f716b76d31b8901a488a471e2df06e0601a944b10e702` |
| `dgg_counterexample.svg` | `c0a84f7c02e474b6892c56b52d6f285d8d6f736dcb9d669e8f3db3e25fd14e73` |
| `Onjecture_resolution_chat.md` (full model transcript, 1162 lines) | `c1343b286b52ea2e0b3912d9cd2f785d040bfa594a7bb450eb851de3459f48d4` |
| `2308.02651v1.pdf` + `arXiv-2308.02651v1.tar.gz` (the paper the campaign was run against) | `e3eb8327...0723bd`, `29415f76...f958e764` |

**Independence rule.** `dgg_counterexample_verify.py` is archived as provenance and is
NOT imported, executed, or consulted while our own checker is written. Our enumerator is
written from the conjecture statement in the literature dossier, and it enumerates paths
by its own search rather than from any supplied path list. Agreement with the proposer's
verifier, if it occurs, is then evidence; agreement obtained by reusing their code would
be worthless.

## 2. The instance, transcribed exactly

Vertices $V = \{s, u, v, w, t_1, t_2, t_3\}$, source $s$, terminals $t_1, t_2, t_3$ with

$$d_1 = 15, \qquad d_2 = 10, \qquad d_3 = 15, \qquad d_{\max} = 15.$$

Nine arcs, with fractional load $x_a$ and per-unit cost $c_a$ (all integer, all costs
nonnegative, unlisted costs zero):

| arc $a$ | $x_a$ | $c_a$ | $x_a + d_{\max}$ |
|---|---|---|---|
| $s \to t_1$ | 10 | 2 | 25 |
| $s \to t_2$ | 6 | 3 | 21 |
| $s \to u$ | 24 | 0 | 39 |
| $u \to t_3$ | 10 | 2 | 25 |
| $u \to v$ | 14 | 0 | 29 |
| $v \to t_1$ | 5 | 0 | 20 |
| $v \to w$ | 9 | 0 | 24 |
| $w \to t_2$ | 4 | 0 | 19 |
| $w \to t_3$ | 5 | 0 | 20 |

Claimed fractional cost: $c^T x = 2 \cdot 10 + 3 \cdot 6 + 2 \cdot 10 = 58$.

Claimed path structure: exactly two $s$-$t_i$ paths per terminal,

$$E_1 = s t_1,\quad Z_1 = s\,u\,v\,t_1; \qquad E_2 = s t_2,\quad Z_2 = s\,u\,v\,w\,t_2; \qquad E_3 = s\,u\,t_3,\quad Z_3 = s\,u\,v\,w\,t_3,$$

with each expensive path $E_i$ costing exactly $30$ when it carries its demand
($15 \cdot 2 = 30$, $10 \cdot 3 = 30$, $15 \cdot 2 = 30$) and each $Z_i$ costing zero.

Claimed mechanism: the three zero-cost choices are PAIRWISE congestion-incompatible
($Z_2 Z_3$ overloads $v \to w$; $Z_1 Z_3$ overloads $u \to v$; $Z_1 Z_2$ overloads
$s \to u$ because $t_3$ uses $s \to u$ on either of its paths), so a congestion-good
routing takes at most one $Z_i$, hence at least two $E_i$, hence cost at least 60 > 58.

Claimed structural reading, from the certificate: the fractional selection weights of the
zero-cost choices are $5/15, 4/10, 5/15 = 1/3, 2/5, 1/3$ summing to $16/15 > 1$, i.e. the
instance realises the triangle (odd-cycle) stable-set LP gap, and the cost vector is a
nonnegative separator of that inequality. The certificate also gives a normalised
parametric family: with $d_1 = d_3 = 1$, $d_2 = b$, cheap-choice probabilities $r, q, r$,
a strict counterexample whenever

$$2r + q > 1, \qquad b(1-q) > r, \qquad 2r + bq < 1,$$

instantiated at $b = 2/3$, $r = 1/3$, $q = 2/5$ and scaled by 15.

## 3. Independent hand-check performed at transcription time

Before any code: source outflow $10 + 6 + 24 = 40 = 15 + 10 + 15$; conservation at
$u$ ($24 = 10 + 14$), $v$ ($14 = 5 + 9$), $w$ ($9 = 4 + 5$); terminal inflows
$10 + 5 = 15$, $6 + 4 = 10$, $10 + 5 = 15$. Pair conflicts: $Z_1 Z_3$ loads $u \to v$
with $30 > 29$; $Z_2 Z_3$ loads $v \to w$ with $25 > 24$; $Z_1 Z_2$ loads $s \to u$ with
$15 + 10 + 15 = 40 > 39$. Each single-$Z$ routing checks out arc by arc. This hand-check
is recorded for honesty about what was known before the machine ran; it is NOT the
verdict, it does not establish path-enumeration completeness (test C8), and it is exactly
the kind of check that has historically missed unintended paths.

## 4. The verification programme (what EXP-002 must decide)

Beyond the C1-C9 battery of the literature dossier, EXP-002 must produce these numbers,
all in exact integer arithmetic:

| ID | Quantity | Why it matters |
|---|---|---|
| Q1 | the complete list of simple $s$-$t_i$ paths, found by our own search | C8; the claim "exactly 2 each" is itself a claim |
| Q2 | the number of unsplittable routings and, for each, its exact load vector, cost, and per-arc violation | the decision itself |
| Q3 | $\min\{c^T y : y$ congestion-good$\}$ versus $c^T x$ | the refutation, or its failure |
| Q4 | $\alpha_{\mathrm{inst}} := \min_{y \text{ cost-good}} \max_a \frac{(y_a - x_a)^+}{d_{\max}}$ | the QUANTITATIVE content: the lower bound on $\alpha^\*$ this instance forces |
| Q5 | acyclicity of the digraph | decides whether Conj 1.4 falls too |
| Q6 | planarity, and presence of a $K_4$ subdivision / series-parallel status | C2, C4; locates the instance against MSW25 and TVZ24 |
| Q7 | whether the demand multiset is closed under divisibility (multiples of one another) | C1 |
| Q8 | existence of a routing meeting the cost-free two-sided bounds | C5, i.e. does Conj 1.3 survive |
| Q9 | existence of a cost-good routing within $2 d_{\max}$ | C4, i.e. does TVZ24 survive on this planar instance |

A hand-computed expectation for Q4, recorded BEFORE the run so it can be wrong: the
cost-good routings are those of cost 0 or 30, i.e. those using at least two $Z_i$; the
cheapest violations among them appear to be one unit over the bound on a single arc, so
$\alpha_{\mathrm{inst}}$ is expected to be $16/15$, not something dramatic. If that is
right, the instance refutes the constant 1 by the smallest possible integer margin and
says nothing about $O(d_{\max})$. This prediction is declared in EXP-002's hypothesis.

## 5. The separation LP: eliminating the cost vector (a tool, not a claim)

The proposer's transcript contains a reduction worth keeping, and worth re-deriving in
our own hands before use. Fix $(G, s, T, d, x)$ and let $\mathcal{U}(x)$ be the finite
set of load vectors of congestion-good unsplittable routings. Then $(G, s, T, d, x)$
admits SOME nonnegative cost vector making it a counterexample if and only if the LP

$$\max\ \delta \quad \text{s.t.} \quad c^T(y - x) \geq \delta \ \ \forall y \in \mathcal{U}(x), \qquad \textstyle\sum_a c_a = 1, \qquad c \geq 0$$

has optimum $\delta > 0$. [CLAIMED as transcribed; the direction "optimum $> 0$ implies
counterexample" is immediate, and the converse follows by scaling a witnessing $c$; our
own derivation and an exact rational implementation are required before this is used to
certify anything, backlog UFB-010.]

Why it matters far beyond this one instance: it removes the cost vector from the search
space entirely. An exhaustive hunt over small instances then ranges over
(digraph, demands, fractional flow) only, with the cost question answered exactly by one
rational LP per instance. That is the engine of the planned exhaustive small-instance
campaign, and it also computes, per instance, the best achievable $\delta$, hence a
principled ranking of "how badly" an instance breaks the conjecture. A parametric version
with the violation budget $\alpha$ as a parameter computes the trade-off curve directly.

## 6. What the transcript records about failed attempts (method value)

The transcript is a log of a long campaign, and its failures are informative for our own
search design. Recorded in it: two-backbone prefix networks cannot give a counterexample;
three tracks cannot enforce a permutation; unequal demands are indispensable; costs must
be genuinely distributed over the fractional support; the graph must go beyond the known
positive structures; and, most operationally, checking only intended paths (or even
hundreds of discovered paths) is insufficient, so a valid counterexample must carry an
exact pricing or exhaustive-routing certificate. [CLAIMED, all of it: these are assertions
in a model transcript, not proofs we have checked. They are logged as SEARCH HEURISTICS
for our own campaign, never as facts, and any of them we come to rely on gets its own
experiment.]

## 7. Honest note on what our verification can and cannot establish

If EXP-002 confirms: we will have established, by our own exact computation, that this
specific finite instance refutes Conjecture 1.2 (and 1.4, and the convex-combination
form). That is a complete mathematical fact requiring no external authority, because the
object is finite and the arithmetic is exact. What it will NOT establish: who found it
first, whether the announcement's framing is accurate, or whether the community accepts
it. Those are social facts, not mathematical ones, and this programme does not adjudicate
them. Any external communication about this remains gated on Felipe.

If EXP-002 refutes the claim (the instance fails feasibility, or a congestion-good
routing of cost at most 58 exists, or the path enumeration was incomplete), that is a
first-class result and gets the same publication treatment, with the failure mode named
precisely.
