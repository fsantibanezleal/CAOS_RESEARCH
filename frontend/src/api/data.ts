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
export type RiemannInterval = { lower: RiemannExact; upper: RiemannExact; width: RiemannExact };
export type RiemannSpectralResult = {
  schema: 'riemann-exp007-results-v1'; status: 'pass'; passed: true;
  checks: Record<string, boolean>;
  claim_boundary: {
    finite_theorem: string; global_record: false; numerical_certificate: string;
    onset_exponent_improved: false; rh_solved: false;
  };
  execution_identity: {
    declaration_commit: string; head: string; hypothesis_sha256: string;
    run_py_sha256: string; tracked_clean_at_start: boolean; python: string;
  };
  target: {
    theta: RiemannExact; h3: RiemannInterval; H: RiemannInterval;
    gain_H_minus_h3: RiemannInterval; certified_gain_floor: RiemannInterval; passed: true;
  } & Record<string, unknown>;
  multiplicity_census: { profiles: number; defect_trials: number; passed: true } & Record<string, unknown>;
  spectral_census: { spectra: number; strict_eigenvalues: number; passed: true } & Record<string, unknown>;
};
export type RiemannSpectralReview = {
  schema: 'riemann-exp007-proof-review-v1'; scientific_verdict: 'confirmed';
  declaration_commit: string; canonical_commit: string; reviewed_utc: string;
  analytic_transfer_reviewed: true; exact_certificate_reviewed: true;
  confirmed_conclusion: string; finite_theorem: string; review_scope: string;
  novelty_scope: string; imported_inputs: string[]; unquantified: string[];
  source_sha256: Record<'hypothesis' | 'mathematical_proof' | 'adversarial_audit' |
    'result' | 'verdict' | 'runner' | 'focused_test', string>;
};
export type RiemannRankPoint = {
  theta: RiemannExact; strong_simple: RiemannInterval; old_linear: RiemannInterval;
} & Record<string, unknown>;
export type RiemannRankSixResult = {
  schema: 'riemann-exp008-results-v1'; status: 'pass'; passed: true;
  checks: Record<string, boolean>;
  claim_boundary: {
    effective_starting_height: false; localization: string; rank_six_profile: string;
    rh_solved: false; scalar_certificate: string;
  };
  execution: {
    declaration_commit: string; device: string; elapsed_seconds: number;
    git: { head: string; tracked_clean_at_start: boolean };
  } & Record<string, unknown>;
  source_constants: {
    C3: { lower: RiemannExact; upper: RiemannExact };
    C6: { lower: RiemannExact; upper: RiemannExact };
  };
  root_brackets: {
    rank_six_coarse: { lower: RiemannRankPoint; upper: RiemannRankPoint };
    rank_six_fine: { lower: RiemannRankPoint; upper: RiemannRankPoint };
    rank_three_fine: { lower: RiemannRankPoint; upper: RiemannRankPoint };
    uniqueness: string;
  };
  edge_theta: { rank_six: RiemannRankPoint; rank_three: RiemannRankPoint };
  point_theta: {
    h6_minus_h3: RiemannInterval; rank_six: RiemannRankPoint; rank_three: RiemannRankPoint;
  };
  spectral_optimized: {
    rho: RiemannExact; h6: RiemannInterval; H6: RiemannInterval;
    gain_floor: RiemannInterval; reserve_alpha_h_minus_beta: RiemannInterval; passed: true;
  } & Record<string, unknown>;
};
export type RiemannRankSixReview = {
  schema: 'riemann-exp008-proof-review-v1';
  scientific_verdict: 'confirmed-relative-to-attributed-rank-six-input';
  declaration_commit: string; canonical_commit: string; reviewed_utc: string;
  confirmed_conclusion: string; critical_limitation: string; spectral_companion: string;
  manuscript_decision: string; review_scope: string; imported_inputs: string[]; unquantified: string[];
  source_sha256: Record<'hypothesis' | 'mathematical_proof' | 'adversarial_audit' |
    'result' | 'verdict' | 'runner' | 'focused_test', string>;
};
export type RiemannWangKernelResult = {
  schema: 'riemann-exp009-results-v1'; status: 'pass'; passed: true;
  checks: Record<string, boolean>;
  claim_boundary: {
    effective_height: false; global_framework: string; onset_exponent_improved: false;
    peer_reviewed: false; ratio_theorem: string; rh_solved: false;
    short_interval_pair_and_rank_six_inputs: string;
  };
  execution: {
    declaration_commit: string; amendment_commit: string; device: string; elapsed_seconds: number;
    git: { head: string; tracked_clean_at_start: boolean };
  } & Record<string, unknown>;
  constants: { d_dagger: RiemannInterval; d_wang: RiemannInterval } & Record<string, unknown>;
  ratio_theorem: { equality_cases: string[]; proof_type: string } & Record<string, unknown>;
  global: {
    H: RiemannExact; simple_proportion: RiemannInterval;
    distinct_proportion: RiemannInterval; gain: RiemannInterval;
  } & Record<string, unknown>;
  wang_reproduction: { simple_proportion: RiemannInterval; gain: RiemannInterval } & Record<string, unknown>;
  short_interval: {
    theta: RiemannExact; cell_length: number; certified_gain: RiemannInterval;
  } & Record<string, unknown>;
};
export type RiemannWangKernelReview = {
  schema: 'riemann-exp009-proof-review-v1';
  scientific_verdict: 'confirmed-relative-to-wang-v1-framework';
  declaration_commit: string; amendment_commit: string;
  canonical_execution_commit: string; canonical_artifact_commit: string;
  reviewed_utc: string; confirmed_conclusion: string; critical_limitation: string;
  short_interval_companion: string; manuscript_decision: string; review_scope: string;
  imported_inputs: string[]; unquantified: string[];
  source_sha256: Record<'hypothesis' | 'amendment' | 'mathematical_proof' | 'runner' |
    'focused_test' | 'result' | 'execution_receipt' | 'adversarial_audit', string>;
};
export type RiemannInterval40 = { lower: string; upper: string; arb: string };
export type RiemannLevinsonRow = {
  theta: string; nu: string; kappa_lower_used: string; wang_c: RiemannInterval40;
  h_L: RiemannInterval40; target: string; pass: boolean;
};
export type RiemannLevinsonResult = {
  experiment: 'EXP-010'; schema: 'exp010-canonical-v1'; accepted: boolean;
  checks: Record<string, boolean>;
  detector_constants: { nu: string; degree_Q: number; kappa: RiemannInterval40; kappa_over_nu_lower: string }[];
  onset: { rows: RiemannLevinsonRow[]; exp008_comparison: { ratio_h_L_over_h6_lower: string; pass: boolean } };
  bindings_sha256: Record<string, string>;
};
export type RiemannLevinsonReview = {
  schema: 'riemann-exp010-proof-review-v1';
  scientific_verdict: 'confirmed-with-scope-correction-to-prediction-A';
  declaration_commit: string; canonical_execution_commit: string;
  confirmed_conclusion: string; scope_correction: string; critical_limitation: string;
  source_sha256: Record<string, string>;
};
export type RiemannArbRecord = { mid: string; rad: string; arb: string };
export type RiemannBarrierResult = {
  experiment: 'EXP-011'; schema: 'exp011-canonical-v1'; accepted: boolean;
  checks: Record<'A' | 'B' | 'C' | 'D', boolean>;
  C1: { N: number; O: number; S: number; Q: RiemannArbRecord; slack_L: RiemannArbRecord };
  C2: { N: number; O: number; S: number; ratio_Q_minus_2N_over_O: RiemannArbRecord };
};
export type RiemannTangCheck = { model_within_2_percent: boolean; rows: Record<string, string>[] };
export type RiemannDistinctZero = {
  schema: 'riemann-distinct-zero-v1'; accepted: boolean;
  counted_objects: string; denominator: string;
  local: { fraction: string; decimal: string; accepted: boolean; m: number; r: number;
    tau: string; c: string; delta: string; pressure: string; completed_shards: number;
    nodes: number; closed_cells: number; corruption_controls: number };
  vector: { fraction: string; decimal: string; accepted: boolean; H_lower: string;
    parameters: { r: number; m: number; tau: string; c: string; delta: string; pressure_sum: string };
    gap_pressures: string[]; source_sha256: string; source_author: string;
    external_local_formalization_rebuilt_here: boolean };
  publication: { passed: boolean; concept_doi: string; version_doi: string; record_url: string;
    files: { filename: string; bytes: number; sha256: string; live_download_exact_match: boolean }[] };
  archive: { passed: boolean; members: number; archive_sha256: string };
  incomplete_experiments: string[]; excluded_claims: string[]; trust_boundary: string;
};
export type RiemannData = {
  schema: 'riemann-replay-v9';
  distinct_zero?: RiemannDistinctZero;
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
  spectral_result: RiemannSpectralResult;
  spectral_review: RiemannSpectralReview;
  rank_six_result: RiemannRankSixResult;
  rank_six_review: RiemannRankSixReview;
  wang_kernel_result: RiemannWangKernelResult;
  wang_kernel_review: RiemannWangKernelReview;
  levinson_result: RiemannLevinsonResult;
  levinson_review: RiemannLevinsonReview;
  barrier_result: RiemannBarrierResult;
  tang_check_output: RiemannTangCheck;
  provenance: {
    role: string; source_exp: string; path: string; source_commit: string;
    bytes: number; sha256: string;
  }[];
};
export const loadRiemann = () => load<RiemannData>('riemann');
