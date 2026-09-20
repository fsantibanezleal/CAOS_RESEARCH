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

export type RiemannBound = { lower: string; upper: string; display: string };
export type RiemannPressureWinner = {
  candidate: number; status: 'arithmetic_verified';
  theta: string; pressure: string; epsilon: string; cutoff: string;
  k: number; frame_size: number;
  baseline: RiemannBound; improved: RiemannBound; gain: RiemannBound; distinct: RiemannBound;
  strict_gain_gate: RiemannBound; certificate_sha256: string;
  audit: {
    verified: boolean; independent_sinc_taylor: boolean; precision_bits: number;
    nodes: number; validated_leaves: number; pressure_leaves: number; certificate_sha256: string;
  };
};
export type RiemannPressureOutcome = RiemannPressureWinner | {
  candidate: number;
  status: 'inconclusive' | 'refuted_by_exact_witness' | 'rejected_gain_gate' | 'not_run_after_higher_ranked_success';
  reason?: string; pressure?: string; epsilon?: string; cutoff?: string;
};
export type RiemannParityResult = {
  schema: 'riemann-exp004-results-v1';
  experiment: 'EXP-004-parity-density-transfer';
  arithmetic_status: 'verified';
  scope: string;
  provenance: {
    declaration_commit: string;
    hypothesis: { path: string; sha256: string; source_commit: string };
    inputs: { path: string; sha256: string; source_commit: string }[];
    runner: { path: string; sha256: string };
  };
  symbolic: { residual_identities: number; multiplicity_regression_cases: number; raw_artifact: string; sha256: string };
  census: {
    vectors: number; sigma_evaluations: number; sigma_values: number[];
    raw_artifact: string; sha256: string; scope: string;
  };
  relaxation: { cases: number; raw_artifact: string; sha256: string };
  sharpness: {
    cases: number; raw_artifact: string; sha256: string;
    negative_control: { N: number; s: number; Z: number; false_half_sum_residual: number };
  };
  threshold: {
    alpha: string; c_alpha_upper: string; c_alpha_upper_negative: boolean;
    derivative_cap: string; derivative_cap_less_than: string; derivative_formula_verified: boolean;
    classical_a: null; kappa: null; theta0_numeric: null; theta1_decimal: null;
    delta_formula: string; theta1_formula: string; simple_lower_formula: string; distinct_lower_formula: string;
    scope: string;
  };
  proof_status: { all_height_theorem: string; classical_seed: string; full_proof_and_final_verdict: string };
};
export type RiemannParityReview = {
  schema: 'riemann-exp004-proof-review-v1';
  scientific_verdict: 'confirmed';
  universal_finite_proof_reviewed: boolean; asymptotic_transfer_reviewed: boolean;
  numerical_exponent_claimed: false;
  declaration_commit: string; reviewed_utc: string; confirmed_conclusion: string;
  review_scope: string; novelty_scope: string; imported_inputs: string[]; unquantified: string[];
  source_sha256: Record<'parity_result' | 'parity_hypothesis' | 'parity_proof' | 'parity_audit' | 'parity_verdict', string>;
};
export type RiemannExact = { decimal: string; numerator: string; denominator: string };
export type RiemannLocalResult = {
  schema: 'riemann-exp005-results-v1'; status: 'pass'; passed: true;
  checks: Record<string, boolean>;
  claim_boundary: { analytic_theorem: string; finite_certificate: string; rh_solved: false };
  boundary_control: { accepted: false; margin: RiemannExact; u: RiemannExact };
  parameters: {
    theta: RiemannExact; negative_control_theta: RiemannExact;
    mollifier_exponent_u: RiemannExact; simple_gate: RiemannExact;
  };
  positive_point: {
    c_lower: RiemannExact; c_upper: RiemannExact;
    fixed_u_kappa_lower: RiemannExact; fixed_u_kappa_upper: RiemannExact;
    fixed_u_simple_lower: RiemannExact; fixed_u_simple_upper: RiemannExact;
    kappa_curve_lower: RiemannExact; kappa_curve_upper: RiemannExact;
    simple_curve_lower: RiemannExact; simple_curve_upper: RiemannExact;
    localization_exponent_margin: RiemannExact;
  };
  negative_control: { simple_curve_lower: RiemannExact; simple_curve_upper: RiemannExact };
  source_constant: { name: string; center: RiemannExact; lower: RiemannExact; upper: RiemannExact; radius: RiemannExact };
  execution_identity: {
    head: string; hypothesis_sha256: string; run_py_sha256: string;
    tracked_clean_at_start: boolean; python: string;
  };
};
export type RiemannLocalReview = {
  schema: 'riemann-exp005-proof-review-v1'; scientific_verdict: 'confirmed';
  declaration_commit: string; canonical_commit: string; reviewed_utc: string;
  analytic_localization_reviewed: true; exact_certificate_reviewed: true;
  confirmed_conclusion: string; review_scope: string; novelty_scope: string;
  imported_inputs: string[]; unquantified: string[];
  source_sha256: Record<'hypothesis' | 'mathematical_proof' | 'adversarial_audit' | 'result' | 'verdict', string>;
};
export type RiemannHilbertResult = {
  schema: 'riemann-exp006-results-v2'; status: 'pass'; passed: true;
  checks: Record<string, boolean>;
  claim_boundary: { analytic_theorem: string; finite_certificate: string; rank_six: string; rh_solved: false };
  parameters: {
    theta: RiemannExact; root_lower_theta: RiemannExact;
    root_upper_theta: RiemannExact; simple_gate: RiemannExact;
  };
  target: {
    c_upper: RiemannExact; k_lower: RiemannExact; old_linear_upper: RiemannExact;
    weak_simple_lower: RiemannExact; weak_simple_upper: RiemannExact;
    strong_simple_lower: RiemannExact; strong_simple_upper: RiemannExact;
  };
  root_bracket: {
    lower: { root_function_upper: RiemannExact };
    upper: { root_function_lower: RiemannExact };
    monotonicity: string;
  };
  finite_census: {
    cases: number; equality_cases: number; strict_cases: number;
    empty_dimension_cases: number; universal_status: string;
  };
  scalar_headline_barrier: { passed: true; checks: Record<string, boolean>; description: string };
  execution_identity: {
    head: string; hypothesis_sha256: string; run_py_sha256: string;
    tracked_clean_at_start: boolean; python: string;
  };
  source_constants: { C3: { center: RiemannExact }; C6: { center: RiemannExact; role: string } };
};
export type RiemannHilbertReview = {
  schema: 'riemann-exp006-proof-review-v1'; scientific_verdict: 'confirmed';
  declaration_commit: string; canonical_commit: string; reviewed_utc: string;
  analytic_transfer_reviewed: true; exact_certificate_reviewed: true;
  confirmed_conclusion: string; finite_theorem: string; review_scope: string;
  novelty_scope: string; imported_inputs: string[]; unquantified: string[];
  source_sha256: Record<'hypothesis' | 'mathematical_proof' | 'adversarial_audit' |
    'result' | 'verdict' | 'runner' | 'focused_test', string>;
};
export type RiemannData = {
  schema: 'riemann-replay-v5';
  reviewed_on: string;
  result: {
    theta: string; radius: string; delta: string;
    baseline: RiemannBound; improved: RiemannBound; gain: RiemannBound;
    audit: {
      verified: boolean; independent_sinc_taylor: boolean; precision_bits: number;
      nodes: number; energy_leaves: number; outside_leaves: number;
    };
    scope: string;
  };
  constant_audit: {
    status: string;
    constants: Record<string, {
      status: string;
      exact: { decimal_lower: string; decimal_upper: string; lower: string; upper: string };
    }>;
  };
  pressure_result: {
    schema: 'riemann-exp003-results-v1';
    stage_a: {
      arithmetic_status: 'verified'; theta: string; radius: string; delta: string;
      k: number; frame_size: number; gain_ratio_to_exp002: string;
      baseline: RiemannBound; improved: RiemannBound; gain: RiemannBound; distinct: RiemannBound;
      invariants: { index_cases: number; symbolic_identities: number; pairs_disjoint: boolean; spans_telescope: boolean };
      replay: { verified: boolean; independent_sinc_taylor: boolean; precision_bits: number;
        nodes: number; energy_leaves: number; outside_leaves: number };
    };
    stage_b: {
      arithmetic_status: 'verified' | 'not_confirmed'; candidate_list_sha256: string;
      outcomes: RiemannPressureOutcome[];
    };
    scope: string;
  };
  parity_result: RiemannParityResult;
  parity_review: RiemannParityReview;
  local_result: RiemannLocalResult;
  local_review: RiemannLocalReview;
  hilbert_result: RiemannHilbertResult;
  hilbert_review: RiemannHilbertReview;
  provenance: {
    role: string; source_exp: string; path: string; source_commit: string;
    bytes: number; sha256: string;
  }[];
};
export const loadRiemann = () => load<RiemannData>('riemann');
