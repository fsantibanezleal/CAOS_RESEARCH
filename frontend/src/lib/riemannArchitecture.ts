import type { ArchitectureConfig, Lang } from '@fasl-work/caos-app-shell';
import { ARCHITECTURE } from './architecture';

const ROOT = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = `${ROOT}/tree/main/problems/number-theory/riemann-hypothesis`;
const PRESSURE_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/mathematical-proof.md`;
const PARITY_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/mathematical-proof.md`;

function diagram(kind: 'science' | 'method', lang: Lang) {
  const t = (en: string, es: string) => lang === 'es' ? es : en;
  const nodes = kind === 'science' ? [
    [t('Wang: short-interval arithmetic', 'Wang: aritmética en intervalos cortos'), 'Q / N → 2 − c(θ)'],
    [t('Finite parity accounting', 'Contabilidad finita de paridad'), '3S − (2N − Q + 2O + D) ≥ 0'],
    [t('Classical odd-zero seed', 'Densidad clásica de ceros impares'), 'O / N ≥ κ  (θ > 51/100)'],
    [t('Range extension and pressure', 'Extensión de rango y presión'), 'θ₁ < θ₀  ·  EXP-003 at θ = 3/4'],
  ] : [
    [t('Declare before computation', 'Declarar antes del cálculo'), 'EXP-001 · EXP-002 · EXP-003 · EXP-004'],
    [t('Replay finite certificates', 'Reproducir certificados finitos'), t('Pair incidence · spans · all offsets', 'Incidencia · extensiones · desplazamientos')],
    [t('Audit parity and pressure', 'Auditar paridad y presión'), t('Exact census · Arb · source binding', 'Censo exacto · Arb · vinculación de fuentes')],
    [t('Review, persist, then replay', 'Revisar, persistir y reproducir'), t('Adversarial tests · verdict · SHA-256', 'Pruebas adversariales · veredicto · SHA-256')],
  ];
  const links = kind === 'science' ? [
    ['Wang', 'https://arxiv.org/abs/2609.07918v1'],
    ['EXP-003', PRESSURE_PROOF],
    ['EXP-004', PARITY_PROOF],
  ] : [
    ['EXP-001', `${PROBLEM}/experiments/EXP-001-source-and-constant-audit`],
    ['EXP-002', `${PROBLEM}/experiments/EXP-002-short-interval-stability`],
    ['EXP-003', `${PROBLEM}/experiments/EXP-003-odd-frame-pressure`],
  ];
  const arrows = kind === 'science' ? ['Q', 'O', 'θ₁'] : [t('audit', 'auditoría'), t('check', 'verificar'), t('review', 'revisar')];
  const title = kind === 'science'
    ? t('Riemann short-interval proof dependencies', 'Dependencias de la prueba de Riemann en intervalos cortos')
    : t('Riemann research and certificate workflow', 'Flujo de investigación y certificación de Riemann');
  const finalLabel = kind === 'science' ? t('Read the complete proof', 'Leer la prueba completa') : t('Read the reproduction instructions', 'Leer las instrucciones de reproducción');
  const finalUrl = kind === 'science' ? PARITY_PROOF : `${ROOT}/blob/main/docs/guides/riemann-replay.md`;
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
        body_en: 'The Riemann experiments were declared and committed before computation. EXP-001 audits source constants and normalization. EXP-002 combines the first short-interval proof with a compact three-point certificate. EXP-003 preserves both records and adds an odd-frame pressure theorem. EXP-004 combines exact parity accounting with a classical odd-zero seed and Wang’s fixed-test transfer.\n\nStage A binds the declared hypothesis and earlier certificate before arithmetic, replays every old cell and checks pair incidence, telescoping spans, frame offsets and boundary cases. Stage B freezes rational pressure candidates before certification. The first candidate passes the all-gap pressure inequality and a strict gain target; the two remaining candidates are not run after success. EXP-004 separately replays its symbolic residuals, multiplicity cases, complete census and sharpness controls.\n\nOutward-rounded Arb bounds and a Lipschitz estimate cover every cell. Pressure alone handles sufficiently large spans. A separate sinc-Taylor evaluator replays the certificate, sharing Arb and geometry. It is not a wholly separate verifier or an end-to-end Lean proof. The EXP-004 proof review also keeps its numerical κ and θ₁ fields explicitly unquantified. Adversarial tests reject modified parameters, malformed trees, forged provenance and unresolved budget stops.\n\nThe saved proof, verdict, source commits and byte hashes bind the exported result. The certificate also has a canonical JSON digest, separately identified from its file-byte hash. This browser reads persisted evidence; the linked reproduction guide explains a fresh offline replay with pinned dependencies and an explicit output directory. CPU arithmetic sufficed. Publication and external mathematical acceptance remain separate gates.',
        body_es: 'Los experimentos de Riemann se declararon y comprometieron antes del cálculo. EXP-001 audita constantes y normalización. EXP-002 combina la primera prueba en intervalos cortos con un certificado compacto de tres puntos. EXP-003 conserva ambos registros y agrega un teorema de presión con marcos impares. EXP-004 combina la contabilidad exacta de paridad con una densidad clásica de ceros impares y la transferencia con prueba fija de Wang.\n\nLa etapa A vincula la hipótesis declarada y el certificado anterior antes de la aritmética, reproduce cada celda antigua y comprueba incidencia de pares, extensiones telescópicas, desplazamientos y fronteras. La etapa B fija candidatos racionales de presión antes de certificarlos. El primero satisface la desigualdad para toda separación y una meta estricta de ganancia; los dos restantes no se ejecutan tras ese éxito. EXP-004 reproduce por separado sus residuos simbólicos, casos de multiplicidad, censo completo y controles de optimalidad.\n\nLas cotas de Arb con redondeo hacia afuera y una estimación de Lipschitz cubren cada celda. La presión por sí sola cubre extensiones suficientemente grandes. Otro evaluador de Taylor para sinc reproduce el certificado y comparte Arb y geometría. No es un verificador totalmente separado ni una prueba Lean de extremo a extremo. La revisión de la prueba de EXP-004 mantiene explícitamente sin cuantificar sus campos κ y θ₁. Las pruebas adversariales rechazan parámetros modificados, árboles malformados, procedencia falsificada y paradas presupuestarias sin resolver.\n\nLa prueba, el veredicto, los commits y los hashes de bytes guardados vinculan el resultado exportado. El certificado también tiene un resumen canónico JSON, identificado por separado del hash de bytes. Este navegador lee evidencia persistida; la guía enlazada explica cómo reproducirla fuera del navegador con dependencias fijadas y un directorio de salida explícito. Bastó la aritmética en CPU. La publicación y la aceptación matemática externa siguen siendo controles separados.',
      };
      if (tab.id === 'science') return {
        ...tab,
        svg: diagram('science', lang),
        body_en: 'The two confirmed branches use different consequences of the same finite operator. For the pressure branch, fix θ above the positive root of Wang’s cosine curve and below one. N counts all nontrivial zero copies in (T, T + T^θ]; S counts simple critical zeros. Wang evaluates Q, the squared Hilbert–Schmidt norm of Lamzouri’s exact finite self-adjoint operator. The inherited stability inequality S ≥ 2N − Q + D(G) retains the nonnegative Gram defect while accounting for signed off-line conjugate pairs and all multiplicities.\n\nThe parity branch retains the odd-point count O and multiplicity excess Eₘ. Its exact finite identity 3S − (2N − Q + 2O + D) ≥ 0 combines with a distinct odd-zero seed O/N ≥ κ for every fixed θ > 51/100. Continuity of Wang’s c(θ) then supplies some fixed θ₁ < θ₀ with positive simple-critical density. κ and θ₁ are existential and unquantified in the export.\n\nFor EXP-003, the all-gap inequality E₃(u,v) + p(u+v) ≥ ε supplies a finite geometric input. Select k alternating triples inside a frame of M = 2k + 1 points. They share vertices but no unordered pair; their spans telescope. When kε ≤ 1, D ≥ min(1,E) yields D(frame) + pL_frame ≥ kε. Spectral defects are then added only over disjoint full frames, not overlapping triples.\n\nAverage the M possible frame offsets. Each adjacent gap occurs in at most M − 1 spans; incomplete frames leave a fixed boundary cost. With α = kε/M and β = 2kp/M, D(G) ≥ α(S − M + 1) − βL. Use L ≤ T^θ log(T)/(2π), whose upper bound divided by N tends to one. This gives c_odd = (Mc − 2kp)/(M − kε). A separate finite inequality 2N^d ≥ 3N − Q + D(G) proves the distinct-zero companion (1 + c_odd)/2 without assuming low multiplicities.\n\nFirst take T to infinity for each fixed smooth support λ < θ. Then approximate the cosine profile and let ε′ rise to ε; the cap endpoint kε = 1 is reached only in this outer limit. The compact EXP-002 floor gives ε = d and p = d/R, strengthening every positive point of the earlier curve. EXP-003 B directly certifies stronger pressure parameters at θ = 3/4. Neither EXP-003 nor EXP-004 supplies an effective height, establishes a global record or solves RH. The links below identify the inputs, prior-art audit and complete proofs.',
        body_es: 'Las dos vías confirmadas usan consecuencias distintas del mismo operador finito. Para la vía de presión, se fija θ por encima de la raíz positiva de la curva coseno de Wang y por debajo de uno. N cuenta todas las copias de ceros no triviales en (T, T + T^θ]; S cuenta los ceros críticos simples. Wang evalúa Q, el cuadrado de la norma de Hilbert–Schmidt del operador autoadjunto finito exacto de Lamzouri. La desigualdad heredada S ≥ 2N − Q + D(G) conserva el defecto de Gram no negativo y trata los pares conjugados con signo fuera de la recta y todas las multiplicidades.\n\nLa vía de paridad conserva el conteo de puntos impares O y el exceso de multiplicidad Eₘ. Su identidad finita exacta 3S − (2N − Q + 2O + D) ≥ 0 se combina con una densidad inicial de ceros impares distintos O/N ≥ κ para cada θ fijo mayor que 51/100. La continuidad de c(θ) de Wang aporta entonces algún θ₁ fijo menor que θ₀ con densidad positiva de ceros críticos simples. κ y θ₁ son existenciales y permanecen sin cuantificar en la exportación.\n\nPara EXP-003, la desigualdad para toda separación E₃(u,v) + p(u+v) ≥ ε aporta una entrada geométrica finita. Se seleccionan k ternas alternadas dentro de un marco de M = 2k + 1 puntos. Comparten vértices, pero ningún par no ordenado; sus extensiones se suman telescópicamente. Si kε ≤ 1, D ≥ min(1,E) da D(marco) + pL_marco ≥ kε. Los defectos espectrales se suman después solo entre marcos completos disjuntos, no entre ternas superpuestas.\n\nSe promedian los M desplazamientos posibles de marcos. Cada separación adyacente aparece en a lo más M − 1 extensiones; los marcos incompletos dejan un costo fijo de frontera. Con α = kε/M y β = 2kp/M se obtiene D(G) ≥ α(S − M + 1) − βL. Se usa L ≤ T^θ log(T)/(2π), cuya cota superior dividida por N tiende a uno. Esto da c_odd = (Mc − 2kp)/(M − kε). Otra desigualdad finita, 2N^d ≥ 3N − Q + D(G), prueba la cota complementaria (1 + c_odd)/2 de ceros distintos sin suponer multiplicidades bajas.\n\nPrimero se toma T hacia infinito para cada soporte suave fijo λ < θ. Después se aproxima el perfil coseno y se hace subir ε′ hacia ε; el extremo kε = 1 se alcanza solo en este límite exterior. La cota compacta de EXP-002 da ε = d y p = d/R, reforzando cada punto positivo de la curva anterior. La etapa B de EXP-003 certifica directamente parámetros de presión más fuertes en θ = 3/4. Ni EXP-003 ni EXP-004 da una altura efectiva, establece un récord global ni resuelve RH. Los enlaces inferiores identifican las entradas, la auditoría de antecedentes y las pruebas completas.',
      };
      return tab;
    }),
  };
}
