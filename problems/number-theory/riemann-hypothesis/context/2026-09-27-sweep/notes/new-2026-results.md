# New 2026 results on simple / critical zeros of zeta (global and short intervals) beyond the tracked list - sweep of 2026-09-27

Access notes (they limit what could be verified): arxiv.org, export.arxiv.org, alphaxiv.org, zenodo.org and semanticscholar.org were all blocked by the egress proxy for direct fetches, and GitHub search/API was repository-scoped. As a result:
- arXiv and Zenodo content below comes from **search-engine snippets (secondary)** unless marked VERIFIED.
- VERIFIED means read directly from a primary artifact: the locally cached arXiv source tarball under `problems/number-theory/riemann-hypothesis/context/source-cache/`, a public git repository cloned via `git clone`/`git ls-remote`, or anthropic.com.
- **Version numbers of arXiv items could not be checked** except where noted, so no v2/v3 of 2608.13637, 2609.07918, 2609.15329 or 2609.24167 could be confirmed or ruled out.

Tracked set used for de-duplication: every arXiv ID in the assignment, plus the program's `references.md` items (2510.18132, 2511.20059, 2603.28104, 2503.15449, 2306.04799, trmdy, teal-sea, Yang-Yang Zenodo 21975237, Yuhang Shi Zenodo 21926962, tawanerguo-cn, zach7036, and Zenodo 22066689/22287432/concept 21940706). The program's own Zenodo records (22727389, 22823615, 22851518, 22852479, 22860012, 22940291, 22984155, 22728168) came up repeatedly in search. They are self-citations and are NOT new external results.

## Q1. New preprints (late Aug to 27 Sep 2026) that improve the global 0.6725 simple-critical proportion or the short-interval onset/proportions

### Takeaway
No external preprint beyond the tracked set improves either the global constant or the short-interval onset/proportions. The only external global improvement found is the already-tracked Wang arXiv:2609.24167, which gains delta_0 = 6.66624e-8 over C_0. The program's `references.md` records that paper under the wrong title. Every short-interval positivity-onset statement near theta ~ 0.5459 that search surfaced is the program's own Zenodo output, not external work.

