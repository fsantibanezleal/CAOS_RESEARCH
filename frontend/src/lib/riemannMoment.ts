import type { RiemannData } from '../api/data';

/** Recorded analytic admission, distinct from the old conditional arithmetic. */
export function shortWindowMomentEvidence(data: RiemannData | null) {
  const m = data?.short_window_moment;
  if (data?.schema !== 'riemann-replay-v9' || m?.schema !== 'riemann-short-window-moment-v1'
      || m.accepted !== true || m.analytic_moment_reviewed !== true
      || m.scientific_verdict !== 'confirmed-internal-relative-to-attributed-inputs'
      || m.theta !== '5339/10000' || m.nu !== '349/10000' || m.eta !== '1/100000'
      || m.gaussian_theta !== '53389/100000' || m.onset !== '0.5339'
      || m.simple_density_decimal !== '0.0003985233159135'
      || m.simple_density_floor !== '797046631827/2000000000000000'
      || m.charged_exponents?.join(',') !== '-7/250000,-937/400000'
      || m.adversarial_boxes !== 7430 || m.arithmetic_alone_proves_theorem !== false
      || m.external_peer_review !== false || m.worldwide_priority_confirmed !== false
      || m.effective_height !== false || m.rh_solved !== false
      || m.publication?.passed !== true || m.publication.status !== 'published'
      || m.publication.version !== '0.02' || m.publication.version_doi !== '10.5281/zenodo.23132248'
      || m.publication.concept_doi !== '10.5281/zenodo.22984154'
      || m.publication.external_peer_review !== false || m.publication.files?.length !== 2
      || !m.publication.files.every((f) => f.live_bytes_verified === true)
      || Object.keys(m.source_sha256 || {}).length !== 22
      || !Object.entries(m.source_sha256).every(([role, sha]) =>
        data.provenance.some((p) => p.role === role && p.sha256 === sha))
      || !data.provenance.some((p) => p.role === 'moment_review')) return null;
  return m;
}
