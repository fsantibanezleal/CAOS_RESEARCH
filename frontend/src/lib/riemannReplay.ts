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
