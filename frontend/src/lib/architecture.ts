// The in-app Architecture / How-it-works modal (ADR-0058). Theme-aware SVGs: everything is
// currentColor or a low-opacity accent tint, so the same markup reads in light and dark.
import type { ArchitectureConfig } from '@fasl-work/caos-app-shell';

const W = 660;
const H = 290;
const FRAME = (inner: string) =>
  `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" font-family="ui-sans-serif, system-ui, sans-serif" role="img">` +
  `<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">` +
  `<path d="M0 0 L10 5 L0 10 z" fill="currentColor" fill-opacity="0.55"/></marker></defs>${inner}</svg>`;
const box = (x: number, y: number, w: number, h: number, title: string, sub = '', hue = '') =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" fill="${hue || 'currentColor'}" fill-opacity="${hue ? '0.12' : '0.05'}" stroke="${hue || 'currentColor'}" stroke-opacity="0.45"/>` +
  `<text x="${x + w / 2}" y="${y + (sub ? h / 2 - 3 : h / 2 + 4)}" text-anchor="middle" fill="currentColor" font-size="13" font-weight="600">${title}</text>` +
  (sub ? `<text x="${x + w / 2}" y="${y + h / 2 + 14}" text-anchor="middle" fill="currentColor" fill-opacity="0.7" font-size="10.5">${sub}</text>` : '');
const arrow = (x1: number, y1: number, x2: number, y2: number) =>
  `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="currentColor" stroke-opacity="0.55" stroke-width="1.6" marker-end="url(#ah)"/>`;
const label = (x: number, y: number, text: string, op = '0.75') =>
  `<text x="${x}" y="${y}" text-anchor="middle" fill="currentColor" fill-opacity="${op}" font-size="11">${text}</text>`;

const BLUE = '#0969DA';
const WARM = '#B02E0C';
const GREEN = '#3d9a50';

const svgApp = FRAME(
  box(20, 30, 190, 78, 'problems/&lt;area&gt;/&lt;slug&gt;', 'context · history · experiments · wiki', BLUE) +
    box(20, 130, 190, 60, 'methodology/', 'the research operating system') +
    box(20, 210, 190, 60, 'program/', 'portfolio board + per-problem plans') +
    box(260, 90, 170, 78, 'export pipeline', 'python -m researchlab.pipeline', GREEN) +
    box(480, 90, 160, 78, 'this web app', 'static replay on GitHub Pages', WARM) +
    arrow(210, 69, 260, 110) + arrow(210, 160, 260, 135) + arrow(210, 240, 260, 155) +
    arrow(430, 129, 480, 129) + label(455, 118, 'JSON + manifests') +
    label(330, 265, 'every page claim traces to an experiment record or a primary source'),
);

const svgOffline = FRAME(
  box(20, 40, 170, 70, 'hypothesis.md', 'declared BEFORE the run', BLUE) +
    box(245, 40, 170, 70, 'run.py', 'exact arithmetic over Q', GREEN) +
    box(470, 40, 170, 70, 'verdict.md', 'confirmed / refuted / null', WARM) +
    arrow(190, 75, 245, 75) + arrow(415, 75, 470, 75) +
    box(245, 160, 170, 60, 'artifacts/', 'outputs, persisted') +
    arrow(330, 110, 330, 160) +
    `<path d="M 555 110 C 555 220, 105 240, 105 116" fill="none" stroke="currentColor" stroke-opacity="0.5" stroke-width="1.6" marker-end="url(#ah)"/>` +
    label(330, 262, 'a refuted run corrects the theory: the loop that produced the family and the theorems'),
);

const svgScience = FRAME(
  box(20, 36, 185, 66, 'Keller map on C^3', 'det JF = -2, constant', BLUE) +
    box(20, 180, 185, 66, 'weighted invariants', 'v = xy,  t = x^2 z') +
    arrow(112, 102, 112, 180) +
    box(255, 108, 165, 66, 'fiber cubic in w', 'preimages = roots', GREEN) +
    arrow(205, 141, 255, 141) +
    box(470, 36, 170, 66, 'collisions', '3 points, 1 image', WARM) +
    box(470, 180, 170, 66, 'escape wall', 'multiple root = lost preimage', WARM) +
    arrow(420, 128, 470, 80) + arrow(420, 155, 470, 205) +
    label(330, 272, 'the mechanism: local diffeomorphism everywhere, sheets merge only at infinity'),
);

