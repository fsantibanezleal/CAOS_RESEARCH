// Typed loaders for the baked CONTRACT-2 artifacts (public/data/research/*.json).
export type PortfolioProblem = {
  slug: string; area: string; state: string; feasibility: string;
  gpu: boolean | string; opened?: string;
};
export type Portfolio = {
  updated: string;
  areas: { slug: string; name: string }[];
  problems: PortfolioProblem[];
};
export type ExperimentRec = {
  problem: string; area: string; id: string; slug: string;
  title: string; verdict: string; date: string;
  hypothesis_md: string; verdict_md: string;
  artifacts: { name: string; bytes: number }[];
};
export type FamilyRow = {
  seed: string; det: number; degrees: number[]; fiber: number;
  collision?: { points: string[][]; target: string[] };
};
export type JacobianData = {
  map: { P: string; Q: string; R: string; u: string; det: number;
         collision_points: number[][]; collision_target: number[] };
  family: FamilyRow[];
  laws: { det: string; fiber_degree: string; degrees: string };
  wall: { equation: string; census: { bracket_negative: number; bracket_positive: number };
          escape_demo: { target: number[]; surviving_point: number[] } };
  fiber_cubic: { phi: string; equation: string };
  cascade: { name: string; prior: string; now: string; chain: string }[];
  landscape: { m: number; o: number[]; status: string }[];
};

async function load<T>(name: string): Promise<T> {
  const res = await fetch(`/data/research/${name}.json`);
  if (!res.ok) throw new Error(`failed to load ${name}: ${res.status}`);
  return (await res.json()) as T;
}
export const loadPortfolio = () => load<Portfolio>('portfolio');
export const loadExperiments = () =>
  load<{ experiments: ExperimentRec[] }>('experiments').then((d) => d.experiments);
export const loadJacobian = () => load<JacobianData>('jacobian');
