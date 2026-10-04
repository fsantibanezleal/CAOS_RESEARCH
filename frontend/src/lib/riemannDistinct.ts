import type { RiemannData } from '../api/data';
import { separatePublicationEvidence } from './riemannPublication';

/** Admit recorded evidence only; this does not verify the underlying theorem. */
export function distinctZeroEvidence(data: RiemannData | null) {
  const d = data?.distinct_zero;
  const roles = new Set(data?.provenance?.map((p) => p.role));
  const required = ['distinct_cover', 'distinct_transfer', 'distinct_native',
    'distinct_controls', 'distinct_archive', 'distinct_vector', 'distinct_vector_preflight',
    'distinct_attestation', 'distinct_external_source', 'distinct_license',
    'distinct_vector_proof', 'distinct_vector_review', 'distinct_vector_verdict',
    'distinct_local_proof', 'distinct_local_verdict', 'distinct_publication', 'distinct_paper',
    'distinct_current_publication', 'distinct_companion'];
  if (data?.schema !== 'riemann-replay-v9' || d?.schema !== 'riemann-distinct-zero-v1'
      || d.accepted !== true || d.local?.accepted !== true || d.vector?.accepted !== true
      || d.local.completed_shards !== 96 || d.local.closed_cells !== 61029
      || d.local.nodes !== 107752902 || d.local.corruption_controls !== 12
      || d.local.fraction !== '3997934614153/4775507750000'
      || d.vector.fraction !== '30945470743359/36955122080000'
      || d.vector.external_local_formalization_rebuilt_here !== false
      || d.vector.gap_pressures?.length !== 6
      || d.publication?.passed !== true || d.archive?.passed !== true
      || d.publication.concept_doi !== '10.5281/zenodo.23128662'
      || !separatePublicationEvidence(d.publication, d.evidence_companion, {
        manuscript: '23128663', companion: '23135359',
        pdf: '2d524ee456b330598a78bf56ab532e93ca027c500c846065b103dcfcd1cba0c4',
        archives: ['91be4798774837bc16007a8236a692078e825ffb1c8dfa476c05d3c733b17879',
          '0fd01004c2a07f5f2500d4d2138cf87f82485ba5f4d7323ef08e096440249c54'],
      })
      || d.publication.files[0].live_download_exact_match !== true
      || !d.incomplete_experiments?.includes('019') || !d.incomplete_experiments.includes('023')
      || !required.every((role) => roles.has(role))) return null;
  const source = data.provenance.find((p) => p.role === 'distinct_external_source');
  if (source?.sha256 !== d.vector.source_sha256) return null;
  return d;
}
