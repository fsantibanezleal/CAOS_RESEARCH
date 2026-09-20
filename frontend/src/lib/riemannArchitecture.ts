import type { ArchitectureConfig, Lang } from '@fasl-work/caos-app-shell';
import { ARCHITECTURE } from './architecture';

const ROOT = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = `${ROOT}/tree/main/problems/number-theory/riemann-hypothesis`;
const PARITY_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/mathematical-proof.md`;
const LOCAL_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/mathematical-proof.md`;

function diagram(kind: 'science' | 'method', lang: Lang) {
  const t = (en: string, es: string) => lang === 'es' ? es : en;
  const nodes = kind === 'science' ? [
    [t('Wang: short-interval arithmetic', 'Wang: aritmética en intervalos cortos'), 'Q / N → 2 − c(θ)'],
    [t('Finite parity accounting', 'Contabilidad finita de paridad'), '3S − (2N − Q + 2O + D) ≥ 0'],
    [t('Localized Selberg odd-zero curve', 'Curva local de Selberg para ceros impares'), 'O / N ≥ (θ − 1/2)/(4eC₃)'],
    [t('Explicit threshold and pressure', 'Umbral explícito y presión'), '0.5459 < θ* < 0.546  ·  EXP-003'],
  ] : [
    [t('Declare before computation', 'Declarar antes del cálculo'), 'EXP-001 · EXP-002 · EXP-003 · EXP-004 · EXP-005'],
    [t('Replay finite certificates', 'Reproducir certificados finitos'), t('Pair incidence · spans · all offsets', 'Incidencia · extensiones · desplazamientos')],
    [t('Audit parity and pressure', 'Auditar paridad y presión'), t('Exact census · Arb · source binding', 'Censo exacto · Arb · vinculación de fuentes')],
    [t('Review, persist, then replay', 'Revisar, persistir y reproducir'), t('Adversarial tests · verdict · SHA-256', 'Pruebas adversariales · veredicto · SHA-256')],
  ];
  const links = kind === 'science' ? [
    ['Wang', 'https://arxiv.org/abs/2609.07918v1'],
    ['EXP-004', PARITY_PROOF],
    ['EXP-005', LOCAL_PROOF],
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
  const finalUrl = kind === 'science' ? LOCAL_PROOF : `${ROOT}/blob/main/docs/guides/riemann-replay.md`;
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
        body_en: 'The Riemann experiments were declared and committed before computation. EXP-001 audits source constants and normalization. EXP-002 combines the first short-interval proof with a compact three-point certificate. EXP-003 adds an odd-frame pressure theorem. EXP-004 combines exact parity accounting with a classical odd-zero seed and Wang’s fixed-test transfer. EXP-005 localizes Pearce-Crump’s optimized Selberg method and certifies the first explicit positive threshold.\n\nEXP-005 separates the analytic localization proof from its finite certificate. The proof tracks the off-diagonal remainder on an interval of length T^θ and requires a fixed mollifier exponent u < (θ − 1/2)/2. The certificate then uses exact rationals and directed interval arithmetic to prove F(0.5459) < 0 < F(0.546), reject the boundary u = 0.023, and compare both the fixed-u and optimized curves.\n\nThe earlier pressure experiments bind their declarations before arithmetic, replay every old cell and check pair incidence, telescoping spans, frame offsets and boundary cases. Outward-rounded Arb bounds and a Lipschitz estimate cover every cell. A separate sinc-Taylor evaluator shares Arb and geometry, so it is not a wholly independent verifier or an end-to-end Lean proof. EXP-004 keeps its numerical κ and θ₁ fields explicitly unquantified.\n\nSaved proofs, verdicts, reviews, source commits and byte hashes bind the exported results. The EXP-005 gate also binds the exact source snapshot and byte-preserved canonical result. This browser reads persisted evidence; the linked reproduction guide explains a fresh offline replay with pinned dependencies and explicit output directories. CPU arithmetic sufficed. Publication and external mathematical acceptance remain separate gates.',
        body_es: 'Los experimentos de Riemann se declararon y comprometieron antes del cálculo. EXP-001 audita constantes y normalización. EXP-002 combina la primera prueba en intervalos cortos con un certificado compacto de tres puntos. EXP-003 agrega un teorema de presión con marcos impares. EXP-004 combina contabilidad exacta de paridad con una densidad clásica de ceros impares y la transferencia de Wang. EXP-005 localiza el método optimizado de Selberg de Pearce-Crump y certifica el primer umbral positivo explícito.\n\nEXP-005 separa la prueba analítica de localización de su certificado finito. La prueba controla el resto no diagonal en un intervalo de longitud T^θ y exige un exponente fijo u < (θ − 1/2)/2. El certificado usa racionales exactos y aritmética de intervalos dirigida para probar F(0.5459) < 0 < F(0.546), rechazar la frontera u = 0.023 y comparar las curvas con u fijo y optimizada.\n\nLos experimentos previos de presión vinculan sus declaraciones antes de la aritmética, reproducen cada celda y comprueban incidencia de pares, extensiones telescópicas, desplazamientos y fronteras. Las cotas de Arb con redondeo hacia afuera y una estimación de Lipschitz cubren cada celda. Otro evaluador de Taylor para sinc comparte Arb y geometría, por lo que no es un verificador totalmente independiente ni una prueba Lean de extremo a extremo. EXP-004 mantiene sin cuantificar sus campos κ y θ₁.\n\nLas pruebas, veredictos, revisiones, commits y hashes de bytes guardados vinculan los resultados exportados. El control de EXP-005 también vincula la copia exacta de la fuente y el resultado canónico preservado byte por byte. Este navegador lee evidencia persistida; la guía enlazada explica una reproducción local con dependencias fijadas y directorios de salida explícitos. Bastó la aritmética en CPU. La publicación y la aceptación matemática externa siguen siendo controles separados.',
      };
      if (tab.id === 'science') return {
        ...tab,
        svg: diagram('science', lang),
        body_en: 'Let N count all nontrivial zero copies in (T, T + T^θ], O count distinct critical-line zeros of odd multiplicity, and S count simple critical zeros. Pearce-Crump’s optimized Selberg method gives an asymptotic lower bound for O on long intervals. EXP-005 localizes its mean-square calculation: the off-diagonal error becomes O(T^(1/2+2u−θ) log T), so every fixed u < (θ − 1/2)/2 yields liminf O/N ≥ (θ − 1/2)/(4eC₃).\n\nThe exact parity identity from EXP-004 is 3S − (2N − Q + 2O + D) ≥ 0. Wang’s short-interval calculation gives Q/N → 2 − c(θ), while the Gram defect D is nonnegative. Therefore liminf S/N is at least the maximum of 0, c(θ), and [c(θ) + (θ − 1/2)/(2eC₃)]/3. This is positive at θ = 0.546 and negative at θ = 0.5459; the unique new threshold lies strictly between them.\n\nAt θ = 0.546 with u = 0.02299, the certified lower bounds are O/N > 0.0064386933093719401643 and S/N > 0.0000976239413345396825. Optimizing the limiting curve improves the latter to 0.0000994910410327771597. The certificate uses the interval C₃ = 0.6567752140190419405677628751089899133 ± 10⁻¹⁷ and encloses e, √2 and every transcendental evaluation by directed intervals.\n\nThe strict inequality on u matters: u = 0.023 at θ = 0.546 is recorded as a rejected boundary control. The theorem holds for every fixed θ above the certified root, with a fixed admissible u; it does not give an effective starting height or include θ = 1/2. The earlier pressure curve remains a separate confirmed route, and EXP-004’s qualitative θ₁ is superseded only as an explicit threshold statement. None of these results proves RH. The links below identify the source, full proof and replayable certificates.',
        body_es: 'Sea N el conteo de todas las copias de ceros no triviales en (T, T + T^θ], O el de ceros distintos de multiplicidad impar en la recta crítica y S el de ceros críticos simples. El método optimizado de Selberg de Pearce-Crump da una cota asintótica para O en intervalos largos. EXP-005 localiza su cálculo de media cuadrática: el error no diagonal pasa a ser O(T^(1/2+2u−θ) log T), por lo que cada u fijo con u < (θ − 1/2)/2 da liminf O/N ≥ (θ − 1/2)/(4eC₃).\n\nLa identidad exacta de paridad de EXP-004 es 3S − (2N − Q + 2O + D) ≥ 0. El cálculo de Wang en intervalos cortos da Q/N → 2 − c(θ), mientras el defecto de Gram D es no negativo. Por tanto, liminf S/N es al menos el máximo de 0, c(θ) y [c(θ) + (θ − 1/2)/(2eC₃)]/3. Esta expresión es positiva en θ = 0.546 y negativa en θ = 0.5459; el nuevo umbral único queda estrictamente entre ambos.\n\nEn θ = 0.546 con u = 0.02299, las cotas certificadas son O/N > 0.0064386933093719401643 y S/N > 0.0000976239413345396825. Optimizar la curva límite mejora la segunda a 0.0000994910410327771597. El certificado usa el intervalo C₃ = 0.6567752140190419405677628751089899133 ± 10⁻¹⁷ y encierra e, √2 y cada evaluación trascendente mediante intervalos dirigidos.\n\nLa desigualdad estricta para u es esencial: u = 0.023 en θ = 0.546 queda registrado como control de frontera rechazado. El teorema vale para cada θ fijo por encima de la raíz certificada, con un u fijo admisible; no da una altura inicial efectiva ni incluye θ = 1/2. La curva previa de presión sigue siendo una vía confirmada separada. Ninguno de estos resultados prueba RH. Los enlaces inferiores identifican la fuente, la prueba completa y los certificados reproducibles.',
      };
      return tab;
    }),
  };
}
