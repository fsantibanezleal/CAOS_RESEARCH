import type { ArchitectureConfig, Lang } from '@fasl-work/caos-app-shell';
import { ARCHITECTURE } from './architecture';

const ROOT = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = `${ROOT}/tree/main/problems/number-theory/riemann-hypothesis`;
const PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/mathematical-proof.md`;

function diagram(kind: 'science' | 'method', lang: Lang) {
  const t = (en: string, es: string) => lang === 'es' ? es : en;
  const nodes = kind === 'science' ? [
    [t('Wang: short-interval arithmetic', 'Wang: aritmética en intervalos cortos'), 'Q / N → 2 − c(θ)'],
    [t('Finite spectral stability', 'Estabilidad espectral finita'), 'S ≥ 2N − Q + D(G)'],
    [t('Three consecutive simple zeros', 'Tres ceros simples consecutivos'), t('Compact gap triangle: energy ≥ d', 'Triángulo compacto: energía ≥ d')],
    [t('Strict asymptotic refinement', 'Refinamiento asintótico estricto'), 'c* = c + d(c − 2/R) / (3 − d)'],
  ] : [
    [t('Declare before computation', 'Declarar antes del cálculo'), 'EXP-001 · EXP-002'],
    [t('Audit the sources and proof', 'Auditar las fuentes y la prueba'), t('Rational bounds + symbolic identities', 'Cotas racionales + identidades simbólicas')],
    [t('Certify every compact-domain cell', 'Certificar cada celda del dominio'), t('Arb + a separate sinc Taylor evaluator', 'Arb + otro evaluador de Taylor para sinc')],
    [t('Review, persist, then replay', 'Revisar, persistir y reproducir'), t('Adversarial tests · verdict · SHA-256', 'Pruebas adversariales · veredicto · SHA-256')],
  ];
  const links = kind === 'science' ? [
    ['Wang', 'https://arxiv.org/abs/2609.07918v1'],
    ['Lamzouri', 'https://arxiv.org/abs/2609.02882v2'],
    ['ainta', 'https://github.com/ainta/zeta-simple-zeros/blob/040c5e899e658aed7b56a2a87f501798fe10761d/docs/proof.md'],
  ] : [
    ['EXP-001', `${PROBLEM}/experiments/EXP-001-source-and-constant-audit`],
    ['EXP-002', `${PROBLEM}/experiments/EXP-002-short-interval-stability`],
    [t('Tests', 'Pruebas'), `${ROOT}/blob/main/tests/test_riemann_certificates.py`],
  ];
  const arrows = kind === 'science' ? ['Q', 'D(G)', 'd &gt; 0'] : [t('audit', 'auditoría'), t('check', 'verificar'), t('review', 'revisar')];
  const title = kind === 'science'
    ? t('Riemann short-interval proof dependencies', 'Dependencias de la prueba de Riemann en intervalos cortos')
    : t('Riemann research and certificate workflow', 'Flujo de investigación y certificación de Riemann');
  const finalLabel = kind === 'science' ? t('Read the complete proof', 'Leer la prueba completa') : t('Read the reproduction instructions', 'Leer las instrucciones de reproducción');
  const finalUrl = kind === 'science' ? PROOF : `${PROBLEM}/code`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 550" role="img" aria-label="${title}" style="display:block;width:100%;max-width:460px;height:auto;margin:auto" font-family="ui-sans-serif,system-ui,sans-serif">
    <title>${title}</title>
    <defs><marker id="rh-arch-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="currentColor"/></marker></defs>
    ${nodes.map(([label, sub], i) => `<g>
      <rect x="10" y="${14 + i * 108}" width="340" height="72" rx="9" fill="var(--color-surface-2)" stroke="var(--color-accent)"/>
      <text x="180" y="${43 + i * 108}" text-anchor="middle" fill="currentColor" font-size="14" font-weight="600">${label}</text>
      <text x="180" y="${68 + i * 108}" text-anchor="middle" fill="currentColor" font-size="12">${sub}</text>
      ${i < 3 ? `<path d="M180 ${88 + i * 108}v29" stroke="currentColor" marker-end="url(#rh-arch-arrow)"/><text x="192" y="${107 + i * 108}" fill="currentColor" font-size="11">${arrows[i]}</text>` : ''}
    </g>`).join('')}
    <text x="180" y="433" text-anchor="middle" fill="currentColor" font-size="12">${t('Sources and evidence', 'Fuentes y evidencia')}</text>
    ${links.map(([label, url], i) => `<a href="${url}" target="_blank" rel="noreferrer" aria-label="${label}"><rect x="${10 + i * 116}" y="442" width="108" height="44" rx="6" fill="var(--color-accent-soft)" stroke="var(--color-border)"/><text x="${64 + i * 116}" y="469" text-anchor="middle" fill="var(--color-accent)" font-size="13">${label}</text></a>`).join('')}
    <a href="${finalUrl}" target="_blank" rel="noreferrer"><rect x="10" y="495" width="340" height="44" rx="6" fill="var(--color-accent-soft)" stroke="var(--color-border)"/><text x="180" y="522" text-anchor="middle" fill="var(--color-accent)" font-size="13">${finalLabel}</text></a>
  </svg>`;
}

