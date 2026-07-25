import type { Citation } from '@fasl-work/caos-app-shell';

// The reference spine, transcribed from the persisted context dossier (problems/.../context/).
// Inline <Cite id="..."/> resolves against this list via the CitationsProvider at the app root.
export const CITATIONS: Citation[] = [
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
    label: 'Chang-Chen 2023-2025',
    citation:
      'Chang K.-M., Chen K.-C. (2024/2025). Toward finiteness of central configurations for the planar six-body problem by symbolic computations, parts I (J. Symbolic Comput.) and II (SIAM J. Appl. Dyn. Syst. 24(3), 2369-2404).',
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
      'Santibañez-Leal F. (2026). Exact replication and screening of tropical finiteness certificates for central configurations. Machine record, versioned with this repository.',
    url: 'https://github.com/fsantibanezleal/CAOS_RESEARCH/tree/main/manuscripts/central-configurations/tropical-replication',
  },
];
