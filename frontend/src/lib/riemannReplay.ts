import type { RiemannData, RiemannPressureWinner } from '../api/data';

/** Select persisted, replayed evidence only. This does no scientific arithmetic. */
export function pressureWinner(data: RiemannData | null): RiemannPressureWinner | undefined {
  if (data?.pressure_result?.stage_b.arithmetic_status !== 'verified') return undefined;
  return data.pressure_result.stage_b.outcomes.find(
    (outcome): outcome is RiemannPressureWinner =>
      outcome.status === 'arithmetic_verified' &&
      outcome.audit.verified && outcome.audit.independent_sinc_taylor &&
      outcome.certificate_sha256 === outcome.audit.certificate_sha256,
  );
}

/** Retain the source decimal center and exponent, without binary-float conversion. */
export function decimalCenter(display: string) {
  return display.replace(/^\[/, '').split(' +/- ')[0];
}

/** A finite census is not the asymptotic theorem. Require its separate review
 * and matching exported source-byte records before displaying the new result. */
export function parityEvidence(data: RiemannData | null) {
  const result = data?.parity_result;
  const review = data?.parity_review;
  if (!data || !result || !review || result.arithmetic_status !== 'verified' ||
      result.schema !== 'riemann-exp004-results-v1' || result.experiment !== 'EXP-004-parity-density-transfer' ||
      review.schema !== 'riemann-exp004-proof-review-v1' ||
      review.scientific_verdict !== 'confirmed' ||
      !review.universal_finite_proof_reviewed || !review.asymptotic_transfer_reviewed ||
      review.numerical_exponent_claimed !== false) return undefined;
  if (result.provenance.declaration_commit !== review.declaration_commit ||
      result.provenance.hypothesis.source_commit !== review.declaration_commit ||
      result.provenance.inputs.some((input) => input.source_commit !== review.declaration_commit)) return undefined;
  const threshold = result.threshold;
  if (threshold.classical_a !== null || threshold.kappa !== null ||
      threshold.theta0_numeric !== null || threshold.theta1_decimal !== null) return undefined;
  const roles = ['parity_result', 'parity_hypothesis', 'parity_proof', 'parity_audit', 'parity_verdict'] as const;
  if (!roles.every((role) =>
    data.provenance.some((source) => source.role === role && source.sha256 === review.source_sha256[role]),
  )) return undefined;
  return { result, review };
}

function compareExact(left: { numerator: string; denominator: string }, right: { numerator: string; denominator: string }) {
  return BigInt(left.numerator) * BigInt(right.denominator) -
    BigInt(right.numerator) * BigInt(left.denominator);
}

/** EXP-005 has a finite exact certificate and a separate analytic proof review.
 * Require both records and their exported byte bindings before showing the threshold. */
export function localSelbergEvidence(data: RiemannData | null) {
  const result = data?.local_result;
  const review = data?.local_review;
  if (!data || !result || !review || data.schema !== 'riemann-replay-v5' ||
      result.schema !== 'riemann-exp005-results-v1' || result.status !== 'pass' || !result.passed ||
      Object.values(result.checks).some((passed) => passed !== true) ||
      result.claim_boundary.rh_solved !== false || result.boundary_control.accepted !== false ||
      review.schema !== 'riemann-exp005-proof-review-v1' || review.scientific_verdict !== 'confirmed' ||
      !review.analytic_localization_reviewed || !review.exact_certificate_reviewed ||
      result.execution_identity.head !== review.canonical_commit) return undefined;
  if (compareExact(result.positive_point.fixed_u_simple_lower, result.parameters.simple_gate) <= 0n ||
      BigInt(result.positive_point.localization_exponent_margin.numerator) <= 0n ||
      BigInt(result.negative_control.simple_curve_upper.numerator) >= 0n) return undefined;
  const roles = {
    hypothesis: 'local_hypothesis', mathematical_proof: 'local_proof',
    adversarial_audit: 'local_audit', result: 'local_result', verdict: 'local_verdict',
  } as const;
  if (!Object.entries(roles).every(([reviewRole, sourceRole]) =>
    data.provenance.some((source) => source.role === sourceRole &&
      source.sha256 === review.source_sha256[reviewRole as keyof typeof roles]),
  )) return undefined;
  return { result, review };
}

/** EXP-006 combines a universal proof with exact finite and interval checks.
 * Display it only when every reviewed source hash is present in the replay. */
export function hilbertParityEvidence(data: RiemannData | null) {
  const result = data?.hilbert_result;
  const review = data?.hilbert_review;
  if (!data || !result || !review || data.schema !== 'riemann-replay-v5' ||
      result.schema !== 'riemann-exp006-results-v2' || result.status !== 'pass' || !result.passed ||
      Object.values(result.checks).some((passed) => passed !== true) ||
      result.claim_boundary.rh_solved !== false ||
      review.schema !== 'riemann-exp006-proof-review-v1' || review.scientific_verdict !== 'confirmed' ||
      !review.analytic_transfer_reviewed || !review.exact_certificate_reviewed ||
      result.execution_identity.head !== review.canonical_commit) return undefined;
  if (compareExact(result.target.strong_simple_lower, result.parameters.simple_gate) <= 0n ||
      compareExact(result.target.strong_simple_lower, result.target.weak_simple_upper) <= 0n ||
      BigInt(result.target.old_linear_upper.numerator) >= 0n ||
      BigInt(result.root_bracket.lower.root_function_upper.numerator) >= 0n ||
      BigInt(result.root_bracket.upper.root_function_lower.numerator) <= 0n ||
      !result.scalar_headline_barrier.passed) return undefined;
  const roles = {
    hypothesis: 'hilbert_hypothesis', mathematical_proof: 'hilbert_proof',
    adversarial_audit: 'hilbert_audit', result: 'hilbert_result', verdict: 'hilbert_verdict',
    runner: 'hilbert_runner', focused_test: 'hilbert_test',
  } as const;
  if (!Object.entries(roles).every(([reviewRole, sourceRole]) =>
    data.provenance.some((source) => source.role === sourceRole &&
      source.sha256 === review.source_sha256[reviewRole as keyof typeof roles]),
  )) return undefined;
  return { result, review };
}
