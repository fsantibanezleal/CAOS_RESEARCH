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
import CentralConfigurations from './pages/CentralConfigurations';
import UnsplittableFlowCost from './pages/UnsplittableFlowCost';
import PetersenColoring from './pages/PetersenColoring';

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
    { path: '/problems/central-configurations', en: 'Central configurations', es: 'Configuraciones centrales' },
    { path: '/problems/unsplittable-flow-cost', en: 'Unsplittable flow cost', es: 'Costo de flujo indivisible' },
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
      en: 'Sources: primary literature (DOI/arXiv linked inline) and the repository experiment records of every problem on this site; every number here is baked from a persisted, hash-manifested artifact. Engines, all offline: sympy over exact rationals, msolve for certified real solving, gfan for the polyhedral and tropical computations, and an exact Bland-rule simplex for the rational linear programs; the site itself computes nothing.',
      es: 'Fuentes: literatura primaria (DOI/arXiv enlazados en linea) y los registros de experimentos de cada problema de este sitio; cada numero aqui se hornea desde un artefacto persistido con manifiesto de hash. Motores, todos offline: sympy sobre racionales exactos, msolve para resolucion real certificada, gfan para las computaciones poliedrales y tropicales, y un simplex exacto con regla de Bland para los programas lineales racionales; el sitio no calcula nada.',
    },
    disclaimer: {
      en: 'A research record, not a peer-reviewed venue: verdicts are labeled machine-verified, derived or conjecture, refuted attempts stay in the record, and open questions are stated as open. The Jacobian conjecture remains open in dimension 2, Smale’s 6th problem remains open from six bodies on, and Goemans’ unsplittable-flow cost conjecture is refuted while its quantitative frontier stays open; results replicated from the literature, including counterexamples found by others, are labeled as replications.',
      es: 'Un registro de investigacion, no un medio con revision por pares: los veredictos se etiquetan como verificados a maquina, derivados o conjetura, los intentos refutados quedan en el registro y las preguntas abiertas se declaran abiertas. La conjetura jacobiana sigue abierta en dimension 2, el sexto problema de Smale sigue abierto desde seis cuerpos, y la conjetura de costo de flujo indivisible de Goemans esta refutada mientras su frontera cuantitativa sigue abierta; los resultados replicados de la literatura, incluidos contraejemplos hallados por otros, se etiquetan como replicaciones.',
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
            <Route path="/problems/central-configurations" element={<CentralConfigurations />} />
            <Route path="/problems/unsplittable-flow-cost" element={<UnsplittableFlowCost />} />
            <Route path="/problems/petersen-coloring" element={<PetersenColoring />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </AppShell>
      </CitationsProvider>
    </BrowserRouter>
  </StrictMode>,
);
