import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { FlaskConical } from 'lucide-react';
import { AppShell, applyTheme, readTheme, CitationsProvider, type ShellConfig } from '@fasl-work/caos-app-shell';
import '@fasl-work/caos-app-shell/styles.css';
import 'katex/dist/katex.min.css';
import './research.css';
import { CITATIONS } from './data/citations';
import { ARCHITECTURE } from './lib/architecture';
import pkg from '../package.json';

import Home from './pages/Home';
import Methodology from './pages/Methodology';
import Jacobian from './pages/Jacobian';

// Display version X.XX.XXX derived from the semver manifest (single source, no drift).
const displayVersion = pkg.version
  .split('.')
  .map((p, i) => (i === 0 ? p : p.padStart(i === 1 ? 2 : 3, '0')))
  .join('.');

applyTheme(readTheme());

// Restore a deep link captured by the Pages 404 shim (public/404.html) before the router mounts.
const redirect = sessionStorage.getItem('cr-redirect');
if (redirect && redirect !== location.pathname + location.search) {
  sessionStorage.removeItem('cr-redirect');
  history.replaceState(null, '', redirect);
}

const config: ShellConfig = {
  product: { name: 'CAOS Research', mark: <FlaskConical size={18} aria-hidden="true" /> },
  routes: [
    { path: '/', en: 'Program', es: 'Programa' },
    { path: '/methodology', en: 'Methodology', es: 'Metodología' },
    { path: '/problems/jacobian-conjecture', en: 'Jacobian conjecture', es: 'Conjetura jacobiana' },
  ],
  links: {
    github: 'https://github.com/fsantibanezleal/CAOS_RESEARCH',
    personal: 'https://fsantibanezleal.github.io',
    portfolio: 'https://portfolio.fasl-work.com',
  },
  version: displayVersion,
  architecture: ARCHITECTURE,
  footer: {
    provenance: {
      en: 'Sources: primary literature (DOI/arXiv linked inline) and the repository experiment records EXP-001..012; every number on this site is baked from a persisted, hash-manifested artifact. Engines: sympy over exact rationals offline; the site itself computes nothing.',
      es: 'Fuentes: literatura primaria (DOI/arXiv enlazados en linea) y los registros de experimentos EXP-001..012 del repositorio; cada numero de este sitio se hornea desde un artefacto persistido con manifiesto de hash. Motores: sympy sobre racionales exactos offline; el sitio no calcula nada.',
    },
    disclaimer: {
      en: 'A research record, not a peer-reviewed venue: verdicts are labeled machine-verified, derived or conjecture, refuted attempts stay in the record, and open questions are stated as open. The Jacobian conjecture remains open in dimension 2.',
      es: 'Un registro de investigacion, no un medio con revision por pares: los veredictos se etiquetan como verificados a maquina, derivados o conjetura, los intentos refutados quedan en el registro y las preguntas abiertas se declaran abiertas. La conjetura jacobiana sigue abierta en dimension 2.',
    },
  },
};

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <CitationsProvider items={CITATIONS}>
        <AppShell config={config}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/methodology" element={<Methodology />} />
            <Route path="/problems/jacobian-conjecture" element={<Jacobian />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </AppShell>
      </CitationsProvider>
    </BrowserRouter>
  </StrictMode>,
);
