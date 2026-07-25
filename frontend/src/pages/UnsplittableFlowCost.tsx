import { Suspense, lazy, useEffect, useState } from 'react';
import { Callout, Cite, Equation, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, type ExperimentRec } from '../api/data';
const ExperimentModal = lazy(() => import('../components/ExperimentModal'));

const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';

export default function UnsplittableFlowCost() {
  const t = useT();
  const [exps, setExps] = useState<ExperimentRec[]>([]);
  const [open, setOpen] = useState<ExperimentRec | null>(null);
  useEffect(() => {
    loadExperiments()
      .then((e) => setExps(e.filter((x) => x.problem === 'unsplittable-flow-cost')))
      .catch(() => setExps([]));
  }, []);

  // Counts come from the baked experiment records, so the page cannot drift from the
  // repository. Until the next data bake picks this problem up, they are simply absent
  // rather than wrong.
  const declared = exps.length;
  const decided = exps.filter((e) => (e.verdict || '').trim().length > 0).length;
  const baked = declared > 0;

  const tabs: TabDef[] = [
    {
      id: 'summary',
      label: t('Summary', 'Resumen'),
      content: (
        <section>
          <p className="rs-lead">
            {t(
              'Goemans conjectured a cost version of the Dinitz-Garg-Goemans theorem: a fractional single-source flow can always be rounded to route each demand on ONE path, exceeding the fractional load on any arc by at most the largest demand AND without paying more. In July 2026 a counterexample was announced publicly, outside peer review. This programme verified that finite object independently, by exact rational enumeration, and then measured what the announcement did not state: how much violation the instance actually forces.',
              'Goemans conjeturo una version con costos del teorema de Dinitz-Garg-Goemans: un flujo fraccional de fuente unica siempre puede redondearse para enrutar cada demanda por UN camino, excediendo la carga fraccional en cualquier arco a lo mas en la demanda maxima Y sin pagar mas. En julio de 2026 se anuncio publicamente un contraejemplo, fuera de revision por pares. Este programa verifico ese objeto finito de forma independiente, por enumeracion racional exacta, y luego midio lo que el anuncio no declaro: cuanta violacion fuerza realmente la instancia.',
            )}
          </p>
          <Equation tex={String.raw`f^{\mathcal P}(a)\;\le\;x(a)+d_{\max}\quad\forall a\in A,\qquad\text{and}\qquad c^{\mathsf T}f^{\mathcal P}\;\le\;c^{\mathsf T}x`} />
          <p>
            {t(
              'The congestion half alone is a theorem ',
              'La mitad de congestion sola es un teorema ',
            )}
            <Cite id="dgg1999" />
            {t(
              '. The cost half alone is trivial (route everything on cheapest paths). The conjecture was that both hold at once, and it was proved when all demands are multiples of one another ',
              '. La mitad de costo sola es trivial (enrutar todo por caminos mas baratos). La conjetura decia que ambas valen a la vez, y fue probada cuando todas las demandas son multiplos entre si ',
            )}
            <Cite id="sku2002" />
            {t(', for series-parallel digraphs ', ', para digrafos serie-paralelo ')}
            <Cite id="msw2025" />
            {t(', and for planar graphs at twice the violation ', ', y para grafos planares al doble de la violacion ')}
            <Cite id="tvz2024" />.
          </p>
          <Callout variant="note" title={t('Result of this programme', 'Resultado de este programa')}>
            {t(
              'The conjecture is FALSE, verified here by our own exact enumeration on a 7-vertex instance: the fractional flow costs 58, and every one of the eight unsplittable routings either breaks the congestion bound or costs at least 60. The instance forces a violation of exactly 16/15 of the largest demand, so the conjecture fails by ONE unit and the question the literature calls the breakthrough target, whether cost-preserving rounding is possible with O(d_max) violation, is untouched.',
              'La conjetura es FALSA, verificada aqui por nuestra propia enumeracion exacta en una instancia de 7 vertices: el flujo fraccional cuesta 58, y cada uno de los ocho enrutamientos indivisibles rompe la cota de congestion o cuesta al menos 60. La instancia fuerza una violacion de exactamente 16/15 de la demanda maxima, asi que la conjetura falla por UNA unidad y la pregunta que la literatura llama el objetivo de ruptura, si el redondeo que preserva costo es posible con violacion O(d_max), queda intacta.',
            )}
          </Callout>
          <h3>{t('Manuscript', 'Manuscrito')}</h3>
          <ul>
            <li>
              <a href={`${REPO}/blob/main/manuscripts/unsplittable-flow-cost/counterexample-verification/main.pdf`} target="_blank" rel="noreferrer">
                {t(
                  'An independent exact verification of the 2026 counterexample to Goemans unsplittable-flow cost conjecture, with the violation constant it forces (preprint)',
                  'Una verificacion exacta e independiente del contraejemplo de 2026 a la conjetura de costo de flujo indivisible de Goemans, con la constante de violacion que fuerza (preprint)',
                )}
              </a>{' '}
              (<a href="https://doi.org/10.5281/zenodo.21554258" target="_blank" rel="noreferrer">DOI 10.5281/zenodo.21554258</a>
              {t(', concept DOI, always the latest version', ', DOI de concepto, siempre la ultima version')})
            </li>
          </ul>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['dgg1999', 'stvz2025', 'msw2025', 'tvz2024', 'rybin2026', 'ufcverification']} />
        </section>
      ),
    },
    {
      id: 'context',
      label: t('Context and history', 'Contexto e historia'),
      content: (
        <section>
          <p>
            {t(
              'Deciding whether an unsplittable flow respecting capacities exists at all is NP-hard, even on a two-vertex graph, so the field studies rounding with a bounded violation instead. Dinitz, Garg and Goemans proved in 1999 that the violation can always be kept to the largest demand ',
              'Decidir si existe un flujo indivisible que respete capacidades es NP-dificil, incluso en un grafo de dos vertices, asi que el area estudia el redondeo con violacion acotada. Dinitz, Garg y Goemans probaron en 1999 que la violacion siempre puede mantenerse en la demanda maxima ',
            )}
            <Cite id="dgg1999" />
            {t(
              '. Goemans conjectured shortly after that one can additionally never pay more than the fractional flow. Morell and Skutella later added arc-wise lower bounds, giving a cost-free and a cost-carrying strengthening ',
              '. Goemans conjeturo poco despues que ademas nunca hay que pagar mas que el flujo fraccional. Morell y Skutella agregaron luego cotas inferiores por arco, dando un fortalecimiento sin costos y otro con costos ',
            )}
            <Cite id="ms2022" />.
          </p>
          <p>
            {t(
              'As of October 2025 the primary literature recorded the conjecture as open in general and noted that proving even an O(d_max) version "would already be considered a breakthrough" ',
              'A octubre de 2025 la literatura primaria registraba la conjetura como abierta en general y notaba que probar incluso una version O(d_max) "ya se consideraria una ruptura" ',
            )}
            <Cite id="stvz2025" />
            {t(
              '. On 22-23 July 2026 a counterexample was announced publicly, attributed to work with a large language model ',
              '. El 22-23 de julio de 2026 se anuncio publicamente un contraejemplo, atribuido a trabajo con un modelo de lenguaje ',
            )}
            <Cite id="rybin2026" />
            {t(
              '. It carried no preprint and no expert confirmation, which is why this programme treated it as a hypothesis to decide by machine rather than as a status to report.',
              '. No traia preprint ni confirmacion experta, por eso este programa lo trato como una hipotesis a decidir por maquina y no como un estado a reportar.',
            )}
          </p>
          <Callout variant="note" title={t('How the adjudication was kept honest', 'Como se mantuvo honesta la adjudicacion')}>
            {t(
              'Our checker was written from the published conjecture statement, not from the proposer materials. Their verifier was archived and hashed but never imported or executed, and the instance was re-typed by hand rather than parsed from their file, so that agreement counts as evidence rather than as a shared-code artifact.',
              'Nuestro verificador se escribio desde el enunciado publicado de la conjetura, no desde los materiales del proponente. Su verificador fue archivado y hasheado pero nunca importado ni ejecutado, y la instancia se retipeo a mano en vez de leerse de su archivo, para que la coincidencia cuente como evidencia y no como artefacto de codigo compartido.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['dgg1999', 'ms2022', 'stvz2025', 'rybin2026']} />
        </section>
      ),
    },
    {
      id: 'mechanism',
      label: t('The mechanism', 'El mecanismo'),
      content: (
        <section>
          <p>
            {t(
              'The instance has three terminals with demands 15, 10 and 15, and exactly two routes each: an expensive direct arc, and a free detour along a shared spine. Each expensive choice costs exactly 30 when it carries its demand; each detour costs nothing.',
              'La instancia tiene tres terminales con demandas 15, 10 y 15, y exactamente dos rutas cada uno: un arco directo caro, y un desvio gratis por una espina compartida. Cada eleccion cara cuesta exactamente 30 al llevar su demanda; cada desvio no cuesta nada.',
            )}
          </p>
          <p>
            {t(
              'The three free detours are PAIRWISE incompatible with the congestion bound: any two of them overload some arc. So a congestion-good routing takes at most one of them, hence pays for at least two expensive choices, hence costs at least 60, while the fractional flow costs 58. The third conflict is the subtle one: two detours clash on the first spine arc only because the third terminal traverses that arc whichever route it takes.',
              'Los tres desvios gratis son incompatibles POR PARES con la cota de congestion: dos cualesquiera sobrecargan algun arco. Entonces un enrutamiento bueno en congestion toma a lo mas uno, paga al menos dos elecciones caras, y cuesta al menos 60, mientras el flujo fraccional cuesta 58. El tercer conflicto es el sutil: dos desvios chocan en el primer arco de la espina solo porque el tercer terminal atraviesa ese arco tome la ruta que tome.',
            )}
          </p>
          <p>
            {t(
              'Read structurally, the counterexample is not a flow phenomenon at all. Let the conflict graph have the free choices as nodes, joined when they cannot both be selected, and let rho be the fraction of each demand the fractional flow sends on its free choice:',
              'Leido estructuralmente, el contraejemplo no es un fenomeno de flujos. Sea el grafo de conflictos con las elecciones gratis como nodos, unidos cuando no pueden elegirse ambas, y sea rho la fraccion de cada demanda que el flujo fraccional envia por su eleccion gratis:',
            )}
          </p>
          <Equation tex={String.raw`\rho=\Big(\tfrac{5}{15},\tfrac{4}{10},\tfrac{5}{15}\Big)=\Big(\tfrac13,\tfrac25,\tfrac13\Big),\qquad \sum_i\rho_i=\tfrac{16}{15}>1`} />
          <p>
            {t(
              'A congestion-good routing selects an independent set of that triangle and so buys at most one unit of free routing, while the fractional flow buys 16/15. The instance is the linear-programming integrality gap of the stable-set polytope on a triangle, transported into flow language, with the arc costs acting as a nonnegative separator of the violated inequality.',
              'Un enrutamiento bueno en congestion selecciona un conjunto independiente de ese triangulo y compra a lo mas una unidad de ruteo gratis, mientras el flujo fraccional compra 16/15. La instancia es la brecha de integralidad del politopo de conjuntos estables sobre un triangulo, trasladada al lenguaje de flujos, con los costos de arco actuando como separador no negativo de la desigualdad violada.',
            )}
          </p>
          <Callout variant="note" title={t('Where the instance sits', 'Donde se ubica la instancia')}>
            {t(
              'Its underlying graph contains a K4 subdivision, and series-parallel digraphs, where the conjecture is proved, are exactly the K4-minor-free ones. So the counterexample sits one structure past the proved class. It is also planar, which pins the planar constant strictly between 1 (refuted here) and 2 (proved). Both facts are machine-checked.',
              'Su grafo subyacente contiene una subdivision de K4, y los digrafos serie-paralelo, donde la conjetura esta probada, son exactamente los libres de menor K4. Asi que el contraejemplo esta una estructura mas alla de la clase probada. Tambien es planar, lo que fija la constante planar estrictamente entre 1 (refutada aqui) y 2 (probada). Ambos hechos estan verificados por maquina.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['msw2025', 'tvz2024', 'ufcverification']} />
        </section>
      ),
    },
    {
      id: 'results',
      label: t('Results', 'Resultados'),
      content: (
        <section>
          <h3>{t('Machine-verified', 'Verificado por maquina')}</h3>
          <ul>
            <li>
              {t(
                'Goemans conjecture is FALSE. All eight routings enumerated by our own path search; the four congestion-good ones cost 90, 60, 60, 60 against a fractional cost of 58.',
                'La conjetura de Goemans es FALSA. Los ocho enrutamientos enumerados por nuestra propia busqueda de caminos; los cuatro buenos en congestion cuestan 90, 60, 60, 60 frente a un costo fraccional de 58.',
              )}
            </li>
            <li>
              {t(
                'The instance forces exactly 16/15 of the largest demand: 16 units of slack where the conjecture allows 15. The conjecture falls by one unit.',
                'La instancia fuerza exactamente 16/15 de la demanda maxima: 16 unidades de holgura donde la conjetura permite 15. La conjetura cae por una unidad.',
              )}
            </li>
            <li>
              {t(
                'The published cost vector is OPTIMAL for that graph and flow, in two senses: it maximises the cost gap and it maximises the violation forced. No reweighting of the arcs does better.',
                'El vector de costos publicado es OPTIMO para ese grafo y flujo, en dos sentidos: maximiza la brecha de costo y maximiza la violacion forzada. Ningun repesado de los arcos lo mejora.',
              )}
            </li>
            <li>
              {t(
                'The instance is acyclic, so the Morell-Skutella cost conjecture and the convex-combination form fall with it. Everything else proved in the area survives its direct test on the instance.',
                'La instancia es aciclica, asi que la conjetura con costos de Morell-Skutella y la forma de combinacion convexa caen con ella. Todo lo demas probado en el area sobrevive su prueba directa sobre la instancia.',
              )}
            </li>
            <li>
              {t(
                'No single-terminal instance is a counterexample, for any nonnegative cost vector (a theorem, machine-checked).',
                'Ninguna instancia de un solo terminal es contraejemplo, para ningun vector de costos no negativo (un teorema, verificado por maquina).',
              )}
            </li>
            <li>
              {t(
                'Over 3456 parameter points of the natural family that contains it, the ONLY counterexample is the published instance at exactly its published parameters. It is isolated and extremal in its own family.',
                'Sobre 3456 puntos de parametros de la familia natural que la contiene, el UNICO contraejemplo es la instancia publicada en exactamente sus parametros publicados. Es aislada y extremal en su propia familia.',
              )}
            </li>
          </ul>
          <h3>{t('Corrections kept in the record', 'Correcciones que quedan en el registro')}</h3>
          <p>
            {t(
              'A derivation claiming that no counterexample can have at most two terminals was recorded in round 1 and refuted in round 2: a terminal may have many path choices, so the conflict-graph argument does not apply as stated. It was flagged as suspect in the hypothesis of the experiment that tested it, and withdrawn in the verdict, the handoff and the manuscript. What replaces it is a sharp necessary condition at two terminals, and the two-terminal case is open.',
              'Una derivacion que afirmaba que ningun contraejemplo puede tener a lo mas dos terminales se registro en la ronda 1 y se refuto en la ronda 2: un terminal puede tener muchas elecciones de camino, asi que el argumento del grafo de conflictos no aplica como se enuncio. Fue marcada como sospechosa en la hipotesis del experimento que la probo, y retirada en el veredicto, el traspaso y el manuscrito. La reemplaza una condicion necesaria precisa con dos terminales, y el caso de dos terminales queda abierto.',
            )}
          </p>
        </section>
      ),
    },
    {
      id: 'experiments',
      label: t('Experiments', 'Experimentos'),
      content: (
        <section>
          <p>
            {t(
              'Every hypothesis is committed before its run; artifacts are written to disk; verdicts honour the machine, including refutations. Click a record to read its hypothesis and verdict.',
              'Cada hipotesis se compromete antes de su corrida; los artefactos se registran; los veredictos honran a la maquina, incluidas las refutaciones. Haz clic en un registro para leer su hipotesis y veredicto.',
            )}
          </p>
          {baked ? (
            <>
              <p>
                {t(
                  `${declared} experiments declared, ${decided} decided.`,
                  `${declared} experimentos declarados, ${decided} decididos.`,
                )}
              </p>
              <ul className="rs-explist">
                {exps.map((e) => (
                  <li key={e.slug}>
                    <button type="button" className="rs-linkbtn" onClick={() => setOpen(e)}>
                      {e.slug}
                    </button>
                    {e.verdict ? ` - ${e.verdict}` : ''}
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p>
              {t(
                'The experiment records for this problem appear here after the next data bake; until then they are readable in the repository.',
                'Los registros de experimentos de este problema apareceran aqui tras el proximo horneado de datos; mientras tanto son legibles en el repositorio.',
              )}{' '}
              <a href={`${REPO}/tree/main/problems/optimization-geometry/unsplittable-flow-cost/experiments`} target="_blank" rel="noreferrer">
                {t('Browse them on GitHub', 'Verlos en GitHub')}
              </a>
              .
            </p>
          )}
          <Suspense fallback={null}>{open ? <ExperimentModal exp={open} onClose={() => setOpen(null)} /> : null}</Suspense>
        </section>
      ),
    },
    {
      id: 'open',
      label: t('Open questions', 'Preguntas abiertas'),
      content: (
        <section>
          <p>
            {t(
              'A counterexample to the constant 1 settles far less than the coverage suggested. What remains open:',
              'Un contraejemplo a la constante 1 resuelve mucho menos de lo que sugirio la cobertura. Lo que queda abierto:',
            )}
          </p>
          <ul>
            <li>
              {t(
                'Does a cost-preserving rounding always exist with O(d_max) violation? No finite constant is known in general; the only upper bound anywhere is 2, for planar graphs. This is the question the literature calls a breakthrough target, and the counterexample does not touch it.',
                'Existe siempre un redondeo que preserva costo con violacion O(d_max)? No se conoce ninguna constante finita en general; la unica cota superior es 2, para grafos planares. Esta es la pregunta que la literatura llama objetivo de ruptura, y el contraejemplo no la toca.',
              )}
            </li>
            <li>
              {t(
                'What is the exact frontier constant? Known: at least 16/15 from this instance, at most 2 for planar graphs. The gap is almost everything.',
                'Cual es la constante frontera exacta? Se sabe: al menos 16/15 por esta instancia, a lo mas 2 para grafos planares. La brecha es casi todo.',
              )}
            </li>
            <li>
              {t(
                'The cost-free two-sided conjecture survives, and by a 2025 theorem it implies a cost statement at twice the violation. It is now the live route.',
                'La conjetura de dos lados sin costos sobrevive, y por un teorema de 2025 implica un enunciado con costos al doble de la violacion. Es ahora la ruta viva.',
              )}
            </li>
            <li>
              {t(
                'How small can a counterexample be? One terminal is impossible (a theorem here); two terminals is open with a necessary condition in hand; the published instance has three.',
                'Cuan pequeno puede ser un contraejemplo? Un terminal es imposible (un teorema aqui); dos terminales queda abierto con una condicion necesaria en mano; la instancia publicada tiene tres.',
              )}
            </li>
            <li>
              {t(
                'Is the coincidence between the stable-set violation and the forced violation, both 16/15 here, structural or accidental? Undecided.',
                'La coincidencia entre la violacion del conjunto estable y la violacion forzada, ambas 16/15 aqui, es estructural o accidental? Sin decidir.',
              )}
            </li>
          </ul>
          <Callout variant="note" title={t('Honest scope', 'Alcance honesto')}>
            {t(
              'The counterexample instance is not ours. What is ours is the independent exact verification, the constant it forces, the consistency battery against every proved result, the class-boundary and planar statements, the optimality of the published prices, the single-terminal theorem, and the null result showing the instance is extremal in its family. We make no claim about priority or attribution.',
              'La instancia del contraejemplo no es nuestra. Nuestro es la verificacion exacta independiente, la constante que fuerza, la bateria de consistencia contra cada resultado probado, los enunciados de frontera de clase y planaridad, la optimalidad de los precios publicados, el teorema de un terminal, y el resultado nulo que muestra que la instancia es extremal en su familia. No hacemos ninguna afirmacion sobre prioridad o atribucion.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['stvz2025', 'tvz2024', 'msw2025', 'ufcverification']} />
        </section>
      ),
    },
  ];

  return (
    <article className="rs-page">
      <header className="rs-head">
        <h1>{t('Goemans unsplittable-flow cost conjecture', 'Conjetura de costo de flujo indivisible de Goemans')}</h1>
        <p className="rs-sub">
          {t(
            'Optimization and discrete geometry - refuted 2026, verified here, with the frontier still open',
            'Optimizacion y geometria discreta - refutada en 2026, verificada aqui, con la frontera aun abierta',
          )}
        </p>
      </header>
      <Tabs tabs={tabs} />
    </article>
  );
}
