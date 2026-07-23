import { Suspense, lazy, useEffect, useState } from 'react';
import { Callout, Cite, Equation, InlineMath, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, loadJacobian, type ExperimentRec, type JacobianData } from '../api/data';
import WallCanvas from '../components/WallCanvas';
import CubicExplorer from '../components/CubicExplorer';
const ExperimentModal = lazy(() => import('../components/ExperimentModal'));

const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const MANUSCRIPTS = [
  { slug: 'foundational', doi: '10.5281/zenodo.21503366', en: 'Paper A, foundational: the counterexample, structure, family, escape geometry and the 3D aftermath', es: 'Articulo A, fundacional: el contraejemplo, estructura, familia, geometria de escape y las consecuencias en 3D' },
  { slug: 'planar', doi: '10.5281/zenodo.21503368', en: 'Paper B, the planar program: the theorem ladder, staircase transport and the (72,108) campaign', es: 'Articulo B, el programa planar: la escalera de teoremas, el transporte de escalera y la campaña (72,108)' },
  { slug: 'cascade', doi: '10.5281/zenodo.21503372', en: 'Paper C, the consequence cascade: the dimension-48 Hessian witness', es: 'Articulo C, la cascada de consecuencias: el testigo Hessiano en dimension 48' },
];

export default function Jacobian() {
  const t = useT();
  const [jac, setJac] = useState<JacobianData | null>(null);
  const [exps, setExps] = useState<ExperimentRec[]>([]);
  const [open, setOpen] = useState<ExperimentRec | null>(null);
  useEffect(() => {
    loadJacobian().then(setJac).catch(() => setJac(null));
    loadExperiments().then((e) => setExps(e.filter((x) => x.problem === 'jacobian-conjecture'))).catch(() => setExps([]));
  }, []);

  const tabs: TabDef[] = [
    {
      id: 'summary',
      label: t('Summary', 'Resumen'),
      content: (
        <section>
          <p className="rs-lead">
            {t(
              'The Jacobian conjecture (1939; two-variable form 1884) asserted that every polynomial map with constant nonzero Jacobian determinant has a polynomial inverse. On 2026-07-19 Levent Alpöge, working with Claude Fable (Anthropic), announced a counterexample in dimension 3 ',
              'La conjetura jacobiana (1939; forma en dos variables 1884) afirmaba que todo mapa polinomial con determinante jacobiano constante no nulo tiene inversa polinomial. El 2026-07-19 Levent Alpöge, trabajando con Claude Fable (Anthropic), anuncio un contraejemplo en dimension 3 ',
            )}
            (<Cite id="alpoge2026" />).
          </p>
          <Equation tex={String.raw`F(x,y,z)=\bigl(u^{3}z+y^{2}u(4+3xy),\;\; y+3xu^{2}z+3xy^{2}(4+3xy),\;\; 2x-3x^{2}y-x^{3}z\bigr),\quad u=1+xy`} />
          <Equation tex={String.raw`\det JF=-2,\qquad F\!\left(0,0,-\tfrac14\right)=F\!\left(1,-\tfrac32,\tfrac{13}{2}\right)=F\!\left(-1,\tfrac32,\tfrac{13}{2}\right)=\left(-\tfrac14,0,0\right)`} />
          <p>
            {t(
              'This program validated the counterexample independently in exact arithmetic and then built on it: the structure, an infinite family of new counterexamples, the exact escape geometry and real census, characteristic-p certificates, a rigidity theorem in dimension 2, and a uniqueness result for the mechanism. Twelve experiments so far, each with a persisted verdict; the still-open two-variable case is the standing target.',
              'Este programa valido el contraejemplo de forma independiente en aritmetica exacta y construyo sobre el: la estructura, una familia infinita de nuevos contraejemplos, la geometria exacta de escape y el censo real, certificados en caracteristica p, un teorema de rigidez en dimension 2 y un resultado de unicidad del mecanismo. Doce experimentos hasta ahora, cada uno con veredicto persistido; el caso de dos variables, aun abierto, es el objetivo permanente.',
            )}
          </p>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['alpoge2026', 'keller1939', 'smale1998', 'caosresearch']} />
          <h3>{t('Manuscripts of this problem', 'Manuscritos de este problema')}</h3>
          <p>
            {t(
              'The written record is a three-paper set, versioned with the repository; each link opens the built PDF directly.',
              'El registro escrito es un conjunto de tres articulos, versionado con el repositorio; cada enlace abre directamente el PDF compilado.',
            )}
          </p>
          <ul>
            {MANUSCRIPTS.map((m) => (
              <li key={m.slug}>
                <a href={`${REPO}/blob/main/manuscripts/jacobian-conjecture/${m.slug}/main.pdf`} target="_blank" rel="noreferrer">
                  {t(m.en, m.es)}
                </a>{' '}
                (<a href={`https://doi.org/${m.doi}`} target="_blank" rel="noreferrer">DOI {m.doi}</a> · <a href={`${REPO}/tree/main/manuscripts/jacobian-conjecture/${m.slug}`} target="_blank" rel="noreferrer">{t('source', 'fuente')}</a>)
              </li>
            ))}
          </ul>
        </section>
      ),
    },
    {
      id: 'context',
      label: t('Context and history', 'Contexto e historia'),
      content: (
        <section>
          <p>
            {t('A Keller map is a polynomial map ', 'Un mapa de Keller es un mapa polinomial ')}
            <InlineMath tex={String.raw`F:\mathbb{C}^N\to\mathbb{C}^N`} />
            {t(' with ', ' con ')}
            <InlineMath tex={String.raw`\det JF\in\mathbb{C}^{\times}`} />
            {t(' constant. Over the complex numbers, invertibility is equivalent to injectivity, so a refutation needs exactly one repeated value.', ' constante. Sobre los numeros complejos, la invertibilidad equivale a la inyectividad, asi que una refutacion necesita exactamente un valor repetido.')}
          </p>
          <div className="rs-scroll">
            <table className="rs-table">
              <thead><tr><th>{t('Year', 'Año')}</th><th>{t('Milestone', 'Hito')}</th></tr></thead>
              <tbody>
                <tr><td className="num">1884</td><td>{t('Kraus states the two-variable case, with a flawed proof; the gap (ramification at infinity) remains the central obstacle ', 'Kraus enuncia el caso de dos variables, con prueba fallida; el hueco (ramificacion en el infinito) sigue siendo el obstaculo central ')}(<Cite id="rodriguez2026" />)</td></tr>
                <tr><td className="num">1939</td><td>{t('Keller popularizes the conjecture and proves the birational case ', 'Keller populariza la conjetura y prueba el caso birracional ')}(<Cite id="keller1939" />)</td></tr>
                <tr><td className="num">1980-83</td><td>{t('Wang proves degree 2; Moh verifies two variables to degree 100; Bass-Connell-Wright and Druzkowski reduce the general case to cubic forms ', 'Wang prueba grado 2; Moh verifica dos variables hasta grado 100; Bass-Connell-Wright y Druzkowski reducen el caso general a formas cubicas ')}(<Cite id="moh1983" />, <Cite id="bcw1982" />, <Cite id="druzkowski1983" />)</td></tr>
                <tr><td className="num">1994</td><td>{t('Pinchuk refutes the strong real variant (non-constant Jacobian) with a non-proper local diffeomorphism ', 'Pinchuk refuta la variante real fuerte (jacobiano no constante) con un difeomorfismo local no propio ')}(<Cite id="pinchuk1994" />)</td></tr>
                <tr><td className="num">1998</td><td>{t('Problem 16 on Smale list ', 'Problema 16 de la lista de Smale ')}(<Cite id="smale1998" />)</td></tr>
                <tr><td className="num">2026</td><td>{t('Alpöge, with Claude Fable, announces the dimension-3 counterexample; false for every N of at least 3; two variables stay open ', 'Alpöge, con Claude Fable, anuncia el contraejemplo en dimension 3; falsa para todo N al menos 3; dos variables queda abierto ')}(<Cite id="alpoge2026" />, <Cite id="sparkes2026" />)</td></tr>
              </tbody>
            </table>
          </div>
          <Refs label={t('References', 'Referencias')} ids={['rodriguez2026', 'keller1939', 'magnus1954', 'moh1983', 'bcw1982', 'druzkowski1983', 'appelgateonishi1985', 'pinchuk1994', 'smale1998', 'vandenessen2000', 'wikipedia-jc']} />
        </section>
      ),
    },
    {
      id: 'strategy',
      label: t('Our strategy', 'Nuestra estrategia'),
      content: (
        <section>
          <p>
            {t(
              'The program runs the experiment loop of the methodology page: validate first, reverse-engineer the structure, generalize with a constructor, make the failure geometry exact, then close the symmetric routes in dimension 2 and map the neighboring weight systems. Refuted runs are kept and mined: the v1 constructor refuted by EXP-003 produced the correct potential form of EXP-004, and the parity hypothesis refuted in EXP-012 produced the uniqueness result.',
              'El programa corre el bucle de experimentos de la pagina de metodologia: validar primero, hacer ingenieria inversa de la estructura, generalizar con un constructor, hacer exacta la geometria de la falla, luego cerrar las rutas simetricas en dimension 2 y mapear los sistemas de pesos vecinos. Las corridas refutadas se conservan y se explotan: el constructor v1 refutado por EXP-003 produjo la forma potencial correcta de EXP-004, y la hipotesis de paridad refutada en EXP-012 produjo el resultado de unicidad.',
            )}
          </p>
          <Callout variant="note" title={t('The structure in one line', 'La estructura en una linea')}>
            {t('The map is a weighted skew-product: with invariants ', 'El mapa es un producto sesgado con pesos: con invariantes ')}
            <InlineMath tex={String.raw`v=xy,\ t=x^{2}z`} />
            {t(', the Keller condition collapses to a two-variable identity and the fibers are governed by one cubic ', ', la condicion de Keller colapsa a una identidad en dos variables y las fibras se gobiernan por una cubica ')}
            <InlineMath tex={String.raw`\Phi(w)=w^{2}-w^{3}`} />
            {t(' at ', ' en ')}
            <InlineMath tex={String.raw`w=u\,c_{1}/2`} />.
          </Callout>
          <h3>{t('Open routes toward the two-variable case', 'Rutas abiertas hacia el caso de dos variables')}</h3>
          <p>
            {t(
              'Three programs follow from the results: (1) a tropical sweep, using the 2D rigidity theorem as the local model at every ray of weighted leading forms of a hypothetical planar Keller map; (2) inverse design of non-proper planar candidates, prescribing the escape geometry first and solving backward with the reconstruction machinery; (3) the m = 1 bridge, where any collision in that 3D weighted class is already a planar counterexample. Each is queued as an experiment in the program backlog.',
              'Tres programas se siguen de los resultados: (1) un barrido tropical, usando el teorema de rigidez 2D como modelo local en cada rayo de formas lideres con peso de un hipotetico mapa de Keller plano; (2) diseño inverso de candidatos planos no propios, prescribiendo primero la geometria de escape y resolviendo hacia atras con la maquinaria de reconstruccion; (3) el puente m = 1, donde cualquier colision en esa clase 3D con pesos ya es un contraejemplo plano. Cada uno esta en la cola de experimentos del backlog del programa.',
            )}
          </p>
        </section>
      ),
    },
    {
      id: 'results',
      label: t('Experiments and results', 'Experimentos y resultados'),
      content: (
        <section>
          <h3>{t('The family of counterexamples', 'La familia de contraejemplos')}</h3>
          <p>
            {t('Constructor: a seed polynomial p with ', 'Constructor: un polinomio semilla p con ')}
            <InlineMath tex={String.raw`p(0)=0,\ \int_0^1 p=0,\ p(1)\neq 0`} />
            {t(', a scale k and a free section give a Keller map with ', ', una escala k y una seccion libre dan un mapa de Keller con ')}
            <InlineMath tex={String.raw`\det=-k\,p(1)^{2}`} />
            {t(' and fiber degree deg p + 1. The degree law is ', ' y grado de fibra deg p + 1. La ley de grados es ')}
            <InlineMath tex={String.raw`(5d-3,\,5d-4,\,4)`} />
            {t(': the announced map is the smallest member of its own family.', ': el mapa anunciado es el miembro mas pequeño de su propia familia.')}
          </p>
          {jac && (
            <div className="rs-scroll">
              <table className="rs-table">
                <thead><tr><th>{t('Seed', 'Semilla')}</th><th>det</th><th>{t('Degrees', 'Grados')}</th><th>{t('Fiber deg', 'Grado de fibra')}</th></tr></thead>
                <tbody>
                  {jac.family.map((f) => (
                    <tr key={f.seed}>
                      <td className="rs-mono">{f.seed}</td>
                      <td className="num">{f.det}</td>
                      <td className="num">({f.degrees.join(', ')})</td>
                      <td className="num">{f.fiber}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <h3>{t('The fiber cubic, live', 'La cubica de fibra, en vivo')}</h3>
          <p>
            {t(
              'Preimages of a target (A, B, C) are the roots of the baked fiber equation; drag the target and watch the census change. The default target is the engineered collision target (-16, -16, 1), whose three roots are the three rational preimages of EXP-007.',
              'Las preimagenes de un objetivo (A, B, C) son las raices de la ecuacion de fibra horneada; arrastre el objetivo y observe cambiar el censo. El objetivo por defecto es el objetivo de colision (-16, -16, 1), cuyas tres raices son las tres preimagenes racionales de EXP-007.',
            )}
          </p>
          <CubicExplorer />
          <h3>{t('The escape wall and the real census', 'El muro de escape y el censo real')}</h3>
          <p>
            {t('A preimage is lost exactly where the fiber cubic has a multiple root; the wall is ', 'Una preimagen se pierde exactamente donde la cubica de fibra tiene raiz multiple; el muro es ')}
            <InlineMath tex={String.raw`27A^{2}C^{2}-18ABC+16A+B^{3}C-B^{2}=0`} />
            {t(' plus the plane C = 0. Over the reals it separates a 3-preimage region from a 1-preimage region, and the map is onto all of R³.', ' mas el plano C = 0. Sobre los reales separa una region de 3 preimagenes de una de 1, y el mapa es sobreyectivo en todo R³.')}
          </p>
          <WallCanvas />
          <h3>{t('The experiment log', 'El registro de experimentos')}</h3>
          <p className="rs-readout">
            {t('Click a title to read the full record (hypothesis, verdict, artifacts) in place.',
               'Haga clic en un titulo para leer el registro completo (hipotesis, veredicto, artefactos) aqui mismo.')}
          </p>
          <ul className="rs-timeline">
            {exps.map((e) => (
              <li key={e.slug}>
                <span className="exp">EXP-{e.id}</span>
                <span className="date rs-readout">{e.date}</span>
                <span>
                  <button type="button" className="rs-exp-open" onClick={() => setOpen(e)}>
                    {e.title}
                  </button>{' '}
                  {e.verdict && <span className={`rs-badge ${e.verdict.split(' ')[0].replace(',', '')}`}>{e.verdict}</span>}
                </span>
              </li>
            ))}
          </ul>
          <Refs label={t('References', 'Referencias')} ids={['caosresearch', 'alpoge2026']} />
        </section>
      ),
    },
    {
      id: 'cascade',
      label: t('Collateral impact', 'Impacto colateral'),
      content: (
        <section>
          <p className="rs-lead">
            {t(
              'One counterexample, many resolutions: the July 19 map (Alpöge, working with Claude Fable) does not only refute the Jacobian conjecture for N of at least 3. Through implication chains published over five decades, and verified here from their primary sources (EXP-016, EXP-018), it resolves or partially resolves a family of named open problems. The credit for every row belongs to the original counterexample; this program contributed the independent validation and the systematic, source-verified evaluation of the impact.',
              'Un contraejemplo, muchas resoluciones: el mapa del 19 de julio (Alpöge, trabajando con Claude Fable) no solo refuta la conjetura jacobiana para N al menos 3. A traves de cadenas de implicacion publicadas durante cinco decadas, y verificadas aqui desde sus fuentes primarias (EXP-016, EXP-018), resuelve o resuelve parcialmente una familia de problemas abiertos con nombre. El credito de cada fila pertenece al contraejemplo original; este programa aporto la validacion independiente y la evaluacion sistematica verificada en fuentes.',
            )}
          </p>
          {jac && jac.cascade && (
            <div className="rs-scroll">
              <table className="rs-table">
                <thead><tr><th>{t('Statement', 'Enunciado')}</th><th>{t('Was', 'Era')}</th><th>{t('Now', 'Ahora')}</th><th>{t('Chain', 'Cadena')}</th></tr></thead>
                <tbody>
                  {jac.cascade.map((r) => (
                    <tr key={r.name}>
                      <td><b>{r.name}</b></td>
                      <td className="rs-readout">{r.prior}</td>
                      <td>{r.now}</td>
                      <td className="rs-readout">{r.chain}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <p>
            {t(
              'What stays open after the cascade: the two-variable Jacobian conjecture, Dixmier at rank 1, Mathieu for SU(2) and the remaining groups, the minimal failing dimensions of the Poisson, moments, vanishing and Image statements, and the explicit witnesses (our queued target: a failing Hessian-nilpotent quartic).',
              'Lo que sigue abierto tras la cascada: la conjetura jacobiana en dos variables, Dixmier en rango 1, Mathieu para SU(2) y los demas grupos, las dimensiones minimas de falla de los enunciados de Poisson, momentos, anulacion e imagen, y los testigos explicitos (nuestro objetivo en cola: una cuartica Hessiana-nilpotente que falle).',
            )}
          </p>
          <Refs label={t('Chain sources', 'Fuentes de las cadenas')} ids={['alpoge2026', 'vandenessen2000', 'wikipedia-jc', 'caosresearch']} />
        </section>
      ),
    },
    {
      id: 'open',
      label: t('Open questions', 'Preguntas abiertas'),
      content: (
        <section>
          <ul>
            <li>{t('JC(2): the two-variable conjecture is open. Our rigidity theorem closes every equivariant route, for all weights; a planar counterexample, if one exists, must be genuinely non-equivariant.', 'JC(2): la conjetura en dos variables esta abierta. Nuestro teorema de rigidez cierra toda ruta equivariante, para todos los pesos; un contraejemplo plano, si existe, debe ser genuinamente no equivariante.')}</li>
            <li>{t('Global minimality: is there any C³ counterexample of total degree 3 to 6? Wang excludes degree 2 only; within our family and the scanned weighted landscape, degree 7 is minimal.', 'Minimalidad global: ¿existe algun contraejemplo en C³ de grado total 3 a 6? Wang excluye solo grado 2; dentro de nuestra familia y del paisaje con pesos explorado, el grado 7 es minimo.')}</li>
            <li>{t('The consequence cascade (Mathieu for SU(3), Gaussian moments, vanishing and image conjectures, Dixmier) is queued for primary-source verification before this program asserts it.', 'La cascada de consecuencias (Mathieu para SU(3), momentos gaussianos, conjeturas de anulacion e imagen, Dixmier) esta en cola para verificacion con fuentes primarias antes de que este programa la afirme.')}</li>
            <li>{t('Widenings queued: general weight systems (1, -2, -m), higher-degree seeds, the m = 4 lattice scan, and an optional Lean hardening of the rigidity theorem.', 'Ampliaciones en cola: sistemas de pesos generales (1, -2, -m), semillas de mayor grado, el barrido de reticula m = 4 y un endurecimiento opcional en Lean del teorema de rigidez.')}</li>
          </ul>
          <Callout variant="honest" title={t('Honesty gate', 'Compuerta de honestidad')}>
            {t('Every claim on this page carries the label of its experiment verdict; scans are bounded and their windows are stated in the corresponding verdict files. Null results and refuted hypotheses are part of the record.', 'Cada afirmacion de esta pagina lleva la etiqueta del veredicto de su experimento; los barridos son acotados y sus ventanas se declaran en los archivos de veredicto correspondientes. Los resultados nulos y las hipotesis refutadas son parte del registro.')}
          </Callout>
        </section>
      ),
    },
  ];

  return (
    <div className="rs-doc">
      <p className="rs-kicker">{t('Problem 1 · algebraic geometry · exploring', 'Problema 1 · geometria algebraica · explorando')}</p>
      <h1>{t('The Jacobian conjecture', 'La conjetura jacobiana')}</h1>
      <Tabs tabs={tabs} ariaLabel={t('Jacobian conjecture sections', 'Secciones de la conjetura jacobiana')} />
      {open && (
        <Suspense fallback={null}>
          <ExperimentModal exp={open} onClose={() => setOpen(null)} />
        </Suspense>
      )}
    </div>
  );
}
