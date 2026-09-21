import type { ArchitectureConfig, Lang } from '@fasl-work/caos-app-shell';
import { ARCHITECTURE } from './architecture';

const ROOT = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = `${ROOT}/tree/main/problems/number-theory/riemann-hypothesis`;
const SPECTRAL_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/mathematical-proof.md`;
const RANK_SIX_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/mathematical-proof.md`;

function diagram(kind: 'science' | 'method', lang: Lang) {
  const t = (en: string, es: string) => lang === 'es' ? es : en;
  const nodes = kind === 'science' ? [
    [t('Wang: short-interval arithmetic', 'Wang: aritmética en intervalos cortos'), 'Q / N → 2 − c(θ)'],
    [t('Finite parity accounting', 'Contabilidad finita de paridad'), '3S − (2N − Q + 2O + D) ≥ 0'],
    [t('Finite-rank local Selberg curve', 'Curva local de Selberg de rango finito'), 'O / N ≥ (θ − 1/2)/(4eCq)'],
    [t('Rank-six Hilbert-parity onset', 'Umbral Hilbert-paridad de rango seis'), '0.5458837 < θ₆ < 0.5458838'],
  ] : [
    [t('Declare before computation', 'Declarar antes del cálculo'), 'EXP-001 · EXP-002 · EXP-003 · EXP-004 · EXP-005 · EXP-006 · EXP-007 · EXP-008'],
    [t('Replay finite certificates', 'Reproducir certificados finitos'), t('Pair incidence · spans · all offsets', 'Incidencia · extensiones · desplazamientos')],
    [t('Audit parity and pressure', 'Auditar paridad y presión'), t('Exact census · Arb · source binding', 'Censo exacto · Arb · vinculación de fuentes')],
    [t('Review, persist, then replay', 'Revisar, persistir y reproducir'), t('Adversarial tests · verdict · SHA-256', 'Pruebas adversariales · veredicto · SHA-256')],
  ];
  const links = kind === 'science' ? [
    ['Wang', 'https://arxiv.org/abs/2609.07918v1'],
    ['EXP-007', SPECTRAL_PROOF],
    ['EXP-008', RANK_SIX_PROOF],
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
  const finalUrl = kind === 'science' ? RANK_SIX_PROOF : `${ROOT}/blob/main/docs/guides/riemann-replay.md`;
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
        body_en: `The eight Riemann experiments were declared and committed before computation. EXP-001 through EXP-006 audit the inputs and build the stability, pressure, parity, localization, and Hilbert layers. EXP-007 retains the spectral defect inside the parity product. EXP-008 proves localization for every fixed finite rank and applies the source-certified rank-six constant.

The exact runners bind their declarations, source bytes, focused tests, proofs, audits, results, verdicts, and independent interval replays. EXP-007 checks 652,260 spectra and 18,479 multiplicity profiles. EXP-008 certifies 0.5458837 < \u03b86 < 0.5458838 and a positive rank-six bound at \u03b8 = 0.545884, where the rank-three bound remains negative.

Replay schema v7 reads committed bytes only and requires the execution receipts plus proof-review hashes. A failed hash, false RH flag, weakened comparison, or stale receipt blocks display. The browser performs no scientific arithmetic. CPU arithmetic sufficed; publication and external mathematical acceptance remain separate gates.`,
        body_es: `Los ocho experimentos de Riemann se declararon y comprometieron antes del c\u00e1lculo. EXP-001 a EXP-006 auditan las entradas y construyen las capas de estabilidad, presi\u00f3n, paridad, localizaci\u00f3n y Hilbert. EXP-007 conserva el defecto espectral dentro del producto de paridad. EXP-008 prueba la localizaci\u00f3n para todo rango finito fijo y aplica la constante de rango seis certificada por la fuente.

Los programas exactos vinculan sus declaraciones, bytes de fuentes, pruebas focalizadas, demostraciones, auditor\u00edas, resultados, veredictos y reproducciones independientes por intervalos. EXP-007 verifica 652.260 espectros y 18.479 perfiles de multiplicidad. EXP-008 certifica 0.5458837 < \u03b86 < 0.5458838 y una cota positiva de rango seis en \u03b8 = 0.545884, donde la cota de rango tres sigue siendo negativa.

El esquema de reproducci\u00f3n v7 lee solo bytes comprometidos y exige los comprobantes de ejecuci\u00f3n y los hashes de revisi\u00f3n. Un hash fallido, una marca falsa de RH, una comparaci\u00f3n debilitada o un comprobante obsoleto bloquean la visualizaci\u00f3n. El navegador no realiza aritm\u00e9tica cient\u00edfica. Bast\u00f3 la CPU; la publicaci\u00f3n y la aceptaci\u00f3n matem\u00e1tica externa siguen siendo controles separados.`,
      };
      if (tab.id === 'science') return {
        ...tab,
        svg: diagram('science', lang),
        body_en: `Let N count all nontrivial zero copies in (T, T + T^\u03b8], S count simple critical zeros, O count distinct odd-multiplicity critical zeros, Q denote the squared-kernel pair sum, and D(G) the convex spectral defect. EXP-007 proves the finite inequality (Q-S-D(G))(N-O) >= 2(N-S)^2. Dropping D recovers the sharp EXP-006 product; retaining it gives a strict full-curve gain.

Wang gives Q/N -> 2-c(\u03b8) for a fixed smooth test. EXP-008 proves that the Selberg detector localizes for every fixed finite rank q, so liminf O/N >= kq(\u03b8) = (\u03b8-1/2)/(4eCq). Pointwise insertion yields hq(\u03b8) = [3+kq(\u03b8)-sqrt((1-kq(\u03b8))(9-kq(\u03b8)-8c(\u03b8)))]/4.

Using Pearce-Crump's stated C6 interval, the exact certificate proves 0.5458837 < \u03b86 < 0.5458838. At \u03b8 = 0.545884, h6 exceeds 2.5541123454645702e-7 while h3 remains negative. At \u03b8 = 0.5459, h6 exceeds 0.0000177645181613023236390595079 and improves h3 by more than 9.263543061777356e-7.

The public source prints the C6 interval but not its coefficient matrix, so CAOS attributes that input and does not claim an independent reconstruction. The theorem is asymptotic for each fixed exponent and supplies no effective starting height. Imported 2026 preprints remain attributed and external review is still needed. None of these results proves RH.`,
        body_es: `Sea N el conteo de todas las copias de ceros no triviales en (T, T + T^\u03b8], S el de ceros cr\u00edticos simples, O el de ceros cr\u00edticos distintos de multiplicidad impar, Q la suma de pares del n\u00facleo al cuadrado y D(G) el defecto espectral convexo. EXP-007 prueba la desigualdad finita (Q-S-D(G))(N-O) >= 2(N-S)^2. Omitir D recupera el producto \u00f3ptimo de EXP-006; conservarlo da una ganancia estricta en toda la curva.

Wang da Q/N -> 2-c(\u03b8) para una prueba suave fija. EXP-008 prueba que el detector de Selberg se localiza para todo rango finito fijo q, por lo que liminf O/N >= kq(\u03b8) = (\u03b8-1/2)/(4eCq). La inserci\u00f3n punto a punto da hq(\u03b8) = [3+kq(\u03b8)-sqrt((1-kq(\u03b8))(9-kq(\u03b8)-8c(\u03b8)))]/4.

Usando el intervalo C6 declarado por Pearce-Crump, el certificado exacto prueba 0.5458837 < \u03b86 < 0.5458838. En \u03b8 = 0.545884, h6 supera 2.5541123454645702e-7 mientras h3 sigue siendo negativa. En \u03b8 = 0.5459, h6 supera 0.0000177645181613023236390595079 y mejora h3 por m\u00e1s de 9.263543061777356e-7.

La fuente p\u00fablica imprime el intervalo C6 pero no su matriz de coeficientes, por lo que CAOS atribuye esa entrada y no afirma una reconstrucci\u00f3n independiente. El teorema es asint\u00f3tico para cada exponente fijo y no aporta una altura inicial efectiva. Los preprints importados de 2026 siguen atribuidos y a\u00fan se necesita revisi\u00f3n externa. Ninguno de estos resultados prueba RH.`,
      };
      return tab;
    }),
  };
}
