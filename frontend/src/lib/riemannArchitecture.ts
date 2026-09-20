import type { ArchitectureConfig, Lang } from '@fasl-work/caos-app-shell';
import { ARCHITECTURE } from './architecture';

const ROOT = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = `${ROOT}/tree/main/problems/number-theory/riemann-hypothesis`;
const LOCAL_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/mathematical-proof.md`;
const HILBERT_PROOF = `${ROOT}/blob/main/problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/mathematical-proof.md`;

function diagram(kind: 'science' | 'method', lang: Lang) {
  const t = (en: string, es: string) => lang === 'es' ? es : en;
  const nodes = kind === 'science' ? [
    [t('Wang: short-interval arithmetic', 'Wang: aritmética en intervalos cortos'), 'Q / N → 2 − c(θ)'],
    [t('Finite parity accounting', 'Contabilidad finita de paridad'), '3S − (2N − Q + 2O + D) ≥ 0'],
    [t('Localized Selberg odd-zero curve', 'Curva local de Selberg para ceros impares'), 'O / N ≥ (θ − 1/2)/(4eC₃)'],
    [t('Hilbert-parity compression', 'Compresión de Hilbert y paridad'), '0.545884 < θHP < 0.545885'],
  ] : [
    [t('Declare before computation', 'Declarar antes del cálculo'), 'EXP-001 · EXP-002 · EXP-003 · EXP-004 · EXP-005 · EXP-006'],
    [t('Replay finite certificates', 'Reproducir certificados finitos'), t('Pair incidence · spans · all offsets', 'Incidencia · extensiones · desplazamientos')],
    [t('Audit parity and pressure', 'Auditar paridad y presión'), t('Exact census · Arb · source binding', 'Censo exacto · Arb · vinculación de fuentes')],
    [t('Review, persist, then replay', 'Revisar, persistir y reproducir'), t('Adversarial tests · verdict · SHA-256', 'Pruebas adversariales · veredicto · SHA-256')],
  ];
  const links = kind === 'science' ? [
    ['Wang', 'https://arxiv.org/abs/2609.07918v1'],
    ['EXP-005', LOCAL_PROOF],
    ['EXP-006', HILBERT_PROOF],
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
  const finalUrl = kind === 'science' ? HILBERT_PROOF : `${ROOT}/blob/main/docs/guides/riemann-replay.md`;
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
        body_en: `The six Riemann experiments were declared and committed before computation. EXP-001 audits sources, EXP-002 begins the short-interval transfer, EXP-003 adds pressure, EXP-004 adds parity, EXP-005 localizes the Selberg detector, and EXP-006 retains the first Hilbert-subspace dimension before scalar compression.

EXP-006 first preserved the declared weaker run, then committed the stronger runner before a new canonical execution. Its proof combines the attributed arbitrary-parameter Hilbert inequality with the parity count 2(r+k) <= N-O. The exact runner checks 18,479 multiplicity profiles, directed rational transcendental bounds, a scalar zero-simple witness, and containment of a separate 100-digit interval replay. It certifies 0.545884 < \u03b8HP < 0.545885 and a positive lower bound at \u03b8 = 0.5459.

Replay schema v5 reads committed bytes only and requires the execution receipt plus proof-review hashes for the amended hypothesis, runner, focused tests, proof, audit, result and verdict. A failed hash, false RH flag, weakened bound, missing scalar barrier, or stale receipt blocks display. The browser performs no scientific arithmetic. CPU arithmetic sufficed; publication and external mathematical acceptance remain separate gates.`,
        body_es: `Los seis experimentos de Riemann se declararon y comprometieron antes del c\u00e1lculo. EXP-001 audita fuentes, EXP-002 inicia la transferencia a intervalos cortos, EXP-003 agrega presi\u00f3n, EXP-004 agrega paridad, EXP-005 localiza el detector de Selberg y EXP-006 conserva la dimensi\u00f3n del primer subespacio de Hilbert antes de la compresi\u00f3n escalar.

EXP-006 conserv\u00f3 primero la ejecuci\u00f3n d\u00e9bil declarada y despu\u00e9s comprometi\u00f3 el programa fortalecido antes de una nueva ejecuci\u00f3n can\u00f3nica. Su prueba combina la desigualdad de Hilbert con par\u00e1metro atribuida con el conteo de paridad 2(r+k) <= N-O. El programa exacto verifica 18.479 perfiles de multiplicidad, intervalos racionales dirigidos, un testigo escalar sin ceros simples y la inclusi\u00f3n de una reproducci\u00f3n independiente con 100 d\u00edgitos. Certifica 0.545884 < \u03b8HP < 0.545885 y una cota positiva en \u03b8 = 0.5459.

