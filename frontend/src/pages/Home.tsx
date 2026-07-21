import { useEffect, useState } from 'react';
import { Callout } from '@fasl-work/caos-app-shell';
import { useT } from '../lib/i18n';
import { loadPortfolio, loadExperiments, type Portfolio, type ExperimentRec } from '../api/data';
import { Link } from 'react-router-dom';

export default function Home() {
  const t = useT();
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [experiments, setExperiments] = useState<ExperimentRec[]>([]);
  useEffect(() => {
    loadPortfolio().then(setPortfolio).catch(() => setPortfolio(null));
    loadExperiments().then(setExperiments).catch(() => setExperiments([]));
  }, []);

  return (
    <div className="rs-doc">
      <p className="rs-kicker">{t('Open problems, as an experiment history', 'Problemas abiertos, como historia de experimentos')}</p>
      <h1>{t('CAOS Research', 'CAOS Research')}</h1>
      <p className="rs-lead">
        {t(
          'A methodical, offline, adversarially validated experimentation program on open mathematical problems. The repository is the record: every experiment declares its hypothesis before the run, uses exact arithmetic, and closes with a persisted verdict. Refuted attempts stay in the record. This site replays that record; it computes nothing.',
          'Un programa de experimentacion metodico, offline y validado adversarialmente sobre problemas matematicos abiertos. El repositorio es el registro: cada experimento declara su hipotesis antes de la corrida, usa aritmetica exacta y cierra con un veredicto persistido. Los intentos refutados quedan en el registro. Este sitio reproduce ese registro; no calcula nada.',
        )}
      </p>

      <Callout variant="note" title={t('First program: the Jacobian conjecture', 'Primer programa: la conjetura jacobiana')}>
        {t(
          'On 2026-07-19 Levent Alpöge announced a counterexample in dimension 3, found working with Claude Fable (Anthropic). This program validated it independently in exact arithmetic, generalized it to an infinite family with new explicit counterexamples, made the escape geometry exact, and proved a rigidity theorem in dimension 2. ',
          'El 2026-07-19 Levent Alpöge anuncio un contraejemplo en dimension 3, encontrado trabajando con Claude Fable (Anthropic). Este programa lo valido de forma independiente en aritmetica exacta, lo generalizo a una familia infinita con nuevos contraejemplos explicitos, hizo exacta la geometria de escape y probo un teorema de rigidez en dimension 2. ',
        )}
        <Link to="/problems/jacobian-conjecture">{t('Open the problem page.', 'Abrir la pagina del problema.')}</Link>
      </Callout>

      <h2>{t('The portfolio board', 'El tablero del portafolio')}</h2>
      <p>
        {t(
          'Problems move through a fixed lifecycle (proposed, scoped, opened, exploring, consolidating, published) with artifact gates between states; one problem is brought to published before the next opens.',
          'Los problemas avanzan por un ciclo de vida fijo (propuesto, delimitado, abierto, explorando, consolidando, publicado) con compuertas de artefactos entre estados; un problema llega a publicado antes de abrir el siguiente.',
        )}
      </p>
      {portfolio ? (
        <div className="rs-scroll">
          <table className="rs-table">
            <thead>
              <tr>
                <th>{t('Problem', 'Problema')}</th>
                <th>{t('Area', 'Area')}</th>
                <th>{t('State', 'Estado')}</th>
                <th>{t('Feasibility', 'Factibilidad')}</th>
                <th>GPU</th>
              </tr>
            </thead>
            <tbody>
              {portfolio.problems.map((p) => {
                const area = portfolio.areas.find((a) => a.slug === p.area);
                const row = (
                  <tr key={p.slug}>
                    <td>
                      {p.slug === 'jacobian-conjecture' ? (
                        <Link to="/problems/jacobian-conjecture">{p.slug}</Link>
                      ) : (
                        p.slug
                      )}
                    </td>
                    <td>{area ? area.name : p.area}</td>
                    <td><span className="rs-badge state">{p.state}</span></td>
                    <td className="num">{p.feasibility}</td>
                    <td className="num">{String(p.gpu)}</td>
                  </tr>
                );
                return row;
              })}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="rs-readout">{t('Loading the baked portfolio…', 'Cargando el portafolio horneado…')}</p>
      )}

      <h2>{t('The experiment log so far', 'El registro de experimentos hasta ahora')}</h2>
      <p>
        {t(
          'Twelve experiments on the Jacobian program in the first three days, including one refuted constructor and one refuted design hypothesis; both refutations produced the next result.',
          'Doce experimentos del programa jacobiano en los primeros tres dias, incluyendo un constructor refutado y una hipotesis de diseño refutada; ambas refutaciones produjeron el siguiente resultado.',
        )}
      </p>
      <ul className="rs-timeline">
        {experiments.map((e) => (
          <li key={e.slug}>
            <span className="exp">EXP-{e.id}</span>
            <span className="date rs-readout">{e.date}</span>
            <span>
              {e.title}{' '}
              {e.verdict && <span className={`rs-badge ${e.verdict.split(' ')[0].replace(',', '')}`}>{e.verdict}</span>}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
