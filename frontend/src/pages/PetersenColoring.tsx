import { Suspense, lazy, useEffect, useState } from 'react';
import { Callout, Cite, Equation, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, type ExperimentRec } from '../api/data';
const ExperimentModal = lazy(() => import('../components/ExperimentModal'));

const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';
const PROBLEM = 'problems/combinatorics/petersen-coloring';

// Transcribed from the problem wiki (01-07) and the experiment verdicts EXP-001..010; every
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

  const auditRows: { en: string; es: string; g112: string; h112: string; g52: string; g52b: string; g68: string; pet: string }[] = [
    { en: 'Berge-Fulkerson cover (6 perfect matchings, every edge twice)', es: 'Cubierta de Berge-Fulkerson (6 emparejamientos perfectos, cada arista dos veces)', g112: 'yes', h112: 'yes', g52: 'yes', g52b: 'yes', g68: 'yes', pet: 'yes' },
    { en: 'Berge cover by 5 perfect matchings', es: 'Cubierta de Berge con 5 emparejamientos perfectos', g112: 'yes', h112: 'yes', g52: 'yes', g52b: 'yes', g68: 'yes', pet: 'yes' },
    { en: 'Cover by 4 perfect matchings', es: 'Cubierta con 4 emparejamientos perfectos', g112: 'yes', h112: 'yes', g52: 'yes', g52b: 'yes', g68: 'yes', pet: 'no (proof)' },
    { en: 'Perfect matching index', es: 'Indice de emparejamientos perfectos', g112: '4', h112: '4', g52: '4', g52b: '4', g68: '4', pet: '5' },
    { en: 'Fan-Raspaud triple (3 perfect matchings, empty intersection)', es: 'Tripleta de Fan-Raspaud (3 emparejamientos perfectos, interseccion vacia)', g112: 'yes', h112: 'yes', g52: 'yes', g52b: 'yes', g68: 'yes', pet: 'yes' },
    { en: '5-cycle double cover', es: 'Doble cubierta por 5 ciclos', g112: 'yes', h112: 'yes', g52: 'yes', g52b: 'yes', g68: 'yes', pet: 'yes' },
    { en: 'Nowhere-zero 5-flow', es: 'Flujo 5 sin ceros', g112: 'yes', h112: 'yes', g52: 'yes', g52b: 'yes', g68: 'yes', pet: 'yes' },
    { en: 'Nowhere-zero 4-flow (equivalently 3-edge-colorable)', es: 'Flujo 4 sin ceros (equivale a 3-arista-coloreable)', g112: 'no (proof)', h112: 'no (proof)', g52: 'no (proof)', g52b: 'no (proof)', g68: 'no (proof)', pet: 'no (proof)' },
    { en: 'Oddness', es: 'Imparidad (oddness)', g112: '4', h112: '4', g52: '2', g52b: '2', g68: '2', pet: '2' },
    { en: 'Resistance', es: 'Resistencia', g112: '3', h112: '3', g52: '2', g52b: '2', g68: '2', pet: '2' },
  ];

  // Transcribed from the EXP-007 verdict (decided target orders and the two forms of the statement).
  const h3En = 'PENDING-EXP-007-VERDICT';
  const h3Es = 'PENDING-EXP-007-VERDICT';

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
            {t('. Every counterexample has at least 40 vertices ', '. Todo contraejemplo tiene al menos 40 vertices ')}
            <Cite id="gjmmmu2026" />
            {t('; the smallest known have 52 ', '; los mas pequenos conocidos tienen 52 ')}
            <Cite id="gjmmm2026" />.
          </p>
          <Callout variant="note" title={t('Second round (September 2026)', 'Segunda ronda (septiembre de 2026)')}>
            {t(
              'Three additions. First, the audit now covers all five retrievable counterexamples (the second 52-vertex graph and the 68-vertex graph were added from the House of Graphs); every value agrees with the first 52-vertex graph. Second, the question of Goedgebeur and coauthors "are the 52-vertex counterexamples colorable only by themselves?" is attacked with two new lemmas on the fibers of a coloring by an unknown cubic graph, which turn it into a finite list of certified refutations. Third, the Petersen defect and the number of abnormal edges are unbounded: rings and frames of counterexamples need one bad vertex per block, which refutes two of the five statements of the sublinear approximation conjecture of Mattiolo, Mazzuoccolo and Mkrtchyan and reduces the conjecture to a single question on cyclically 4-edge-connected graphs.',
              'Tres adiciones. Primero, la auditoria cubre ahora los cinco contraejemplos recuperables (el segundo grafo de 52 vertices y el de 68 vertices se agregaron desde House of Graphs); todos los valores coinciden con el primer grafo de 52 vertices. Segundo, la pregunta de Goedgebeur y coautores "son los contraejemplos de 52 vertices coloreables solo por si mismos?" se ataca con dos lemas nuevos sobre las fibras de una coloracion por un grafo cubico desconocido, que la convierten en una lista finita de refutaciones certificadas. Tercero, el defecto de Petersen y el numero de aristas anormales no estan acotados: anillos y marcos de contraejemplos necesitan un vertice malo por bloque, lo que refuta dos de los cinco enunciados de la conjetura de aproximacion sublineal de Mattiolo, Mazzuoccolo y Mkrtchyan y reduce la conjetura a una sola pregunta sobre grafos ciclicamente 4-arista-conexos.',
            )}
          </Callout>
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
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['jaeger1988', 'jaeger1985', 'putman2026', 'jooken2026', 'gjmmm2026', 'gjmmmu2026', 'pccaudit']} />
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
          <p>
            {t(
              'The extended account of 11 September 2026 adds a second 52-vertex counterexample, a purely theoretical proof for both, counterexamples of every even order at least 60, and raises the lower bound to 40 by an exhaustive check of the weak snarks on 38 vertices. For five graphs it also reports Berge-Fulkerson covers, perfect matching index at most 4, 5-cycle double covers, strong normal 6-edge-colorings and colorings with exactly two abnormal edges; those items were obtained here independently (for the first three graphs on 3 September). It asks whether the 52-vertex graphs are colorable only by themselves ',
              'El relato ampliado del 11 de septiembre de 2026 agrega un segundo contraejemplo de 52 vertices, una prueba puramente teorica para ambos, contraejemplos de todo orden par desde 60, y sube la cota inferior a 40 mediante una revision exhaustiva de los snarks debiles de 38 vertices. Para cinco grafos reporta ademas cubiertas de Berge-Fulkerson, indice de emparejamientos perfectos a lo mas 4, dobles cubiertas por 5 ciclos, 6-arista-coloraciones normales fuertes y coloraciones con exactamente dos aristas anormales; esos puntos se obtuvieron aqui de forma independiente (para los tres primeros grafos el 3 de septiembre). Pregunta si los grafos de 52 vertices son coloreables solo por si mismos ',
            )}
            <Cite id="gjmmmu2026" />.
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
              'Our Petersen encoding uses edge-image variables with pairwise adjacency constraints (valid because the Petersen graph is triangle-free); our normal-5 encoding uses side-presence variables and a rich indicator. Neither shares a variable scheme with the public encoders. All ten refutations (five graphs, two encodings) carry DRAT proofs verified by drat-trim; five colorable controls are accepted; Putman public proofs verify under our checker; cyclic edge connectivity 4 is certified for all five graphs.',
              'Nuestra codificacion de Petersen usa variables de imagen de arista con restricciones de adyacencia por pares (valido porque el grafo de Petersen no tiene triangulos); nuestra codificacion normal-5 usa variables de presencia por lado y un indicador de riqueza. Ninguna comparte esquema de variables con los codificadores publicos. Las diez refutaciones (cinco grafos, dos codificaciones) llevan pruebas DRAT verificadas por drat-trim; cinco controles coloreables son aceptados; las pruebas publicas de Putman se verifican con nuestro verificador; la conectividad ciclica por aristas 4 esta certificada para los cinco grafos.',
            )}
          </p>
          <h3>{t('The consequence audit (EXP-002, EXP-003, EXP-008)', 'La auditoria de consecuencias (EXP-002, EXP-003, EXP-008)')}</h3>
          <div className="rs-scroll">
            <table className="rs-table">
              <thead>
                <tr>
                  <th>{t('Property', 'Propiedad')}</th>
                  <th>G112</th>
                  <th>H112</th>
                  <th>G52</th>
                  <th>G52b</th>
                  <th>G68</th>
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
                    <td className="num">{r.g52b}</td>
                    <td className="num">{r.g68}</td>
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
          <h3>{t('How far from colorable: the Petersen defect (EXP-004, EXP-006)', 'Cuan lejos de coloreable: el defecto de Petersen (EXP-004, EXP-006)')}</h3>
          <p>
            {t(
              'All three graphs admit normal and strong normal 6-edge-colorings, so their normal chromatic index is exactly 6. Define the Petersen defect as the least number of vertices at which the star condition must fail over all edge maps into the Petersen graph. A parity argument shows the defect is never exactly 1 for any cubic graph: the label vectors of the bad vertices sum to an element of the cut space of the Petersen graph, and an odd cut of size 1 or 3 there is a star. So every counterexample has defect at least 2. The 52-vertex graph attains 2, and does so at every one of its 1,326 vertex pairs (explicit witnesses; all 52 single-vertex relaxations refuted with checked proofs); both 112-vertex graphs attain 2 at every pair of their 16 vertices outside the twelve disjoint copies of F.',
              'Los tres grafos admiten 6-arista-coloraciones normales y normales fuertes, asi que su indice cromatico normal es exactamente 6. Definase el defecto de Petersen como el menor numero de vertices en los que la condicion de estrella debe fallar sobre todos los mapas de aristas al grafo de Petersen. Un argumento de paridad muestra que el defecto nunca es exactamente 1 para ningun grafo cubico: los vectores de etiquetas de los vertices malos suman un elemento del espacio de cortes del grafo de Petersen, y un corte impar de tamano 1 o 3 alli es una estrella. Asi, todo contraejemplo tiene defecto al menos 2. El grafo de 52 vertices lo alcanza, y lo hace en cada uno de sus 1.326 pares de vertices (testigos explicitos; las 52 relajaciones de un solo vertice refutadas con pruebas verificadas); ambos grafos de 112 vertices lo alcanzan en cada par de sus 16 vertices fuera de las doce copias disjuntas de F.',
            )}
          </p>
          <Equation tex={String.raw`\sum_{v\ \mathrm{bad}} \chi_v \;=\; \sum_{u\ \mathrm{good}} \chi(\partial_P(w_u)) \;\in\; \mathrm{Cut}(P)\subset\mathbb F_2^{E(P)}`} />
          <p>
            {t(
              'The full sweeps of the 112-vertex graphs (6,216 pairs each) and of the two graphs added in the second round (1,326 pairs for the second 52-vertex graph; the sweep of the 68-vertex graph is reported in EXP-008) found every pair critical: relaxing the star condition at any two vertices restores colorability. On the 1,326 stored witnesses of the first 52-vertex graph the label vectors of the two bad vertices always lie in the same nonzero class modulo the cut space, as the parity argument requires.',
              'Los barridos completos de los grafos de 112 vertices (6.216 pares cada uno) y de los dos grafos agregados en la segunda ronda (1.326 pares para el segundo grafo de 52 vertices; el barrido del grafo de 68 vertices se reporta en EXP-008) hallaron todos los pares criticos: relajar la condicion de estrella en dos vertices cualesquiera restaura la colorabilidad. En los 1.326 testigos guardados del primer grafo de 52 vertices los vectores de etiquetas de los dos vertices malos estan siempre en la misma clase no nula modulo el espacio de cortes, como exige el argumento de paridad.',
            )}
          </p>
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
      id: 'onlyitself',
      label: t('Colorable only by itself', 'Coloreable solo por si mismo'),
      content: (
        <section>
          <p>
            {t(
              'For cubic graphs G and H (parallel edges allowed in H), an H-coloring of G maps the edges of G to the edges of H so that every vertex star of G goes bijectively onto a vertex star of H. A Petersen coloring is a P-coloring, and the relation "H colors G" is transitive, so a graph that colors a counterexample is itself a counterexample. Ma, Mattiolo, Steffen and Wolf proved that there is a unique minimal set of connected bridgeless cubic graphs coloring every bridgeless cubic graph, and that a graph belongs to it exactly when no smaller bridgeless cubic graph colors it ',
              'Para grafos cubicos G y H (con aristas paralelas permitidas en H), una H-coloracion de G envia las aristas de G a las aristas de H de modo que cada estrella de vertice de G va biyectivamente sobre una estrella de vertice de H. Una coloracion de Petersen es una P-coloracion, y la relacion "H colorea a G" es transitiva, asi que un grafo que colorea a un contraejemplo es el mismo un contraejemplo. Ma, Mattiolo, Steffen y Wolf probaron que existe un unico conjunto minimal de grafos cubicos conexos sin puentes que colorea a todo grafo cubico sin puentes, y que un grafo pertenece a el exactamente cuando ningun grafo cubico sin puentes mas pequeno lo colorea ',
            )}
            <Cite id="mmsw2025" />
            {t(
              '. The conjecture was the statement that this set is the Petersen graph alone; after the disproof the set is infinite. Goedgebeur and coauthors ask whether their 52-vertex counterexamples are colorable only by themselves, a necessary condition for being smallest counterexamples ',
              '. La conjetura era el enunciado de que este conjunto es solo el grafo de Petersen; tras la refutacion el conjunto es infinito. Goedgebeur y coautores preguntan si sus contraejemplos de 52 vertices son coloreables solo por si mismos, condicion necesaria para ser contraejemplos minimos ',
            )}
            <Cite id="gjmmmu2026" />.
          </p>
          <h3>{t('Two lemmas on the fibers of the vertex map', 'Dos lemas sobre las fibras del mapa de vertices')}</h3>
          <p>
            {t(
              'Let phi be the vertex map of an H-coloring f, and n_x the number of vertices of G sent to the vertex x of H. Lemma A: for every edge e = xy of H the preimage of e is a perfect matching of the subgraph of G induced on the two fibers, because a vertex meets an edge of image e exactly when its image is x or y, and then exactly one. Hence n_x + n_y is even on every edge, and all fibers have the same parity when H is connected.',
              'Sea phi el mapa de vertices de una H-coloracion f, y n_x el numero de vertices de G enviados al vertice x de H. Lema A: para cada arista e = xy de H la preimagen de e es un emparejamiento perfecto del subgrafo de G inducido en las dos fibras, porque un vertice toca una arista de imagen e exactamente cuando su imagen es x o y, y entonces toca exactamente una. Por lo tanto n_x + n_y es par en cada arista, y todas las fibras tienen la misma paridad cuando H es conexo.',
            )}
          </p>
          <Equation tex={String.raw`f^{-1}(xy)\ \text{is a perfect matching of}\ G[\varphi^{-1}(x)\cup\varphi^{-1}(y)]\quad\Longrightarrow\quad n_x\equiv n_y \pmod 2`} />
          <p>
            {t(
              'Lemma B: if a connected bridgeless cubic graph H colors G and some vertices of H are not used, then a connected bridgeless cubic graph with the same used vertices and at most one unused vertex also colors G. The proof identifies the unused vertices to one vertex and splits it back to degree 3 (or removes it) with the splitting lemma of Fleischner, in the bridgeless form of Kaiser, Kuzel, Li and Wang ',
              'Lema B: si un grafo cubico conexo sin puentes H colorea a G y algunos vertices de H no se usan, entonces un grafo cubico conexo sin puentes con los mismos vertices usados y a lo mas un vertice sin usar tambien colorea a G. La prueba identifica los vertices sin usar en uno solo y lo vuelve a dividir hasta grado 3 (o lo elimina) con el lema de division de Fleischner, en la forma sin puentes de Kaiser, Kuzel, Li y Wang ',
            )}
            <Cite id="kaiser2007" />
            {t(
              '. So the search has three kinds only: all fibers odd and every target vertex used; all fibers even and every target vertex used (at most n/2 of them); all fibers even with exactly one unused target vertex.',
              '. Asi, la busqueda tiene solo tres tipos: todas las fibras impares y todo vertice del blanco usado; todas las fibras pares y todo vertice del blanco usado (a lo mas n/2); todas las fibras pares con exactamente un vertice del blanco sin usar.',
            )}
          </p>
          <Callout variant="note" title={t('Why the lemmas decide the computation', 'Por que los lemas deciden el computo')}>
            {t(
              'Without them the unknown target graph has a part that the graph G does not constrain. On the 52-vertex graph the lazy loop that excludes disconnected or bridged targets learned about two thousand cuts per target order in half an hour and decided nothing. With the lemmas every edge of the target is the image of an edge of G, and every decided order was refuted without a single cut. The two encodings agree on all 21 control instances (K4, the prism, the Petersen graph, the flower snarks J3 and J5, every even order below their own).',
              'Sin ellos el grafo blanco desconocido tiene una parte que el grafo G no restringe. En el grafo de 52 vertices el ciclo perezoso que excluye blancos desconexos o con puentes aprendio cerca de dos mil cortes por orden del blanco en media hora y no decidio nada. Con los lemas cada arista del blanco es imagen de una arista de G, y cada orden decidido se refuto sin un solo corte. Las dos codificaciones coinciden en las 21 instancias de control (K4, el prisma, el grafo de Petersen, los snarks flor J3 y J5, todo orden par bajo el propio).',
            )}
          </Callout>
          <h3>{t('Result (EXP-007)', 'Resultado (EXP-007)')}</h3>
          <p>{t(h3En, h3Es)}</p>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['mmsw2025', 'gjmmmu2026', 'kaiser2007', 'hog2023']} />
        </section>
      ),
    },
    {
      id: 'defects',
      label: t('Large defects', 'Defectos grandes'),
      content: (
        <section>
          <p>
            {t(
              'Two numbers measure the distance from a Petersen coloring: the Petersen defect pd (the least number of vertices at which an edge map into the Petersen graph fails the star condition) and ab, the least number of abnormal edges (neither poor nor rich) of a proper 5-edge-coloring. Mattiolo, Mazzuoccolo and Mkrtchyan proved that ab is never 1 and asked whether ab at most 2 forces a normal 5-edge-coloring; the five counterexamples show that it does not ',
              'Dos numeros miden la distancia a una coloracion de Petersen: el defecto de Petersen pd (el menor numero de vertices en los que un mapa de aristas al grafo de Petersen falla la condicion de estrella) y ab, el menor numero de aristas anormales (ni pobres ni ricas) de una 5-arista-coloracion propia. Mattiolo, Mazzuoccolo y Mkrtchyan probaron que ab nunca es 1 y preguntaron si ab a lo mas 2 fuerza una 5-arista-coloracion normal; los cinco contraejemplos muestran que no ',
            )}
            <Cite id="mmm2021" />
            <Cite id="gjmmmu2026" />.
          </p>
          <Equation tex={String.raw`\mathrm{pd}(G)\;\le\;\mathrm{ab}(G),\qquad \mathrm{pd}=\mathrm{ab}=2\ \text{ on } G_{112},\,H_{112},\,G_{52},\,G'_{52},\,G_{68}`} />
          <p>
            {t(
              'The inequality comes from the Kneser model of the Petersen graph: a proper 5-edge-coloring gives every vertex the 2-set of its missing colors and every edge, seen from one end, the Petersen edge at that 2-set with the color of the edge; the two views of a poor or rich edge agree, so only one end of each abnormal edge can be bad. With the parity theorem this reproves that ab is never 1.',
              'La desigualdad viene del modelo de Kneser del grafo de Petersen: una 5-arista-coloracion propia da a cada vertice el 2-conjunto de sus colores faltantes y a cada arista, vista desde un extremo, la arista de Petersen en ese 2-conjunto con el color de la arista; las dos vistas de una arista pobre o rica coinciden, asi que solo un extremo de cada arista anormal puede ser malo. Con el teorema de paridad esto vuelve a probar que ab nunca es 1.',
            )}
          </p>
          <h3>{t('Rings and frames: one bad vertex per block', 'Anillos y marcos: un vertice malo por bloque')}</h3>
          <p>
            {t(
              'Open t counterexamples at one edge each and join them cyclically through 2-edge cuts. If a block had only good vertices, the sum of its label vectors would be a sum of stars of P, hence a cut of P, equal to the two labels leaving the block; a cut with at most two edges is empty in a 3-edge-connected graph, so the labels agree and the opened edge can be restored: a Petersen coloring of the block. The same argument with three leaving labels (an odd cut of the Petersen graph with at most three edges is a star) handles a cubic frame whose vertices are replaced by counterexamples minus a vertex, which keeps 3-connectivity.',
              'Abra t contraejemplos en una arista cada uno y unalos ciclicamente por cortes de 2 aristas. Si un bloque tuviera solo vertices buenos, la suma de sus vectores de etiquetas seria una suma de estrellas de P, por lo tanto un corte de P, igual a las dos etiquetas que salen del bloque; un corte con a lo mas dos aristas es vacio en un grafo 3-arista-conexo, asi que las etiquetas coinciden y la arista abierta se puede restaurar: una coloracion de Petersen del bloque. El mismo argumento con tres etiquetas salientes (un corte impar del grafo de Petersen con a lo mas tres aristas es una estrella) cubre un marco cubico cuyos vertices se reemplazan por contraejemplos menos un vertice, lo que conserva la 3-conexidad.',
            )}
          </p>
          <Equation tex={String.raw`\mathrm{ab}(R_t)\;\ge\;\mathrm{pd}(R_t)\;\ge\;t,\qquad |V(R_t)| = 52\,t`} />
          <div className="rs-scroll">
            <table className="rs-table">
              <thead>
                <tr>
                  <th>{t('Graph', 'Grafo')}</th>
                  <th>{t('Order', 'Orden')}</th>
                  <th>{t('Connectivity', 'Conexidad')}</th>
                  <th>pd</th>
                  <th>ab</th>
                </tr>
              </thead>
              <tbody>
                <tr><td>{t('Ring of 2 copies of G52', 'Anillo de 2 copias de G52')}</td><td className="num">104</td><td className="num">2</td><td className="num">2</td><td className="num">2 to 4</td></tr>
                <tr><td>{t('Ring of 3 copies', 'Anillo de 3 copias')}</td><td className="num">156</td><td className="num">2</td><td className="num">3</td><td className="num">{t('at least 3', 'al menos 3')}</td></tr>
                <tr><td>{t('Ring of 4 copies', 'Anillo de 4 copias')}</td><td className="num">208</td><td className="num">2</td><td className="num">4</td><td className="num">{t('at least 4', 'al menos 4')}</td></tr>
                <tr><td>{t('K4 frame of G52 minus a vertex', 'Marco K4 de G52 menos un vertice')}</td><td className="num">204</td><td className="num">3</td><td className="num">4</td><td className="num">{t('at least 4', 'al menos 4')}</td></tr>
              </tbody>
            </table>
          </div>
          <p>
            {t(
              'Every witness has exactly one bad vertex in each block (EXP-009); twenty relaxations of the 2-ring at two vertices of the same block were refuted with checked proofs, as the theorem predicts; rings and frames of the Petersen-colorable snark J5 are colorable (controls).',
              'Cada testigo tiene exactamente un vertice malo en cada bloque (EXP-009); veinte relajaciones del 2-anillo en dos vertices del mismo bloque se refutaron con pruebas verificadas, como predice el teorema; anillos y marcos del snark J5, coloreable por Petersen, son coloreables (controles).',
            )}
          </p>
          <h3>{t('Consequence: sublinear approximations', 'Consecuencia: aproximaciones sublineales')}</h3>
          <p>
            {t(
              'Mattiolo, Mazzuoccolo and Mkrtchyan conjectured that five statements are equivalent: the Petersen coloring conjecture, and the existence of a sublinear bound on ab for all bridgeless, all 2-connected, all 3-connected, and all cyclically 4-edge-connected cubic graphs. They used the same ring and frame constructions with a weaker conclusion (a block without abnormal edges gives a coloring of the block with at most 5 or 7 abnormal edges). The cut-space argument gives a genuine Petersen coloring of the block, so on 2-connected and on 3-connected cubic graphs a sublinear bound exists only if every graph of the class is normally 5-edge-colorable, which the 52-vertex graph refutes. The first four statements are therefore false, and the conjectured equivalence now amounts to one question: is there a cyclically 4-edge-connected cubic graph with ab at least 10? A smaller target suffices: one such graph with Petersen defect at least 3 would do, because every 4-pole obtained from it by deleting two edges would then be non-colorable and could be chained.',
              'Mattiolo, Mazzuoccolo y Mkrtchyan conjeturaron que cinco enunciados son equivalentes: la conjetura de coloracion de Petersen, y la existencia de una cota sublineal para ab en todos los grafos cubicos sin puentes, 2-conexos, 3-conexos y ciclicamente 4-arista-conexos. Usaron las mismas construcciones de anillo y marco con una conclusion mas debil (un bloque sin aristas anormales da una coloracion del bloque con a lo mas 5 o 7 aristas anormales). El argumento del espacio de cortes da una coloracion de Petersen genuina del bloque, asi que en los grafos cubicos 2-conexos y en los 3-conexos existe una cota sublineal solo si todo grafo de la clase es normalmente 5-arista-coloreable, lo que el grafo de 52 vertices refuta. Los cuatro primeros enunciados son entonces falsos, y la equivalencia conjeturada equivale ahora a una sola pregunta: existe un grafo cubico ciclicamente 4-arista-conexo con ab al menos 10? Basta un objetivo menor: un grafo asi con defecto de Petersen al menos 3, porque todo 4-polo obtenido de el al borrar dos aristas seria no coloreable y se podria encadenar.',
            )}
          </p>
          <Callout variant="note" title={t('What the search found on the known graphs (EXP-010)', 'Lo que la busqueda hallo en los grafos conocidos (EXP-010)')}>
            {t(
              'Every 4-pole obtained from the two 52-vertex graphs and from the 68-vertex graph by deleting two independent edges is Petersen colorable (482, 482 and 4,947 orbit representatives), with exactly the two boundary patterns the cut space allows: two crossed equal pairs, or the four edges around one edge of the Petersen graph. A 4-pole with a crossed pattern can be chained around a ring with an even number of copies, so those cyclic joins are Petersen colorable. Dot products of the 52-vertex graph with itself are new 102-vertex counterexamples, all with defect 2. The question stays open.',
              'Todo 4-polo obtenido de los dos grafos de 52 vertices y del de 68 vertices al borrar dos aristas independientes es coloreable por Petersen (482, 482 y 4.947 representantes de orbita), con exactamente los dos patrones de borde que el espacio de cortes permite: dos pares iguales cruzados, o las cuatro aristas alrededor de una arista del grafo de Petersen. Un 4-polo con patron cruzado se puede encadenar alrededor de un anillo con un numero par de copias, asi que esas uniones ciclicas son coloreables por Petersen. Los productos punto del grafo de 52 vertices consigo mismo son contraejemplos nuevos de 102 vertices, todos con defecto 2. La pregunta sigue abierta.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['mmm2021', 'gjmmmu2026', 'pccaudit']} />
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
                'The smallest counterexample: between 40 and 52 vertices. A smallest counterexample is colorable only by itself, which is the property tested in the second round for the 52-vertex graphs.',
                'El contraejemplo mas pequeno: entre 40 y 52 vertices. Un contraejemplo minimo es coloreable solo por si mismo, que es la propiedad puesta a prueba en la segunda ronda para los grafos de 52 vertices.',
              )}
            </li>
            <li>
              {t(
                'Is there a cyclically 4-edge-connected cubic graph with Petersen defect at least 3? One such graph would show that no sublinear function bounds the number of abnormal edges on that class and would complete the equivalence conjectured by Mattiolo, Mazzuoccolo and Mkrtchyan. All five known counterexamples have defect 2, with every vertex pair critical; whether every pair of every counterexample is critical is open as well.',
                'Existe un grafo cubico ciclicamente 4-arista-conexo con defecto de Petersen al menos 3? Un grafo asi mostraria que ninguna funcion sublineal acota el numero de aristas anormales en esa clase y completaria la equivalencia conjeturada por Mattiolo, Mazzuoccolo y Mkrtchyan. Los cinco contraejemplos conocidos tienen defecto 2, con todos los pares de vertices criticos; tambien esta abierto si todo par de todo contraejemplo es critico.',
              )}
            </li>
            <li>
              {t(
                'Are the 68-vertex and the 112-vertex counterexamples colorable only by themselves, or does a smaller counterexample color one of them?',
                'Son los contraejemplos de 68 y de 112 vertices coloreables solo por si mismos, o algun contraejemplo mas pequeno colorea a alguno de ellos?',
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
                'Does every bridgeless cubic graph have a normal 6-edge-coloring? Open in general; true on the five counterexamples (EXP-004, EXP-008). Are the compositions of copies of F with a few free vertices below 52 vertices all colorable? Classes without free vertices are (a one-line proof); the classes with free vertices did not converge under counterexample-guided search and need symmetry breaking (EXP-005).',
                'Todo grafo cubico sin puentes tiene una 6-arista-coloracion normal? Abierto en general; cierto en los cinco contraejemplos (EXP-004, EXP-008). Son coloreables todas las composiciones de copias de F con pocos vertices libres bajo 52 vertices? Las clases sin vertices libres lo son (prueba de una linea); las clases con vertices libres no convergieron bajo busqueda guiada por contraejemplos y necesitan ruptura de simetria (EXP-005).',
              )}
            </li>
            <li>
              {t(
                'Is perfect matching index 4 forced for every graph built from the pole F? Does oddness stay 4 along the infinite family grown from the 112-vertex graphs and 2 along the family grown from the 52-vertex graph?',
                'Esta forzado el indice de emparejamientos perfectos 4 para todo grafo construido desde el polo F? Se mantiene la imparidad en 4 a lo largo de la familia infinita crecida desde los grafos de 112 vertices y en 2 en la familia crecida desde el de 52?',
              )}
            </li>
          </ul>
          <Callout variant="note" title={t('Scope', 'Alcance')}>
            {t(
              'The counterexamples are not ours: discovery priority belongs to Putman, to Goedgebeur, Jooken, Macajova, Mattiolo and Mazzuoccolo, and to Jooken for the human-checkable proof. What is ours is the independent certification with a second encoding, and the audit: perfect matching covers and index, cycle double covers, flows, oddness, resistance, normal 6-edge-colorings and exact defects, each with a certificate. The ring and frame constructions are those of Mattiolo, Mazzuoccolo and Mkrtchyan; ours is the cut-space argument that strengthens their conclusion. Nothing here bears on the general covering and flow conjectures beyond these five graphs.',
              'Los contraejemplos no son nuestros: la prioridad de descubrimiento pertenece a Putman, a Goedgebeur, Jooken, Macajova, Mattiolo y Mazzuoccolo, y a Jooken por la prueba verificable a mano. Nuestro es la certificacion independiente con una segunda codificacion, y la auditoria: cubiertas e indice de emparejamientos perfectos, dobles cubiertas por ciclos, flujos, imparidad, resistencia, 6-arista-coloraciones normales y defectos exactos, cada uno con certificado. Las construcciones de anillo y marco son las de Mattiolo, Mazzuoccolo y Mkrtchyan; nuestro es el argumento del espacio de cortes que refuerza su conclusion. Nada aqui incide en las conjeturas generales de cubiertas y flujos mas alla de estos cinco grafos.',
            )}
          </Callout>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['gjmmm2026', 'gjmmmu2026', 'mmm2021', 'mazzmkrt2020', 'pccaudit']} />
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