const svgDeploy = FRAME(
  box(20, 90, 170, 78, 'GitHub main', 'push / merge', BLUE) +
    box(250, 90, 170, 78, 'Actions build', 'bake + npm build', GREEN) +
    box(480, 90, 160, 78, 'GitHub Pages', 'research.fasl-work.com', WARM) +
    arrow(190, 129, 250, 129) + arrow(420, 129, 480, 129) +
    label(330, 200, 'no backend, no runtime compute: the site replays committed, hash-manifested artifacts') +
    label(330, 222, 'DNS: CNAME research -> fsantibanezleal.github.io (overrides the *.fasl-work.com wildcard)'),
);

export const ARCHITECTURE: ArchitectureConfig = {
  title_en: 'Architecture / How it works',
  title_es: 'Arquitectura / Cómo funciona',
  tabs: [
    {
      id: 'app',
      en: 'The app',
      es: 'La app',
      svg: svgApp,
      body_en:
        'The repository is the record: per-problem context, an append-only history, numbered experiments and a curated wiki. The export pipeline bakes the program registry and per-problem payloads into JSON artifacts with hash manifests; this static app replays them. Nothing on this site is computed from claims: every number traces to an experiment artifact in the repository.',
      body_es:
        'El repositorio es el registro: contexto por problema, historia solo-anexar, experimentos numerados y una wiki curada. El pipeline de exportacion hornea el registro del programa y las cargas por problema en artefactos JSON con manifiestos de hash; esta app estatica los reproduce. Nada en este sitio se calcula desde afirmaciones: cada numero se rastrea a un artefacto de experimento en el repositorio.',
    },
    {
      id: 'method',
      en: 'The method',
      es: 'El metodo',
      svg: svgOffline,
      body_en:
        'Every experiment declares a falsifiable hypothesis before the run, executes an exact check (rational or symbolic arithmetic; floats never certify), and closes with a persisted verdict: confirmed, refuted, null or inconclusive. Refuted attempts stay in the record: the analysis of one refuted constructor produced the correct family, and a refuted parity hypothesis produced the uniqueness result.',
      body_es:
        'Cada experimento declara una hipotesis falsable antes de la corrida, ejecuta una verificacion exacta (aritmetica racional o simbolica; los flotantes nunca certifican) y cierra con un veredicto persistido: confirmado, refutado, nulo o no concluyente. Los intentos refutados quedan en el registro: el analisis de un constructor refutado produjo la familia correcta, y una hipotesis de paridad refutada produjo el resultado de unicidad.',
    },
    {
      id: 'science',
      en: 'The science',
      es: 'La ciencia',
      svg: svgScience,
      body_en:
        'The 2026 counterexample is a weighted skew-product: two scaling invariants carry everything, the Keller condition collapses to a two-variable identity, and the fibers are governed by one cubic. Collisions are generic; preimages are lost exactly where the fiber polynomial has a multiple root, so the escape locus is an explicit surface. In dimension 2 the mechanism is closed: every equivariant Keller map of the plane is linear.',
      body_es:
        'El contraejemplo de 2026 es un producto sesgado con pesos: dos invariantes de escala lo cargan todo, la condicion de Keller colapsa a una identidad en dos variables y las fibras se gobiernan por una cubica. Las colisiones son genericas; las preimagenes se pierden exactamente donde el polinomio de fibra tiene raiz multiple, asi que el lugar de escape es una superficie explicita. En dimension 2 el mecanismo esta cerrado: todo mapa de Keller equivariante del plano es lineal.',
    },
    {
      id: 'deploy',
      en: 'The deploy',
      es: 'El deploy',
      svg: svgDeploy,
      body_en:
        'A push to main triggers GitHub Actions: the pipeline re-bakes the artifacts deterministically, the SPA builds, and GitHub Pages serves it at research.fasl-work.com. There is no backend and no telemetry; the site is fully static and reproducible from the repository.',
      body_es:
        'Un push a main dispara GitHub Actions: el pipeline vuelve a hornear los artefactos de forma determinista, la SPA compila y GitHub Pages la sirve en research.fasl-work.com. No hay backend ni telemetria; el sitio es totalmente estatico y reproducible desde el repositorio.',
    },
  ],
};