### Cited Findings
- **VERIFIED from the cached source tarball: arXiv:2609.24167v1 (Biao Wang, Yunnan University, submitted 2026-09-21).**
  - The actual title is "*Proportions of the non-trivial zeros of the Riemann zeta function*" (MSC 11M06, 11M26).
  - The abstract defines C_0 = 3/2 - cot(1/sqrt2)/sqrt2 = 0.67250... and C_1 = (C_0+1)/2 = 0.83625....
  - It improves these to C_0 + delta_0 and C_1 + delta_0/2, with delta_0 = 6.66624... x 10^-8, "by refining the method of Lamzouri".
  - Theorem 1.1 reads: liminf N_0^s(T)/N(T) >= C_0 + delta_0, unconditionally.
  - **Internal erratum:** `references.md` item 28 gives the title as "A refinement of the two-thirds theorem for simple critical zeros of the Riemann zeta-function". That does not match the source title and should be corrected.
  - Sources: local `context/source-cache/wang-global-refinement-2609.24167v1.tar.gz` (main.tex); [arXiv html](https://arxiv.org/html/2609.24167).
- The web index for "arXiv 2609 simple zeros critical line proportion" and its variants surfaced only these zeta-zero papers: 2608.13637, 2609.02882, 2609.07918, 2609.15329, 2609.24167, 2609.27808, 2501.14545, 2503.15449, 2511.20059 and 2603.28104. All are tracked. - [search result set incl. arXiv 2609.07918](https://arxiv.org/pdf/2609.07918), [arXiv 2609.15329](https://arxiv.org/abs/2609.15329)
- Short-interval positivity statements found by search are all program self-citations:
  - "positivity threshold in (0.5459, 0.546); at theta = 0.546 the certified simple-critical lower proportion exceeds 0.0000976239413345" - [Zenodo 22851518](https://zenodo.org/records/22851518)
  - "six-square constant places the unique positivity onset in (0.5458837, 0.5458838); at theta = 0.545884 the lower bound exceeds 2.5541123454645702e-7" - [Zenodo 22860012](https://zenodo.org/records/22860012)
  - "(theta - 1/2)/(4 e C3) of distinct odd-multiplicity critical zeros for every 1/2 < theta < 1" - [Zenodo 22851518](https://zenodo.org/records/22851518)
  - "At theta = 3/4: simple-critical >= 0.4190768284253039967, distinct >= 0.7095384142126519983" - [Zenodo 22727389](https://zenodo.org/records/22727389)
  - The linked GitHub-release record is "fsantibanezleal/CAOS_RESEARCH: 0.64.000" - [Zenodo 22728168](https://zenodo.org/records/22728168)
- A Zenodo record titled "A sharp three-point kernel bound and improved proportions of zeta zeros" states that Wang's three-point kernel argument yields 0.6725007995946757558. It is also the program's own record (references.md lines 327-329). - [Zenodo 22940291](https://zenodo.org/records/22940291)
- Other unreviewed Zenodo global claims of 67.27556%, 67.2913% and 67.3399% are all versions under concept 21940706, which is already tracked in the Levinson preflight dossier. The 67.3399% record also claims "conditional advances beyond 67.92%". - [Zenodo 21940707](https://zenodo.org/records/21940707), [Zenodo 21960305](https://zenodo.org/records/21960305), [Zenodo 22066689](https://zenodo.org/records/22066689)

### Inferences
- The global external frontier as of 27 Sep 2026 is C_0 + 6.67e-8 ≈ 0.67250007 (Wang v1, unreviewed).
  - The program's claimed sharp-kernel value 0.6725007995946757558 appears to be at or above Wang's C_0 + delta_0. Wang's exact decimal should be compared against it, to rule out a coincidence with Wang's own number rather than an improvement.
  - Nine-point and 219-point candidates of about 0.67331 (trmdy, Yuhang Shi) remain unrefereed GitHub/Zenodo claims.
- No external paper yet states a positive proportion of simple or critical zeros in (T, T+T^theta] for theta below Wang's baseline onset. The program's onset near 0.5459 is not contested or superseded in anything found.

### Gaps
- Could not list arXiv math.NT for 22-27 Sep 2026 directly, so a preprint posted in the last ~5 days and not yet web-indexed could be missed.
- Could not check whether 2609.07918, 2609.24167 or 2609.15329 have v2 revisions.

## Q2. New 2026 results on distinct zeros, multiplicity bounds, zeros of derivatives, Levinson-Conrey type proportions

### Takeaway
The main new external finding is a **retraction**. On 2026-09-03 the Hongyi Yang "critical-line program" (mathematics credited to Claude) retracted its "density one" preprint v0.92, Zenodo 22065921. The stated reason is that unconditional higher even trace moments of the compressed Weil matrix cannot be proved with the declared tools. The same authors' 0.7962/0.8981 repository, Zenodo 21975237 (already quarantined by the program), has not been updated since 2026-08-17. No new external distinct-zero, multiplicity or zeta' proportion results were found.

### Cited Findings
- **VERIFIED from a git clone of `JoshuaHKU/zeta-density-one-reproduction`, HEAD commit `ac85152`, 2026-09-03: "Retract v0.92: unconditional higher-moment claims untenable".**
  - RETRACTION.md says the preprint "asserted **unconditional** convergence of higher even trace moments of the compressed Weil matrix (the mu_4 -> 13/4 tier and above), and consequences drawn from them (the 'density one' tier)".
  - A reviewer's "Proposition R" shows "finite unconditional bounds on higher even moments would already force zero-free regions of power-law strength ... the claimed proofs necessarily contain an essential gap. The gap was located; the claims do not survive."
  - It lists as still valid: "a two-window cluster-energy floor theorem; an energy-counting zero-density estimate with an unconditional <=4-cluster form and one explicitly starred lemma; a conditional simple-zeros proportion 0.6788 modulo the same starred lemma", with those results to be released separately.
  - Signed "mathematics: Claude (Anthropic); program director: Hongyi Yang".
  - Links: [repo](https://github.com/JoshuaHKU/zeta-density-one-reproduction), [Zenodo 22065921](https://zenodo.org/records/22065921)
- **VERIFIED from a git clone of `JoshuaHKU/zeta-0.7947-reproduction`, last commit `d85bddf`, 2026-08-17, "paper upgraded to proof grade".**
  - The README still claims N_0^s/N >= 0.7962 and N_d/N >= 0.8981, built on the Claude two-thirds preprint, with authors Hongyi Yang and Shihua Yang.
  - The inputs include M_6 = 12809/1260 and C_5 = 1/36, i.e. sixth-moment data.
  - There is no retraction file in this repository.
  - Links: [repo](https://github.com/JoshuaHKU/zeta-0.7947-reproduction), [Zenodo 21975237](https://zenodo.org/records/21975237)
- Lamzouri v2 (tracked) supplies the distinct-zero constant 83.62%, simple-or-critical >= 88.76%, and average of simple and critical proportions >= 83.62%. Search found nothing that improves these beyond Wang's delta_0/2 gain. - [arXiv 2609.02882](https://arxiv.org/abs/2609.02882)
- The Dirichlet-family analogues found are the tracked 2608.16034 and 2609.27808 (Zhixu Hua, Xiufan Yang). The latter proves "unconditional lower bounds, relative to the total zero multiplicity in (T,2T], for both simple and distinct critical-line zeros and for all distinct zeros in a family of nonprincipal characters modulo q". - [arXiv 2609.27808](https://arxiv.org/abs/2609.27808)
- arXiv:2511.06109, "Levinson's theorem and its generalization for Dirichlet L-functions", is a 2025 expository report (search dates a version to June 2026). It re-proves Levinson's 1/3 and Wu's (2018) >2/5 simple-critical result for Dirichlet L-functions. There is no new constant. - [arXiv 2511.06109](https://arxiv.org/abs/2511.06109)
- No 2026 paper on zeros of zeta' or higher derivatives, or on Levinson-Montgomery proportions, was found. The searches returned only pre-2022 work such as [arXiv 2104.10243](https://arxiv.org/pdf/2104.10243).

### Inferences
- The retraction's Proposition R targets unconditional control of higher even moments. The 0.7962 claim relies on sixth-moment constants, so Proposition R very plausibly undermines it too, even though that repository has not been formally retracted.
  - This strengthens the program's existing quarantine of the "79.62%" figure.
  - This is my inference; the retraction text does not name the 0.7962 repository.
- The "conditional 0.6788 simple-zeros proportion modulo a starred lemma" is a new claim to watch. It is simple zeros only, not critical, and conditional. It is not yet public as a standalone document.

### Gaps
- No public document yet for the Yang program's post-retraction results: the cluster-energy floor, the energy-counting zero density, and the conditional 0.6788.
- No 2026 multiplicity-bound result (m(rho) << log T / log log T type) was found.

## Q3. Levinson's method in short intervals / new mollifiers in 2026

### Takeaway
No new external 2026 short-interval Levinson paper or new mollifier construction (Feng-type, multi-piece, improvements on 2/5 or 41%) was found beyond the tracked Conrey-Farmer-Kwan-Lin-Turnage-Butterbaugh arXiv:2508.11108 and the Selberg-method paper arXiv:2609.15329.

### Cited Findings
- Search results for Levinson/mollifier 2026 returned only tracked items (2508.11108, 2609.15329, 2609.07918, 2609.24167) and classical work (Feng 1003.0059, Bui-Conrey-Young 1002.4127, 1706.04593). - [arXiv 2508.11108](https://arxiv.org/abs/2508.11108), [arXiv 1706.04593](https://ar5iv.labs.arxiv.org/html/1706.04593)
- Wang 2609.07918 cites the prior short-interval Levinson baseline: Steuding (2002) N_0^s(T,H) >> H log T for T^0.552 <= H <= T, plus Karatsuba (1985). This is secondary: a search snippet of Wang's text. - [arXiv 2609.07918](https://arxiv.org/pdf/2609.07918)

### Inferences
- The program's EXP-010 (Young/Conrey mollifier localized to (T, T+T^theta]) still appears to have no external 2026 competitor.

### Gaps
- No access to arXiv full-text search, so a Levinson short-interval paper whose abstract lacks the words "simple"/"critical"/"proportion" could be missed.

## Q4. Improved pair-correlation (Montgomery) support or RH-free extensions in 2026

### Takeaway
No 2026 announcement of Montgomery pair-correlation support beyond the classical range was found. The 2026 activity is:
- RH-free and hypothesis-transfer papers by Goldston, Suriajaya and coauthors (tracked);
- a new certified Weil-positivity computation in compact windows (Zhu, arXiv:2608.24827, new to the list);
- new finite Weil-matrix constructions (arXiv:2609.04908, 2607.02828, new).

None of the new items gives a zero proportion.

### Cited Findings
- **NEW: arXiv:2608.24827, Xuefeng Zhu, "Weil positivity in compact windows: a finite reduction, certified two-sided bounds, and a Landau-Widom decay law" (submitted 2026-08-25, revised 2026-09-02; version number not visible).** Per search summaries:
  - Certified computation shows Q(f) >= 8.9e-18 ||f||^2 for all test functions supported in [-0.8, 0.8], i.e. autocorrelation support 1.6, "2.3 times the classical range".
  - A "one-stroke reduction" (a pointwise envelope for the Weil symbol) turns window positivity into positive semidefiniteness of a single finite matrix.
  - The window ground state is simple and even, the spectral hypothesis needed by the Connes-Consani-Moscovici-van Suijlekom program.
  - Upper bounds follow a Landau-Widom decay law.
  - It gives **no zero-proportion theorem**.
  - Third-party replays exist as a GitHub issue and PR: [murillo128/mathia #152](https://github.com/murillo128/mathia/issues/152) (independent replay of the L = 0.8 certificate) and [DrMurphyIsIn/Arda PR #580](https://github.com/DrMurphyIsIn/Arda/pull/580) (imported "as a CONDITIONAL node").
  - Sources: [arXiv abs](https://arxiv.org/abs/2608.24827), [arXiv html](https://arxiv.org/html/2608.24827)
- **NEW: arXiv:2609.04908, Yaoming Shi, "Construction of Finite Hilbert–Pólya Matrices from Weil's Explicit Formula" (submitted 2026-09-04).**
  - Builds finite real-symmetric "Prime–Weil" matrices from pole, archimedean and prime-power data.
  - The off-diagonal part is a Loewner divided-difference matrix with a rank-two displacement identity.
  - Spectra are handled as a Hermitian-definite generalized eigenproblem on a zero-mean contrast space.
  - It is a representation paper and gives no proportion theorem.
  - Sources: [arXiv abs](https://arxiv.org/abs/2609.04908), [Pith summary](https://pith.science/paper/2609.04908)
- **NEW, found incidentally: arXiv:2607.02828, "A finite Guinand-Weil dictionary and archimedean tail order for the truncated Weil quadratic form" (July 2026).** Its content was not read beyond the title. - [arXiv pdf](https://arxiv.org/pdf/2607.02828)
- Marco Desogus's 2609.20367 ("The Three Gates", 2026-09-16, tracked) also has a Zenodo deposit. - [Zenodo 22864282](https://zenodo.org/records/22864282), [arXiv 2609.20367](https://arxiv.org/abs/2609.20367)
- Goldston–Lee–Schettler–Suriajaya arXiv:2503.15449v4 (2026-03-30, tracked) shows that the PCC implies, without RH, that 100% of zeros are simple and critical. Part II (Alternative Hypothesis), arXiv:2507.06823, is now in J. Number Theory 2026 (article S0022314X26001101). The journal version is new relative to the list. - [arXiv 2503.15449v4](https://arxiv.org/html/2503.15449v4), [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0022314X26001101), [arXiv 2507.06823](https://arxiv.org/abs/2507.06823)
- Goldston–Suriajaya "Zeta zeros on the critical line" (arXiv:2511.20059, tracked) is now **published in Analysis Mathematica (2026), DOI 10.1007/s10476-026-00186-w**. Their "Zeta zeros in a narrow vertical box" (arXiv:2603.28104, tracked; search dates a revision to 2026-08-24) is said to be forthcoming in the same journal. The volume/number "52(3)" comes from a snippet and is unverified. - [Springer](https://link.springer.com/article/10.1007/s10476-026-00186-w), [arXiv 2603.28104](https://arxiv.org/html/2603.28104)
- Search also surfaced arXiv:2508.10857, "The Alternative Hypothesis for Zeros of the Riemann Zeta-Function" (Aug 2025), a background companion. - [arXiv 2508.10857](https://arxiv.org/pdf/2508.10857)

### Inferences
- Zhu's support-1.6 certified positivity is the kind of finite-window Weil-form input that could feed rank-trace / Weil-compression proportion arguments. That link is unproved: the paper is about positivity, not proportions.

### Gaps
- Nothing found on extending Montgomery's F(alpha) asymptotic beyond |alpha| <= 1 in 2026, conditionally or not.

## Q5. Errata, retractions, disputes, reception and independent verification of the tracked sources

### Takeaway
No published erratum, retraction or dispute of 2608.13637, 2609.02882, 2609.07918, 2609.15329 or 2609.24167 was found. Reception so far:
- Anthropic's own statement that Brian Conrey and Dan Goldston reviewed the paper on short notice;
- the Lean formalization;
- follow-up proofs (Lamzouri, Wang);
- secondary press/blog coverage that explicitly calls it an unrefereed high-evidence preprint.

The formalization repositories have not changed since the program's last inspection. The retraction in the ecosystem is the Yang density-one claim (Q2), not a tracked result.

### Cited Findings
- **VERIFIED from www.anthropic.com/research/riemann-zeta (dated 2026-08-10, updated 2026-08-13).**
  - It claims the bound improved "from 41.6% to 67.2%" using 31M output tokens, 60 subagents and 2,400 shell commands.
  - The paper was "revised by Claude to provide a clearer proof and additional historical context" (13 Aug update).
  - It thanks Conrey and Goldston as outside reviewers and mentions a Lean formalization.
  - There is no erratum on the page. - [Anthropic](https://www.anthropic.com/research/riemann-zeta)
- Secondary coverage:
  - A kingy.ai blog says there was "no public independent referee report or broad expert consensus" on publication day, calling it "a high-evidence preprint claim awaiting community scrutiny". - [kingy.ai](https://kingy.ai/blog/claude-riemann-hypothesis-67-percent-result/)
  - Other press: [officechai](https://officechai.com/ai/claude-couldnt-prove-riemann-hypothesis-but-improved-the-longstanding-lower-bound-of-a-related-function-from-41-to-67/), [DataCamp](https://www.datacamp.com/tutorial/claude-and-the-riemann-hypothesis), [windowsforum](https://windowsforum.com/windows-news.4/claude-claims-67-25-of-riemann-zeta-zeros-on-critical-line.442304/)
  - None reports an error.
- The independent-verification status of the tracked results is unchanged:
  - Lamzouri's proof (2609.02882, v2 of 2026-09-08) and Wang's refinement (2609.24167) independently reprove or extend the 2608.13637 constants by different routes, and they are the de facto independent checks.
  - Wang 2609.24167 cites both Alpöge–Furman and Lamzouri without flagging errors (VERIFIED abstract).
  - Sources: [arXiv 2609.02882](https://arxiv.org/abs/2609.02882), local 2609.24167 source.
- **VERIFIED via `git ls-remote`/`git clone` on 2026-09-27: formalizations and candidate repositories.**
  - [AxiomMath/ZetaZerosV2](https://github.com/AxiomMath/ZetaZerosV2): `main` = `4c73b31` ("Publication of Files", 2026-09-08). PR #1 head = `02dfc0b1c63d…`, identical to the program's inspected head, so nothing new.
  - [anthropics/formal-math](https://github.com/anthropics/formal-math): last commit on main is `fbdc36b` (2026-09-05, a lean-action bump). The zeta23 Palomar layout/authorship PRs #19-#24 were merged 2026-08-28. The highest PR ref is #24, so nothing new since then.
  - `trmdy/zeta-simple-zeros-673137`: HEAD is still the pinned `1610b97b…`, unchanged.
  - `ainta/zeta-simple-zeros`: HEAD is `040c5e899e…`. This could not be compared, because the program's pin for it was not checked in this sweep.
  - [teal-sea/zeta-lab](https://github.com/teal-sea/zeta-lab): HEAD moved from the program's inspected `f402358c` to `8941a80` (2026-09-22). The 27 changed files are "prime_pair_error" Möbius-pairing hunts, Mertens II / Turán Lean band tightening and CI fixes. None concerns simple/critical proportions or the Palomar four-point bound.
- Search snippets attribute to 2609.02882 a passage saying that a shorter proof "produced by an internal research version of Claude ... verified by Alpöge and Furman" replaces the matrix framework by a Hilbert-space inequality. The program's Lamzouri dossier records 2609.02882 as Lamzouri's paper, and I could not open arXiv to settle it. The passage may be a quotation within Lamzouri's introduction, or it may belong to an Anthropic follow-up note. - [arXiv 2609.02882v1 html](https://arxiv.org/html/2609.02882v1)
  - **UNRESOLVED:** the program should reread 2609.02882v2 §1 to confirm the attribution.

### Inferences
- A month after posting, the tracked breakthrough has attracted independent reproofs and extensions but no public objection. The only "errata" traffic concerns downstream amateur/AI-assisted extensions: the Yang density-one retraction, and the program's own quarantine of the 79.62% claim.

### Gaps
- MathOverflow, Tao's blog and Quanta: no relevant 2026 post was found by search. Their absence is not certain, because direct site search was not possible.
- Could not check arXiv comment fields or version histories for silent v2 corrections of 2608.13637 (the program tracks v2), 2609.07918 or 2609.15329.
