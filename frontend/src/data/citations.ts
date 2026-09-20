import type { Citation } from '@fasl-work/caos-app-shell';

// The reference spine, transcribed from the persisted context dossier (problems/.../context/).
// Inline <Cite id="..."/> resolves against this list via the CitationsProvider at the app root.
export const CITATIONS: Citation[] = [
  {
    id: 'riemann-anthropic2026', label: 'Anthropic 2026',
    citation: 'Anthropic (2026). New results on the Riemann zeta function. Research announcement, original and revised proofs, human verification notes, and formalization links. Reviewed 2026-09-12.',
    url: 'https://www.anthropic.com/research/riemann-zeta',
  },
  {
    id: 'riemann-alpogefurman2026', label: 'Alpoge–Furman 2026',
    citation: 'Alpöge L., Furman R. (2026). More than two thirds of the zeros of the Riemann zeta function are simple and on the critical line. arXiv:2608.13637v2. The named authors verified and take responsibility for the Claude-discovered and written argument.',
    url: 'https://arxiv.org/abs/2608.13637v2',
  },
  {
    id: 'riemann-lamzouri2026', label: 'Lamzouri 2026',
    citation: 'Lamzouri Y. (2026). A new proof that more than 2/3 of the zeros of the Riemann zeta function are simple and on the critical line. arXiv:2609.02882v2. The pinned source for the finite self-adjoint operator and multiplicity bounds.',
    url: 'https://arxiv.org/abs/2609.02882v2',
  },
  {
    id: 'riemann-wang2026', label: 'Wang 2026',
    citation: 'Wang B. (2026). Simple critical zeros and distinct zeros of the Riemann zeta-function in short intervals. arXiv:2609.07918v1, submitted September 7; manuscript dated September 9. The arithmetic input and cosine baseline used in the refinement.',
    url: 'https://arxiv.org/abs/2609.07918v1',
  },
  {
    id: 'riemann-pearcecrump2026', label: 'Pearce-Crump 2026',
    citation: 'Pearce-Crump A. (2026). Optimising Selberg\'s method for critical zeros. arXiv:2609.15329v1. Source of the positive-semidefinite sign detector, coefficient-uniform approximate functional equation, arbitrary-subinterval mean-value estimate, and certified rank-three profile localized in EXP-005.',
    url: 'https://arxiv.org/abs/2609.15329v1',
  },
  {
    id: 'riemann-karatsuba1985', label: 'Karatsuba 1985',
    citation: 'Karatsuba A. A. (1985). On the zeros of the Riemann zeta-function on the critical line. Mathematics of the USSR-Izvestiya 24(3), 523–537. Theorem B restates Selberg’s distinct odd-order critical-zero density; the paper also proves a stronger shorter seed exponent.',
    url: 'https://www.mathnet.ru/eng/im1456',
  },
  {
    id: 'riemann-parity2026', label: 'CAOS EXP-004: parity transfer',
    citation: 'Santibáñez-Leal F. (2026). Parity density transfer across the cosine positivity threshold. CAOS Research EXP-004: complete finite proof, exact controls, independent source binding and qualitative short-interval range extension. No numerical new exponent or RH proof is claimed.',
    url: 'https://github.com/fsantibanezleal/CAOS_RESEARCH/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/mathematical-proof.md',
  },
  {
    id: 'riemann-bgstb2026', label: 'BGSTB, corrected version 2026',
    citation: 'Baluyot S. A. C., Goldston D. A., Suriajaya A. I., Turnage-Butterbaugh C. L. (2026). Pair correlation of zeros of the Riemann zeta function I: Proportions of simple zeros and critical zeros. arXiv:2501.14545v3. Corrected uniform error terms; the cited integrated applications remain valid.',
    url: 'https://arxiv.org/abs/2501.14545v3',
  },
  {
    id: 'riemann-axiom2026', label: 'AxiomMath: ZetaZerosV2',
    citation: 'AxiomMath (2026). ZetaZerosV2, commit 4c73b317232173a5e6d4253702c9870ee66c2c7b. Apache-2.0 Lean development. Headline zeta results explicitly assume Riemann–von Mangoldt and pair correlation.',
    url: 'https://github.com/AxiomMath/ZetaZerosV2/tree/4c73b317232173a5e6d4253702c9870ee66c2c7b',
  },
  {
    id: 'riemann-formalmath2026', label: 'Anthropic: formal-math',
    citation: 'Anthropic (2026). formal-math, commit fbdc36bbf17d20af3fd0447c6d1a8a02773c9844. The zeta23 development contains the analytic input proofs; source review and upstream verification receipts are distinguished from local replay.',
    url: 'https://github.com/anthropics/formal-math/tree/fbdc36bbf17d20af3fd0447c6d1a8a02773c9844',
  },
  {
    id: 'riemann-ainta2026', label: 'ainta: spectral stability',
    citation: 'ainta (2026). zeta-simple-zeros, commit 040c5e899e658aed7b56a2a87f501798fe10761d. A convex spectral defect and finite configurations of consecutive simple zeros. Source of the inherited stability mechanism.',
    url: 'https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/docs/proof.md',
  },
  {
    id: 'riemann-trmdy2026', label: 'trmdy: successor certificates',
    citation: 'trmdy (2026). zeta-simple-zeros-673137, commit 1610b97b7895ff34982260f8dcaf04a0f7b82cf7. Higher-point stability certificates and record candidates; the analytic interfaces are not all formalized in Lean.',
    url: 'https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7',
  },
  {
    id: 'riemann-refinement2026', label: 'CAOS short-interval refinement',
    citation: 'Santibáñez-Leal F. (2026). Simple critical zeros in short intervals: stability, pressure, parity, and localization, version 0.05. The explicit local Selberg transfer, threshold certificate, prior pressure and parity results, and stated analytic boundaries are included.',
    doi: '10.5281/zenodo.22851518',
  },
  {
    id: 'riemann-local2026', label: 'CAOS EXP-005: local Selberg transfer',
    citation: 'Santibáñez-Leal F. (2026). Local optimized Selberg transfer. CAOS Research EXP-005: complete analytic localization, exact threshold bracket, fixed mollifier witness, independent interval replay, adversarial review, and source-bound proof review. RH remains open.',
    url: 'https://github.com/fsantibanezleal/CAOS_RESEARCH/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/mathematical-proof.md',
  },
  {
    id: 'riemann-pressure2026', label: 'CAOS EXP-003: odd-frame pressure',
    citation: 'Santibáñez-Leal F. (2026). Odd-frame pressure refinement of the short-interval cosine bound. EXP-003 mathematical proof and confirmed verdict. Stronger short-interval consequences of attributed finite stability and pressure frameworks; finite arithmetic and analytic scope are separate evidence layers.',
    url: 'https://github.com/fsantibanezleal/CAOS_RESEARCH/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/mathematical-proof.md',
  },
  {
    id: 'riemann-tawanerguo2026', label: 'tawanerguo: pressure and capacities',
    citation: 'tawanerguo-cn (2026). zeta-simple-zeros, commit 45149f6d403059a71be73c5e3f884cee7cd62b20. Global finite stability, pressure-frame and nonuniform-capacity framework. Attribution does not import the repository’s global numerical claims as short-interval results.',
    url: 'https://github.com/tawanerguo-cn/zeta-simple-zeros/tree/45149f6d403059a71be73c5e3f884cee7cd62b20',
  },
  {
    id: 'riemann-yuhangshi2026', label: 'Yuhang Shi: mixed frames',
    citation: 'Yuhang Shi (2026). zeta-simple-zeros-673316977, commit 1aeda8e9f0678166a824c75313a813b09eb478cd. Mixed-frame and spectral-envelope refinements in the existing global framework. The audited short-interval consequence is separately stated in EXP-003.',
    url: 'https://github.com/yuhangshi888/zeta-simple-zeros-673316977/tree/1aeda8e9f0678166a824c75313a813b09eb478cd',
  },
  {
    id: 'alpoge2026',
    label: 'Alpöge 2026',
    citation:
      'Alpöge L. (2026). Announcement of a counterexample to the Jacobian conjecture in dimension 3, found working with Claude Fable (Anthropic); question posed by Akhil. X, 2026-07-20.',
    url: 'https://x.com/__alpoge__/status/2079028340955197566',
  },
  {
    id: 'keller1939',
    label: 'Keller 1939',
    citation:
      'Keller O.-H. (1939). Ganze Cremona-Transformationen. Monatshefte für Mathematik und Physik 47(1), 299-306.',
    doi: '10.1007/BF01695502',
  },
  {
    id: 'rodriguez2026',
    label: 'Rodríguez Díaz 2026',
    citation:
      'Rodríguez Díaz L. O. (2026). On the origin of the Jacobian conjecture. Comptes Rendus. Mathématique 364, 363-370.',
    url: 'https://arxiv.org/abs/2512.23614',
  },
  {
    id: 'bcw1982',
    label: 'Bass, Connell & Wright 1982',
    citation:
      'Bass H., Connell E. H., Wright D. (1982). The Jacobian conjecture: reduction of degree and formal expansion of the inverse. Bulletin of the AMS (N.S.) 7(2), 287-330.',
    doi: '10.1090/S0273-0979-1982-15032-7',
  },
  {
    id: 'druzkowski1983',
    label: 'Drużkowski 1983',
    citation:
      'Drużkowski L. M. (1983). An effective approach to Keller’s Jacobian conjecture. Mathematische Annalen 264(3), 303-313.',
    doi: '10.1007/BF01459126',
  },
  {
    id: 'pinchuk1994',
    label: 'Pinchuk 1994',
    citation:
      'Pinchuk S. (1994). A counterexample to the strong real Jacobian conjecture. Mathematische Zeitschrift 217(1), 1-4.',
    doi: '10.1007/BF02571929',
  },
  {
    id: 'smale1998',
    label: 'Smale 1998',
    citation:
      'Smale S. (1998). Mathematical problems for the next century. The Mathematical Intelligencer 20(2), 7-15. Problem 16 is the Jacobian conjecture.',
    doi: '10.1007/BF03025291',
  },
  {
    id: 'vandenessen2000',
    label: 'van den Essen 2000',
    citation:
      'van den Essen A. (2000). Polynomial Automorphisms and the Jacobian Conjecture. Progress in Mathematics 190, Birkhäuser.',
    doi: '10.1007/978-3-0348-8440-2',
  },
  {
    id: 'moh1983',
    label: 'Moh 1983',
    citation:
      'Moh T.-T. (1983). On the Jacobian conjecture and the configurations of roots. Journal für die reine und angewandte Mathematik 340, 140-212. Verifies the two-variable case to degree 100.',
    url: 'https://eudml.org/doc/152513',
  },
  {
    id: 'sparkes2026',
    label: 'Sparkes 2026',
    citation:
      'Sparkes M. (2026). Coverage of the Jacobian conjecture counterexample announcement. New Scientist, 2026-07-20.',
    url: 'https://www.newscientist.com',
  },
  {
    id: 'wikipedia-jc',
    label: 'Wikipedia: Jacobian conjecture',
    citation:
      'Wikipedia (as of 2026-07-20). Jacobian conjecture: reference hub used to locate primary sources; every claim re-verified against them.',
    url: 'https://en.wikipedia.org/wiki/Jacobian_conjecture',
  },
  {
    id: 'caosresearch',
    label: 'CAOS Research repository',
    citation:
      'Santibañez-Leal F. (2026). CAOS_RESEARCH: experiment records EXP-001..012, exact scripts, artifacts and the working manuscript (MIT).',
    url: 'https://github.com/fsantibanezleal/CAOS_RESEARCH',
  },
  {
    id: 'magnus1954',
    label: 'Magnus 1954',
    citation:
      'Magnus A. (1954). Volume preserving transformations in several complex variables. Proc. Amer. Math. Soc. 5, 256-266.',
    url: 'https://doi.org/10.1090/S0002-9939-1954-0060050-7',
  },
  {
    id: 'appelgateonishi1985',
    label: 'Appelgate-Onishi 1985',
    citation:
      'Appelgate H., Onishi H. (1985). The Jacobian conjecture in two variables. J. Pure Appl. Algebra 37, 215-227.',
    url: 'https://doi.org/10.1016/0022-4049(85)90099-4',
  },
  // --- central-configurations (Smale 6) reference spine; transcribed from
  // problems/dynamical-systems/central-configurations/context/references.md ---
  {
    id: 'hm2006',
    label: 'Hampton-Moeckel 2006',
    citation:
      'Hampton M., Moeckel R. (2006). Finiteness of relative equilibria of the four-body problem. Inventiones mathematicae 163(2), 289-312.',
    doi: '10.1007/s00222-005-0461-0',
  },
  {
    id: 'ak2012',
    label: 'Albouy-Kaloshin 2012',
    citation:
      'Albouy A., Kaloshin V. (2012). Finiteness of central configurations of five bodies in the plane. Annals of Mathematics 176(1), 535-588.',
    doi: '10.4007/annals.2012.176.1.10',
  },
  {
    id: 'hj2011',
    label: 'Hampton-Jensen 2011',
    citation:
      'Hampton M., Jensen A. N. (2011). Finiteness of spatial central configurations in the five-body problem. Celestial Mechanics and Dynamical Astronomy 109(4), 321-332.',
    doi: '10.1007/s10569-010-9328-9',
  },
  {
    id: 'jl2025',
    label: 'Jensen-Leykin 2025',
    citation:
      "Jensen A., Leykin A. (2025). Smale's 6th problem for generic masses. arXiv:2301.02305v2.",
    url: 'https://arxiv.org/abs/2301.02305',
  },
  {
    id: 'mz2019',
    label: 'Moczurad-Zgliczynski 2019',
    citation:
      'Moczurad M., Zgliczynski P. (2019). Central configurations in planar n-body problem with equal masses for n = 5, 6, 7. Celestial Mechanics and Dynamical Astronomy 131.',
    doi: '10.1007/s10569-019-9920-6',
  },
  {
    id: 'roberts1999',
    label: 'Roberts 1999',
    citation:
      'Roberts G. E. (1999). A continuum of relative equilibria in the five-body problem. Physica D 127, 141-145.',
    doi: '10.1016/S0167-2789(98)00315-7',
  },
  {
    id: 'ac1998',
    label: 'Albouy-Chenciner 1998',
    citation:
      'Albouy A., Chenciner A. (1998). Le probleme des n corps et les distances mutuelles. Inventiones mathematicae 131, 151-184.',
  },
  {
    id: 'changchen2023',
    label: 'Chang-Chen 2024',
    citation:
      'Chang K.-M., Chen K.-C. (2024). Toward finiteness of central configurations for the planar six-body problem by symbolic computations. (I) Determine diagrams and orders. Journal of Symbolic Computation 123, 102277. Programme preprint: arXiv:2303.02853; a second part on mass relations is announced in the same programme.',
    url: 'https://arxiv.org/abs/2303.02853',
  },
  {
    id: 'moulton1910',
    label: 'Moulton 1910',
    citation:
      'Moulton F. R. (1910). The straight line solutions of the problem of n bodies. Annals of Mathematics 12, 1-17.',
  },
  {
    id: 'ccmanuscript',
    label: 'Replication record 2026',
    citation:
      'Santibañez-Leal F. (2026). Exact replication and screening of tropical finiteness certificates for central configurations. Preprint, CC BY 4.0.',
    doi: '10.5281/zenodo.21542483',
  },
  {
    id: 'dgg1999',
    label: 'Dinitz-Garg-Goemans 1999',
    citation:
      'Dinitz Y., Garg N., Goemans M. X. (1999). On the single-source unsplittable flow problem. Combinatorica 19(1), 17-41. FOCS 1998.',
    doi: '10.1007/s004930050043',
  },
  {
    id: 'sku2002',
    label: 'Skutella 2002',
    citation:
      'Skutella M. (2002). Approximating the single source unsplittable min-cost flow problem. Mathematical Programming 91. Proves Goemans conjecture when the demands are multiples of one another.',
  },
  {
    id: 'ms2022',
    label: 'Morell-Skutella 2022',
    citation:
      'Morell A., Skutella M. (2022). Single source unsplittable flows with arc-wise lower and upper bounds. Mathematical Programming. States the two-sided conjectures, with and without costs.',
  },
  {
    id: 'tvz2024',
    label: 'Traub-Vargas Koch-Zenklusen 2024',
    citation:
      'Traub V., Vargas Koch L., Zenklusen R. (2026). Single-source unsplittable flows in planar and bounded-genus graphs. Mathematical Programming. Preprint arXiv:2308.02651 (2023). Proves the cost statement for planar graphs at twice the conjectured violation.',
    doi: '10.1007/s10107-026-02365-x',
  },
  {
    id: 'msw2025',
    label: 'Majthoub Almoghrabi-Skutella-Warode 2025',
    citation:
      'Majthoub Almoghrabi M., Skutella M., Warode P. (2026). Integer and unsplittable multiflows in series-parallel digraphs. Mathematical Programming; IPCO 2025. Preprint arXiv:2412.05182. Proves Goemans conjecture, in the stronger convex-combination form with strict deviation, for series-parallel digraphs: the first non-trivial class.',
    doi: '10.1007/s10107-026-02392-8',
  },
  {
    id: 'stvz2025',
    label: 'Swamy-Traub-Vargas Koch-Zenklusen 2025',
    citation:
      'Swamy C., Traub V., Vargas Koch L., Zenklusen R. (2025). Unsplittable cost flows from unweighted error-bounded variants. Preprint arXiv:2510.21287. Source of the conjecture numbering used here, and of the record that the O(d_max) question was wide open as of October 2025.',
    doi: '10.48550/arXiv.2510.21287',
  },
  {
    id: 'rybin2026',
    label: 'Counterexample announcement 2026',
    citation:
      'Rybin D. (2026). Public announcement of a counterexample to the Dinitz-Garg-Goemans cost conjecture, found working with a large language model. X, 2026-07-22/23. Not peer reviewed; the instance is verified independently in this programme.',
    url: 'https://x.com/DmitryRybin1/status/2079904005652893709',
  },
  {
    id: 'ufcverification',
    label: 'Verification record 2026',
    citation:
      'Santibañez-Leal F. (2026). An independent exact verification of the 2026 counterexample to Goemans unsplittable-flow cost conjecture, with the violation constant it forces. Preprint, CC BY 4.0.',
    doi: '10.5281/zenodo.21554258',
  },
  {
    id: 'jaeger1988',
    label: 'Jaeger 1988',
    citation:
      'Jaeger F. (1988). Nowhere-zero flow problems. In Beineke L. W., Wilson R. J. (eds.), Selected Topics in Graph Theory 3, Academic Press, 71-95. Origin of the Petersen coloring conjecture.',
    url: 'https://www.openproblemgarden.org/op/petersen_coloring_conjecture',
  },
  {
    id: 'jaeger1985',
    label: 'Jaeger 1985',
    citation:
      'Jaeger F. (1985). On five-edge-colorings of cubic graphs and nowhere-zero flow problems. Ars Combinatoria 20-B, 229-244. Petersen colorings are equivalent to normal 5-edge-colorings.',
    url: 'https://arxiv.org/abs/1804.09449',
  },
  {
    id: 'putman2026',
    label: 'Putman 2026',
    citation:
      'Putman B. (2026). A 112-vertex counterexample to the Petersen Coloring Conjecture. Zenodo v1.1.0, 2026-08-08; arXiv:2608.10012. Two nonisomorphic 112-vertex counterexamples with CaDiCaL/DRAT certificates.',
    doi: '10.5281/zenodo.21845291',
  },
  {
    id: 'jooken2026',
    label: 'Jooken 2026',
    citation:
      'Jooken J. (2026). A human-checkable proof of the 112-vertex counterexample to the Petersen coloring conjecture. arXiv:2608.10028v2, 2026-08-14.',
    url: 'https://arxiv.org/abs/2608.10028',
  },
  {
    id: 'gjmmm2026',
    label: 'Goedgebeur, Jooken, Macajova, Mattiolo & Mazzuoccolo 2026',
    citation:
      'Goedgebeur J., Jooken J., Macajova E., Mattiolo D., Mazzuoccolo G. (2026). A smaller counterexample and infinite family of counterexamples to the Petersen Coloring Conjecture. Zenodo, 2026-08-14. The 52-vertex counterexample, infinite cyclically 4-edge-connected families, and the frontier 38 to 52 for the smallest counterexample.',
    doi: '10.5281/zenodo.21933785',
  },
  {
    id: 'bghm2013',
    label: 'Brinkmann, Goedgebeur, Hagglund & Markstrom 2013',
    citation:
      'Brinkmann G., Goedgebeur J., Hagglund J., Markstrom K. (2013). Generation and properties of snarks. Journal of Combinatorial Theory, Series B 103(4), 468-488. All snarks on at most 36 vertices; the Petersen coloring conjecture holds for all of them.',
    doi: '10.1016/j.jctb.2013.05.001',
  },
  {
    id: 'gms2019',
    label: 'Goedgebeur, Macajova & Skoviera 2019',
    citation:
      'Goedgebeur J., Macajova E., Skoviera M. (2019). Smallest snarks with oddness 4 and cyclic connectivity 4 have order 44. Ars Mathematica Contemporanea 16, 277-298. Completes the order-36 verification for weak snarks of girth 4.',
    doi: '10.26493/1855-3974.1601.e75',
  },
  {
    id: 'mazzmkrt2020',
    label: 'Mazzuoccolo & Mkrtchyan 2020',
    citation:
      'Mazzuoccolo G., Mkrtchyan V. V. (2020). Normal edge-colorings of cubic graphs. Journal of Graph Theory 94(1), 75-91. Every simple cubic graph has a normal 7-edge-coloring; the normal 6 question.',
    doi: '10.1002/jgt.22507',
  },
  {
    id: 'gjmmmu2026',
    label: 'Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo & Ulyanov 2026',
    citation:
      'Goedgebeur J., Jooken J., Macajova E., Mattiolo D., Mazzuoccolo G., Ulyanov S. (2026). Disproving the Petersen Coloring Conjecture: theoretical analysis and an infinite family of counterexamples. arXiv:2608.10028v3, 2026-09-11. Two 52-vertex counterexamples with a theoretical proof, counterexamples of every even order at least 60, the bounds 40 to 52 for a smallest counterexample, and the question whether the 52-vertex graphs are colorable only by themselves.',
    url: 'https://arxiv.org/abs/2608.10028v3',
  },
  {
    id: 'mmsw2025',
    label: 'Ma, Mattiolo, Steffen & Wolf 2025',
    citation:
      'Ma Y., Mattiolo D., Steffen E., Wolf I. H. (2025). Sets of r-graphs that color all r-graphs. Combinatorica 45, Article 16. The unique minimal set of bridgeless cubic graphs coloring every bridgeless cubic graph, and its characterization: a graph belongs to it if and only if no smaller bridgeless cubic graph colors it.',
    doi: '10.1007/s00493-025-00144-4',
  },
  {
    id: 'mmm2021',
    label: 'Mattiolo, Mazzuoccolo & Mkrtchyan 2021',
    citation:
      'Mattiolo D., Mazzuoccolo G., Mkrtchyan V. (2021). On sublinear approximations for the Petersen coloring conjecture. Bulletin of the Institute of Combinatorics and its Applications 92, 78-90. Abnormal edges of proper 5-edge-colorings, the conjectured equivalence of five statements on sublinear bounds, and the proposition that a coloring never has exactly one abnormal edge.',
    url: 'https://arxiv.org/abs/2104.09241',
  },
  {
    id: 'hog2023',
    label: 'Coolsaet, D\'hondt & Goedgebeur 2023',
    citation:
      'Coolsaet K., D\'hondt S., Goedgebeur J. (2023). House of Graphs 2.0: a database of interesting graphs and more. Discrete Applied Mathematics 325, 97-107. Source of the second 52-vertex and the 68-vertex counterexample (entries 57278 and 57280).',
    url: 'https://houseofgraphs.org',
  },
  {
    id: 'kaiser2007',
    label: 'Kaiser, Kuzel, Li & Wang 2007',
    citation:
      'Kaiser T., Kuzel R., Li H., Wang G. (2007). A note on k-walks in bridgeless graphs. Graphs and Combinatorics 23, 303-308. Lemma 1: the bridgeless form of Fleischner\'s splitting lemma used to reduce unused target vertices.',
    url: 'http://home.zcu.cz/~kaisert/papers/deg-walk.pdf',
  },
  {
    id: 'pccaudit',
    label: 'Audit record 2026',
    citation:
      'Santibañez-Leal F. (2026). Berge-Fulkerson covers, cycle double covers, flows and exact normality defects of the first counterexamples to the Petersen coloring conjecture. Preprint, CC BY 4.0.',
    doi: '10.5281/zenodo.22285164',
  },
];
