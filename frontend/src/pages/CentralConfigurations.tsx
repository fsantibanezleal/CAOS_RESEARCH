import { Suspense, lazy, useEffect, useState } from 'react';
import { Callout, Cite, Equation, Refs, Tabs, type TabDef } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadExperiments, type ExperimentRec } from '../api/data';
const ExperimentModal = lazy(() => import('../components/ExperimentModal'));

const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';

export default function CentralConfigurations() {
  const t = useT();
  const [exps, setExps] = useState<ExperimentRec[]>([]);
  const [open, setOpen] = useState<ExperimentRec | null>(null);
  useEffect(() => {
    loadExperiments()
      .then((e) => setExps(e.filter((x) => x.problem === 'central-configurations')))
      .catch(() => setExps([]));
  }, []);

  const tabs: TabDef[] = [
    {
      id: 'summary',
      label: t('Summary', 'Resumen'),
      content: (
        <section>
          <p className="rs-lead">
            {t(
              "Smale's 6th problem asks whether, for every n and every choice of positive masses, the number of planar central configurations (relative equilibria) of the Newtonian n-body problem is finite up to symmetry. It is open for n at least 6. This program is a machine record: exact calibrations, an independent exact reproduction of the state-of-the-art generic-mass certificate for n = 5, a screening study over valuations and equation variants, and a live computation at the n = 6 frontier.",
              'El sexto problema de Smale pregunta si, para todo n y toda eleccion de masas positivas, el numero de configuraciones centrales planas (equilibrios relativos) del problema newtoniano de n cuerpos es finito modulo simetria. Esta abierto para n mayor o igual a 6. Este programa es un registro de maquina: calibraciones exactas, una reproduccion exacta e independiente del certificado generico de referencia para n = 5, un estudio de barrido sobre valuaciones y variantes de ecuaciones, y una computacion viva en la frontera n = 6.',
            )}
          </p>
          <Equation tex={String.raw`\lambda\,(x_i-c)=\sum_{j\neq i}\frac{m_j\,(x_j-x_i)}{r_{ij}^{3}},\qquad i=1,\dots,n`} />
          <p>
            {t(
              'The modern ladder: n = 4 finite for all positive masses (computer-assisted BKK certificate, count in [32, 8472]) ',
              'La escalera moderna: n = 4 finito para todas las masas positivas (certificado BKK asistido por computador, conteo en [32, 8472]) ',
            )}
            (<Cite id="hm2006" />),{' '}
            {t('n = 5 finite except possibly on an explicit codimension-2 mass subvariety ', 'n = 5 finito salvo quiza sobre una subvariedad explicita de codimension 2 en las masas ')}
            (<Cite id="ak2012" />),{' '}
            {t('generic masses for n up to 5 by a purely polyhedral tropical certificate ', 'masas genericas para n hasta 5 por un certificado tropical puramente poliedral ')}
            (<Cite id="jl2025" />),{' '}
            {t('and n = 6 open, reduced to a finite list of residual diagram cases ', 'y n = 6 abierto, reducido a una lista finita de casos residuales de diagramas ')}
            (<Cite id="changchen2023" />).
          </p>
          <Callout variant="note" title={t('State of this program', 'Estado de este programa')}>
            {t(
              'Exploring (opened 2026-07-23). Five experiments declared, four decided, one running: the n = 6 tropical prevariety at powers-of-3 valuations, a multi-day computation whose positive outcome would give generic-mass finiteness for n = 6. Every hypothesis is committed before its run; refutations stay in the record.',
              'Explorando (abierto el 2026-07-23). Cinco experimentos declarados, cuatro decididos, uno corriendo: la prevariedad tropical n = 6 con valuaciones potencias de 3, una computacion de varios dias cuyo resultado positivo daria finitud generica para n = 6. Toda hipotesis se compromete antes de su corrida; las refutaciones permanecen en el registro.',
            )}
          </Callout>
          <h3>{t('Manuscript', 'Manuscrito')}</h3>
          <ul>
            <li>
              <a href={`${REPO}/blob/main/manuscripts/central-configurations/tropical-replication/main.pdf`} target="_blank" rel="noreferrer">
                {t(
                  'Exact replication and screening of tropical finiteness certificates for central configurations (machine record, versioned drafts)',
                  'Replicacion exacta y barrido de certificados tropicales de finitud para configuraciones centrales (registro de maquina, borradores versionados)',
                )}
              </a>
            </li>
          </ul>
          <Refs label={t('Key sources', 'Fuentes clave')} ids={['smale1998', 'hm2006', 'ak2012', 'jl2025', 'caosresearch']} />
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
              'A central configuration released from rest collapses homothetically; rotated rigidly in the plane it is a relative equilibrium. Euler (1767) found the collinear three-body solutions, Lagrange (1772) the equilateral one; Moulton (1910) proved there are exactly n!/2 collinear classes for any masses ',
              'Una configuracion central soltada desde el reposo colapsa homoteticamente; rotada rigidamente en el plano es un equilibrio relativo. Euler (1767) encontro las soluciones colineales de tres cuerpos, Lagrange (1772) la equilatera; Moulton (1910) probo que hay exactamente n!/2 clases colineales para cualesquiera masas ',
            )}
            (<Cite id="moulton1910" />).
          </p>
          <p>
            {t(
              'The finiteness question goes back to Chazy (1918) and Wintner (1941); Smale made it problem 6 of his list for the 21st century. Chazy postulated that all central configurations are nondegenerate, which would give mass-independent counts; Palmore (1975) refuted the postulate with an explicit degenerate example, and the count does vary with the masses. With one negative mass a continuum of relative equilibria exists ',
              'La pregunta de finitud se remonta a Chazy (1918) y Wintner (1941); Smale la hizo el problema 6 de su lista para el siglo XXI. Chazy postulo que todas las configuraciones centrales son no degeneradas, lo que daria conteos independientes de las masas; Palmore (1975) refuto el postulado con un ejemplo degenerado explicito, y el conteo si varia con las masas. Con una masa negativa existe un continuo de equilibrios relativos ',
            )}
            (<Cite id="roberts1999" />)
            {t(', so positivity is essential. Rigorous equal-mass censuses exist through n = 7 ', ', asi que la positividad es esencial. Existen censos rigurosos de masas iguales hasta n = 7 ')}
            (<Cite id="mz2019" />).
          </p>
          <Refs label={t('Sources', 'Fuentes')} ids={['moulton1910', 'roberts1999', 'mz2019', 'ak2012']} />
        </section>
      ),
    },
    {
      id: 'approaches',
      label: t('References and approaches', 'Referencias y enfoques'),
      content: (
        <section>
          <p>
            {t(
              'Every modern finiteness certificate is an exclusion argument over the Albouy-Chenciner equations in mutual distances ',
              'Todo certificado moderno de finitud es un argumento de exclusion sobre las ecuaciones de Albouy-Chenciner en distancias mutuas ',
            )}
            (<Cite id="ac1998" />):
          </p>
          <Equation tex={String.raw`f_{ij}=\sum_{k=1}^{n} m_k\!\left[S_{ik}\,(r_{jk}^2-r_{ik}^2-r_{ij}^2)+S_{jk}\,(r_{ik}^2-r_{jk}^2-r_{ij}^2)\right],\qquad S_{ij}=r_{ij}^{-3}-1`} />
          <p>
            {t(
              'Hampton-Moeckel exclude torus directions via BKK theory and Newton polytopes; Hampton-Jensen recast the same logic tropically (prevariety via gfan, per-ray exact kills); Albouy-Kaloshin follow complex continua into their singularities; Chang-Chen industrialize the diagram bookkeeping; Jensen-Leykin specialize masses into the Puiseux field and reduce generic finiteness to a single polyhedral computation: if every connected component (comet) of the tropical prevariety has a pointed recession cone, the variety is zero-dimensional and generic finiteness follows.',
              'Hampton-Moeckel excluyen direcciones del toro via teoria BKK y politopos de Newton; Hampton-Jensen reformulan la misma logica tropicalmente (prevariedad via gfan, exclusiones exactas por rayo); Albouy-Kaloshin siguen continuos complejos hasta sus singularidades; Chang-Chen industrializan la contabilidad de diagramas; Jensen-Leykin especializan las masas en el cuerpo de Puiseux y reducen la finitud generica a una sola computacion poliedral: si toda componente conexa (cometa) de la prevariedad tropical tiene cono de recesion puntiagudo, la variedad es de dimension cero y la finitud generica sigue.',
            )}
          </p>
          <Refs label={t('The certificate papers', 'Los articulos de certificados')} ids={['hm2006', 'hj2011', 'ak2012', 'changchen2023', 'jl2025']} />
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
              'Replication-first, then the frontier: (1) exact calibration of the equations in open tooling; (2) independent reproduction of each certificate (Hampton-Moeckel numeric targets transcribed from a full read; the Jensen-Leykin n = 5 computation reproduced digit for digit); (3) the experiments the frontier papers themselves call for: valuation screening and equation-variant prevariety shrinking; (4) the n = 6 shot with the best-evidenced configuration. Everything exact or certified; hypotheses committed before runs; multi-day computations run detached while other fronts (census engines, manuscript, degeneracy instruments) advance.',
              'Primero replicacion, luego la frontera: (1) calibracion exacta de las ecuaciones en herramientas abiertas; (2) reproduccion independiente de cada certificado (los objetivos numericos de Hampton-Moeckel transcritos de una lectura completa; la computacion n = 5 de Jensen-Leykin reproducida digito a digito); (3) los experimentos que los propios articulos de frontera piden: barrido de valuaciones y reduccion de prevariedad por variantes de ecuaciones; (4) el intento n = 6 con la configuracion mejor evidenciada. Todo exacto o certificado; hipotesis comprometidas antes de las corridas; las computaciones de varios dias corren desacopladas mientras otros frentes (motores de censo, manuscrito, instrumentos de degeneracion) avanzan.',
            )}
          </p>
          <Callout variant="strong" title={t('The enrichment law (our measurement)', 'La ley de enriquecimiento (nuestra medicion)')}>
            {t(
              'Dropping the ten dependent symmetric Albouy-Chenciner equations destroys pointedness at every tested valuation (300+ positive unbounded directions); adjoining the asymmetric equations and the energy-inertia relation makes the affine n = 3 ideal zero-dimensional directly. The "redundant" equations carry essential tropical information: this is the quantitative version of a pattern visible in every certificate paper since 2006.',
              'Eliminar las diez ecuaciones simetricas dependientes de Albouy-Chenciner destruye la puntiagudez en toda valuacion probada (mas de 300 direcciones no acotadas positivas); adjuntar las ecuaciones asimetricas y la relacion energia-inercia hace el ideal afin n = 3 de dimension cero directamente. Las ecuaciones "redundantes" portan informacion tropical esencial: es la version cuantitativa de un patron visible en todos los articulos de certificados desde 2006.',
            )}
          </Callout>
          <p>
            {t('Program files: ', 'Archivos del programa: ')}
            <a href={`${REPO}/tree/main/program/central-configurations`} target="_blank" rel="noreferrer">program/central-configurations</a>
            {t(' (plan, backlog, routes, research lines, RESUME); problem tree: ', ' (plan, backlog, rutas, lineas de investigacion, RESUME); arbol del problema: ')}
            <a href={`${REPO}/tree/main/problems/dynamical-systems/central-configurations`} target="_blank" rel="noreferrer">problems/dynamical-systems/central-configurations</a>.
          </p>
        </section>
      ),
    },
    {
      id: 'experiments',
      label: t('Experiments and results', 'Experimentos y resultados'),
      content: (
        <section>
          <p>
            {t(
              'One row per experiment; verdicts are quoted verbatim from the persisted records and are never upgraded here. Highlights: EXP-001 refuted its own uniqueness prediction with structural content (the distance equations are dimension-blind: the regular tetrahedron coexists with the square, whose side satisfies 32a^6 - 32a^3 + 7 = 0, until Cayley-Menger is adjoined); EXP-003 reproduced both published Jensen-Leykin f-vectors exactly, with pointedness verified by an independent exact parser; EXP-005 (running) is the n = 6 attempt.',
              'Una fila por experimento; los veredictos se citan textualmente de los registros persistidos y nunca se mejoran aqui. Destacados: EXP-001 refuto su propia prediccion de unicidad con contenido estructural (las ecuaciones de distancias son ciegas a la dimension: el tetraedro regular coexiste con el cuadrado, cuyo lado satisface 32a^6 - 32a^3 + 7 = 0, hasta adjuntar Cayley-Menger); EXP-003 reprodujo exactamente los dos f-vectores publicados de Jensen-Leykin, con puntiagudez verificada por un parser exacto independiente; EXP-005 (corriendo) es el intento n = 6.',
            )}
          </p>
          {exps.length === 0 ? (
            <Callout variant="note" title={t('Records', 'Registros')}>
              {t(
                'Baked experiment records appear here after the next data release; the full records live in the repository now: ',
                'Los registros compilados apareceran aqui tras la proxima publicacion de datos; los registros completos viven en el repositorio ahora: ',
              )}
              <a href={`${REPO}/tree/main/problems/dynamical-systems/central-configurations/experiments`} target="_blank" rel="noreferrer">
                {t('experiment folders', 'carpetas de experimentos')}
              </a>.
            </Callout>
          ) : (
            <ul className="rs-exp-list">
              {exps.map((e) => (
                <li key={e.id}>
                  <button type="button" onClick={() => setOpen(e)}>
                    {e.id} · {e.verdict}
                  </button>
                </li>
              ))}
            </ul>
          )}
          <Refs label={t('Ground truths used', 'Verdades de referencia usadas')} ids={['jl2025', 'mz2019', 'hm2006']} />
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
                'Smale 6 itself: all-masses finiteness for n = 6 (24 residual diagram cases) and everything beyond; generic-mass finiteness for n = 6 is exactly the live computation of this program.',
                'El propio Smale 6: finitud para todas las masas con n = 6 (24 casos residuales de diagramas) y todo lo posterior; la finitud generica para n = 6 es exactamente la computacion viva de este programa.',
              )}
            </li>
            <li>
              {t(
                'Which valuation families make the Jensen-Leykin certificate work, and why: our screening found powers of 3 globally pointed and the standard controls comet-pointed at n = 5; a structural explanation is open.',
                'Que familias de valuaciones hacen funcionar el certificado de Jensen-Leykin, y por que: nuestro barrido encontro potencias de 3 globalmente puntiagudo y los controles estandar puntiagudos por cometas en n = 5; una explicacion estructural esta abierta.',
              )}
            </li>
            <li>
              {t(
                'Our census for two integer-separated mass vectors at n = 3 is honestly inconclusive under the sympy engine caps; the msolve re-run is queued.',
                'Nuestro censo para dos vectores de masas separadas enteras en n = 3 es honestamente inconcluso bajo los topes del motor sympy; la repeticion con msolve esta en cola.',
              )}
            </li>
          </ul>
        </section>
      ),
    },
  ];

  return (
    <div className="rs-page">
      <h1>{t('Central configurations (Smale 6)', 'Configuraciones centrales (Smale 6)')}</h1>
      <Tabs tabs={tabs} />
      {open && (
        <Suspense fallback={null}>
          <ExperimentModal exp={open} onClose={() => setOpen(null)} />
        </Suspense>
      )}
    </div>
  );
}