/** Retain the shared modal API and repository-wide App/Deploy tabs. Only the
 * Riemann route receives its own Method/Science evidence and localized diagrams. */
export function riemannArchitecture(lang: Lang): ArchitectureConfig {
  return {
    ...ARCHITECTURE,
    tabs: ARCHITECTURE.tabs.map((tab) => {
      if (tab.id === 'method') return {
        ...tab,
        svg: diagram('method', lang),
        body_en: 'The Riemann experiments were declared and committed before computation. EXP-001 reproduces the source constants with exact rational Taylor bounds, checks them with Arb, and audits symbolic identities and the normalization correction. EXP-002 combines a written finite proof with a compact-domain interval certificate.\n\nArb certifies every accepted cell using outward rounding and a Lipschitz bound. A separate sinc Taylor evaluator replays the certificate; it shares Arb and the partition geometry, so this is an independent evaluator, not a wholly separate verifier. Adversarial tests check tampering, boundary coverage, and resumable budget stops.\n\nThe verdict, proof, and source artifacts are persisted with hashes. This browser only replays the committed data. It does not search for zeta zeros, run a GPU computation, or replace the analytic proof with numerical samples. The source links below open the exact experiment records and checker tests.',
        body_es: 'Los experimentos de Riemann se declararon y comprometieron antes del cálculo. EXP-001 reproduce las constantes de las fuentes con cotas de Taylor racionales exactas, las contrasta con Arb y audita identidades simbólicas y la corrección de normalización. EXP-002 combina una prueba finita escrita con un certificado de intervalos sobre un dominio compacto.\n\nArb certifica cada celda aceptada mediante redondeo hacia afuera y una cota de Lipschitz. Otro evaluador de Taylor para sinc reproduce el certificado; comparte Arb y la geometría de la partición, por lo que es un evaluador independiente, no un verificador totalmente separado. Las pruebas adversariales revisan alteraciones, cobertura de la frontera y paradas reanudables por presupuesto.\n\nEl veredicto, la prueba y los artefactos originales se conservan con hashes. Este navegador solo reproduce los datos comprometidos. No busca ceros de zeta, no ejecuta cálculos en GPU ni reemplaza la prueba analítica con muestras numéricas. Los enlaces inferiores abren los registros experimentales y las pruebas del verificador.',
      };
      if (tab.id === 'science') return {
        ...tab,
        svg: diagram('science', lang),
        body_en: 'Riemann mechanism: fix θ above the positivity threshold of Wang’s cosine bound and below one. N counts all zeros with multiplicity in (T, T + T^θ]; S counts simple critical zeros. Wang’s short-interval pair correlation evaluates the second moment Q of Lamzouri’s exact finite self-adjoint operator.\n\nThe stability inequality inherited from ainta retains D(G), a nonnegative spectral defect of the simple-zero Gram matrix. It handles the signed off-line conjugate pairs instead of treating them as positive atoms. Three consecutive simple zeros with normalized span at most R force positive compact-domain kernel energy d; averaging three disjoint block partitions converts that energy into a zero-count improvement.\n\nChoose the normalized gap radius R greater than 2/c. The fixed-test limit in T precedes smoothing and support limits, yielding c* greater than c for every fixed admissible θ. The full certificate constant is reached by a final outer limit. This is a short-interval asymptotic refinement, not RH, a finite-height zero count, or a global proportion record. The dependency links below identify the imported results and the complete proof.',
        body_es: 'Mecanismo de Riemann: se fija θ por encima del umbral de positividad de la cota coseno de Wang y por debajo de uno. N cuenta todos los ceros con multiplicidad en (T, T + T^θ]; S cuenta los ceros críticos simples. La correlación por pares en intervalos cortos de Wang evalúa el segundo momento Q del operador autoadjunto finito exacto de Lamzouri.\n\nLa desigualdad de estabilidad heredada de ainta retiene D(G), un defecto espectral no negativo de la matriz de Gram de ceros simples. Trata los pares conjugados con signo fuera de la recta sin convertirlos en átomos positivos. Tres ceros simples consecutivos con amplitud normalizada a lo sumo R fuerzan una energía positiva d del núcleo en un dominio compacto; promediar tres particiones de bloques disjuntos convierte esa energía en una mejora del conteo.\n\nSe elige el radio normalizado R de separaciones mayor que 2/c. El límite en T con función de prueba fija precede a los límites de suavizado y soporte, dando c* mayor que c para cada θ fijo admisible. Un límite exterior final alcanza la constante completa del certificado. Es un refinamiento asintótico en intervalos cortos, no RH, un conteo a altura finita ni un récord de proporción global. Los enlaces inferiores identifican los resultados importados y la prueba completa.',
      };
      return tab;
    }),
  };
}
