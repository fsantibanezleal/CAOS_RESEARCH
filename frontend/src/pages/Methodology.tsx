import { Callout, Refs } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';

export default function Methodology() {
  const t = useT();
  return (
    <div className="rs-doc">
      <p className="rs-kicker">{t('The research operating system', 'El sistema operativo de investigacion')}</p>
      <h1>{t('Methodology', 'Metodologia')}</h1>
      <p className="rs-lead">
        {t(
          'Every problem in the repository is worked under one fixed operating system, so the record stays honest, reproducible and adversarially validated, independent of who (or what) runs a given session.',
          'Cada problema del repositorio se trabaja bajo un mismo sistema operativo, para que el registro se mantenga honesto, reproducible y validado adversarialmente, independiente de quien (o que) corra una sesion.',
        )}
      </p>

      <h2>{t('Six binding documents', 'Seis documentos vinculantes')}</h2>
      <div className="rs-scroll">
        <table className="rs-table">
          <thead>
            <tr><th>{t('Doc', 'Doc')}</th><th>{t('Governs', 'Gobierna')}</th></tr>
          </thead>
          <tbody>
            <tr><td className="rs-mono">01-lifecycle</td><td>{t('Problem states (proposed to published) and the artifact gates between them; one problem publishes before the next opens.', 'Estados del problema (de propuesto a publicado) y las compuertas de artefactos entre ellos; un problema publica antes de abrir el siguiente.')}</td></tr>
            <tr><td className="rs-mono">02-experiment-standard</td><td>{t('The EXP-NNN record: hypothesis declared and committed BEFORE the run; deterministic headless entry point; artifacts; a verdict with an explicit label.', 'El registro EXP-NNN: hipotesis declarada y comprometida ANTES de la corrida; punto de entrada determinista sin cabeza; artefactos; un veredicto con etiqueta explicita.')}</td></tr>
            <tr><td className="rs-mono">03-adversarial-validation</td><td>{t('The validation ladder: exact re-derivation by an independent route, certified numerics, cross-implementation agreement, stress families; plus a mandatory "how could this be wrong?" section.', 'La escalera de validacion: re-derivacion exacta por ruta independiente, numerica certificada, acuerdo entre implementaciones, familias de estres; mas una seccion obligatoria de "como podria estar mal".')}</td></tr>
            <tr><td className="rs-mono">04-code-standards</td><td>{t('Exact arithmetic certifies; floats explore and visualize. Isolated environments; tests never write canonical artifacts; CI re-runs the cheap certificates.', 'La aritmetica exacta certifica; los flotantes exploran y visualizan. Entornos aislados; los tests nunca escriben artefactos canonicos; el CI re-ejecuta los certificados baratos.')}</td></tr>
            <tr><td className="rs-mono">05-writing-standards</td><td>{t('English-only repo; KaTeX equations; primary sources with DOI/arXiv inline; UNVERIFIED flags until verified; vertical writing (each unit finished with its docs in the same session).', 'Repositorio solo en ingles; ecuaciones KaTeX; fuentes primarias con DOI/arXiv en linea; banderas UNVERIFIED hasta verificar; escritura vertical (cada unidad terminada con sus docs en la misma sesion).')}</td></tr>
            <tr><td className="rs-mono">06-web-publication</td><td>{t('What may appear on this site and when: verdicts surface verbatim, the web never upgrades a claim, and every visualization is traceable to a baked, hash-manifested artifact.', 'Que puede aparecer en este sitio y cuando: los veredictos se muestran textuales, la web nunca mejora una afirmacion y cada visualizacion es rastreable a un artefacto horneado con manifiesto de hash.')}</td></tr>
          </tbody>
        </table>
      </div>

      <h2>{t('The loop that does the work', 'El bucle que hace el trabajo')}</h2>
      <p>
        {t(
          'State a falsifiable hypothesis, build the exact check, run it, and let a failed run correct the theory. In this program the loop paid off twice: a refuted family constructor produced the correct one (and with it the new counterexamples), and a refuted parity hypothesis produced the uniqueness result for the mechanism.',
          'Declarar una hipotesis falsable, construir la verificacion exacta, correrla y dejar que una corrida fallida corrija la teoria. En este programa el bucle rindio dos veces: un constructor de familia refutado produjo el correcto (y con el los nuevos contraejemplos), y una hipotesis de paridad refutada produjo el resultado de unicidad del mecanismo.',
        )}
      </p>

      <Callout variant="note" title={t('Why the trail matters', 'Por que importa el rastro')}>
        {t(
          'The 2026 counterexample arrived as an artifact plus its verification; the reasoning trail that produced it is not public. This repository standardizes exactly that trail: hypotheses, exact checks, verdicts, refutations. The mindset that designs the experiment is what turns a verified example into understanding.',
          'El contraejemplo de 2026 llego como artefacto mas su verificacion; el rastro de razonamiento que lo produjo no es publico. Este repositorio estandariza exactamente ese rastro: hipotesis, verificaciones exactas, veredictos, refutaciones. La mentalidad que diseña el experimento es lo que convierte un ejemplo verificado en comprension.',
        )}
      </Callout>

      <Refs label={t('References', 'Referencias')} ids={['caosresearch', 'alpoge2026', 'vandenessen2000']} />
    </div>
  );
}
