import type { ArchitectureConfig, Lang } from '@fasl-work/caos-app-shell';
import { ARCHITECTURE } from './architecture';

const ROOT = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = `${ROOT}/tree/main/problems/number-theory/riemann-hypothesis`;
const RANK_SIX_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/mathematical-proof.md`;
const MOMENT_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-028-chirp-separated-moment/mellin-proof.md`;
const SHARP_KERNEL_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-009-wang-kernel-sharpening/mathematical-proof.md`;

function diagram(kind: 'science' | 'method', lang: Lang) {
  const t = (en: string, es: string) => lang === 'es' ? es : en;
  const nodes = kind === 'science' ? [
    [t('Wang: global and short-interval frameworks', 'Wang: marcos global y de intervalos cortos'), 'pair statistic · block packing'],
    [t('Sharp three-point kernel', 'Núcleo óptimo de tres puntos'), 'R(α, β) ≤ √2'],
    [t('Localized Levinson detector', 'Detector de Levinson localizado'), 'O / N ≥ κ > 0.7170 ν|ν < min(1/2, (17/33)(2θ−1))'],
    [t('Certified global and local bounds', 'Cotas globales y locales certificadas'), 'S / N > 0.6725007995|S / N > 0 for θ ≥ 0.5339'],
  ] : [
    [t('Declare before computation', 'Declarar antes del cálculo'), 'EXP-001 · EXP-002 · … · EXP-006|EXP-007 · EXP-008 · … · EXP-028'],
    [t('Replay finite certificates', 'Reproducir certificados finitos'), t('Pair incidence · spans · all offsets', 'Incidencia · extensiones · desplazamientos')],
    [t('Audit parity and pressure', 'Auditar paridad y presión'), t('Exact census · Arb · source binding', 'Censo exacto · Arb · vinculación de fuentes')],
    [t('Review, persist, then replay', 'Revisar, persistir y reproducir'), t('Adversarial tests · verdict · SHA-256', 'Pruebas adversariales · veredicto · SHA-256')],
  ];
  const links = kind === 'science' ? [
    ['EXP-028', MOMENT_PROOF],
    ['EXP-009', SHARP_KERNEL_PROOF],
    ['EXP-008', RANK_SIX_PROOF],
  ] : [
    ['EXP-001', `${PROBLEM}/experiments/EXP-001-source-and-constant-audit`],
    ['EXP-002', `${PROBLEM}/experiments/EXP-002-short-interval-stability`],
    ['EXP-003', `${PROBLEM}/experiments/EXP-003-odd-frame-pressure`],
  ];
  const arrows = kind === 'science' ? [t('isolate', 'aislar'), t('substitute', 'sustituir'), t('certify', 'certificar')] : [t('audit', 'auditoría'), t('check', 'verificar'), t('review', 'revisar')];
  const title = kind === 'science'
    ? t('Riemann short-interval proof dependencies', 'Dependencias de la prueba de Riemann en intervalos cortos')
    : t('Riemann research and certificate workflow', 'Flujo de investigación y certificación de Riemann');
  const finalLabel = kind === 'science' ? t('Read the complete proof', 'Leer la prueba completa') : t('Read the reproduction instructions', 'Leer las instrucciones de reproducción');
  const finalUrl = kind === 'science' ? MOMENT_PROOF : `${ROOT}/blob/main/docs/guides/riemann-replay.md`;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 550" role="img" aria-label="${title}" style="display:block;width:100%;max-width:460px;height:auto;margin:auto" font-family="ui-sans-serif,system-ui,sans-serif">
    <title>${title}</title>
    <defs><marker id="rh-arch-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0L7 3.5L0 7Z" fill="currentColor"/></marker></defs>
    ${nodes.map(([label, sub], i) => `<g>
      <rect x="10" y="${14 + i * 108}" width="340" height="72" rx="9" fill="var(--color-surface-2)" stroke="var(--color-accent)"/>
      <text x="180" y="${43 + i * 108}" text-anchor="middle" fill="currentColor" font-size="14" font-weight="600">${label}</text>
      <text x="180" y="${(sub.includes('|') ? 61 : 68) + i * 108}" text-anchor="middle" fill="currentColor" font-size="${sub.includes('|') ? 10 : 12}">${sub.includes('|') ? sub.split('|').map((line, j) => `<tspan x="180" dy="${j ? 13 : 0}">${line}</tspan>`).join('') : sub}</text>
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
        body_en: `EXP-028 internally extends the signed moment range to nu < min(1/2,(17/33)(2theta-1)) and the simple-critical onset to 0.5339, with explicit smoothing loss, two analytic derivations and published v0.02 DOI 10.5281/zenodo.23132248. External review and worldwide priority remain unconfirmed.

Completed EXP-020 certifies 96/96 shards and gives a distinct-strip proportion at least 0.8371747724947154. EXP-025 derives at least 0.8373797460706156 from Lavery’s externally certified local theorem, using the full pressure sum B. Its Lean/nanoda verification was archived, not rebuilt locally. Native EXP-020 checks share FLINT/Arb. The published companion has concept DOI 10.5281/zenodo.23128662. EXP-019 is suspended and EXP-023 remains incomplete; their candidate bounds are excluded. Global distinct counts and short-window simple-critical counts remain separate.

The first twelve Riemann experiments were declared and committed before computation. EXP-001 through EXP-006 audit the inputs and build the stability, pressure, parity, localization, and Hilbert layers. EXP-007 retains the spectral defect inside the parity product. EXP-008 proves localization for every fixed finite rank and applies the source-certified rank-six constant. EXP-009 proves the sharp three-point ratio and applies it inside Wang's pinned v1 global framework. EXP-010 localizes Levinson's method and moves the simple-critical onset to 0.534. EXP-011 certifies counterexamples that cap linear refinements of the finite inequality, and EXP-012 records why Tang's reciprocity with standard bounds does not lengthen the mollifier.

The exact runners bind their declarations, source bytes, focused tests, proofs, audits, results, verdicts, and independent interval replays. EXP-007 checks 652,260 spectra and 18,479 multiplicity profiles. EXP-008 certifies 0.5458837 < \u03b86 < 0.5458838 and a positive rank-six bound at \u03b8 = 0.545884, where the rank-three bound remains negative.

EXP-009 proves R(alpha,beta) <= sqrt(2) with exact equality cases and certifies a global simple-critical proportion above 0.6725007995946757558. Replay schema v9 reads committed bytes only and requires the execution receipts plus proof-review hashes. A failed hash, false RH flag, weakened comparison, or stale receipt blocks display. The browser performs no scientific arithmetic. CPU arithmetic sufficed; publication and external mathematical acceptance remain separate gates.`,
        body_es: `EXP-028 amplía internamente el rango del momento con signo a nu < min(1/2,(17/33)(2theta-1)) y el umbral de ceros críticos simples a 0.5339, con pérdida explícita de suavizado, dos derivaciones analíticas y v0.02 publicado con DOI 10.5281/zenodo.23132248. La revisión externa y la prioridad mundial siguen sin confirmar.

EXP-020 completo certifica 96/96 fragmentos y da una proporción de ceros distintos en toda la franja de al menos 0.8371747724947154. EXP-025 deriva al menos 0.8373797460706156 del teorema local certificado externamente por Lavery, usando la suma completa B de presiones. Su verificación Lean/nanoda se archivó y no se reconstruyó aquí. Las verificaciones nativas de EXP-020 comparten FLINT/Arb. El manuscrito tiene DOI de concepto 10.5281/zenodo.23128662. EXP-019 está suspendido y EXP-023 sigue incompleto; sus cotas candidatas se excluyen. Los conteos globales de puntos distintos y los de ceros críticos simples en ventanas cortas se conservan separados.

Los doce experimentos de Riemann se declararon y comprometieron antes del c\u00e1lculo. EXP-001 a EXP-006 auditan las entradas y construyen las capas de estabilidad, presi\u00f3n, paridad, localizaci\u00f3n y Hilbert. EXP-007 conserva el defecto espectral dentro del producto de paridad. EXP-008 prueba la localizaci\u00f3n para todo rango finito fijo y aplica la constante de rango seis certificada por la fuente. EXP-009 prueba el cociente \u00f3ptimo de tres puntos y lo aplica dentro del marco global v1 fijado de Wang. EXP-010 localiza el m\u00e9todo de Levinson y mueve el umbral de ceros cr\u00edticos simples a 0.534. EXP-011 certifica contraejemplos que acotan los refinamientos lineales de la desigualdad finita, y EXP-012 registra por qu\u00e9 la reciprocidad de Tang con cotas est\u00e1ndar no alarga el mollificador.

Los programas exactos vinculan sus declaraciones, bytes de fuentes, pruebas focalizadas, demostraciones, auditor\u00edas, resultados, veredictos y reproducciones independientes por intervalos. EXP-007 verifica 652.260 espectros y 18.479 perfiles de multiplicidad. EXP-008 certifica 0.5458837 < \u03b86 < 0.5458838 y una cota positiva de rango seis en \u03b8 = 0.545884, donde la cota de rango tres sigue siendo negativa.

EXP-009 prueba R(alpha,beta) <= sqrt(2) con casos de igualdad exactos y certifica una proporci\u00f3n global de ceros cr\u00edticos simples superior a 0.6725007995946757558. El esquema de reproducci\u00f3n v9 lee solo bytes comprometidos y exige los comprobantes de ejecuci\u00f3n y los hashes de revisi\u00f3n. Un hash fallido, una marca falsa de RH, una comparaci\u00f3n debilitada o un comprobante obsoleto bloquean la visualizaci\u00f3n. El navegador no realiza aritm\u00e9tica cient\u00edfica. Bast\u00f3 la CPU; la publicaci\u00f3n y la aceptaci\u00f3n matem\u00e1tica externa siguen siendo controles separados.`,
      };
      if (tab.id === 'science') return {
        ...tab,
        svg: diagram('science', lang),
        body_en: `EXP-028 internally extends the signed moment range to nu < min(1/2,(17/33)(2theta-1)) and the simple-critical onset to 0.5339, with explicit smoothing loss, two analytic derivations and published v0.02 DOI 10.5281/zenodo.23132248. External review and worldwide priority remain unconfirmed.

Completed EXP-020 certifies 96/96 shards and gives a distinct-strip proportion at least 0.8371747724947154. EXP-025 derives at least 0.8373797460706156 from Lavery’s externally certified local theorem, using the full pressure sum B. Its Lean/nanoda verification was archived, not rebuilt locally. Native EXP-020 checks share FLINT/Arb. The published companion has concept DOI 10.5281/zenodo.23128662. EXP-019 is suspended and EXP-023 remains incomplete; their candidate bounds are excluded. Global distinct counts and short-window simple-critical counts remain separate.

Let N count all nontrivial zero copies in (T, T + T^\u03b8], S count simple critical zeros, O count distinct odd-multiplicity critical zeros, Q denote the squared-kernel pair sum, and D(G) the convex spectral defect. EXP-007 proves the finite inequality (Q-S-D(G))(N-O) >= 2(N-S)^2. Dropping D recovers the sharp EXP-006 product; retaining it gives a strict full-curve gain.

Wang gives Q/N -> 2-c(\u03b8) for a fixed smooth test. EXP-008 proves that the Selberg detector localizes for every fixed finite rank q, so liminf O/N >= kq(\u03b8) = (\u03b8-1/2)/(4eCq). Pointwise insertion yields hq(\u03b8) = [3+kq(\u03b8)-sqrt((1-kq(\u03b8))(9-kq(\u03b8)-8c(\u03b8)))]/4.

Using Pearce-Crump's stated C6 interval, the exact certificate proves 0.5458837 < \u03b86 < 0.5458838. At \u03b8 = 0.545884, h6 exceeds 2.5541123454645702e-7 while h3 remains negative. At \u03b8 = 0.5459, h6 exceeds 0.0000177645181613023236390595079 and improves h3 by more than 9.263543061777356e-7.

EXP-009 separately proves the exact auxiliary ratio R(alpha,beta) <= sqrt(2), with equality only at (0,1) and (1,0). Substitution into Wang's pinned global v1 framework gives a simple-critical proportion above 0.6725007995946757558 and a distinct-zero proportion above 0.8362503997973378779.

EXP-010 replaces the Selberg detector by Levinson's, with Conrey's operator polynomial of any degree, localized to (T, T + T^\u03b8] for mollifier exponents \u03bd < \u03b8 - 1/2. Certified degree-201 detectors give \u03ba > 0.7170 \u03bd, and the same Hilbert-parity product gives a positive proportion of simple critical zeros for every fixed \u03b8 in [0.534, 1).

The public source prints the C6 interval but not its coefficient matrix, so CAOS attributes that input and does not claim an independent reconstruction. The theorem is asymptotic for each fixed exponent and supplies no effective starting height. Imported 2026 preprints remain attributed and external review is still needed. None of these results proves RH.`,
        body_es: `EXP-028 amplía internamente el rango del momento con signo a nu < min(1/2,(17/33)(2theta-1)) y el umbral de ceros críticos simples a 0.5339, con pérdida explícita de suavizado, dos derivaciones analíticas y v0.02 publicado con DOI 10.5281/zenodo.23132248. La revisión externa y la prioridad mundial siguen sin confirmar.

EXP-020 completo certifica 96/96 fragmentos y da una proporción de ceros distintos en toda la franja de al menos 0.8371747724947154. EXP-025 deriva al menos 0.8373797460706156 del teorema local certificado externamente por Lavery, usando la suma completa B de presiones. Su verificación Lean/nanoda se archivó y no se reconstruyó aquí. Las verificaciones nativas de EXP-020 comparten FLINT/Arb. El manuscrito tiene DOI de concepto 10.5281/zenodo.23128662. EXP-019 está suspendido y EXP-023 sigue incompleto; sus cotas candidatas se excluyen. Los conteos globales de puntos distintos y los de ceros críticos simples en ventanas cortas se conservan separados.

Sea N el conteo de todas las copias de ceros no triviales en (T, T + T^\u03b8], S el de ceros cr\u00edticos simples, O el de ceros cr\u00edticos distintos de multiplicidad impar, Q la suma de pares del n\u00facleo al cuadrado y D(G) el defecto espectral convexo. EXP-007 prueba la desigualdad finita (Q-S-D(G))(N-O) >= 2(N-S)^2. Omitir D recupera el producto \u00f3ptimo de EXP-006; conservarlo da una ganancia estricta en toda la curva.

Wang da Q/N -> 2-c(\u03b8) para una prueba suave fija. EXP-008 prueba que el detector de Selberg se localiza para todo rango finito fijo q, por lo que liminf O/N >= kq(\u03b8) = (\u03b8-1/2)/(4eCq). La inserci\u00f3n punto a punto da hq(\u03b8) = [3+kq(\u03b8)-sqrt((1-kq(\u03b8))(9-kq(\u03b8)-8c(\u03b8)))]/4.

Usando el intervalo C6 declarado por Pearce-Crump, el certificado exacto prueba 0.5458837 < \u03b86 < 0.5458838. En \u03b8 = 0.545884, h6 supera 2.5541123454645702e-7 mientras h3 sigue siendo negativa. En \u03b8 = 0.5459, h6 supera 0.0000177645181613023236390595079 y mejora h3 por m\u00e1s de 9.263543061777356e-7.

EXP-009 prueba por separado el cociente auxiliar exacto R(alpha,beta) <= sqrt(2), con igualdad solo en (0,1) y (1,0). Sustituirlo en el marco global v1 fijado de Wang da una proporci\u00f3n de ceros cr\u00edticos simples superior a 0.6725007995946757558 y una proporci\u00f3n de ceros distintos superior a 0.8362503997973378779.

EXP-010 reemplaza el detector de Selberg por el de Levinson, con el polinomio operador de Conrey de cualquier grado, localizado en (T, T + T^\u03b8] para exponentes de mollificador \u03bd < \u03b8 - 1/2. Detectores certificados de grado 201 dan \u03ba > 0.7170 \u03bd, y el mismo producto de Hilbert-paridad da una proporci\u00f3n positiva de ceros cr\u00edticos simples para cada \u03b8 fijo en [0.534, 1).

La fuente p\u00fablica imprime el intervalo C6 pero no su matriz de coeficientes, por lo que CAOS atribuye esa entrada y no afirma una reconstrucci\u00f3n independiente. El teorema es asint\u00f3tico para cada exponente fijo y no aporta una altura inicial efectiva. Los preprints importados de 2026 siguen atribuidos y a\u00fan se necesita revisi\u00f3n externa. Ninguno de estos resultados prueba RH.`,
      };
      return tab;
    }),
  };
}
