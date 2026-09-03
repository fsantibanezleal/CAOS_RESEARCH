import { Suspense, lazy, useEffect, useState } from 'react';
import { Callout, Cite, Equation, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, type ExperimentRec } from '../api/data';
const ExperimentModal = lazy(() => import('../components/ExperimentModal'));

const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = 'problems/combinatorics/petersen-coloring';

// Transcribed from the problem wiki (01-04) and the experiment verdicts EXP-001..004; every
// number here is traceable to a verdict file in the repository. The page computes nothing.
export default function PetersenColoring() {
  const t = useT();
  const [exps, setExps] = useState<ExperimentRec[]>([]);
  const [open, setOpen] = useState<ExperimentRec | null>(null);
  useEffect(() => {
    loadExperiments()
      .then((e) => setExps(e.filter((x) => x.problem === 'petersen-coloring')))
      .catch(() => setExps([]));
  }, []);
  const declared = exps.length;
  const decided = exps.filter((e) => (e.verdict || '').trim().length > 0).length;
  const baked = declared > 0;

  const auditRows: { en: string; es: string; g112: string; h112: string; g52: string; pet: string }[] = [
    { en: 'Berge-Fulkerson cover (6 perfect matchings, every edge twice)', es: 'Cubierta de Berge-Fulkerson (6 emparejamientos perfectos, cada arista dos veces)', g112: 'yes', h112: 'yes', g52: 'yes', pet: 'yes' },
    { en: 'Berge cover by 5 perfect matchings', es: 'Cubierta de Berge con 5 emparejamientos perfectos', g112: 'yes', h112: 'yes', g52: 'yes', pet: 'yes' },
    { en: 'Cover by 4 perfect matchings', es: 'Cubierta con 4 emparejamientos perfectos', g112: 'yes', h112: 'yes', g52: 'yes', pet: 'no (proof)' },
    { en: 'Perfect matching index', es: 'Indice de emparejamientos perfectos', g112: '4', h112: '4', g52: '4', pet: '5' },
    { en: 'Fan-Raspaud triple (3 perfect matchings, empty intersection)', es: 'Tripleta de Fan-Raspaud (3 emparejamientos perfectos, interseccion vacia)', g112: 'yes', h112: 'yes', g52: 'yes', pet: 'yes' },
    { en: '5-cycle double cover', es: 'Doble cubierta por 5 ciclos', g112: 'yes', h112: 'yes', g52: 'yes', pet: 'yes' },
    { en: 'Nowhere-zero 5-flow', es: 'Flujo 5 sin ceros', g112: 'yes', h112: 'yes', g52: 'yes', pet: 'yes' },
    { en: 'Nowhere-zero 4-flow (equivalently 3-edge-colorable)', es: 'Flujo 4 sin ceros (equivale a 3-arista-coloreable)', g112: 'no (proof)', h112: 'no (proof)', g52: 'no (proof)', pet: 'no (proof)' },
    { en: 'Oddness', es: 'Imparidad (oddness)', g112: '4', h112: '4', g52: '2', pet: '2' },
    { en: 'Resistance', es: 'Resistencia', g112: '3', h112: '3', g52: '2', pet: '2' },
  ];

  const tabs: TabDef[] = [
    {
      id: 'summary',
      label: t('Summary', 'Resumen'),
      content: (
        <section>
          <p className="rs-lead">
            {t(
              'Jaeger conjectured in 1988 that every bridgeless cubic graph admits a Petersen coloring: a map of its edges onto the edges of the Petersen graph sending every vertex star onto a vertex star. The conjecture implied the Berge-Fulkerson conjecture and the 5-cycle double cover conjecture. In August 2026 it was refuted: two 112-vertex counterexamples by Putman, a human-checkable proof by Jooken, and a 52-vertex counterexample with infinite families by Goedgebeur, Jooken, Macajova, Mattiolo and Mazzuoccolo. This programme certified the three retrievable counterexamples independently and audited, by exact proof-carrying computation, what the conjecture used to imply.',
              'Jaeger conjeturo en 1988 que todo grafo cubico sin puentes admite una coloracion de Petersen: un mapa de sus aristas sobre las aristas del grafo de Petersen que envia cada estrella de vertice sobre una estrella de vertice. La conjetura implicaba la conjetura de Berge-Fulkerson y la conjetura de la doble cubierta por 5 ciclos. En agosto de 2026 fue refutada: dos contraejemplos de 112 vertices de Putman, una prueba verificable a mano de Jooken, y un contraejemplo de 52 vertices con familias infinitas de Goedgebeur, Jooken, Macajova, Mattiolo y Mazzuoccolo. Este programa certifico de forma independiente los tres contraejemplos recuperables y audito, por computo exacto con certificados, lo que la conjetura solia implicar.',
            )}
          </p>
          <Equation tex={String.raw`\sigma : E(G)\to E(P),\qquad \sigma(\partial_G(v)) = \partial_P(w_v)\ \text{ for every } v\in V(G)`} />
          <p>
            {t('The conjecture is equivalent to the existence of a normal 5-edge-coloring ', 'La conjetura equivale a la existencia de una 5-arista-coloracion normal ')}
            <Cite id="jaeger1985" />
            {t(' and implies Berge-Fulkerson and the 5-cycle double cover conjecture ', ' e implica Berge-Fulkerson y la doble cubierta por 5 ciclos ')}
            <Cite id="jooken2026" />
            {t('. Every counterexample has at least 38 vertices ', '. Todo contraejemplo tiene al menos 38 vertices ')}
            <Cite id="bghm2013" />
            <Cite id="gms2019" />
            {t('; the smallest known has 52 ', '; el mas pequeno conocido tiene 52 ')}
            <Cite id="gjmmm2026" />.
          </p>
          <Callout variant="note" title={t('Result of this programme', 'Resultado de este programa')}>
            {t(
              'Every conjecture the Petersen coloring conjecture used to imply survives on all three retrievable counterexamples: each has a Berge-Fulkerson cover, a Fan-Raspaud triple, a 5-cycle double cover and a nowhere-zero 5-flow, given as explicit witnesses re-verified from the graph alone. Their perfect matching index is 4, one below the Petersen graph. The two 112-vertex graphs have oddness 4 and resistance 3; the 52-vertex graph has oddness 2 and resistance 2. Our own encodings, sharing no variable scheme with the public ones, refute all three graphs with drat-trim-verified proofs.',
              'Toda conjetura que la conjetura de coloracion de Petersen solia implicar sobrevive en los tres contraejemplos recuperables: cada uno tiene una cubierta de Berge-Fulkerson, una tripleta de Fan-Raspaud, una doble cubierta por 5 ciclos y un flujo 5 sin ceros, dados como testigos explicitos reverificados solo desde el grafo. Su indice de emparejamientos perfectos es 4, uno menos que el grafo de Petersen. Los dos grafos de 112 vertices tienen imparidad 4 y resistencia 3; el de 52 vertices tiene imparidad 2 y resistencia 2. Nuestras propias codificaciones, sin compartir esquema de variables con las publicas, refutan los tres grafos con pruebas verificadas por drat-trim.',
            )}
          </Callout>
          <h3>{t('Manuscript', 'Manuscrito')}</h3>
          <ul>
            <li>
              <a href={`${REPO}/blob/main/manuscripts/petersen-coloring/consequence-audit/main.pdf`} target="_blank" rel="noreferrer">
                {t(
                  'Berge-Fulkerson covers, cycle double covers, flows and exact normality defects of the first counterexamples to the Petersen coloring conjecture (preprint)',
                  'Cubiertas de Berge-Fulkerson, dobles cubiertas por ciclos, flujos y defectos exactos de normalidad de los primeros contraejemplos a la conjetura de coloracion de Petersen (preprint)',
                )}
              </a>{' '}
              (<Cite id="pccaudit" />)
            </li>
          </ul>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['jaeger1988', 'jaeger1985', 'putman2026', 'jooken2026', 'gjmmm2026', 'pccaudit']} />
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
              'A Petersen coloring maps the edges of a cubic graph G to the edges of the Petersen graph P so that the three edges at every vertex of G go bijectively onto the three edges at some vertex of P. Jaeger posed the conjecture in 1988 ',
              'Una coloracion de Petersen envia las aristas de un grafo cubico G a las aristas del grafo de Petersen P de modo que las tres aristas en cada vertice de G van biyectivamente sobre las tres aristas en algun vertice de P. Jaeger planteo la conjetura en 1988 ',
            )}
            <Cite id="jaeger1988" />
            {t(
              ' and had shown in 1985 that it is equivalent to a normal 5-edge-coloring: a proper coloring in which every edge sees three colors (poor) or five colors (rich) on its two end stars ',
              ' y habia mostrado en 1985 que equivale a una 5-arista-coloracion normal: una coloracion propia en la que cada arista ve tres colores (pobre) o cinco (rica) en sus dos estrellas extremas ',
            )}
            <Cite id="jaeger1985" />
            {t(
              '. Three-edge-colorable graphs are trivially colorable, so the conjecture is a statement about snarks. Exhaustive generation had verified it for every snark on at most 36 vertices ',
              '. Los grafos 3-arista-coloreables son trivialmente coloreables, asi que la conjetura es un enunciado sobre snarks. La generacion exhaustiva la habia verificado para todo snark de a lo mas 36 vertices ',
            )}
            <Cite id="bghm2013" />
            {t(' and for the weak snarks of girth 4 on 36 vertices ', ' y para los snarks debiles de cintura 4 en 36 vertices ')}
            <Cite id="gms2019" />.
          </p>
          <p>
            {t(
              'On 6 August 2026 Putman published a 112-vertex counterexample with SAT-solver certificates, assembled from copies of the Petersen graph minus two adjacent vertices (a 4-pole F) and claw connectors, plus a nonisomorphic D3-symmetric one ',
              'El 6 de agosto de 2026 Putman publico un contraejemplo de 112 vertices con certificados de un solucionador SAT, ensamblado con copias del grafo de Petersen menos dos vertices adyacentes (un 4-polo F) y conectores garra, mas uno no isomorfo con simetria D3 ',
            )}
            <Cite id="putman2026" />
            {t('. Jooken gave a proof a human can check ', '. Jooken dio una prueba verificable por una persona ')}
            <Cite id="jooken2026" />
            {t(
              ', and Goedgebeur, Jooken, Macajova, Mattiolo and Mazzuoccolo found a 52-vertex cyclically 4-edge-connected counterexample of girth 5 and infinite families, pinning the smallest counterexample between 38 and 52 vertices ',
              ', y Goedgebeur, Jooken, Macajova, Mattiolo y Mazzuoccolo hallaron un contraejemplo de 52 vertices ciclicamente 4-arista-conexo de cintura 5 y familias infinitas, fijando el contraejemplo mas pequeno entre 38 y 52 vertices ',
            )}
            <Cite id="gjmmm2026" />.
          </p>
          <Callout variant="note" title={t('Why an audit and not a minimality race', 'Por que una auditoria y no una carrera de minimalidad')}>
            {t(
              'The authors of the snark generators pinned the minimality window within days of the disproof. What nobody had reported was whether these first counterexamples still satisfy the conjectures the Petersen coloring conjecture used to imply. Those are finite questions on fixed graphs, with certificates on both sides, and they are what this record decides.',
              'Los autores de los generadores de snarks fijaron la ventana de minimalidad a dias de la refutacion. Lo que nadie habia reportado era si estos primeros contraejemplos siguen satisfaciendo las conjeturas que la conjetura de coloracion de Petersen solia implicar. Esas son preguntas finitas sobre grafos fijos, con certificados de ambos lados, y son lo que este registro decide.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['jaeger1988', 'jaeger1985', 'bghm2013', 'gms2019', 'putman2026', 'jooken2026', 'gjmmm2026']} />
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
              'Let Q be the line graph of the Petersen graph and F the 4-pole obtained from the Petersen graph by deleting the endpoints of one edge, with semi-edges i1, i2 (inputs) and o1, o2 (outputs). Jooken proved that every Petersen coloring of F places the two input labels at distance at most 2 in Q, and that the output labels are then determined: equal to the inputs at distance 0, copied at distance 1, and copied or both replaced by a canonical neighbour at distance 2.',
              'Sea Q el grafo de lineas del grafo de Petersen y F el 4-polo obtenido del grafo de Petersen al borrar los extremos de una arista, con semiaristas i1, i2 (entradas) y o1, o2 (salidas). Jooken probo que toda coloracion de Petersen de F pone las dos etiquetas de entrada a distancia a lo mas 2 en Q, y que las etiquetas de salida quedan determinadas: iguales a las entradas a distancia 0, copiadas a distancia 1, y copiadas o ambas reemplazadas por un vecino canonico a distancia 2.',
            )}
          </p>
          <Equation tex={String.raw`\mathrm{dist}_Q(\sigma(i_1),\sigma(i_2))\le 2,\qquad (\sigma(o_1),\sigma(o_2))\in R(\sigma(i_1),\sigma(i_2))`} />
          <p>
            {t(
              'Four copies of F around a claw form the 36-vertex 4-pole L, whose outputs are equal at input distance 0, copied at distance 1, and swapped at distance 2 or 3. Three copies of L around a claw then force four edges of P to be pairwise adjacent in Q, a 4-clique that the line graph of a triangle-free cubic graph cannot contain. That is the whole contradiction ',
              'Cuatro copias de F alrededor de una garra forman el 4-polo L de 36 vertices, cuyas salidas son iguales a distancia de entrada 0, copiadas a distancia 1, e intercambiadas a distancia 2 o 3. Tres copias de L alrededor de una garra fuerzan entonces cuatro aristas de P a ser adyacentes por pares en Q, un 4-clique que el grafo de lineas de un grafo cubico sin triangulos no puede contener. Esa es toda la contradiccion ',
            )}
            <Cite id="jooken2026" />
            {t(
              '. Goedgebeur and coauthors showed that F can be replaced by longer poles with the same coloring set, which gives the infinite families, and found the 52-vertex graph by a similar idea ',
              '. Goedgebeur y coautores mostraron que F puede reemplazarse por polos mas largos con el mismo conjunto de coloraciones, lo que da las familias infinitas, y hallaron el grafo de 52 vertices con una idea similar ',
            )}
            <Cite id="gjmmm2026" />.
          </p>
          <Callout variant="note" title={t('What the audit adds to the mechanism', 'Lo que la auditoria agrega al mecanismo')}>
            {t(
              'The obstruction is a distance rigidity in the line graph of P, not a covering obstruction: the same graphs are covered by four perfect matchings, better than the Petersen graph itself. And the two constructions differ in oddness (4 for the 112-vertex graphs, 2 for the 52-vertex graph) although both contain the same pole F.',
              'La obstruccion es una rigidez de distancias en el grafo de lineas de P, no una obstruccion de cubierta: los mismos grafos se cubren con cuatro emparejamientos perfectos, mejor que el propio grafo de Petersen. Y las dos construcciones difieren en imparidad (4 para los grafos de 112 vertices, 2 para el de 52) aunque ambas contienen el mismo polo F.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['jooken2026', 'gjmmm2026', 'putman2026']} />
        </section>
      ),
    },
    {
      id: 'results',
      label: t('Results', 'Resultados'),
      content: (
        <section>
          <h3>{t('Independent certification (EXP-001)', 'Certificacion independiente (EXP-001)')}</h3>
          <p>
            {t(
              'Our Petersen encoding uses edge-image variables with pairwise adjacency constraints (valid because the Petersen graph is triangle-free); our normal-5 encoding uses side-presence variables and a rich indicator. Neither shares a variable scheme with the public encoders. All six refutations carry DRAT proofs verified by drat-trim; five colorable controls are accepted; Putman public proofs verify under our checker; cyclic edge connectivity 4 is certified for all three graphs.',
              'Nuestra codificacion de Petersen usa variables de imagen de arista con restricciones de adyacencia por pares (valido porque el grafo de Petersen no tiene triangulos); nuestra codificacion normal-5 usa variables de presencia por lado y un indicador de riqueza. Ninguna comparte esquema de variables con los codificadores publicos. Las seis refutaciones llevan pruebas DRAT verificadas por drat-trim; cinco controles coloreables son aceptados; las pruebas publicas de Putman se verifican con nuestro verificador; la conectividad ciclica por aristas 4 esta certificada para los tres grafos.',
            )}
          </p>
          <h3>{t('The consequence audit (EXP-002, EXP-003)', 'La auditoria de consecuencias (EXP-002, EXP-003)')}</h3>
          <div className="rs-scroll">
            <table className="rs-table">
              <thead>
                <tr>
                  <th>{t('Property', 'Propiedad')}</th>
                  <th>G112</th>
                  <th>H112</th>
                  <th>G52</th>
                  <th>{t('Petersen (control)', 'Petersen (control)')}</th>
                </tr>
              </thead>
              <tbody>
                {auditRows.map((r) => (
                  <tr key={r.en}>
                    <td>{t(r.en, r.es)}</td>
                    <td className="num">{r.g112}</td>
                    <td className="num">{r.h112}</td>
                    <td className="num">{r.g52}</td>
                    <td className="num">{r.pet}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p>
            {t(
              'Every "yes" is an explicit witness re-verified by a checker that reads only the graph; every "no (proof)" and every lower bound of oddness and resistance is a DRAT proof checked by drat-trim. Oddness is decided exactly through the observation that a 2-coloring of the vertices of a 2-factor has at least one monochromatic edge on every odd cycle and none on even cycles:',
              'Cada "yes" es un testigo explicito reverificado por un verificador que lee solo el grafo; cada "no (proof)" y cada cota inferior de imparidad y resistencia es una prueba DRAT verificada por drat-trim. La imparidad se decide exactamente mediante la observacion de que una 2-coloracion de los vertices de un 2-factor tiene al menos una arista monocromatica en cada ciclo impar y ninguna en los pares:',
            )}
          </p>
          <Equation tex={String.raw`\mathrm{oddness}(G)=\min_{M,\ \mathrm{col}}\ \#\{\,e\in E\setminus M:\ \mathrm{col}(u_e)=\mathrm{col}(v_e)\,\}`} />
          <h3>{t('Predictions kept in the record', 'Predicciones que quedan en el registro')}</h3>
          <p>
            {t(
              'The committed prediction "perfect matching index 4" was right. The committed prediction "oddness 2 for all three" was refuted by the machine on the 112-vertex graphs (oddness 4, resistance 3) and is preserved as such in the verdict, the handoff and the manuscript.',
              'La prediccion comprometida "indice de emparejamientos perfectos 4" fue correcta. La prediccion comprometida "imparidad 2 para los tres" fue refutada por la maquina en los grafos de 112 vertices (imparidad 4, resistencia 3) y se conserva asi en el veredicto, el traspaso y el manuscrito.',
            )}
          </p>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['putman2026', 'gjmmm2026', 'gms2019', 'pccaudit']} />
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
              <p>{t(`${declared} experiments declared, ${decided} decided.`, `${declared} experimentos declarados, ${decided} decididos.`)}</p>
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
              <a href={`${REPO}/tree/main/${PROBLEM}/experiments`} target="_blank" rel="noreferrer">
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
          <ul>
            <li>
              {t(
                'The smallest counterexample: between 38 and 52 vertices. This record does not compete for it; a bounded search inside the gadget grammar (copies of F with small connectors) is the declared next line.',
                'El contraejemplo mas pequeno: entre 38 y 52 vertices. Este registro no compite por el; una busqueda acotada dentro de la gramatica de gadgets (copias de F con conectores pequenos) es la siguiente linea declarada.',
              )}
            </li>
            <li>
              {t(
                'Cyclically 5-edge-connected counterexamples (Problem 5 of Goedgebeur and coauthors): open.',
                'Contraejemplos ciclicamente 5-arista-conexos (Problema 5 de Goedgebeur y coautores): abierto.',
              )}
            </li>
            <li>
              {t(
                'Does every bridgeless cubic graph have a normal 6-edge-coloring? Open in general; decided on the three counterexamples in EXP-004.',
                'Todo grafo cubico sin puentes tiene una 6-arista-coloracion normal? Abierto en general; decidido en los tres contraejemplos en EXP-004.',
              )}
            </li>
            <li>
              {t(
                'Is perfect matching index 4 forced for every graph built from the pole F? Does oddness stay 4 along the infinite family grown from the 112-vertex graphs and 2 along the family grown from the 52-vertex graph?',
                'Esta forzado el indice de emparejamientos perfectos 4 para todo grafo construido desde el polo F? Se mantiene la imparidad en 4 a lo largo de la familia infinita crecida desde los grafos de 112 vertices y en 2 en la familia crecida desde el de 52?',
              )}
            </li>
          </ul>
          <Callout variant="note" title={t('Honest scope', 'Alcance honesto')}>
            {t(
              'The counterexamples are not ours: discovery priority belongs to Putman, to Goedgebeur, Jooken, Macajova, Mattiolo and Mazzuoccolo, and to Jooken for the human-checkable proof. What is ours is the independent certification with a second encoding, and the audit: perfect matching covers and index, cycle double covers, flows, oddness, resistance, normal 6-edge-colorings and exact defects, each with a certificate. Nothing here bears on the general conjectures beyond these three graphs.',
              'Los contraejemplos no son nuestros: la prioridad de descubrimiento pertenece a Putman, a Goedgebeur, Jooken, Macajova, Mattiolo y Mazzuoccolo, y a Jooken por la prueba verificable a mano. Nuestro es la certificacion independiente con una segunda codificacion, y la auditoria: cubiertas e indice de emparejamientos perfectos, dobles cubiertas por ciclos, flujos, imparidad, resistencia, 6-arista-coloraciones normales y defectos exactos, cada uno con certificado. Nada aqui incide en las conjeturas generales mas alla de estos tres grafos.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['gjmmm2026', 'mazzmkrt2020', 'pccaudit']} />
        </section>
      ),
    },
  ];

  return (
    <article className="rs-page">
      <header className="rs-head">
        <h1>{t('Petersen coloring counterexamples', 'Contraejemplos a la coloracion de Petersen')}</h1>
        <p className="rs-sub">
          {t(
            'Combinatorics and graph theory - conjecture refuted 2026, counterexamples certified and audited here',
            'Combinatoria y teoria de grafos - conjetura refutada en 2026, contraejemplos certificados y auditados aqui',
          )}
        </p>
      </header>
      <Tabs tabs={tabs} />
    </article>
  );
}