El esquema de reproducci\u00f3n v5 lee solo bytes comprometidos y exige el comprobante de ejecuci\u00f3n y los hashes de revisi\u00f3n para la hip\u00f3tesis enmendada, el programa, las pruebas focalizadas, la demostraci\u00f3n, la auditor\u00eda, el resultado y el veredicto. Un hash fallido, una marca falsa de RH, una cota debilitada, una barrera escalar ausente o un comprobante obsoleto bloquean la visualizaci\u00f3n. El navegador no realiza aritm\u00e9tica cient\u00edfica. Bast\u00f3 la CPU; la publicaci\u00f3n y la aceptaci\u00f3n matem\u00e1tica externa siguen siendo controles separados.`,
      };
      if (tab.id === 'science') return {
        ...tab,
        svg: diagram('science', lang),
        body_en: `Let N count all nontrivial zero copies in (T, T + T^\u03b8], S count simple critical zeros, O count distinct odd-multiplicity critical zeros, and Q denote the squared-kernel pair sum. EXP-006 proves the sharp finite inequality (Q-S)(N-O) >= 2(N-S)^2. It follows from the attributed Hilbert coefficient inequality Q >= S + (N-S)^2/(r+k) and the new parity compression 2(r+k) <= N-O.

Wang gives Q/N -> 2-c(\u03b8) for a fixed smooth test, while EXP-005 gives liminf O/N >= k3(\u03b8) = (\u03b8-1/2)/(4eC3). Pointwise insertion before taking limits yields the smaller quadratic root h3(\u03b8) = [3+k3(\u03b8)-sqrt((1-k3(\u03b8))(9-k3(\u03b8)-8c(\u03b8)))]/4 as a lower bound for liminf S/N. The complete bound also retains 0, c(\u03b8), and the earlier linear parity term.

The exact certificate proves that h3 becomes positive at one unique root with 0.545884 < \u03b8HP < 0.545885. At \u03b8 = 0.5459 the old linear term is still negative, while the strengthened term exceeds 0.0000168381638551244569880374399. A printed rank-six constant gives sensitivity only because its full profile is unavailable.

The theorem is asymptotic for each fixed exponent and supplies no effective starting height. The finite census checks implementation and equality cases; the written proof supplies universality. Imported 2026 preprints remain attributed and external review is still needed. None of these results proves RH.`,
        body_es: `Sea N el conteo de todas las copias de ceros no triviales en (T, T + T^\u03b8], S el de ceros cr\u00edticos simples, O el de ceros cr\u00edticos distintos de multiplicidad impar y Q la suma de pares del n\u00facleo al cuadrado. EXP-006 prueba la desigualdad finita \u00f3ptima (Q-S)(N-O) >= 2(N-S)^2. Se deduce de la desigualdad atribuida de coeficientes de Hilbert Q >= S + (N-S)^2/(r+k) y de la nueva compresi\u00f3n de paridad 2(r+k) <= N-O.

Wang da Q/N -> 2-c(\u03b8) para una prueba suave fija, mientras EXP-005 da liminf O/N >= k3(\u03b8) = (\u03b8-1/2)/(4eC3). Insertar estas cotas punto a punto antes de tomar l\u00edmites produce la ra\u00edz cuadr\u00e1tica menor h3(\u03b8) = [3+k3(\u03b8)-sqrt((1-k3(\u03b8))(9-k3(\u03b8)-8c(\u03b8)))]/4 como cota inferior para liminf S/N. La cota completa tambi\u00e9n conserva 0, c(\u03b8) y el t\u00e9rmino lineal de paridad anterior.

El certificado exacto prueba que h3 se vuelve positiva en una ra\u00edz \u00fanica con 0.545884 < \u03b8HP < 0.545885. En \u03b8 = 0.5459 el t\u00e9rmino lineal anterior sigue siendo negativo, mientras el t\u00e9rmino fortalecido supera 0.0000168381638551244569880374399. Una constante impresa de rango seis aporta solo sensibilidad porque su perfil completo no est\u00e1 disponible.

El teorema es asint\u00f3tico para cada exponente fijo y no aporta una altura inicial efectiva. El censo finito comprueba la implementaci\u00f3n y los casos de igualdad; la prueba escrita aporta la universalidad. Los preprints importados de 2026 siguen atribuidos y a\u00fan se necesita revisi\u00f3n externa. Ninguno de estos resultados prueba RH.`,
      };
      return tab;
    }),
  };
}
