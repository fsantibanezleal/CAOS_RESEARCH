import { useEffect, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { X, FlaskConical, FileText } from 'lucide-react';
import { useT } from '../lib/i18n';
import type { ExperimentRec } from '../api/data';

const REPO = 'https://github.com/fsantibanezleal/CAOS_RESEARCH';

function expPath(e: ExperimentRec): string {
  return `problems/${e.area}/${e.problem}/experiments/${e.slug}`;
}

export default function ExperimentModal({ exp, onClose }: { exp: ExperimentRec; onClose: () => void }) {
  const t = useT();
  const panelRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const onKey = (ev: KeyboardEvent) => {
      if (ev.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKey);
    panelRef.current?.focus();
    const prev = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = prev;
    };
  }, [onClose]);

  return (
    <div className="rs-modal-overlay" onClick={onClose} role="presentation">
      <div
        className="rs-modal"
        role="dialog"
        aria-modal="true"
        aria-label={`EXP-${exp.id}: ${exp.title}`}
        ref={panelRef}
        tabIndex={-1}
        onClick={(ev) => ev.stopPropagation()}
      >
        <header className="rs-modal-head">
          <div className="rs-modal-title">
            <span className="exp">EXP-{exp.id}</span>
            <span className="rs-badge state">{exp.problem}</span>
            {exp.verdict && (
              <span className={`rs-badge ${exp.verdict.split(' ')[0].replace(',', '')}`}>{exp.verdict}</span>
            )}
            {exp.date && <span className="rs-readout">{exp.date}</span>}
          </div>
          <button className="rs-modal-close" onClick={onClose} aria-label={t('Close', 'Cerrar')}>
            <X size={18} />
          </button>
        </header>
        <div className="rs-modal-body">
          <h2>{exp.title}</h2>
          {exp.hypothesis_md ? (
            <section>
              <h3 className="rs-modal-sec">
                <FlaskConical size={16} /> {t('Hypothesis (declared before the run)', 'Hipotesis (declarada antes de la corrida)')}
              </h3>
              <div className="rs-md">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{exp.hypothesis_md}</ReactMarkdown>
              </div>
            </section>
          ) : (
            <p className="rs-readout">{t('No hypothesis file in this record.', 'Sin archivo de hipotesis en este registro.')}</p>
          )}
          {exp.verdict_md ? (
            <section>
              <h3 className="rs-modal-sec">
                <FileText size={16} /> {t('Verdict (persisted after the run)', 'Veredicto (persistido despues de la corrida)')}
              </h3>
              <div className="rs-md">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{exp.verdict_md}</ReactMarkdown>
              </div>
            </section>
          ) : (
            <p className="rs-readout">
              {t('No verdict yet: the experiment is declared or in flight.', 'Aun sin veredicto: el experimento esta declarado o en curso.')}
            </p>
          )}
          {exp.artifacts.length > 0 && (
            <section>
              <h3 className="rs-modal-sec">{t('Run artifacts', 'Artefactos de la corrida')}</h3>
              <ul className="rs-modal-artifacts">
                {exp.artifacts.map((a) => (
                  <li key={a.name}>
                    <a href={`${REPO}/blob/main/${expPath(exp)}/artifacts/${a.name}`} target="_blank" rel="noreferrer">
                      {a.name}
                    </a>{' '}
                    <span className="rs-readout">{a.bytes.toLocaleString()} B</span>
                  </li>
                ))}
              </ul>
            </section>
          )}
          <p className="rs-modal-foot">
            <a href={`${REPO}/tree/main/${expPath(exp)}`} target="_blank" rel="noreferrer">
              {t('Open the full record on GitHub (code, artifacts, history)', 'Abrir el registro completo en GitHub (codigo, artefactos, historia)')}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
