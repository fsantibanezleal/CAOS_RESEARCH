import { Suspense, lazy, useEffect, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { Callout, Cite, Equation, InlineMath, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, loadRiemann, type ExperimentRec, type RiemannData } from '../api/data';
import { decimalCenter as center, parityEvidence, pressureWinner } from '../lib/riemannReplay';

const ExperimentModal = lazy(() => import('../components/ExperimentModal'));
const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = 'problems/number-theory/riemann-hypothesis';
const EXP = `${PROBLEM}/experiments/EXP-002-short-interval-stability`;
const PROOF = `${REPO}/blob/main/${EXP}/mathematical-proof.md`;
const PRESSURE_EXP = `${PROBLEM}/experiments/EXP-003-odd-frame-pressure`;
const PRESSURE_PROOF = `${REPO}/blob/main/${PRESSURE_EXP}/mathematical-proof.md`;
const PARITY_EXP = `${PROBLEM}/experiments/EXP-004-parity-density-transfer`;
const PARITY_PROOF = `${REPO}/blob/main/${PARITY_EXP}/mathematical-proof.md`;
const REPLAY_GUIDE = `${REPO}/blob/main/docs/guides/riemann-replay.md`;
const PAPER = `${REPO}/blob/main/manuscripts/riemann-hypothesis/short-interval-stability/main.pdf`;
const DOI = 'https://doi.org/10.5281/zenodo.22823615';
const CONCEPT_DOI = 'https://doi.org/10.5281/zenodo.22727388';

function SourceLink({ href, children }: { href: string; children: ReactNode }) {
  return <a href={href} target="_blank" rel="noreferrer">{children}</a>;
}

function ProofDiagram({ kind }: { kind: 'parity' | 'pressure' }) {
  const t = useT();
  const [step, setStep] = useState(0);
  const stages = kind === 'parity' ? [
    {
      title: t('Classical odd-zero seed', 'Densidad clásica de ceros impares'), formula: 'liminf O / N ≥ κ > 0',
      detail: t('Selberg’s theorem, in Karatsuba’s primary restatement, supplies distinct odd-multiplicity critical zeros in every sufficiently high interval with exponent α = 51/100. Packing these disjoint seed intervals into every fixed longer interval loses only an asymptotically negligible tail. One fixed positive κ works for every fixed θ > α; no numerical κ is extracted.', 'El teorema de Selberg, en la reformulación primaria de Karatsuba, aporta ceros críticos distintos de multiplicidad impar en cada intervalo suficientemente alto con exponente α = 51/100. Agrupar estos intervalos iniciales disjuntos dentro de cada intervalo fijo más largo solo pierde una cola asintóticamente despreciable. Un mismo κ positivo sirve para cada θ fijo mayor que α; no se extrae un κ numérico.'),
      href: 'https://www.mathnet.ru/eng/im1456',
    },
    {
      title: t('Multiplicity accounting', 'Contabilidad de multiplicidades'), formula: '3S ≥ 2N − Q + 2O + D',
      detail: t('An odd-multiplicity zero need not be simple. Every odd multiple point pays at least one unit of multiplicity excess E. The atom-by-atom identity S + E − O ≥ 0 and the inherited finite stability inequality give the displayed simple-zero bound and a separate distinct-zero bound. All off-line signs and multiplicities remain in the operator.', 'Un cero de multiplicidad impar no tiene por qué ser simple. Cada punto impar múltiple aporta al menos una unidad de exceso de multiplicidad E. La identidad por tipos de átomos S + E − O ≥ 0 y la desigualdad finita de estabilidad heredada dan la cota mostrada de ceros simples y otra separada de ceros distintos. Todos los signos fuera de la recta y las multiplicidades se conservan en el operador.'),
      href: `${PARITY_PROOF}#3-parity-and-the-exact-residual-certificates`,
    },
    {
      title: t('Fixed-test transfer', 'Transferencia con prueba fija'), formula: 'S / N ≥ (c(θ) + 2κ)/3 − o(1)',
      detail: t('Wang’s pair theorem applies with fixed smooth support λ < θ even when the cosine baseline c is negative. First take T to infinity, then smooth to the cosine profile and let λ rise to θ. Combining Q/N → 2 − c(θ) with the odd-zero seed preserves a positive parity contribution at the old cosine root.', 'El teorema de pares de Wang se aplica con soporte suave fijo λ < θ incluso cuando la cota coseno c es negativa. Primero se toma T hacia infinito, después se aproxima el perfil coseno y se hace subir λ hacia θ. Combinar Q/N → 2 − c(θ) con la densidad de ceros impares conserva una contribución positiva de paridad en la antigua raíz coseno.'),
      href: `${PARITY_PROOF}#5-wangs-arithmetic-input-and-the-exact-pair-sum-interface`,
    },
    {
      title: t('A strictly wider range', 'Un rango estrictamente mayor'), formula: 'θ₁ < θ₀ · liminf S / N ≥ κ/3',
      detail: t('The exact comparisons c(51/100) < 0 and c′ < 4 yield δ = min((θ₀ − 51/100)/2, κ/4) > 0. Put θ₁ = θ₀ − δ. Every fixed θ in [θ₁, 1) has simple-critical lower asymptotic proportion at least κ/3. This is a qualitative range extension: θ₁, κ and effective starting heights remain unquantified.', 'Las comparaciones exactas c(51/100) < 0 y c′ < 4 dan δ = min((θ₀ − 51/100)/2, κ/4) > 0. Se define θ₁ = θ₀ − δ. Cada θ fijo en [θ₁, 1) tiene proporción asintótica inferior de ceros críticos simples de al menos κ/3. Es una extensión cualitativa del rango: θ₁, κ y las alturas iniciales efectivas permanecen sin cuantificar.'),
      href: `${PARITY_PROOF}#7-the-positivity-threshold-and-the-quantitative-dependence-on-the-seed`,
    },
  ] : [
    {
      title: t('Arithmetic input', 'Entrada aritmética'), formula: 'Q / N → 2 − c(θ)',
      detail: t('Wang evaluates the second moment for a fixed smooth density supported inside an interval of width λ < θ. This supplies the short-interval arithmetic. The limit in height comes before the support and smoothing limits.', 'Wang evalúa el segundo momento para una densidad suave fija cuyo soporte está dentro de un intervalo de ancho λ < θ. Esto aporta la aritmética en intervalos cortos. El límite en altura precede a los límites del soporte y del suavizado.'),
      href: 'https://arxiv.org/abs/2609.07918v1',
    },
    {
      title: t('Retained defect', 'Defecto retenido'), formula: 'S ≥ 2N − Q + D(G)',
      detail: t('The simple critical zeros determine a positive Gram matrix G. Its convex spectral defect D(G) survives the finite operator argument, including the signed contributions of off-line conjugate pairs. Dropping this defect recovers the baseline.', 'Los ceros críticos simples determinan una matriz de Gram positiva G. Su defecto espectral convexo D(G) sobrevive al argumento del operador finito, incluidas las contribuciones con signo de los pares conjugados fuera de la recta. Descartar este defecto recupera la cota base.'),
      href: `${PROOF}#2-stable-rank-trace-inequality-with-a-self-contained-spectral-proof`,
    },
    {
      title: t('All-gap pressure', 'Presión para toda separación'), formula: 'E₃(u,v) + p(u+v) ≥ ε',
      detail: t('EXP-003 adds a linear span penalty to the three-point energy. Interval arithmetic certifies every cell inside u + v ≤ ε/p; outside, pressure alone proves the inequality. The earlier compact certificate also supplies a valid pressure inequality with ε = d and p = d/R.', 'EXP-003 suma una penalización lineal de la extensión a la energía de tres puntos. La aritmética de intervalos certifica cada celda dentro de u + v ≤ ε/p; fuera, la presión por sí sola prueba la desigualdad. El certificado compacto anterior también aporta una desigualdad válida con ε = d y p = d/R.'),
      href: `${REPO}/blob/main/${PRESSURE_EXP}/artifacts/stage-b/candidate-1/pressure-certificate.json`,
    },
    {
      title: t('Odd-frame transfer', 'Transferencia con marcos impares'), formula: 'cₒdd = (Mc − 2kp)/(M − kε)',
      detail: t('Take k alternating triples inside an M = 2k + 1 point frame. They share vertices but never duplicate pair energy; their spans telescope. Under kε ≤ 1, the spectral cap and averaging M disjoint-frame partitions give the displayed bound. The height limit comes before smoothing and ε′ rising to ε, including the cap endpoint kε = 1.', 'Se toman k ternas alternadas dentro de un marco de M = 2k + 1 puntos. Comparten vértices, pero nunca repiten energía de pares; sus extensiones se suman telescópicamente. Bajo kε ≤ 1, la cota espectral y el promedio de M particiones de marcos disjuntos dan la cota mostrada. El límite en altura precede al suavizado y a ε′ que sube hacia ε, incluso cuando kε = 1.'),
      href: PRESSURE_PROOF,
    },
  ];
  const title = kind === 'parity' ? t('How parity extends the interval range', 'Cómo la paridad amplía el rango de intervalos') : t('How pressure improves the proportion', 'Cómo la presión mejora la proporción');
  const description = kind === 'parity'
    ? t('Four stages connect a classical odd-zero density, exact multiplicity accounting, fixed-test short-interval arithmetic and a qualitative range extension.', 'Cuatro etapas conectan una densidad clásica de ceros impares, contabilidad exacta de multiplicidades, aritmética en intervalos cortos con prueba fija y una extensión cualitativa del rango.')
    : t('Four stages connect short-interval arithmetic, spectral stability, all-gap pressure and the odd-frame counting theorem.', 'Cuatro etapas conectan aritmética en intervalos cortos, estabilidad espectral, presión para toda separación y conteo con marcos impares.');
  const prefix = `rh-${kind}-proof`;
  return <figure className="rh-figure">
    <svg className="rh-proof-map-wide" viewBox="0 0 920 170" role="img" aria-labelledby={`${prefix}-title ${prefix}-desc`}>
      <title id={`${prefix}-title`}>{title}</title>
      <desc id={`${prefix}-desc`}>{description}</desc>
      <defs><marker id={`${prefix}-arrow`} markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7z" className="dg-arrowhead" /></marker></defs>
      {stages.map((s, i) => <g key={s.title}>
        {i > 0 && <path d={`M${i * 232 - 20} 68 h22`} className="dg-edge" markerEnd={`url(#${prefix}-arrow)`} />}
        <rect x={i * 232 + 3} y="20" width="213" height="100" rx="9" className={`dg-box${step === i ? ' accent' : ''}`} />
        <text x={i * 232 + 109} y="51" textAnchor="middle" className="dg-box-title">{s.title}</text>
        <text x={i * 232 + 109} y="84" textAnchor="middle" className="dg-box-sub">{s.formula}</text>
      </g>)}
      <path d="M110 143 H805" className="dg-edge" />
      <text x="460" y="163" textAnchor="middle" className="dg-axis-label">{kind === 'parity' ? t('Classical density + a universal finite argument + a separately reviewed analytic transfer', 'Densidad clásica + argumento finito universal + transferencia analítica revisada por separado') : t('Cited analytic inputs + a written finite proof + a reproducible energy certificate', 'Entradas analíticas citadas + una prueba finita escrita + un certificado reproducible de energía')}</text>
    </svg>
    <svg className="rh-proof-map-mobile" viewBox="0 0 320 410" role="img" aria-label={description}>
      {stages.map((s, i) => <g key={s.title}>
        {i > 0 && <path d={`M160 ${i * 102 - 13} v17 m-4 -4 l4 4 l4 -4`} className="dg-edge" />}
        <rect x="5" y={i * 102 + 7} width="310" height="80" rx="9" className={`dg-box${step === i ? ' accent' : ''}`} />
        <text x="160" y={i * 102 + 36} textAnchor="middle" className="dg-box-title">{s.title}</text>
        <text x="160" y={i * 102 + 63} textAnchor="middle" className="dg-box-sub">{s.formula}</text>
      </g>)}
    </svg>
    <div className={kind === 'parity' ? 'rh-stage-controls' : 'rh-stage-controls rh-pressure-stage-controls'} aria-label={kind === 'parity' ? t('Inspect a parity proof stage', 'Examinar una etapa de la prueba de paridad') : t('Inspect a pressure proof stage', 'Examinar una etapa de la prueba de presión')}>
      {stages.map((s, i) => <button key={s.title} className={`btn${step === i ? ' primary' : ''}`} onClick={() => setStep(i)} aria-pressed={step === i}>{s.title}</button>)}
    </div>
    <figcaption className={kind === 'parity' ? 'rh-stage-detail' : 'rh-stage-detail rh-pressure-stage-detail'} aria-live="polite">
      <p>{stages[step].detail}</p>
      <SourceLink href={stages[step].href}>{t('Read the source for this step', 'Leer la fuente de esta etapa')}</SourceLink>
    </figcaption>
  </figure>;
}

function TriangleDiagram() {
  const t = useT();
  return <figure className="rh-figure rh-triangle">
    <svg className="rh-proof-map-wide" viewBox="0 0 760 260" role="img" aria-labelledby="rh-triangle-title">
      <title id="rh-triangle-title">{t('Three gaps and their compact certification domain; schematic, not sampled zeros', 'Tres separaciones y su dominio compacto de certificación; esquema, no ceros muestreados')}</title>
      <line x1="35" y1="118" x2="345" y2="118" className="dg-axis" />
      {[70, 176, 304].map((x, i) => <g key={x}><circle cx={x} cy="118" r="6" className="dg-node" /><text x={x} y="148" textAnchor="middle" className="dg-node-label">x<tspan baselineShift="sub">{i + 1}</tspan></text></g>)}
      <path d="M70 98 v-20 H176 v20 M176 98 v-20 H304 v20" className="dg-edge" />
      <text x="123" y="67" textAnchor="middle" className="dg-node-label">u</text><text x="240" y="67" textAnchor="middle" className="dg-node-label">v</text>
      <path d="M70 166 v20 H304 v-20" className="dg-edge" /><text x="187" y="213" textAnchor="middle" className="dg-node-label">u + v</text>
      <path d="M466 213 V32 M466 213 H702" className="dg-axis" />
      <path d="M466 213 L466 48 L667 213 Z" className="dg-fill-accent" />
      <text x="705" y="231" className="dg-axis-label">u</text><text x="450" y="29" className="dg-axis-label">v</text>
      <text x="675" y="231" className="dg-tick">R</text><text x="444" y="50" className="dg-tick">R</text>
      <text x="509" y="171" className="dg-box-title">u + v ≤ R</text>
      <text x="380" y="251" textAnchor="middle" className="dg-axis-label">{t('Schematic geometry: every point of the closed triangle must pass the energy bound.', 'Geometría esquemática: cada punto del triángulo cerrado debe satisfacer la cota de energía.')}</text>
    </svg>
    <svg className="rh-proof-map-mobile" viewBox="0 0 320 285" role="img" aria-label={t('Schematic gap triangle u ≥ 0, v ≥ 0, u + v ≤ R; all boundary points included', 'Triángulo esquemático de separaciones u ≥ 0, v ≥ 0, u + v ≤ R; se incluye toda la frontera')}>
      <path d="M45 242 V32 M45 242 H285" className="dg-axis" />
      <path d="M45 242 L45 48 L267 242 Z" className="dg-fill-accent" />
      <text x="290" y="262" className="dg-axis-label">u</text><text x="28" y="29" className="dg-axis-label">v</text>
      <text x="265" y="263" className="dg-tick">R</text><text x="25" y="51" className="dg-tick">R</text>
      <text x="90" y="200" className="dg-box-title">u + v ≤ R</text>
      <text x="160" y="282" textAnchor="middle" className="dg-axis-label">{t('Closed domain; schematic geometry', 'Dominio cerrado; geometría esquemática')}</text>
    </svg>
  </figure>;
}

function OddFrameDiagram() {
  const t = useT();
  return <figure className="rh-figure">
    <svg viewBox="0 0 360 285" role="img" aria-labelledby="rh-frame-title rh-frame-desc" style={{ maxWidth: 520, marginInline: 'auto' }}>
      <title id="rh-frame-title">{t('Three pair-disjoint triples inside a seven-point frame', 'Tres ternas sin pares repetidos dentro de un marco de siete puntos')}</title>
      <desc id="rh-frame-desc">{t('Schematic k = 3: triples 1,2,3; 3,4,5; 5,6,7. A repeated endpoint represents the same point. Each selected pair appears once. The three spans add to x7 minus x1.', 'Esquema con k = 3: ternas 1,2,3; 3,4,5; 5,6,7. Un extremo repetido representa el mismo punto. Cada par seleccionado aparece una vez. Las tres extensiones suman x7 menos x1.')}</desc>
      {[0, 1, 2].map((j) => <g key={j}>
        <path d={`M40 ${54 + j * 78} H320 M40 ${48 + j * 78} Q180 ${2 + j * 78} 320 ${48 + j * 78}`} className="dg-edge" />
        {[0, 1, 2].map((i) => <g key={i}>
          <circle cx={40 + i * 140} cy={54 + j * 78} r="6" className="dg-node" />
          <text x={40 + i * 140} y={76 + j * 78} textAnchor="middle" className="dg-node-label">x<tspan baselineShift="sub">{2 * j + i + 1}</tspan></text>
        </g>)}
        <text x="180" y={27 + j * 78} textAnchor="middle" className="dg-box-title">{t('Triple', 'Terna')} {j + 1}</text>
      </g>)}
      <text x="180" y="268" textAnchor="middle" className="dg-node-label">L₁ + L₂ + L₃ = x₇ − x₁</text>
    </svg>
    <figcaption>{t('Pair energies add inside one frame. Spectral defects are added only across disjoint full frames. The picture is an index illustration, not sampled zeta zeros or the size of the certified frame.', 'Las energías de pares se suman dentro de un marco. Los defectos espectrales se suman solo entre marcos completos disjuntos. La figura ilustra índices; no representa ceros de zeta muestreados ni el tamaño del marco certificado.')}</figcaption>
  </figure>;
}

export default function RiemannHypothesis() {
  const t = useT();
  const [data, setData] = useState<RiemannData | null>(null);
  const [exps, setExps] = useState<ExperimentRec[]>([]);
  const [error, setError] = useState(false);
  const [recordsError, setRecordsError] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [open, setOpen] = useState<ExperimentRec | null>(null);
  useEffect(() => {
    let active = true;
    setError(false); setRecordsError(false);
    loadRiemann().then((value) => { if (active) setData(value); }).catch(() => { if (active) setError(true); });
    loadExperiments().then((value) => { if (active) setExps(value.filter((e) => e.problem === 'riemann-hypothesis' && ['001', '002', '003', '004'].includes(e.id))); }).catch(() => { if (active) setRecordsError(true); });
    return () => { active = false; };
  }, [attempt]);
  const result = data?.result;
  // Keep a readable fallback while an older baked replay is being replaced by
  // the v3 export. The page must not throw when the optional new branch is
  // absent during a deployment roll-forward.
  const stageA = data?.pressure_result?.stage_a;
  const winner = pressureWinner(data);
  const parity = parityEvidence(data);
  const sourceRole = (role: string) => ({
    constant_audit: t('constant audit', 'auditoría de constantes'),
    result: t('arithmetic result', 'resultado aritmético'),
    certificate: t('finite certificate', 'certificado finito'),
    proof: t('mathematical proof', 'prueba matemática'),
    verdict: t('experiment verdict', 'veredicto experimental'),
    source_manifest: t('source inventory', 'inventario de fuentes'),
    pressure_result: t('EXP-003 arithmetic results', 'Resultados aritméticos de EXP-003'),
    pressure_proof: t('EXP-003 complete proof', 'Prueba completa de EXP-003'),
    pressure_verdict: t('EXP-003 verdict', 'Veredicto de EXP-003'),
    pressure_audit: t('EXP-003 adversarial review', 'Revisión adversarial de EXP-003'),
    pressure_hypothesis: t('EXP-003 declaration before computation', 'Declaración de EXP-003 antes del cálculo'),
    pressure_candidates: t('Frozen pressure candidates', 'Candidatos de presión fijados'),
    pressure_code: t('Pressure certificate checker', 'Verificador del certificado de presión'),
    legacy_certificate_code: t('Reused compact certificate checker', 'Verificador compacto reutilizado'),
    pressure_runner: t('Pressure experiment runner', 'Programa del experimento de presión'),
    pressure_exploration: t('Pressure design script', 'Programa de diseño de presión'),
    legacy_exploration: t('Original compact-domain design script', 'Programa original de diseño compacto'),
    pressure_certificate_1: t('Candidate 1 pressure certificate', 'Certificado de presión del candidato 1'),
    parity_result: t('EXP-004 exact finite controls', 'Controles finitos exactos de EXP-004'),
    parity_hypothesis: t('EXP-004 declaration before computation', 'Declaración de EXP-004 antes del cálculo'),
    parity_proof: t('EXP-004 complete proof', 'Prueba completa de EXP-004'),
    parity_audit: t('EXP-004 adversarial review', 'Revisión adversarial de EXP-004'),
    parity_verdict: t('EXP-004 confirmed verdict', 'Veredicto confirmado de EXP-004'),
    parity_review: t('Separate mathematical review and source binding', 'Revisión matemática separada y vinculación de fuentes'),
    parity_runner: t('EXP-004 exact runner', 'Programa exacto de EXP-004'),
    parity_symbolic_raw: t('Symbolic identities and atom checks', 'Identidades simbólicas y controles de átomos'),
    parity_census_raw: t('Complete count census', 'Censo completo de conteos'),
    parity_relaxation_raw: t('Exact primal and dual witnesses', 'Testigos primales y duales exactos'),
    parity_sharpness_raw: t('Finite sharpness and negative control', 'Optimalidad finita y control negativo'),
    parity_premise_0: t('Classical density source audit', 'Auditoría de la fuente de densidad clásica'),
    parity_premise_1: t('Parity preflight audit', 'Auditoría previa de paridad'),
    parity_premise_2: t('Wang transfer audit', 'Auditoría de la transferencia de Wang'),
    parity_premise_3: t('Declared finite stability premise', 'Premisa declarada de estabilidad finita'),
  }[role] || role);
  const refsLabel = t('Sources for this section', 'Fuentes de esta sección');
  const resultTable = result ? <div className="rs-scroll"><table className="rs-table rh-results">
    <caption>{t('At θ = 3/4: asymptotic simple-critical proportions, with all zero copies in the denominator', 'Para θ = 3/4: proporciones asintóticas de ceros críticos simples, con todas las copias de ceros en el denominador')}</caption>
    <thead><tr><th>{t('Quantity', 'Cantidad')}</th><th>{t('Recorded decimal approximation', 'Aproximación decimal registrada')}</th></tr></thead>
    <tbody>
      <tr><td>{t('Wang baseline c(θ)', 'Cota base de Wang c(θ)')}</td><td className="rh-number">{center(result.baseline.display)}</td></tr>
      <tr><td>{t('EXP-002: first published example (v0.01)', 'EXP-002: primer ejemplo publicado (v0.01)')}</td><td className="rh-number">{center(result.improved.display)}</td></tr>
      {stageA && <tr><td>{t('EXP-003 A: same certificate, odd frames', 'EXP-003 A: mismo certificado, marcos impares')}</td><td className="rh-number">{center(stageA.improved.display)}</td></tr>}
      {winner && <tr><td>{t('EXP-003 B: new pressure certificate', 'EXP-003 B: nuevo certificado de presión')}</td><td className="rh-number"><strong>{center(winner.improved.display)}</strong></td></tr>}
      {winner && <tr><td>{t('Stage B gain above Wang, in proportion', 'Ganancia de la etapa B sobre Wang, en proporción')}</td><td className="rh-number">{center(winner.gain.display)}</td></tr>}
    </tbody>
  </table></div> : <p role="status">{error ? t('The recorded result could not be loaded. The proof and source artifacts remain available below.', 'No se pudo cargar el resultado registrado. La prueba y los artefactos originales siguen disponibles abajo.') : t('Loading the recorded arithmetic result…', 'Cargando el resultado aritmético registrado…')}</p>;

  const tabs: TabDef[] = [
    {
      id: 'summary', label: t('Summary', 'Resumen'), content: <section>
        <p className="rh-lead">{t('EXP-004 connects classical odd-zero density with the finite Hilbert-space method and Wang’s short-interval arithmetic. Its confirmed deduction extends positive simple-critical density to a fixed exponent strictly below the zero of Wang’s cosine bound. The improvement in interval range is qualitative: the new exponent and density constant have not been numerically determined. EXP-003 supplies a separate certified numerical improvement at θ = 3/4.', 'EXP-004 conecta la densidad clásica de ceros impares con el método de espacios de Hilbert finitos y la aritmética de Wang en intervalos cortos. Su deducción confirmada extiende la densidad positiva de ceros críticos simples a un exponente fijo estrictamente menor que la raíz de la cota coseno de Wang. La mejora del rango de intervalos es cualitativa: el nuevo exponente y la constante de densidad no se han determinado numéricamente. EXP-003 aporta una mejora numérica certificada separada en θ = 3/4.')}</p>
        <Equation tex={String.raw`\exists\,\kappa>0,\quad \frac{51}{100}<\theta_1<\theta_0:\qquad \forall\,\theta\in[\theta_1,1)\ {\rm fixed},\quad \liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}\ge\frac\kappa3>0`}
          caption={t('N counts all nontrivial zero copies with multiplicity in (T, T + T^θ]; S = N₀ˢ counts simple critical zeros. θ₀ is the unique zero of c(θ) = 2 − θ/2 − cot(θ/√2)/√2. One fixed κ serves every fixed exponent; eventual heights can depend on that exponent.', 'N cuenta todas las copias de ceros no triviales con multiplicidad en (T, T + T^θ]; S = N₀ˢ cuenta los ceros críticos simples. θ₀ es la raíz única de c(θ) = 2 − θ/2 − cot(θ/√2)/√2. Un mismo κ fijo sirve para cada exponente fijo; las alturas eventuales pueden depender de ese exponente.')} />
        <p className="small">{t('Classical seed: ', 'Densidad inicial clásica: ')}<Cite id="riemann-karatsuba1985" />{t(' · Arithmetic: ', ' · Aritmética: ')}<Cite id="riemann-wang2026" />{t(' · Range extension: ', ' · Extensión del rango: ')}<Cite id="riemann-parity2026" /></p>
        <p>{t('The theorem gives an explicit dependence on an unspecified positive classical constant: δ = min((θ₀ − 51/100)/2, κ/4) and θ₁ = θ₀ − δ. It does not supply a certified decimal θ₁. The distinct-zero result is proved separately; it is not obtained by halving one plus the new simple-zero bound.', 'El teorema da una dependencia explícita respecto de una constante clásica positiva no especificada: δ = min((θ₀ − 51/100)/2, κ/4) y θ₁ = θ₀ − δ. No aporta un decimal certificado para θ₁. El resultado de ceros distintos se prueba por separado; no se obtiene dividiendo por dos la suma de uno y la nueva cota de ceros simples.')}</p>
        {parity ? <p className="small">{t('Scientific verdict: confirmed. The export binds the finite result to a separate full-proof and analytic-transfer review; the census alone establishes no all-height theorem.', 'Veredicto científico: confirmado. La exportación vincula el resultado finito con una revisión separada de la prueba completa y la transferencia analítica; el censo por sí solo no establece un teorema para todas las alturas.')}</p> : <p role="status">{t('Loading the separately reviewed parity evidence. The full proof and verdict are available through the source links.', 'Cargando la evidencia de paridad revisada por separado. La prueba completa y el veredicto están disponibles en los enlaces a las fuentes.')}</p>}
        <ProofDiagram kind="parity" />
        <h2>{t('Quantitative companion: the pressure refinement', 'Resultado cuantitativo complementario: refinamiento por presión')}</h2>
        <p>{t('At the fixed exponent θ = 3/4, the earlier experiments retain their certified numerical bounds. These decimals quantify the pressure branch, not κ or the new interval exponent in the parity theorem.', 'Para el exponente fijo θ = 3/4, los experimentos anteriores conservan sus cotas numéricas certificadas. Estos decimales cuantifican la vía de presión, no κ ni el nuevo exponente de intervalos del teorema de paridad.')} <Cite id="riemann-pressure2026" /></p>
        {winner && <p className="rh-parameters">θ = <b>{winner.theta}</b> · p = <b>{winner.pressure}</b> · ε = <b>{winner.epsilon}</b><br />k = <b>{winner.k}</b> · M = <b>{winner.frame_size}</b></p>}
        {resultTable}
        <p>{t('These are decimal approximations to limiting lower-bound constants; exact rational enclosures are available in Results. Stage B exceeded the declared target of 5/4 times Stage A’s gain above Wang. The comparison concerns the small gain, not a 25% increase in the full zero proportion.', 'Son aproximaciones decimales a constantes de cotas inferiores límite; los intervalos racionales exactos están en Resultados. La etapa B superó la meta declarada de 5/4 de la ganancia de la etapa A sobre Wang. La comparación corresponde a la pequeña ganancia, no a un aumento del 25% en la proporción total de ceros.')}</p>
        <Callout variant="honest" title={t('What the result establishes', 'Qué establece el resultado')}>
          {t('The confirmed repository deduction is a qualitative extension below the cosine positivity threshold plus a separate numerical pressure refinement. RH remains open. No numerical new exponent, effective starting height, global record or universal simplicity follows. The manuscript series awaits external review; automated audits, finite certificates and publication do not constitute peer acceptance or an end-to-end formal proof.', 'La deducción confirmada en el repositorio es una extensión cualitativa bajo el umbral de positividad coseno junto con un refinamiento numérico separado por presión. RH sigue abierta. No se obtiene un nuevo exponente numérico, una altura inicial efectiva, un récord global ni simplicidad universal. La serie de manuscritos espera revisión externa; las auditorías automatizadas, los certificados finitos y la publicación no constituyen aceptación por pares ni una prueba formal de extremo a extremo.')}
        </Callout>
        <div className="rh-source-links"><SourceLink href={PARITY_PROOF}>{t('Full EXP-004 parity proof', 'Prueba completa de paridad de EXP-004')}</SourceLink><SourceLink href={PRESSURE_PROOF}>{t('Full EXP-003 pressure proof', 'Prueba completa de presión de EXP-003')}</SourceLink><SourceLink href={PAPER}>{t('Read the manuscript PDF', 'Leer el manuscrito PDF')}</SourceLink><SourceLink href={DOI}>{t('Current Zenodo version (0.03)', 'Versión actual en Zenodo (0.03)')}</SourceLink><SourceLink href={CONCEPT_DOI}>{t('Zenodo record and versions', 'Registro y versiones de Zenodo')}</SourceLink><SourceLink href="https://doi.org/10.5281/zenodo.22727389">{t('First published version (0.01)', 'Primera versión publicada (0.01)')}</SourceLink></div>
        <Refs label={refsLabel} ids={['riemann-karatsuba1985', 'riemann-wang2026', 'riemann-ainta2026', 'riemann-lamzouri2026', 'riemann-refinement2026', 'riemann-pressure2026', 'riemann-parity2026']} />
      </section>,
    },
    {
      id: 'context', label: t('Context & history', 'Contexto e historia'), content: <section>
        <h2>{t('What “on the critical line” means', 'Qué significa «en la recta crítica»')}</h2>
        <p>{t('The nontrivial zeros lie in the strip between real parts zero and one. RH asserts that all of them have real part one-half. A positive-proportion theorem addresses a different question: how many zeros can be proved to lie on that line, or to be simple, compared with the total count? A simple zero has multiplicity one. A distinct-zero count counts each location once even when its multiplicity is larger.', 'Los ceros no triviales están en la franja entre partes reales cero y uno. RH afirma que todos tienen parte real un medio. Un teorema de proporción positiva aborda otra pregunta: ¿cuántos ceros pueden demostrarse en esa recta, o simples, respecto del número total? Un cero simple tiene multiplicidad uno. El conteo de ceros distintos cuenta cada ubicación una sola vez aunque su multiplicidad sea mayor.')}</p>
        <Equation tex={String.raw`N_0^s\le N_0\le N,\qquad N^d\le N,\qquad \mathrm{RH}:\ \zeta(\rho)=0,\ 0<\Re\rho<1\Longrightarrow\Re\rho=\tfrac12`}
          caption={t('N₀ counts critical-line zeros with multiplicity; N₀ˢ counts simple critical zeros; Nᵈ counts distinct zeros anywhere in the strip. RH does not itself assert simplicity.', 'N₀ cuenta ceros en la recta crítica con multiplicidad; N₀ˢ cuenta ceros críticos simples; Nᵈ cuenta ceros distintos en cualquier lugar de la franja. RH no afirma por sí misma que sean simples.')} />
        <h2>{t('How the recent proof changed', 'Cómo evolucionó la prueba reciente')}</h2>
        <p>{t('Anthropic’s August announcement introduced a Claude-assisted proof, followed by a shorter revised manuscript and a human account by Alpoge and Furman. The original method assembles a finite Weil matrix, evaluates its trace and second moment, and exploits the different inertia of critical zeros and reflected off-line pairs. It reaches the optimized Montgomery–Taylor cosine constant.', 'El anuncio de agosto de Anthropic presentó una prueba asistida por Claude, seguida de un manuscrito revisado más corto y una exposición humana de Alpoge y Furman. El método original construye una matriz de Weil finita, evalúa su traza y segundo momento y aprovecha la distinta inercia de los ceros críticos y de los pares reflejados fuera de la recta. Alcanza la constante coseno optimizada de Montgomery–Taylor.')} <Cite id="riemann-anthropic2026" /> <Cite id="riemann-alpogefurman2026" /></p>
        <Equation tex={String.raw`C_0=\frac32-\frac1{\sqrt2}\cot\frac1{\sqrt2},\qquad C_1=\frac{1+C_0}{2}`}
          caption={t('C₀ is the optimized global simple-critical proportion in the baseline proof; C₁ is its distinct-zero companion. These are prior results reproduced by the constant audit.', 'C₀ es la proporción global optimizada de ceros críticos simples en la prueba base; C₁ es su cota complementaria de ceros distintos. Son resultados previos reproducidos por la auditoría de constantes.')} />
        {data && <p className="rh-number">C₀ &gt; {data.constant_audit.constants.c0.exact.decimal_lower}<br />C₁ &gt; {data.constant_audit.constants.c1.exact.decimal_lower}</p>}
        <p>{t('Lamzouri replaced much of the original analytic machinery with an exact finite-rank self-adjoint operator on a Hilbert space. Pair correlation computes its squared Hilbert–Schmidt norm, and a finite inequality turns that moment into a zero count. His second version also treats simple-or-critical zeros and related multiplicity bounds. This already supplies the main simplification of the original proof.', 'Lamzouri reemplazó gran parte de la maquinaria analítica original por un operador autoadjunto exacto de rango finito en un espacio de Hilbert. La correlación por pares calcula el cuadrado de su norma de Hilbert–Schmidt y una desigualdad finita convierte ese momento en un conteo de ceros. Su segunda versión también trata ceros simples o críticos y cotas relacionadas de multiplicidad. Esto ya proporciona la principal simplificación de la prueba original.')} <Cite id="riemann-lamzouri2026" /></p>
        <p>{t('Wang then supplied the pair-correlation theorem for intervals of length T^θ and applied Lamzouri’s operator there. A global bound and a short-interval bound have different scope: the latter must hold asymptotically in every interval of that prescribed length. Retaining a known spectral stability defect in this setting is the target of the present refinement.', 'Wang aportó después el teorema de correlación por pares para intervalos de longitud T^θ y aplicó allí el operador de Lamzouri. Una cota global y una cota en intervalos cortos tienen distinto alcance: esta última debe valer asintóticamente en cada intervalo de la longitud prescrita. Retener un defecto conocido de estabilidad espectral en este contexto es el objetivo del refinamiento presente.')} <Cite id="riemann-wang2026" /></p>
        <h2>{t('A classical input changes the interval range', 'Una entrada clásica cambia el rango de intervalos')}</h2>
        <p>{t('Odd-order critical zeros change the sign of the real Hardy Z function, but they can have multiplicity three or more. Selberg proved a positive density of distinct odd-order critical zeros in every sufficiently high interval of exponent 1/2 + ε. Karatsuba’s primary article restates that theorem and proves a stronger seed interval result. EXP-004 only needs one fixed seed exponent α = 51/100, with an unspecified positive constant.', 'Los ceros críticos de orden impar cambian el signo de la función real Z de Hardy, pero pueden tener multiplicidad tres o mayor. Selberg probó una densidad positiva de ceros críticos distintos de orden impar en cada intervalo suficientemente alto de exponente 1/2 + ε. El artículo primario de Karatsuba reformula ese teorema y prueba un resultado más fuerte para intervalos iniciales. EXP-004 solo necesita un exponente inicial fijo α = 51/100, con una constante positiva no especificada.')} <Cite id="riemann-karatsuba1985" /></p>
        <p>{t('EXP-002 and EXP-003 improve proportions above the positive root θ₀ of Wang’s cosine curve. EXP-004 retains the multiplicity excess from the same finite method and combines it with the classical odd count. At θ₀, where the cosine baseline vanishes, this gives at least 2κ/3 simple-critical density. Continuity with an explicit derivative bound then proves positivity at a fixed smaller exponent θ₁. The reviewed novelty concerns this short-interval combination, not the classical seed or the general finite multiplicity inequality.', 'EXP-002 y EXP-003 mejoran proporciones por encima de la raíz positiva θ₀ de la curva coseno de Wang. EXP-004 conserva el exceso de multiplicidad del mismo método finito y lo combina con el conteo clásico de ceros impares. En θ₀, donde se anula la cota coseno base, esto da al menos 2κ/3 de densidad de ceros críticos simples. La continuidad con una cota explícita de la derivada prueba entonces positividad en un exponente fijo menor θ₁. La novedad revisada corresponde a esta combinación en intervalos cortos, no a la densidad clásica ni a la desigualdad general finita de multiplicidad.')} <Cite id="riemann-parity2026" /></p>
        <Callout variant="note" title={t('Corrections preserved in the review', 'Correcciones conservadas en la revisión')}>
          {t('The source audit corrects an additive grid-dimension error in the revised original proof: the discrepancy is of order T, while the relative error still tends to zero. It therefore does not by itself refute the limiting theorem. The review also preserves the corrected BGSTB error terms and distinguishes historical critical-line counts from simple-critical counts.', 'La auditoría corrige un error aditivo en la dimensión de la malla de la prueba original revisada: la discrepancia es de orden T, mientras que el error relativo aún tiende a cero. Por ello no refuta por sí sola el teorema límite. La revisión también conserva los términos de error corregidos de BGSTB y distingue los conteos históricos de ceros críticos de los conteos de ceros críticos simples.')}
        </Callout>
        <Refs label={refsLabel} ids={['riemann-anthropic2026', 'riemann-alpogefurman2026', 'riemann-lamzouri2026', 'riemann-wang2026', 'riemann-bgstb2026', 'riemann-karatsuba1985', 'riemann-parity2026']} />
      </section>,
    },
    {
      id: 'approaches', label: t('References & approaches', 'Referencias y enfoques'), content: <section>
        <h2>{t('A map of the evidence', 'Un mapa de la evidencia')}</h2>
        <p>{t('The review follows primary proof documents, pinned source repositories, and their explicit theorem statements. An announcement, a successful library build, a finite interval certificate, and an end-to-end formal theorem answer different questions. Each source below is useful within its own boundary.', 'La revisión sigue documentos primarios de prueba, repositorios fijados por versión y sus enunciados explícitos. Un anuncio, una compilación exitosa de biblioteca, un certificado finito de intervalos y un teorema formal de extremo a extremo responden preguntas distintas. Cada fuente es útil dentro de su propio alcance.')}</p>
        <div className="rs-scroll"><table className="rs-table">
          <thead><tr><th>{t('Approach', 'Enfoque')}</th><th>{t('What it contributes', 'Qué aporta')}</th><th>{t('Review boundary', 'Límite de la revisión')}</th></tr></thead>
          <tbody>
            <tr><td><Cite id="riemann-anthropic2026" /></td><td>{t('Weil matrix, prime-side moments, optimized cosine bound.', 'Matriz de Weil, momentos del lado de los primos y cota coseno optimizada.')}</td><td>{t('Revised claims and rate corrections matter; process transcripts are supporting history.', 'Importan las afirmaciones revisadas y las correcciones de tasas; las transcripciones documentan el proceso.')}</td></tr>
            <tr><td><Cite id="riemann-lamzouri2026" /></td><td>{t('Exact finite Hilbert operator and multiplicity inequalities.', 'Operador de Hilbert finito exacto y desigualdades de multiplicidad.')}</td><td>{t('Classical pair correlation supplies the analytic moment.', 'La correlación por pares clásica aporta el momento analítico.')}</td></tr>
            <tr><td><Cite id="riemann-wang2026" /></td><td>{t('Short-interval arithmetic and the exponent-dependent baseline.', 'Aritmética en intervalos cortos y cota base dependiente del exponente.')}</td><td>{t('Fixed support strictly below θ; the order of limits is essential.', 'Soporte fijo estrictamente menor que θ; el orden de los límites es esencial.')}</td></tr>
            <tr><td><Cite id="riemann-karatsuba1985" /></td><td>{t('Selberg’s distinct odd-zero seed, restated in a primary paper; Karatsuba also proves a stronger classical seed.', 'Densidad inicial de ceros impares distintos de Selberg, reformulada en un artículo primario; Karatsuba también prueba una densidad inicial clásica más fuerte.')}</td><td>{t('EXP-004 uses α = 51/100 with an unspecified positive constant. Odd multiplicity is not assumed to mean simplicity.', 'EXP-004 usa α = 51/100 con una constante positiva no especificada. No se supone que multiplicidad impar signifique simplicidad.')}</td></tr>
            <tr><td><Cite id="riemann-ainta2026" /><br /><Cite id="riemann-trmdy2026" /></td><td>{t('Retained convex Gram defect, window pressure and larger frames.', 'Defecto convexo de Gram retenido, presión de ventanas y marcos mayores.')}</td><td>{t('These global frameworks predate our transfer. Their numerical global headlines are not imported as short-interval bounds.', 'Estos marcos globales preceden a nuestra transferencia. Sus cifras globales anunciadas no se importan como cotas en intervalos cortos.')}</td></tr>
            <tr><td><Cite id="riemann-tawanerguo2026" /><br /><Cite id="riemann-yuhangshi2026" /></td><td>{t('Nonuniform pair capacities, mixed frames and spectral envelopes.', 'Capacidades no uniformes de pares, marcos mixtos y cotas espectrales.')}</td><td>{t('The alternating triple schedule is a choice within this existing finite framework. EXP-003 claims its stronger short-interval consequence, not the general packing mechanism.', 'La selección de ternas alternadas es una opción dentro de este marco finito existente. EXP-003 propone su consecuencia más fuerte en intervalos cortos, no el mecanismo general de agrupación.')}</td></tr>
          </tbody>
        </table></div>
        <h2>{t('What the Lean source actually covers', 'Qué cubre realmente la fuente Lean')}</h2>
        <p>{t('AxiomMath’s second development gives explicit Riemann–von Mangoldt and pair-correlation assumptions to its headline zeta theorems. Its finite inequalities and numerical corollaries are formal source, while those two analytic inputs remain assumptions in that project. The pinned upstream CI confirms a default-library build; it does not itself show the separate challenge comparator running.', 'El segundo desarrollo de AxiomMath incluye supuestos explícitos de Riemann–von Mangoldt y correlación por pares en sus teoremas principales sobre zeta. Sus desigualdades finitas y corolarios numéricos son fuente formal, mientras que esas dos entradas analíticas siguen siendo supuestos en ese proyecto. El CI de la versión fijada confirma una compilación de la biblioteca predeterminada; no demuestra por sí solo la ejecución del comparador separado de desafíos.')} <Cite id="riemann-axiom2026" /></p>
        <p>{t('Anthropic’s current formal-math development contains proofs of the analytic inputs and headline statements without those external hypotheses. Our source inspection distinguishes this stronger intended scope from the verification receipts available for particular commits. We did not locally rebuild the full upstream Lean developments, and we do not present upstream author reports as our own independent kernel verification.', 'El desarrollo actual formal-math de Anthropic contiene pruebas de las entradas analíticas y enunciados principales sin esas hipótesis externas. Nuestra inspección distingue este alcance más fuerte de los comprobantes de verificación disponibles para ciertos commits. No recompilamos localmente los desarrollos Lean completos y no presentamos los informes de los autores como verificación independiente del núcleo realizada por nosotros.')} <Cite id="riemann-formalmath2026" /></p>
        <Callout variant="honest" title={t('Novelty is narrower than a larger decimal', 'La novedad exige más que un decimal mayor')}>
          {t('The finite stability inequalities, odd-zero seed and global pressure frameworks are attributed prior work. The confirmed repository deductions are their stronger short-interval consequences: a quantitative pressure refinement and a qualitative extension below the cosine positivity root. The source search found no matching parity combination, but cannot guarantee priority. Higher-moment or short-mollifier headlines are not substituted for a proved simple-zero input.', 'Las desigualdades finitas de estabilidad, la densidad inicial de ceros impares y los marcos globales de presión se atribuyen a trabajos previos. Las deducciones confirmadas en el repositorio son sus consecuencias más fuertes en intervalos cortos: un refinamiento cuantitativo por presión y una extensión cualitativa bajo la raíz de positividad coseno. La búsqueda no encontró una combinación de paridad equivalente, pero no garantiza prioridad. Los anuncios sobre momentos superiores o mollificadores cortos no sustituyen una entrada demostrada sobre ceros simples.')}
        </Callout>
        <h2>{t('Alternative reformulations: source preflight', 'Reformulaciones alternativas: revisión previa de fuentes')}</h2>
        <p>{t('The review also compares approximation in Hilbert spaces, Li–Weil positivity, spectral realizations and heat flow. These dossiers state exact equivalences, finite diagnostics and known barriers. Finite positive tests cannot establish an infinite positivity criterion; a proposed self-adjoint operator also needs a proved bridge to the zeta function. None of these source reviews is reported here as a confirmed new experiment.', 'La revisión también compara aproximación en espacios de Hilbert, positividad de Li–Weil, realizaciones espectrales y flujo de calor. Los informes establecen equivalencias exactas, diagnósticos finitos y barreras conocidas. Pruebas positivas finitas no establecen un criterio de positividad infinito; un operador autoadjunto propuesto también necesita un vínculo demostrado con zeta. Ninguna de estas revisiones de fuentes se presenta aquí como un nuevo experimento confirmado.')}</p>
        <div className="rh-source-links"><SourceLink href={`${REPO}/blob/main/${PROBLEM}/context/2026-09-12-alternative-rh-reformulations.md`}>{t('Four reformulations and falsifiable questions', 'Cuatro reformulaciones y preguntas refutables')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PROBLEM}/context/2026-09-12-spectral-optimization-alternatives.md`}>{t('Spectral and positivity barriers', 'Barreras espectrales y de positividad')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PROBLEM}/context/2026-09-12-pressure-frame-prior-art.md`}>{t('Pressure and frame prior-art audit', 'Auditoría de antecedentes sobre presión y marcos')}</SourceLink></div>
        <div className="rh-source-links"><SourceLink href={`${REPO}/tree/main/${PROBLEM}/context`}>{t('Read the source audits', 'Leer las auditorías de fuentes')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PROBLEM}/context/source-manifest.json`}>{t('Versions, licenses and source hashes', 'Versiones, licencias y hashes de fuentes')}</SourceLink></div>
        <Refs label={refsLabel} ids={['riemann-anthropic2026', 'riemann-lamzouri2026', 'riemann-wang2026', 'riemann-axiom2026', 'riemann-formalmath2026', 'riemann-ainta2026', 'riemann-trmdy2026', 'riemann-tawanerguo2026', 'riemann-yuhangshi2026', 'riemann-pressure2026', 'riemann-karatsuba1985', 'riemann-parity2026']} />
      </section>,
    },
    {
      id: 'strategy', label: t('Strategy', 'Estrategia'), content: <section>
        <h2>{t('Keep the information lost at equality', 'Conservar la información perdida en la igualdad')}</h2>
        <p>{t('A normalized even density determines vectors for the zeros and a finite self-adjoint operator A. Its trace is the total multiplicity N; its squared Hilbert–Schmidt norm is Q. The simple real atoms form a positive operator with Gram matrix G. The residual operator includes signed off-line conjugate pairs, so replacing the complex pair sum by a sum of absolute squares would change the mathematics.', 'Una densidad par normalizada determina vectores para los ceros y un operador autoadjunto finito A. Su traza es la multiplicidad total N; el cuadrado de su norma de Hilbert–Schmidt es Q. Los átomos reales simples forman un operador positivo con matriz de Gram G. El operador residual incluye pares conjugados con signo fuera de la recta, de modo que reemplazar la suma compleja por una suma de módulos al cuadrado cambiaría la matemática.')}</p>
        <Equation tex={String.raw`S\ge2N-Q+D(G),\qquad D(G)=\operatorname{tr}\Psi(G),\qquad \Psi(t)=\begin{cases}(t-1)^2&0\le t\le2,\\2t-3&t\ge2.\end{cases}`}
          caption={t('S is the simple-critical count. G is positive semidefinite with unit diagonal. Ψ measures the spectral defect; the stability mechanism is inherited from ainta and transferred to Lamzouri’s finite operator.', 'S es el conteo de ceros críticos simples. G es semidefinida positiva con diagonal unitaria. Ψ mide el defecto espectral; el mecanismo de estabilidad proviene de ainta y se transfiere al operador finito de Lamzouri.')} />
        <p>{t('The stable inequality is inherited from ainta; the exact finite operator is due to Lamzouri.', 'La desigualdad estable proviene de ainta; el operador finito exacto se debe a Lamzouri.')} <Cite id="riemann-ainta2026" /> <Cite id="riemann-lamzouri2026" /></p>
        <Equation tex={String.raw`2N^d\ge3N-Q+D(G),\qquad E(B)=\operatorname{tr}(B-I)^2,\qquad D(B)\ge\min\{1,E(B)\}`}
          caption={t('The distinct-zero companion uses this separate finite inequality, valid with all multiplicities retained. The spectral energy cap applies to any positive semidefinite unit-diagonal block B.', 'La cota complementaria de ceros distintos usa esta desigualdad finita separada, válida conservando todas las multiplicidades. La cota espectral de energía se aplica a cualquier bloque B semidefinido positivo con diagonal unitaria.')} />
        <h2>{t('Parity branch: keep the multiplicity excess', 'Vía de paridad: conservar el exceso de multiplicidad')}</h2>
        <p>{t('Let O count distinct odd-multiplicity critical points, r multiple critical points, b off-line conjugate pairs and Z = Nᵈ all distinct complex points. The excess Eₘ = N − S − 2r − 2b is nonnegative. Here Eₘ is a multiplicity count, distinct from the matrix energy E(B). Put D = D(G) and σ = Q − (4N − 3S − 4r − 4b + D) ≥ 0 using the inherited stable inequality. Each possible support atom makes a nonnegative contribution to S + Eₘ − O.', 'Sea O el conteo de puntos críticos distintos de multiplicidad impar, r el de puntos críticos múltiples, b el de pares conjugados fuera de la recta y Z = Nᵈ el de todos los puntos complejos distintos. El exceso Eₘ = N − S − 2r − 2b no es negativo. Aquí Eₘ es un conteo de multiplicidad, distinto de la energía matricial E(B). Se define D = D(G) y σ = Q − (4N − 3S − 4r − 4b + D) ≥ 0 usando la desigualdad estable heredada. Cada tipo posible de átomo aporta una cantidad no negativa a S + Eₘ − O.')}</p>
        <div className="rs-scroll"><table className="rs-table">
          <thead><tr><th>{t('Support atom', 'Átomo del soporte')}</th><th>{t('Contribution to S + Eₘ − O', 'Contribución a S + Eₘ − O')}</th></tr></thead>
          <tbody>
            <tr><td>{t('Simple critical point', 'Punto crítico simple')}</td><td>0</td></tr>
            <tr><td>{t('Critical point, even multiplicity m ≥ 2', 'Punto crítico, multiplicidad par m ≥ 2')}</td><td>m − 2 ≥ 0</td></tr>
            <tr><td>{t('Critical point, odd multiplicity m ≥ 3', 'Punto crítico, multiplicidad impar m ≥ 3')}</td><td>m − 3 ≥ 0</td></tr>
            <tr><td>{t('Off-line pair, multiplicity m ≥ 1 at each point', 'Par fuera de la recta, multiplicidad m ≥ 1 en cada punto')}</td><td>2(m − 1) ≥ 0</td></tr>
          </tbody>
        </table></div>
        <Equation tex={String.raw`3S-(2N-Q+2O+D)=2(S+E_m-O)+\sigma\ge0`} />
        <Equation tex={String.raw`6Z-(7N-2Q+O+2D)=(S+E_m-O)+6b+2\sigma\ge0`}
          caption={t('These identities are universal in multiplicity. The finite census checks transcription; it does not supply the universal proof. The two formulas retain different information, which is why the distinct consequence must be derived separately.', 'Estas identidades son universales respecto de la multiplicidad. El censo finito comprueba la transcripción; no aporta la prueba universal. Las dos fórmulas conservan información diferente, por lo que la consecuencia de ceros distintos debe derivarse por separado.')} />
        <h2>{t('Import one fixed odd-zero seed', 'Importar una densidad inicial fija de ceros impares')}</h2>
        <p>{t('Use Selberg’s theorem as restated in Karatsuba, Theorem B, printed page 523; the distinct sign-change convention is checked on page 536. Fix α = 51/100. There are constants a > 0 and a sufficiently large starting height such that each seed interval (t, t + t^α] has at least a t^α log t distinct odd-order critical zeros. Pack disjoint seed intervals into (T, T + T^θ] for each fixed θ > α. The uncovered tail is O(T^α) = o(T^θ), so a fixed κ > 0 gives liminf O/N ≥ κ. This does not assume those odd zeros are simple.', 'Se usa el teorema de Selberg reformulado en Karatsuba, Teorema B, página impresa 523; la convención de cambios de signo distintos se verifica en la página 536. Se fija α = 51/100. Existen constantes a > 0 y una altura inicial suficientemente grande tales que cada intervalo inicial (t, t + t^α] contiene al menos a t^α log t ceros críticos distintos de orden impar. Se agrupan intervalos iniciales disjuntos dentro de (T, T + T^θ] para cada θ fijo mayor que α. La cola no cubierta es O(T^α) = o(T^θ), de modo que un κ > 0 fijo da liminf O/N ≥ κ. Esto no supone que esos ceros impares sean simples.')} <Cite id="riemann-karatsuba1985" /></p>
        <p>{t('Wang’s fixed-test pair estimate remains valid on either side of the cosine root. Normalize by N ∼ T^θ log T/(2π), first take T → ∞ for each fixed smooth density with support λ < θ, then approximate the cosine profile and take λ ↑ θ. The exact deweighting Q = W(g) − W(g″)/(4 log²T), with g = f * f, uses two fixed tests and gives Q/N → 2 − c(θ). Dropping the nonnegative Gram defect yields the two bounds below.', 'La estimación de pares de Wang con prueba fija sigue siendo válida a ambos lados de la raíz coseno. Se normaliza por N ∼ T^θ log T/(2π), primero se toma T → ∞ para cada densidad suave fija con soporte λ < θ, después se aproxima el perfil coseno y se toma λ ↑ θ. La eliminación exacta del peso Q = W(g) − W(g″)/(4 log²T), con g = f * f, usa dos pruebas fijas y da Q/N → 2 − c(θ). Descartar el defecto de Gram no negativo produce las dos cotas siguientes.')} <Cite id="riemann-wang2026" /></p>
        <Equation tex={String.raw`\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}\ge\max\left\{0,c(\theta),\frac{c(\theta)+2\kappa}{3}\right\},\qquad \frac{51}{100}<\theta<1`} />
        <Equation tex={String.raw`\liminf_{T\to\infty}\frac{Z(T,T^\theta)}{N(T,T^\theta)}\ge\max\left\{\kappa,\frac{1+c(\theta)}2,\frac{3+2c(\theta)+\kappa}{6}\right\}`}
          caption={t('All exponents are fixed. The distinct formula combines Z ≥ O with its two finite stability inequalities. It is not (1 + the parity simple bound)/2.', 'Todos los exponentes son fijos. La fórmula de ceros distintos combina Z ≥ O con sus dos desigualdades finitas de estabilidad. No es (1 + la cota simple de paridad)/2.')} />
        <h2>{t('Cross the old positivity root without inventing a decimal', 'Cruzar la antigua raíz de positividad sin inventar un decimal')}</h2>
        <Equation tex={String.raw`c(51/100)\le-\frac{1801}{20400}<0,\qquad 0<c'(\theta)<\frac{10000}{2601}<4\quad(\alpha\le\theta\le\theta_0)`} />
        <p>{t('The exact definition c(θ₀) = 0 and the derivative bound give c(θ₀ − δ) > −4δ. With δ = min((θ₀ − α)/2, κ/4), one has α < θ₁ = θ₀ − δ < θ₀ and c(θ₁) > −κ. Hence the simple-critical lower density is at least κ/3 for every fixed θ ≥ θ₁ below one. At θ₀ itself the bound is at least 2κ/3. No numerical evaluation of κ or θ₁ is needed for this existence theorem, and none was certified.', 'La definición exacta c(θ₀) = 0 y la cota de la derivada dan c(θ₀ − δ) > −4δ. Con δ = min((θ₀ − α)/2, κ/4), se tiene α < θ₁ = θ₀ − δ < θ₀ y c(θ₁) > −κ. Por tanto, la densidad inferior de ceros críticos simples es al menos κ/3 para cada θ fijo mayor o igual que θ₁ y menor que uno. En θ₀ la cota es al menos 2κ/3. Este teorema de existencia no necesita evaluar numéricamente κ o θ₁, y no se certificó ninguno de esos valores.')}</p>
        <Equation tex={String.raw`\theta_{\rm half}=\theta_0-\min\left\{\frac{\theta_0-\alpha}{2},\frac{\kappa}{16}\right\},\qquad \theta\in[\theta_{\rm half},1)\ \Longrightarrow\ \liminf\frac ZN\ge\frac12+\frac{\kappa}{12}`}
          caption={t('This distinct-above-one-half consequence follows from its separate formula. It is not a new threshold for merely positive distinct density, which is known on substantially shorter classical intervals. θ_half remains unquantified.', 'Esta consecuencia de ceros distintos por encima de un medio se sigue de su fórmula separada. No es un nuevo umbral para densidad distinta meramente positiva, conocida en intervalos clásicos considerablemente más cortos. θ_half sigue sin cuantificar.')} />
        <div className="rh-source-links"><SourceLink href={PARITY_PROOF}>{t('Complete parity proof and limit accounting', 'Prueba completa de paridad y contabilidad de límites')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PARITY_EXP}/adversarial-audit.md`}>{t('Parity adversarial review', 'Revisión adversarial de paridad')}</SourceLink></div>
        <h2>{t('Quantitative branch: pressure on odd frames', 'Vía cuantitativa: presión en marcos impares')}</h2>
        <ProofDiagram kind="pressure" />
        <h2>{t('Turn three gaps into a positive defect', 'Convertir tres separaciones en un defecto positivo')}</h2>
        <p>{t('For the cosine density, let kθ be its real Fourier transform. Its zero equation is incompatible with three positive arguments u, v and u + v all being roots. Consequently the doubled three-point energy has a strictly positive minimum on any fixed compact gap triangle. The proof gives an explicit conservative analytic bound, while interval arithmetic gives a stronger numerical bound for the recorded example.', 'Para la densidad coseno, sea kθ su transformada de Fourier real. Su ecuación de ceros es incompatible con que tres argumentos positivos u, v y u + v sean raíces simultáneas. Por tanto, la energía duplicada de tres puntos tiene un mínimo estrictamente positivo en cualquier triángulo compacto fijo de separaciones. La prueba da una cota analítica explícita conservadora, mientras que la aritmética de intervalos da una cota numérica más fuerte para el ejemplo registrado.')}</p>
        <Equation tex={String.raw`f_\theta(t)=\frac{\cos(\sqrt2t)}{\sqrt2\sin(\theta/\sqrt2)}\mathbf1_{|t|\le\theta/2},\quad k_\theta=\widehat f_\theta,\quad 2\bigl(k_\theta(u)^2+k_\theta(v)^2+k_\theta(u+v)^2\bigr)\ge d`}
          caption={t('The Fourier convention is kθ(x) = ∫fθ(t)e^(−2πixt)dt. The bound applies to u, v ≥ 0 and u + v ≤ R, with 0 < d ≤ 1.', 'La convención de Fourier es kθ(x) = ∫fθ(t)e^(−2πixt)dt. La cota vale para u, v ≥ 0 y u + v ≤ R, con 0 < d ≤ 1.')} />
        <TriangleDiagram />
        <h2>{t('Replace a cutoff loss with pressure', 'Reemplazar la pérdida por corte con presión')}</h2>
        <p>{t('Write E₃ for the doubled three-point energy. EXP-003 requires an inequality for all nonnegative gaps. Stage A obtains it immediately from the earlier compact floor: ε = d and p = d/R. Stage B certifies a new rational pair p, ε directly. Once u + v reaches ε/p, nonnegative energy and the pressure term suffice; only the closed triangle below that cutoff needs an interval certificate.', 'Sea E₃ la energía duplicada de tres puntos. EXP-003 exige una desigualdad para todas las separaciones no negativas. La etapa A la obtiene directamente de la cota compacta anterior: ε = d y p = d/R. La etapa B certifica directamente un nuevo par racional p, ε. Cuando u + v alcanza ε/p, bastan la energía no negativa y el término de presión; solo el triángulo cerrado bajo ese corte necesita un certificado de intervalos.')}</p>
        <Equation tex={String.raw`E_3(u,v)+p(u+v)\ge\epsilon\quad(u,v\ge0),\qquad R_{\rm cut}=\epsilon/p,\qquad M=2k+1,\quad k\epsilon\le1`}
          caption={t('The word pressure denotes a linear penalty for normalized span. It is a finite geometric inequality, not a new prime-correlation assumption.', 'La palabra presión designa una penalización lineal de la extensión normalizada. Es una desigualdad geométrica finita, no un nuevo supuesto de correlación de primos.')} />
        <h2>{t('Add pair energies inside an odd frame', 'Sumar energías de pares dentro de un marco impar')}</h2>
        <OddFrameDiagram />
        <p>{t('Within M = 2k + 1 ordered points, select triples starting at indices 1, 3, …, 2k − 1. They share endpoints but no unordered pair, so their nonnegative pair energies fit inside the full frame energy. Their spans telescope to the frame span L_F. The unit cap kε ≤ 1 then converts the energy inequality to the spectral defect inequality.', 'Dentro de M = 2k + 1 puntos ordenados se seleccionan ternas que empiezan en los índices 1, 3, …, 2k − 1. Comparten extremos, pero ningún par no ordenado, por lo que sus energías no negativas de pares caben en la energía del marco completo. Sus extensiones se suman telescópicamente a la extensión L_F del marco. La condición kε ≤ 1 convierte entonces la desigualdad de energía en la desigualdad de defecto espectral.')}</p>
        <Equation tex={String.raw`E(G_F)+pL_F\ge k\epsilon\quad\Longrightarrow\quad D(G_F)+pL_F\ge k\epsilon`}
          caption={t('The implication follows from D ≥ min(1, E). It does not add the defects of overlapping triples.', 'La implicación se sigue de D ≥ min(1, E). No suma los defectos de ternas que se superponen.')} />
        <h2>{t('Average disjoint full frames, keeping the boundary', 'Promediar marcos completos disjuntos, conservando la frontera')}</h2>
        <p>{t('Partition frame starts by their residue modulo M and fill leftover points with singleton blocks. Convex trace pinching applies inside each of these M disjoint partitions. Across all offsets, there are (S − M + 1)₊ complete frames. Every adjacent gap occurs in at most M − 1 frame spans. Averaging gives the inequality below; it also holds when S < M because the right side is then nonpositive.', 'Se particionan los inicios de marcos según su residuo módulo M y se completan los puntos sobrantes con bloques unitarios. La compresión convexa de la traza se aplica dentro de cada una de estas M particiones disjuntas. Entre todos los desplazamientos hay (S − M + 1)₊ marcos completos. Cada separación adyacente aparece en a lo más M − 1 extensiones de marcos. El promedio da la desigualdad siguiente; también vale cuando S < M porque entonces el lado derecho no es positivo.')}</p>
        <Equation tex={String.raw`D(G)\ge\alpha(S-M+1)-\beta L,\qquad \alpha=\frac{k\epsilon}{M},\quad\beta=\frac{2kp}{M}`}
          caption={t('L is the actual normalized span, bounded by X_T = T^θ log(T)/(2π). Only X_T/N → 1 is used; L/N need not tend to one. The fixed boundary cost vanishes after division by N.', 'L es la extensión normalizada real, acotada por X_T = T^θ log(T)/(2π). Solo se usa X_T/N → 1; L/N no tiene por qué tender a uno. El costo fijo de la frontera desaparece al dividir por N.')} />
        <Equation tex={String.raw`c_{\rm odd}=\frac{Mc-2kp}{M-k\epsilon}=c+\frac{k(\epsilon c-2p)}{M-k\epsilon},\qquad \liminf\frac{N^d}{N}\ge\frac{1+c_{\rm odd}}2`}
          caption={t('The improvement is strict when εc > 2p. The distinct companion follows by inserting the simple-critical lower bound into its own finite stability inequality; the tempting general bound Nᵈ ≥ (N + S)/2 is false at high multiplicity.', 'La mejora es estricta cuando εc > 2p. La cota de ceros distintos se obtiene al insertar la cota de ceros críticos simples en su propia desigualdad finita de estabilidad; la tentadora cota general Nᵈ ≥ (N + S)/2 es falsa con multiplicidades altas.')} />
        <h2>{t('Strengthen every positive point of the curve', 'Reforzar cada punto positivo de la curva')}</h2>
        <p>{t('Reuse the explicit analytic d from EXP-002, which is positive and less than 1/4, and choose R > 2/c. Thus k = 2 is always admissible. The identity below proves a strictly larger gain than EXP-002 for every fixed θ above the same positivity threshold. Larger admissible k strengthen this unit-cap family further; they do not lower the positivity threshold.', 'Se reutiliza el d analítico explícito de EXP-002, positivo y menor que 1/4, y se elige R > 2/c. Así, k = 2 siempre es admisible. La identidad siguiente prueba una ganancia estrictamente mayor que EXP-002 para cada θ fijo por encima del mismo umbral de positividad. Valores mayores admisibles de k refuerzan esta familia con cota unitaria; no reducen el umbral de positividad.')}</p>
        <Equation tex={String.raw`c_A=c+\frac{kd(c-2/R)}{2k+1-kd},\qquad \frac{kd}{2k+1-kd}-\frac d{3-d}=\frac{d(k-1)}{(2k+1-kd)(3-d)}>0\quad(k>1)`} />
        <p><SourceLink href={PROOF}>{t('Earlier analytic energy bound and first proof', 'Cota analítica de energía anterior y primera prueba')}</SourceLink>{' · '}<SourceLink href={`${PRESSURE_PROOF}#7-reusing-a-compact-certificate-and-strengthening-the-entire-curve`}>{t('Complete analytic whole-curve derivation', 'Derivación analítica completa para toda la curva')}</SourceLink></p>
        <h2>{t('Respect the support and the order of limits', 'Respetar el soporte y el orden de los límites')}</h2>
        <p>{t('Fix λ < θ and a smooth normalized nonnegative density f = η². Wang gives Q/N → C(f), with normalized error O_f(1/log T + T^(λ−θ) log T). Take the height limit with f fixed. Next approximate the cosine density in L¹ and L² using smooth supports rising to θ. The three-point energies differ by at most 12‖f − fθ‖₁ uniformly in all real gaps. Therefore each ε′ < ε survives with the same p and fixed k. The final outer limit ε′ ↑ ε reaches the full certificate, including kε = 1. A smoothing scale depending on T is not used.', 'Se fija λ < θ y una densidad suave normalizada no negativa f = η². Wang da Q/N → C(f), con error normalizado O_f(1/log T + T^(λ−θ) log T). Se toma el límite en altura con f fija. Después se aproxima la densidad coseno en L¹ y L² mediante soportes suaves que suben hacia θ. Las energías de tres puntos difieren a lo más en 12‖f − fθ‖₁ uniformemente para todas las separaciones reales. Por tanto, cada ε′ < ε se conserva con el mismo p y k fijo. El límite exterior final ε′ ↑ ε alcanza el certificado completo, incluso cuando kε = 1. No se usa una escala de suavizado dependiente de T.')}</p>
        <p>{t('The required fixed-support estimate is the short-interval input from Wang.', 'La estimación requerida con soporte fijo es la entrada para intervalos cortos de Wang.')} <Cite id="riemann-wang2026" /></p>
        <Callout variant="honest" title={t('Assumptions and failure checks', 'Supuestos y controles de fallo')}>
          {t('The exponent and frame size are fixed before the height limit. The audit checked signed nonreal contributions, multiplicities, spectral zero padding, pair-disjoint incidence, the M − 1 span capacity, incomplete frames, the cap endpoint and smoothing. No uniform improvement at the positivity threshold, effective height or extension beyond the cited Fourier support follows.', 'El exponente y el tamaño del marco se fijan antes del límite en altura. La auditoría revisó contribuciones no reales con signo, multiplicidades, ceros añadidos al espectro, incidencia sin pares repetidos, capacidad M − 1 de las extensiones, marcos incompletos, extremo de la cota y suavizado. No se obtiene una mejora uniforme en el umbral de positividad, una altura efectiva ni una extensión más allá del soporte de Fourier citado.')}
        </Callout>
        <SourceLink href={`${REPO}/blob/main/${PRESSURE_EXP}/adversarial-audit.md`}>{t('Read the EXP-003 adversarial proof review', 'Leer la revisión adversarial de la prueba de EXP-003')}</SourceLink>
        <Refs label={refsLabel} ids={['riemann-lamzouri2026', 'riemann-ainta2026', 'riemann-wang2026', 'riemann-trmdy2026', 'riemann-tawanerguo2026', 'riemann-yuhangshi2026', 'riemann-pressure2026']} />
      </section>,
    },
    {
      id: 'results', label: t('Experiments & results', 'Experimentos y resultados'), content: <section>
        <h2>{t('Read the experiment records', 'Leer los registros experimentales')}</h2>
        <p>{t('EXP-001 audits source constants and normalization. EXP-002 proves the first short-interval refinement and certifies its compact three-point example. EXP-003 proves the odd-frame pressure theorem: Stage A reuses that certificate, and Stage B certifies a stronger all-gap inequality. EXP-004 combines the finite multiplicity accounting with a classical odd-zero seed and Wang’s fixed-test transfer to extend positive simple-critical density below the cosine root. Open a record to read its original declaration, verbatim verdict, artifacts and source history. The records retain their original language.', 'EXP-001 audita constantes y normalización. EXP-002 prueba el primer refinamiento en intervalos cortos y certifica su ejemplo compacto de tres puntos. EXP-003 prueba el teorema de presión con marcos impares: la etapa A reutiliza ese certificado y la etapa B certifica una desigualdad más fuerte para toda separación. EXP-004 combina la contabilidad finita de multiplicidades con una densidad clásica de ceros impares y la transferencia con prueba fija de Wang para extender la densidad positiva de ceros críticos simples bajo la raíz coseno. Abra un registro para leer su declaración original, veredicto literal, artefactos e historia. Los registros conservan su idioma original.')}</p>
        <ul className="rh-experiments">{exps.map((e) => <li key={e.slug}><button className="rs-exp-open" onClick={() => setOpen(e)}>EXP-{e.id}: {e.id === '001' ? t('Source and constant audit', 'Auditoría de fuentes y constantes') : e.id === '002' ? t('Short-interval stability refinement', 'Refinamiento por estabilidad en intervalos cortos') : e.id === '003' ? t('Odd-frame pressure refinement', 'Refinamiento por presión con marcos impares') : t('Parity density transfer', 'Transferencia de densidad por paridad')}</button><span className="rs-badge state">{e.verdict || t('Record available', 'Registro disponible')}</span></li>)}</ul>
        {(recordsError || !exps.length) && <p>{t('Experiment records are currently unavailable in the viewer.', 'Los registros experimentales no están disponibles actualmente en el visor.')} <SourceLink href={`${REPO}/tree/main/${PROBLEM}/experiments`}>{t('Open the source records', 'Abrir los registros originales')}</SourceLink></p>}
        {resultTable}
        <p>{t('The baseline is Wang’s short-interval theorem. EXP-003 derives numerical simple-critical and distinct-zero refinements at θ = 3/4. EXP-004 derives a qualitative fixed-exponent interval-range extension; its κ and new exponent remain symbolic.', 'La cota base es el teorema de Wang en intervalos cortos. EXP-003 deriva refinamientos numéricos de ceros críticos simples y de ceros distintos para θ = 3/4. EXP-004 deriva una extensión cualitativa del rango para exponentes fijos; κ y el nuevo exponente permanecen simbólicos.')} <Cite id="riemann-wang2026" /> <Cite id="riemann-pressure2026" /> <Cite id="riemann-parity2026" /></p>
        <Equation tex={String.raw`\liminf_{T\to\infty}\frac{N^d(T,T^\theta)}{N(T,T^\theta)}\ge\frac{1+c_*(\theta)}2`}
          caption={t('Nᵈ counts each distinct nontrivial zero once, regardless of multiplicity or position in the strip. This companion bound has the same fixed-exponent and asymptotic scope.', 'Nᵈ cuenta cada cero no trivial distinto una sola vez, sin importar su multiplicidad o ubicación en la franja. Esta cota complementaria tiene el mismo alcance asintótico y de exponente fijo.')} />
        {winner && <p className="rh-number">{t('Stage B distinct-zero companion: ', 'Cota complementaria de ceros distintos de la etapa B: ')}<strong>{center(winner.distinct.display)}</strong></p>}
        <h2>{t('Stage A: reuse the first certificate', 'Etapa A: reutilizar el primer certificado')}</h2>
        {stageA && <>
          <p className="rh-parameters">θ = {stageA.theta} · R = {stageA.radius} · d = {stageA.delta}<br />k = {stageA.k} · M = {stageA.frame_size}</p>
          <p>{t('The same compact energy floor now enters the odd-frame theorem. The exact ratio between this gain and the first release’s gain is ', 'La misma cota compacta de energía entra ahora en el teorema de marcos impares. La razón exacta entre esta ganancia y la de la primera versión es ')}<strong>{stageA.gain_ratio_to_exp002}</strong>{t('. It compares gains above Wang, not the complete proportions. The finite audit checks pair incidence, telescoping spans, every offset and incomplete frames.', '. Compara ganancias sobre Wang, no las proporciones completas. La auditoría finita verifica incidencia de pares, extensiones telescópicas, cada desplazamiento y marcos incompletos.')}</p>
          <dl className="rh-audit-grid">
            <div><dt>{t('Exact index cases', 'Casos exactos de índices')}</dt><dd>{stageA.invariants.index_cases}</dd></div>
            <div><dt>{t('Symbolic identities', 'Identidades simbólicas')}</dt><dd>{stageA.invariants.symbolic_identities}</dd></div>
            <div><dt>{t('Replayed nodes', 'Nodos reproducidos')}</dt><dd>{stageA.replay.nodes.toLocaleString(t('en-US', 'es-CL'))}</dd></div>
            <div><dt>{t('Replay precision', 'Precisión de reproducción')}</dt><dd>{stageA.replay.precision_bits} bits</dd></div>
          </dl>
        </>}
        <h2>{t('Stage B: certify energy plus pressure', 'Etapa B: certificar energía más presión')}</h2>
        <p>{t('A floating-point design pass proposed rational candidates; it is not certificate evidence. The frozen candidate list was then checked in its declared order. Candidate 1 passed the all-gap inequality and the strict gain target. Candidates 2 and 3 were not run after this success. They are neither confirmed nor refuted.', 'Una exploración de coma flotante propuso candidatos racionales; no es evidencia de certificación. La lista fijada de candidatos se revisó después en el orden declarado. El candidato 1 satisfizo la desigualdad para toda separación y la meta estricta de ganancia. Los candidatos 2 y 3 no se ejecutaron tras ese éxito. No están confirmados ni refutados.')}</p>
        {data?.pressure_result && <div className="rs-scroll"><table className="rs-table">
          <thead><tr><th>{t('Frozen candidate', 'Candidato fijado')}</th><th>{t('Recorded outcome', 'Resultado registrado')}</th></tr></thead>
          <tbody>{data.pressure_result.stage_b.outcomes.map((o) => <tr key={o.candidate}><td>{o.candidate}</td><td>{o.status === 'arithmetic_verified' ? t('Arithmetic verified', 'Aritmética verificada') : o.status === 'not_run_after_higher_ranked_success' ? t('Not run after earlier success', 'No ejecutado tras el éxito anterior') : o.status === 'refuted_by_exact_witness' ? t('Refuted by exact witness', 'Refutado por testigo exacto') : o.status === 'rejected_gain_gate' ? t('Gain target not met', 'Meta de ganancia no satisfecha') : t('Inconclusive', 'Inconcluso')}</td></tr>)}</tbody>
        </table></div>}
        {winner ? <>
          <p className="rh-parameters">p = {winner.pressure} · ε = {winner.epsilon}<br />R<sub>cut</sub> = {winner.cutoff} · k = {winner.k} · M = {winner.frame_size}</p>
          <p>{t('Every cell is accepted only if an outward-rounded bound proves energy plus pressure throughout it, or if pressure alone suffices. The exact cutoff ε/p also proves the inequality for all larger spans. Complete tree coverage and exact rational boundaries leave no unresolved cells. Construction used 160-bit Arb arithmetic; the persisted replay uses the precision below.', 'Cada celda solo se acepta si una cota con redondeo hacia afuera prueba energía más presión en toda ella, o si la presión por sí sola basta. El corte exacto ε/p también prueba la desigualdad para todas las extensiones mayores. La cobertura completa del árbol y las fronteras racionales exactas no dejan celdas sin resolver. La construcción usó aritmética Arb de 160 bits; la reproducción persistida usa la precisión indicada abajo.')}</p>
          <dl className="rh-audit-grid">
            <div><dt>{t('Partition nodes', 'Nodos de la partición')}</dt><dd>{winner.audit.nodes.toLocaleString(t('en-US', 'es-CL'))}</dd></div>
            <div><dt>{t('Energy + pressure leaves', 'Hojas de energía + presión')}</dt><dd>{winner.audit.validated_leaves.toLocaleString(t('en-US', 'es-CL'))}</dd></div>
            <div><dt>{t('Pressure-only leaves', 'Hojas de solo presión')}</dt><dd>{winner.audit.pressure_leaves}</dd></div>
            <div><dt>{t('Replay precision', 'Precisión de reproducción')}</dt><dd>{winner.audit.precision_bits} bits</dd></div>
          </dl>
          <p className="rh-number">{t('Strict gain check, gB − (5/4)gA: ', 'Control estricto de ganancia, gB − (5/4)gA: ')}{center(winner.strict_gain_gate.display)} &gt; 0</p>
          <details className="rh-details"><summary>{t('Inspect exact Stage A and B enclosures', 'Examinar intervalos exactos de las etapas A y B')}</summary>
            {[
              [t('Stage A simple-critical bound', 'Cota de ceros críticos simples de la etapa A'), stageA?.improved],
              [t('Stage A gain', 'Ganancia de la etapa A'), stageA?.gain],
              [t('Stage B simple-critical bound', 'Cota de ceros críticos simples de la etapa B'), winner.improved],
              [t('Stage B distinct-zero bound', 'Cota de ceros distintos de la etapa B'), winner.distinct],
              [t('Stage B gain', 'Ganancia de la etapa B'), winner.gain],
              [t('Strict gain target margin', 'Margen de la meta estricta de ganancia'), winner.strict_gain_gate],
            ].map(([label, bound]) => typeof label === 'string' && bound && typeof bound !== 'string' ? <div key={label}><h3>{label}</h3><p className="rh-hash">{bound.lower} ≤ x ≤ {bound.upper}</p></div> : null)}
          </details>
          <p>{t('Certificate canonical SHA-256 (sorted compact JSON plus LF):', 'SHA-256 canónico del certificado (JSON compacto ordenado más LF):')}</p><p className="rh-hash">{winner.certificate_sha256}</p>
          <p>{t('This canonical digest differs from the saved file’s byte hash. The provenance panel below records byte hashes tied to source commits.', 'Este resumen canónico difiere del hash de bytes del archivo guardado. El panel de procedencia inferior registra hashes de bytes ligados a commits de fuente.')}</p>
        </> : <p role="status">{t('A fully replayed pressure winner is not available in the loaded record; consult the source verdict before using a numerical claim.', 'El registro cargado no contiene un candidato ganador de presión completamente reproducido; consulte el veredicto original antes de usar una afirmación numérica.')}</p>}
        <div className="rh-source-links"><SourceLink href={PRESSURE_PROOF}>{t('Complete pressure theorem', 'Teorema completo de presión')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PRESSURE_EXP}/verdict.md`}>{t('Confirmed EXP-003 verdict', 'Veredicto confirmado de EXP-003')}</SourceLink><SourceLink href={REPLAY_GUIDE}>{t('Source-bound replay instructions', 'Instrucciones de reproducción ligadas a las fuentes')}</SourceLink></div>
        <h2>{t('Preserved EXP-002 compact certificate', 'Certificado compacto de EXP-002 conservado')}</h2>
        <p>{t('The certificate encodes a complete binary subdivision of a square containing the closed gap triangle. A cell is accepted only when an outward-rounded energy bound certifies the entire rectangle; it is excluded only when its lower coordinates place it strictly outside the triangle. Exact rational coordinates preserve coverage and the boundary. A Lipschitz bound controls the variation between each center evaluation and every point in its cell.', 'El certificado codifica una subdivisión binaria completa de un cuadrado que contiene el triángulo cerrado de separaciones. Una celda solo se acepta cuando una cota de energía con redondeo hacia afuera certifica todo el rectángulo; solo se excluye cuando sus coordenadas inferiores la sitúan estrictamente fuera del triángulo. Las coordenadas racionales exactas conservan la cobertura y la frontera. Una cota de Lipschitz controla la variación entre la evaluación central y todos los puntos de la celda.')}</p>
        {result && <dl className="rh-audit-grid">
          <div><dt>{t('Partition nodes', 'Nodos de la partición')}</dt><dd>{result.audit.nodes.toLocaleString(t('en-US', 'es-CL'))}</dd></div>
          <div><dt>{t('Certified energy leaves', 'Hojas de energía certificadas')}</dt><dd>{result.audit.energy_leaves.toLocaleString(t('en-US', 'es-CL'))}</dd></div>
          <div><dt>{t('Excluded outside leaves', 'Hojas exteriores excluidas')}</dt><dd>{result.audit.outside_leaves.toLocaleString(t('en-US', 'es-CL'))}</dd></div>
          <div><dt>{t('Replay precision', 'Precisión de la reproducción')}</dt><dd>{result.audit.precision_bits} bits</dd></div>
        </dl>}
        <p>{t('A second kernel evaluator replays every accepted leaf using a sinc Taylor expansion with a rigorous remainder. This is a meaningful arithmetic cross-check, but it shares Arb, the partition reconstruction, and the geometric bound with the first route. It is not a separately implemented full verifier or an end-to-end Lean proof. Adversarial tests reject malformed trees, modified parameters, forged counts and hashes, invalid thresholds, and unresolved budget stops.', 'Un segundo evaluador del núcleo reproduce cada hoja aceptada usando una expansión de Taylor de sinc con resto riguroso. Es una comprobación aritmética adicional significativa, pero comparte Arb, la reconstrucción de la partición y la cota geométrica con la primera ruta. No es un verificador completo implementado por separado ni una prueba Lean de extremo a extremo. Las pruebas adversariales rechazan árboles malformados, parámetros modificados, conteos y hashes falsificados, umbrales inválidos y paradas por presupuesto sin resolver.')}</p>
        {result && <details className="rh-details"><summary>{t('Inspect the exact rational enclosures', 'Examinar los intervalos racionales exactos')}</summary>{(['baseline', 'improved', 'gain'] as const).map((key) => <div key={key}><h3>{key === 'baseline' ? t('Baseline', 'Cota base') : key === 'improved' ? t('Refinement', 'Refinamiento') : t('Gain', 'Ganancia')}</h3><p className="rh-number">{result[key].display}</p><dl><dt>{t('Lower endpoint', 'Extremo inferior')}</dt><dd className="rh-hash">{result[key].lower}</dd><dt>{t('Upper endpoint', 'Extremo superior')}</dt><dd className="rh-hash">{result[key].upper}</dd></dl></div>)}</details>}
        {data && <details className="rh-details"><summary>{t('Inspect source provenance and SHA-256 hashes', 'Examinar procedencia y hashes SHA-256')}</summary><p>{t('Each export reads a committed source version. These hashes describe its exact bytes, including the proof and finite certificate.', 'Cada exportación lee una versión comprometida de la fuente. Estos hashes describen sus bytes exactos, incluidas la prueba y el certificado finito.')}</p><ul>{data.provenance.map((p) => <li key={p.role}><SourceLink href={`${REPO}/blob/${p.source_commit}/${p.path}`}>{sourceRole(p.role)}</SourceLink><p className="rh-hash">SHA-256 {p.sha256}</p><p className="rh-hash">{t('Source commit', 'Commit de fuente')}: {p.source_commit}</p></li>)}</ul></details>}
        <div className="rh-source-links"><SourceLink href={`${REPO}/blob/main/${EXP}/run.py`}>{t('Reproduction runner', 'Programa de reproducción')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PROBLEM}/code/riemann_certificates.py`}>{t('Certificate checker', 'Verificador del certificado')}</SourceLink><SourceLink href={`${REPO}/blob/main/tests/test_riemann_certificates.py`}>{t('Adversarial tests', 'Pruebas adversariales')}</SourceLink><a href="/data/research/riemann.json" download>{t('Download the replay data', 'Descargar los datos de reproducción')}</a></div>
        <div className="rh-source-links"><SourceLink href={`${REPO}/blob/main/${PRESSURE_EXP}/run.py`}>{t('EXP-003 runner', 'Programa de EXP-003')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PROBLEM}/code/riemann_pressure.py`}>{t('Pressure checker and provenance gates', 'Verificador de presión y controles de procedencia')}</SourceLink><SourceLink href={`${REPO}/blob/main/tests/test_riemann_pressure.py`}>{t('Pressure adversarial tests', 'Pruebas adversariales de presión')}</SourceLink></div>
        <Callout variant="note" title={t('Reproduction boundary', 'Alcance de la reproducción')}>
          {t('The browser reads persisted results; it does not search for zeros or run the arithmetic proof. The offline runner uses pinned dependencies and an explicit output directory. A budget stop saves a checkpoint and cannot be reported as a certificate. CPU arithmetic was sufficient for this experiment.', 'El navegador lee resultados persistidos; no busca ceros ni ejecuta la prueba aritmética. El programa externo usa dependencias fijadas y un directorio de salida explícito. Una parada por presupuesto guarda un punto de control y no puede presentarse como certificado. La aritmética en CPU fue suficiente para este experimento.')}
        </Callout>
        <Refs label={refsLabel} ids={['riemann-refinement2026', 'riemann-pressure2026', 'riemann-wang2026']} />
      </section>,
    },
    {
      id: 'open', label: t('Open questions', 'Preguntas abiertas'), content: <section>
        <h2>{t('What remains to be established', 'Qué falta establecer')}</h2>
        <p>{t('The Riemann hypothesis remains the overarching open problem. The refinement gives a small strict gain inside a specified asymptotic counting problem. It does not place every zero on the line, prove all zeros simple, or determine a finite height beyond which the proportion holds. Those conclusions need additional mathematics.', 'La hipótesis de Riemann sigue siendo el problema abierto general. El refinamiento da una pequeña ganancia estricta dentro de un problema de conteo asintótico especificado. No sitúa todos los ceros en la recta, no demuestra que todos sean simples ni determina una altura finita a partir de la cual valga la proporción. Esas conclusiones requieren matemática adicional.')}</p>
        <ol className="rh-questions">
          <li><h3>{t('External proof and priority review', 'Revisión externa de la prueba y la prioridad')}</h3><p>{t('Can an independent specialist validate the transfer, the signed finite operator, and the nested limits? The reviewed sources contain the stability lemma and global geometric refinements; the candidate novelty is the short-interval consequence. Earlier or concurrent work could narrow that claim.', '¿Puede un especialista independiente validar la transferencia, el operador finito con signo y los límites anidados? Las fuentes revisadas contienen el lema de estabilidad y refinamientos geométricos globales; la novedad candidata es la consecuencia en intervalos cortos. Trabajos anteriores o simultáneos podrían reducir ese alcance.')}</p></li>
          <li><h3>{t('A useful improvement near the threshold', 'Una mejora útil cerca del umbral')}</h3><p>{t('The analytic gain stays positive for each fixed admissible exponent but may become extremely small near the threshold. Improving the positivity exponent itself requires a mechanism beyond the present baseline-plus-defect argument.', 'La ganancia analítica permanece positiva para cada exponente fijo admisible, pero puede ser extremadamente pequeña cerca del umbral. Mejorar el propio exponente de positividad requiere un mecanismo adicional al argumento actual de cota base más defecto.')}</p></li>
          <li><h3>{t('Beyond the confirmed pressure family', 'Más allá de la familia de presión confirmada')}</h3><p>{t('EXP-003 now answers the odd-frame question and improves the recorded example. It does not optimize every finite configuration or every spectral envelope. A further declared experiment must identify an additional theorem or mechanism, and compare it against the known nonuniform-capacity and mixed-frame methods. The two unrun Stage B candidates carry no verdict.', 'EXP-003 responde ahora la pregunta de los marcos impares y mejora el ejemplo registrado. No optimiza todas las configuraciones finitas ni todas las cotas espectrales. Un nuevo experimento declarado debe identificar un teorema o mecanismo adicional y compararlo con los métodos conocidos de capacidad no uniforme y marcos mixtos. Los dos candidatos no ejecutados de la etapa B no tienen veredicto.')}</p></li>
          <li><h3>{t('A bridge to a different RH criterion', 'Un vínculo con otro criterio de RH')}</h3><p>{t('Can an approximation or positivity route yield a new uniform estimate rather than another finite pass? The source-preflight dossiers isolate a Nyman–Beurling approximation-and-tail objective, finite Weil witnesses, and the missing limits in spectral and heat-flow approaches. These are proposed questions with explicit failure conditions, not established advances toward RH.', '¿Puede una vía de aproximación o positividad dar una nueva estimación uniforme en vez de otra verificación finita? Los informes previos aíslan un objetivo de aproximación y control de colas de Nyman–Beurling, testigos finitos de Weil y los límites faltantes en los enfoques espectrales y de flujo de calor. Son preguntas propuestas con condiciones explícitas de fallo, no avances establecidos hacia RH.')}</p></li>
          <li><h3>{t('Effective heights and formalization', 'Alturas efectivas y formalización')}</h3><p>{t('Can the arithmetic and smoothing errors be made explicit enough to give a usable starting height? Can the complete analytic transfer and certificate checker be formalized, with all imported theorem scopes visible? Current exact arithmetic validates the finite energy claim and remains only one layer of that larger task.', '¿Pueden explicitarse los errores aritméticos y de suavizado lo suficiente para dar una altura inicial utilizable? ¿Pueden formalizarse la transferencia analítica completa y el verificador del certificado, mostrando el alcance de todos los teoremas importados? La aritmética exacta actual valida la afirmación finita de energía y sigue siendo solo una capa de esa tarea mayor.')}</p></li>
        </ol>
        <Callout variant="honest" title={t('Claim boundary', 'Límite de las afirmaciones')}>
          {t('Analytic derivation, finite machine verification, source review, and publication are separate evidence layers. A successful numerical certificate cannot repair a missing asymptotic estimate, and publication does not substitute for independent mathematical acceptance.', 'La derivación analítica, la verificación finita por máquina, la revisión de fuentes y la publicación son capas de evidencia separadas. Un certificado numérico exitoso no puede reparar una estimación asintótica faltante, y publicar no sustituye la aceptación matemática independiente.')}
        </Callout>
        <SourceLink href={`${REPO}/issues/262`}>{t('Follow the research issue and further work', 'Seguir el tema de investigación y los trabajos posteriores')}</SourceLink>
        <Refs label={refsLabel} ids={['riemann-refinement2026', 'riemann-wang2026', 'riemann-ainta2026', 'riemann-trmdy2026', 'riemann-axiom2026']} />
      </section>,
    },
  ];
  return <article className="page-body prose rh-page">
    <header className="rh-head">
      <div className="rh-title-row"><Link to="/">{t('Program board', 'Panel del programa')}</Link><span className="badge">{t('RH remains open', 'RH sigue abierta')}</span>{data && <span className="small muted">{t('Source review', 'Revisión de fuentes')}: {data.reviewed_on}</span>}</div>
      <h1>{t('Riemann zeta: zeros in short intervals', 'Zeta de Riemann: ceros en intervalos cortos')}</h1>
      <p className="muted">{t('A source review and a certified stability refinement for ', 'Una revisión de fuentes y un refinamiento certificado por estabilidad para ')}<InlineMath tex={String.raw`(T,T+T^\theta]`} />.</p>
      {(error || recordsError) && <button className="btn" onClick={() => setAttempt((value) => value + 1)}>{t('Retry loading the research data', 'Reintentar la carga de datos')}</button>}
    </header>
    <Tabs tabs={tabs} ariaLabel={t('Riemann research sections', 'Secciones de investigación de Riemann')} />
    <Suspense fallback={<p role="status">{t('Opening the experiment record…', 'Abriendo el registro experimental…')}</p>}>{open && <ExperimentModal exp={open} onClose={() => setOpen(null)} />}</Suspense>
  </article>;
}
