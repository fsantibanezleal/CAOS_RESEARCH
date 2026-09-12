import { Suspense, lazy, useEffect, useState, type ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { Callout, Cite, Equation, InlineMath, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, loadRiemann, type ExperimentRec, type RiemannData } from '../api/data';

const ExperimentModal = lazy(() => import('../components/ExperimentModal'));
const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = 'problems/number-theory/riemann-hypothesis';
const EXP = `${PROBLEM}/experiments/EXP-002-short-interval-stability`;
const PROOF = `${REPO}/blob/main/${EXP}/mathematical-proof.md`;
const PAPER = `${REPO}/blob/main/manuscripts/riemann-hypothesis/short-interval-stability/main.pdf`;
const DOI = 'https://doi.org/10.5281/zenodo.22727388';

function SourceLink({ href, children }: { href: string; children: ReactNode }) {
  return <a href={href} target="_blank" rel="noreferrer">{children}</a>;
}

// Formatting only: preserve the source's decimal center, including its exponent.
function center(display: string) {
  return display.replace(/^\[/, '').split(' +/- ')[0];
}

function ProofDiagram() {
  const t = useT();
  const [step, setStep] = useState(0);
  const stages = [
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
      title: t('Three-point geometry', 'Geometría de tres puntos'), formula: 'u ≥ 0, v ≥ 0, u + v ≤ R',
      detail: t('Three consecutive simple zeros supply gaps u, v and u + v. The cosine kernel cannot vanish at all three gaps. A complete interval partition certifies a positive energy floor on the compact triangle; a separate analytic estimate proves positivity for every fixed admissible exponent.', 'Tres ceros simples consecutivos aportan las separaciones u, v y u + v. El núcleo coseno no puede anularse en las tres separaciones. Una partición exhaustiva con aritmética de intervalos certifica un mínimo positivo de energía en el triángulo compacto; una estimación analítica separada prueba la positividad para cada exponente fijo admisible.'),
      href: `${REPO}/blob/main/${EXP}/artifacts/triangle-certificate.json`,
    },
    {
      title: t('Asymptotic refinement', 'Refinamiento asintótico'), formula: 'c* = (3c − 2d/R) / (3 − d)',
      detail: t('Average three disjoint partitions of consecutive triples, control the total span, then pass through the fixed-test limits. Choosing R > 2/c and d > 0 makes the improvement strict. The result gives a limiting proportion; it does not count zeros at a specified finite height.', 'Se promedian tres particiones disjuntas de ternas consecutivas, se controla la extensión total y luego se toman los límites con función de prueba fija. Elegir R > 2/c y d > 0 hace estricta la mejora. El resultado da una proporción límite; no cuenta ceros a una altura finita especificada.'),
      href: PROOF,
    },
  ];
  return <figure className="rh-figure">
    <svg className="rh-proof-map-wide" viewBox="0 0 920 170" role="img" aria-labelledby="rh-proof-title rh-proof-desc">
      <title id="rh-proof-title">{t('How the improvement follows', 'Cómo se obtiene la mejora')}</title>
      <desc id="rh-proof-desc">{t('Four stages connect short-interval arithmetic, spectral stability, three-point geometry, and a strict asymptotic refinement. Select a stage below to inspect its role and source.', 'Cuatro etapas conectan la aritmética en intervalos cortos, la estabilidad espectral, la geometría de tres puntos y un refinamiento asintótico estricto. Seleccione una etapa abajo para examinar su función y fuente.')}</desc>
      <defs><marker id="rh-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7z" className="dg-arrowhead" /></marker></defs>
      {stages.map((s, i) => <g key={s.title}>
        {i > 0 && <path d={`M${i * 232 - 20} 68 h22`} className="dg-edge" markerEnd="url(#rh-arrow)" />}
        <rect x={i * 232 + 3} y="20" width="213" height="100" rx="9" className={`dg-box${step === i ? ' accent' : ''}`} />
        <text x={i * 232 + 109} y="51" textAnchor="middle" className="dg-box-title">{s.title}</text>
        <text x={i * 232 + 109} y="84" textAnchor="middle" className="dg-box-sub">{s.formula}</text>
      </g>)}
      <path d="M110 143 H805" className="dg-edge" />
      <text x="460" y="163" textAnchor="middle" className="dg-axis-label">{t('Cited analytic inputs + a written finite proof + a reproducible energy certificate', 'Entradas analíticas citadas + una prueba finita escrita + un certificado reproducible de energía')}</text>
    </svg>
    <svg className="rh-proof-map-mobile" viewBox="0 0 320 410" role="img" aria-label={t('Four proof stages: arithmetic, retained defect, three-point geometry, asymptotic refinement', 'Cuatro etapas: aritmética, defecto retenido, geometría de tres puntos y refinamiento asintótico')}>
      {stages.map((s, i) => <g key={s.title}>
        {i > 0 && <path d={`M160 ${i * 102 - 13} v17 m-4 -4 l4 4 l4 -4`} className="dg-edge" />}
        <rect x="5" y={i * 102 + 7} width="310" height="80" rx="9" className={`dg-box${step === i ? ' accent' : ''}`} />
        <text x="160" y={i * 102 + 36} textAnchor="middle" className="dg-box-title">{s.title}</text>
        <text x="160" y={i * 102 + 63} textAnchor="middle" className="dg-box-sub">{s.formula}</text>
      </g>)}
    </svg>
    <div className="rh-stage-controls" aria-label={t('Inspect a proof stage', 'Examinar una etapa de la prueba')}>
      {stages.map((s, i) => <button key={s.title} className={`btn${step === i ? ' primary' : ''}`} onClick={() => setStep(i)} aria-pressed={step === i}>{s.title}</button>)}
    </div>
    <figcaption className="rh-stage-detail" aria-live="polite">
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
    loadExperiments().then((value) => { if (active) setExps(value.filter((e) => e.problem === 'riemann-hypothesis')); }).catch(() => { if (active) setRecordsError(true); });
    return () => { active = false; };
  }, [attempt]);
  const result = data?.result;
  const sourceRole = (role: string) => ({
    constant_audit: t('constant audit', 'auditoría de constantes'),
    result: t('arithmetic result', 'resultado aritmético'),
    certificate: t('finite certificate', 'certificado finito'),
    proof: t('mathematical proof', 'prueba matemática'),
    verdict: t('experiment verdict', 'veredicto experimental'),
    source_manifest: t('source inventory', 'inventario de fuentes'),
  }[role] || role);
  const refsLabel = t('Sources for this section', 'Fuentes de esta sección');
  const resultTable = result ? <div className="rs-scroll"><table className="rs-table rh-results">
    <caption>{t('Certified example: proportions of all zeros counted with multiplicity', 'Ejemplo certificado: proporciones de todos los ceros contados con multiplicidad')}</caption>
    <thead><tr><th>{t('Quantity', 'Cantidad')}</th><th>{t('Recorded decimal approximation', 'Aproximación decimal registrada')}</th></tr></thead>
    <tbody>
      <tr><td>{t('Wang baseline c(θ)', 'Cota base de Wang c(θ)')}</td><td className="rh-number">{center(result.baseline.display)}</td></tr>
      <tr><td>{t('Refined simple-critical bound c*', 'Cota refinada de ceros críticos simples c*')}</td><td className="rh-number"><strong>{center(result.improved.display)}</strong></td></tr>
      <tr><td>{t('Gain in proportion c* − c', 'Ganancia en proporción c* − c')}</td><td className="rh-number">{center(result.gain.display)}</td></tr>
    </tbody>
  </table></div> : <p role="status">{error ? t('The recorded result could not be loaded. The proof and source artifacts remain available below.', 'No se pudo cargar el resultado registrado. La prueba y los artefactos originales siguen disponibles abajo.') : t('Loading the recorded arithmetic result…', 'Cargando el resultado aritmético registrado…')}</p>;

  const tabs: TabDef[] = [
    {
      id: 'summary', label: t('Summary', 'Resumen'), content: <section>
        <p className="rh-lead">{t('This research record follows the recent proof that more than two-thirds of the nontrivial zeta zeros are simple and on the critical line, its Hilbert-space simplification, and the new short-interval theory. Our contribution is a strict stability refinement of Wang’s positive short-interval curve, with a written proof and a reproducible finite certificate.', 'Este registro sigue la prueba reciente de que más de dos tercios de los ceros no triviales de zeta son simples y están en la recta crítica, su simplificación mediante espacios de Hilbert y la nueva teoría en intervalos cortos. Nuestra contribución es un refinamiento estricto por estabilidad de la curva positiva de Wang en intervalos cortos, con una prueba escrita y un certificado finito reproducible.')}</p>
        <Equation tex={String.raw`\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}\ge c_*(\theta)>c(\theta),\qquad c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot\frac\theta{\sqrt2}`}
          caption={t('N counts all nontrivial zeros with multiplicity in (T, T + T^θ]; N₀ˢ counts simple zeros on Re(s) = 1/2. The exponent θ is fixed and lies between the positive root of c and 1.', 'N cuenta todos los ceros no triviales con multiplicidad en (T, T + T^θ]; N₀ˢ cuenta los ceros simples en Re(s) = 1/2. El exponente θ es fijo y está entre la raíz positiva de c y 1.')} />
        <p className="small">{t('Original result: ', 'Resultado original: ')}<Cite id="riemann-anthropic2026" />{t(' · Short-interval baseline: ', ' · Cota base en intervalos cortos: ')}<Cite id="riemann-wang2026" />{t(' · Refinement: ', ' · Refinamiento: ')}<Cite id="riemann-refinement2026" /></p>
        {result && <p className="rh-parameters">θ = <b>{result.theta}</b> · R = <b>{result.radius}</b> · d = <b>{result.delta}</b></p>}
        {resultTable}
        <p>{t('The displayed gain is a fraction of the total zero count. It is small; moving the decimal point to report a percentage must not change the theorem’s scale. The entire positive curve has an analytic strict improvement, while the displayed example uses a stronger certified finite energy bound.', 'La ganancia mostrada es una fracción del número total de ceros. Es pequeña; mover la coma decimal para expresar un porcentaje no debe cambiar la escala del teorema. Toda la curva positiva tiene una mejora analítica estricta, mientras que el ejemplo mostrado usa una cota finita certificada de energía más fuerte.')}</p>
        <Callout variant="honest" title={t('What the result establishes', 'Qué establece el resultado')}>
          {t('This is a self-published research preprint awaiting external review. It refines an asymptotic short-interval bound. The Riemann hypothesis remains open; no global proportion record, effective starting height, or smaller positivity exponent is established. The theorem combines cited analytic inputs with our finite proof; the arithmetic certificate alone does not prove the zeta statement.', 'Este es un preprint de investigación autopublicado, pendiente de revisión externa. Refina una cota asintótica en intervalos cortos. La hipótesis de Riemann sigue abierta; no se establece un récord de proporción global, una altura inicial efectiva ni un exponente de positividad menor. El teorema combina entradas analíticas citadas con nuestra prueba finita; el certificado aritmético por sí solo no demuestra el enunciado sobre zeta.')}
        </Callout>
        <ProofDiagram />
        <div className="rh-source-links"><SourceLink href={PAPER}>{t('Read the manuscript PDF', 'Leer el manuscrito PDF')}</SourceLink><SourceLink href={DOI}>{t('Zenodo publication and versions', 'Publicación y versiones en Zenodo')}</SourceLink><SourceLink href={PROOF}>{t('Read the full proof', 'Leer la prueba completa')}</SourceLink></div>
        <Refs label={refsLabel} ids={['riemann-anthropic2026', 'riemann-wang2026', 'riemann-ainta2026', 'riemann-lamzouri2026', 'riemann-refinement2026']} />
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
        <Callout variant="note" title={t('Corrections preserved in the review', 'Correcciones conservadas en la revisión')}>
          {t('The source audit corrects an additive grid-dimension error in the revised original proof: the discrepancy is of order T, while the relative error still tends to zero. It therefore does not by itself refute the limiting theorem. The review also preserves the corrected BGSTB error terms and distinguishes historical critical-line counts from simple-critical counts.', 'La auditoría corrige un error aditivo en la dimensión de la malla de la prueba original revisada: la discrepancia es de orden T, mientras que el error relativo aún tiende a cero. Por ello no refuta por sí sola el teorema límite. La revisión también conserva los términos de error corregidos de BGSTB y distingue los conteos históricos de ceros críticos de los conteos de ceros críticos simples.')}
        </Callout>
        <Refs label={refsLabel} ids={['riemann-anthropic2026', 'riemann-alpogefurman2026', 'riemann-lamzouri2026', 'riemann-wang2026', 'riemann-bgstb2026']} />
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
            <tr><td><Cite id="riemann-ainta2026" /><br /><Cite id="riemann-trmdy2026" /></td><td>{t('Retained convex Gram defect and higher-point certificates.', 'Defecto convexo de Gram retenido y certificados con más puntos.')}</td><td>{t('These global candidate refinements predate our transfer; their interfaces must be audited separately.', 'Estos refinamientos globales candidatos preceden a nuestra transferencia; sus interfaces requieren auditoría separada.')}</td></tr>
          </tbody>
        </table></div>
        <h2>{t('What the Lean source actually covers', 'Qué cubre realmente la fuente Lean')}</h2>
        <p>{t('AxiomMath’s second development gives explicit Riemann–von Mangoldt and pair-correlation assumptions to its headline zeta theorems. Its finite inequalities and numerical corollaries are formal source, while those two analytic inputs remain assumptions in that project. The pinned upstream CI confirms a default-library build; it does not itself show the separate challenge comparator running.', 'El segundo desarrollo de AxiomMath incluye supuestos explícitos de Riemann–von Mangoldt y correlación por pares en sus teoremas principales sobre zeta. Sus desigualdades finitas y corolarios numéricos son fuente formal, mientras que esas dos entradas analíticas siguen siendo supuestos en ese proyecto. El CI de la versión fijada confirma una compilación de la biblioteca predeterminada; no demuestra por sí solo la ejecución del comparador separado de desafíos.')} <Cite id="riemann-axiom2026" /></p>
        <p>{t('Anthropic’s current formal-math development contains proofs of the analytic inputs and headline statements without those external hypotheses. Our source inspection distinguishes this stronger intended scope from the verification receipts available for particular commits. We did not locally rebuild the full upstream Lean developments, and we do not present upstream author reports as our own independent kernel verification.', 'El desarrollo actual formal-math de Anthropic contiene pruebas de las entradas analíticas y enunciados principales sin esas hipótesis externas. Nuestra inspección distingue este alcance más fuerte de los comprobantes de verificación disponibles para ciertos commits. No recompilamos localmente los desarrollos Lean completos y no presentamos los informes de los autores como verificación independiente del núcleo realizada por nosotros.')} <Cite id="riemann-formalmath2026" /></p>
        <Callout variant="honest" title={t('Novelty is narrower than a larger decimal', 'La novedad exige más que un decimal mayor')}>
          {t('Recomputing the cosine constant, repackaging the arbitrary-parameter rank–trace inequality, or repeating already published global stability arguments is not claimed as discovery. Higher-moment headlines with unresolved analytic objections are not adopted as established results. Our candidate contribution is the explicit short-interval transfer and positive-curve refinement; source searches cannot guarantee priority.', 'Recalcular la constante coseno, reformular la desigualdad rango–traza con parámetro arbitrario o repetir argumentos globales de estabilidad ya publicados no se presenta como descubrimiento. Los anuncios basados en momentos superiores con objeciones analíticas sin resolver no se adoptan como resultados establecidos. Nuestra contribución candidata es la transferencia explícita a intervalos cortos y el refinamiento de la curva positiva; las búsquedas de fuentes no garantizan prioridad.')}
        </Callout>
        <div className="rh-source-links"><SourceLink href={`${REPO}/tree/main/${PROBLEM}/context`}>{t('Read the source audits', 'Leer las auditorías de fuentes')}</SourceLink><SourceLink href={`${REPO}/blob/main/${PROBLEM}/context/source-manifest.json`}>{t('Versions, licenses and source hashes', 'Versiones, licencias y hashes de fuentes')}</SourceLink></div>
        <Refs label={refsLabel} ids={['riemann-anthropic2026', 'riemann-lamzouri2026', 'riemann-wang2026', 'riemann-axiom2026', 'riemann-formalmath2026', 'riemann-ainta2026', 'riemann-trmdy2026']} />
      </section>,
    },
    {
      id: 'strategy', label: t('Strategy', 'Estrategia'), content: <section>
        <h2>{t('Keep the information lost at equality', 'Conservar la información perdida en la igualdad')}</h2>
        <p>{t('A normalized even density determines vectors for the zeros and a finite self-adjoint operator A. Its trace is the total multiplicity N; its squared Hilbert–Schmidt norm is Q. The simple real atoms form a positive operator with Gram matrix G. The residual operator includes signed off-line conjugate pairs, so replacing the complex pair sum by a sum of absolute squares would change the mathematics.', 'Una densidad par normalizada determina vectores para los ceros y un operador autoadjunto finito A. Su traza es la multiplicidad total N; el cuadrado de su norma de Hilbert–Schmidt es Q. Los átomos reales simples forman un operador positivo con matriz de Gram G. El operador residual incluye pares conjugados con signo fuera de la recta, de modo que reemplazar la suma compleja por una suma de módulos al cuadrado cambiaría la matemática.')}</p>
        <Equation tex={String.raw`S\ge2N-Q+D(G),\qquad D(G)=\operatorname{tr}\Psi(G),\qquad \Psi(t)=\begin{cases}(t-1)^2&0\le t\le2,\\2t-3&t\ge2.\end{cases}`}
          caption={t('S is the simple-critical count. G is positive semidefinite with unit diagonal. Ψ measures the spectral defect; the stability mechanism is inherited from ainta and transferred to Lamzouri’s finite operator.', 'S es el conteo de ceros críticos simples. G es semidefinida positiva con diagonal unitaria. Ψ mide el defecto espectral; el mecanismo de estabilidad proviene de ainta y se transfiere al operador finito de Lamzouri.')} />
        <p>{t('The stable inequality is inherited from ainta; the exact finite operator is due to Lamzouri.', 'La desigualdad estable proviene de ainta; el operador finito exacto se debe a Lamzouri.')} <Cite id="riemann-ainta2026" /> <Cite id="riemann-lamzouri2026" /></p>
        <h2>{t('Turn three gaps into a positive defect', 'Convertir tres separaciones en un defecto positivo')}</h2>
        <p>{t('For the cosine density, let kθ be its real Fourier transform. Its zero equation is incompatible with three positive arguments u, v and u + v all being roots. Consequently the doubled three-point energy has a strictly positive minimum on any fixed compact gap triangle. The proof gives an explicit conservative analytic bound, while interval arithmetic gives a stronger numerical bound for the recorded example.', 'Para la densidad coseno, sea kθ su transformada de Fourier real. Su ecuación de ceros es incompatible con que tres argumentos positivos u, v y u + v sean raíces simultáneas. Por tanto, la energía duplicada de tres puntos tiene un mínimo estrictamente positivo en cualquier triángulo compacto fijo de separaciones. La prueba da una cota analítica explícita conservadora, mientras que la aritmética de intervalos da una cota numérica más fuerte para el ejemplo registrado.')}</p>
        <Equation tex={String.raw`f_\theta(t)=\frac{\cos(\sqrt2t)}{\sqrt2\sin(\theta/\sqrt2)}\mathbf1_{|t|\le\theta/2},\quad k_\theta=\widehat f_\theta,\quad 2\bigl(k_\theta(u)^2+k_\theta(v)^2+k_\theta(u+v)^2\bigr)\ge d`}
          caption={t('The Fourier convention is kθ(x) = ∫fθ(t)e^(−2πixt)dt. The bound applies to u, v ≥ 0 and u + v ≤ R, with 0 < d ≤ 1.', 'La convención de Fourier es kθ(x) = ∫fθ(t)e^(−2πixt)dt. La cota vale para u, v ≥ 0 y u + v ≤ R, con 0 < d ≤ 1.')} />
        <TriangleDiagram />
        <p>{t('Order the simple critical zeros along the line. The sum of the spans of all consecutive triples is at most twice the total span L. At least S − 2 − 2L/R triples therefore have span at most R. Partition the triple starting indices by their residue modulo three: each class gives disjoint Gram blocks. Convex pinching and averaging the three classes retain the required one-third factor.', 'Se ordenan los ceros críticos simples en la recta. La suma de las extensiones de todas las ternas consecutivas es a lo más dos veces la extensión total L. Por tanto, al menos S − 2 − 2L/R ternas tienen extensión a lo más R. Se particionan los índices iniciales según su residuo módulo tres: cada clase da bloques de Gram disjuntos. La compresión convexa por bloques y el promedio de las tres clases conservan el factor necesario de un tercio.')}</p>
        <Equation tex={String.raw`D(G)\ge\frac d3\left(S-2-\frac{2L}{R}\right),\qquad c_*=c+\frac{d(c-2/R)}{3-d}>c\quad\text{if }R>2/c`}
          caption={t('L is the actual normalized span. Its upper bound X_T = T^θ log(T)/(2π) satisfies X_T/N → 1; no asymptotic equality for L is assumed. The constant d is an energy floor on the compact triangle.', 'L es la extensión normalizada real. Su cota superior X_T = T^θ log(T)/(2π) satisface X_T/N → 1; no se supone igualdad asintótica para L. La constante d es una cota inferior de energía en el triángulo compacto.')} />
        <h2>{t('Respect the support and the order of limits', 'Respetar el soporte y el orden de los límites')}</h2>
        <p>{t('Fix a support width λ below θ and a smooth nonnegative density of the form η². Apply Wang’s pair-correlation estimate to this fixed test function and take T to infinity. Only afterwards approximate the cosine density and let λ rise to θ. Uniform Fourier control preserves every strict energy floor below d; the final outer limit reaches the full certified d. Choosing a smoothing scale depending on T would require uniform estimates that this proof does not claim.', 'Se fija un ancho de soporte λ menor que θ y una densidad suave no negativa de la forma η². Se aplica la estimación de correlación por pares de Wang a esta función de prueba fija y se toma T hacia infinito. Solo después se aproxima la densidad coseno y se eleva λ hacia θ. El control uniforme de Fourier preserva cada cota estricta de energía menor que d; el límite exterior final alcanza el d certificado completo. Elegir una escala de suavizado dependiente de T exigiría estimaciones uniformes que esta prueba no afirma.')}</p>
        <p>{t('The required fixed-support estimate is the short-interval input from Wang.', 'La estimación requerida con soporte fijo es la entrada para intervalos cortos de Wang.')} <Cite id="riemann-wang2026" /></p>
        <Callout variant="honest" title={t('Assumptions and failure checks', 'Supuestos y controles de fallo')}>
          {t('The exponent is fixed above the positivity threshold. No uniform improvement at the threshold, finite-height estimate, or extension past the cited Fourier-support range follows. The independent audit checked multiplicities, off-line signs, spectral zero padding, the three-offset count, removable kernel singularities, smoothing, and the final limit.', 'El exponente es fijo y mayor que el umbral de positividad. No se obtiene una mejora uniforme en el umbral, una estimación a altura finita ni una extensión más allá del rango citado del soporte de Fourier. La auditoría independiente revisó multiplicidades, signos fuera de la recta, ceros añadidos al espectro, el conteo de tres desplazamientos, singularidades removibles del núcleo, suavizado y límite final.')}
        </Callout>
        <SourceLink href={`${REPO}/blob/main/${EXP}/adversarial-audit.md`}>{t('Read the adversarial proof review', 'Leer la revisión adversarial de la prueba')}</SourceLink>
        <Refs label={refsLabel} ids={['riemann-lamzouri2026', 'riemann-ainta2026', 'riemann-wang2026', 'riemann-refinement2026']} />
      </section>,
    },
    {
      id: 'results', label: t('Experiments & results', 'Experimentos y resultados'), content: <section>
        <h2>{t('Read the experiment records', 'Leer los registros experimentales')}</h2>
        <p>{t('The first experiment reproduces the source constants with exact rational Taylor bounds and an Arb comparison, and checks the normalization correction. The second proves the short-interval refinement and certifies its finite three-point example. Open either record to read the original declared hypothesis, persisted verdict, artifacts, and source history. The records are preserved in their original language.', 'El primer experimento reproduce las constantes de las fuentes mediante cotas de Taylor racionales exactas y una comparación con Arb, y verifica la corrección de normalización. El segundo demuestra el refinamiento en intervalos cortos y certifica su ejemplo finito de tres puntos. Abra cualquier registro para leer la hipótesis declarada, el veredicto persistido, los artefactos y la historia de la fuente. Los registros se conservan en su idioma original.')}</p>
        <ul className="rh-experiments">{exps.map((e) => <li key={e.slug}><button className="rs-exp-open" onClick={() => setOpen(e)}>EXP-{e.id}: {e.id === '001' ? t('Source and constant audit', 'Auditoría de fuentes y constantes') : t('Short-interval stability refinement', 'Refinamiento por estabilidad en intervalos cortos')}</button><span className="rs-badge state">{e.verdict || t('Record available', 'Registro disponible')}</span></li>)}</ul>
        {(recordsError || !exps.length) && <p>{t('Experiment records are currently unavailable in the viewer.', 'Los registros experimentales no están disponibles actualmente en el visor.')} <SourceLink href={`${REPO}/tree/main/${PROBLEM}/experiments`}>{t('Open the source records', 'Abrir los registros originales')}</SourceLink></p>}
        {resultTable}
        <p>{t('The baseline is Wang’s short-interval theorem; the strict refinement and its distinct-zero companion are derived in the present preprint.', 'La cota base es el teorema de Wang en intervalos cortos; el refinamiento estricto y su cota complementaria de ceros distintos se derivan en el preprint presente.')} <Cite id="riemann-wang2026" /> <Cite id="riemann-refinement2026" /></p>
        <Equation tex={String.raw`\liminf_{T\to\infty}\frac{N^d(T,T^\theta)}{N(T,T^\theta)}\ge\frac{1+c_*(\theta)}2`}
          caption={t('Nᵈ counts each distinct nontrivial zero once, regardless of multiplicity or position in the strip. This companion bound has the same fixed-exponent and asymptotic scope.', 'Nᵈ cuenta cada cero no trivial distinto una sola vez, sin importar su multiplicidad o ubicación en la franja. Esta cota complementaria tiene el mismo alcance asintótico y de exponente fijo.')} />
        <h2>{t('What the arithmetic certificate checks', 'Qué verifica el certificado aritmético')}</h2>
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
        <Callout variant="note" title={t('Reproduction boundary', 'Alcance de la reproducción')}>
          {t('The browser reads persisted results; it does not search for zeros or run the arithmetic proof. The offline runner uses pinned dependencies and an explicit output directory. A budget stop saves a checkpoint and cannot be reported as a certificate. CPU arithmetic was sufficient for this experiment.', 'El navegador lee resultados persistidos; no busca ceros ni ejecuta la prueba aritmética. El programa externo usa dependencias fijadas y un directorio de salida explícito. Una parada por presupuesto guarda un punto de control y no puede presentarse como certificado. La aritmética en CPU fue suficiente para este experimento.')}
        </Callout>
        <Refs label={refsLabel} ids={['riemann-refinement2026', 'riemann-wang2026']} />
      </section>,
    },
    {
      id: 'open', label: t('Open questions', 'Preguntas abiertas'), content: <section>
        <h2>{t('What remains to be established', 'Qué falta establecer')}</h2>
        <p>{t('The Riemann hypothesis remains the overarching open problem. The refinement gives a small strict gain inside a specified asymptotic counting problem. It does not place every zero on the line, prove all zeros simple, or determine a finite height beyond which the proportion holds. Those conclusions need additional mathematics.', 'La hipótesis de Riemann sigue siendo el problema abierto general. El refinamiento da una pequeña ganancia estricta dentro de un problema de conteo asintótico especificado. No sitúa todos los ceros en la recta, no demuestra que todos sean simples ni determina una altura finita a partir de la cual valga la proporción. Esas conclusiones requieren matemática adicional.')}</p>
        <ol className="rh-questions">
          <li><h3>{t('External proof and priority review', 'Revisión externa de la prueba y la prioridad')}</h3><p>{t('Can an independent specialist validate the transfer, the signed finite operator, and the nested limits? The reviewed sources contain the stability lemma and global geometric refinements; the candidate novelty is the short-interval consequence. Earlier or concurrent work could narrow that claim.', '¿Puede un especialista independiente validar la transferencia, el operador finito con signo y los límites anidados? Las fuentes revisadas contienen el lema de estabilidad y refinamientos geométricos globales; la novedad candidata es la consecuencia en intervalos cortos. Trabajos anteriores o simultáneos podrían reducir ese alcance.')}</p></li>
          <li><h3>{t('A useful improvement near the threshold', 'Una mejora útil cerca del umbral')}</h3><p>{t('The analytic gain stays positive for each fixed admissible exponent but may become extremely small near the threshold. Improving the positivity exponent itself requires a mechanism beyond the present baseline-plus-defect argument.', 'La ganancia analítica permanece positiva para cada exponente fijo admisible, pero puede ser extremadamente pequeña cerca del umbral. Mejorar el propio exponente de positividad requiere un mecanismo adicional al argumento actual de cota base más defecto.')}</p></li>
          <li><h3>{t('Larger point configurations', 'Configuraciones con más puntos')}</h3><p>{t('More consecutive simple zeros may force a stronger Gram defect. A useful next experiment would compare a declared family of configurations at a fixed exponent, with rigorous compact-domain certificates and explicit counting factors. Global successor work provides ideas, not a license to reuse its headline constants in short intervals.', 'Más ceros simples consecutivos pueden forzar un defecto de Gram más fuerte. Un siguiente experimento útil compararía una familia declarada de configuraciones a exponente fijo, con certificados rigurosos del dominio compacto y factores explícitos de conteo. Los trabajos sucesores globales aportan ideas, pero no permiten reutilizar sus constantes principales en intervalos cortos.')}</p></li>
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
