import type { RiemannEvidenceCompanion, RiemannManuscriptPublication } from '../api/data';

/** Check recorded packaging and links. This does not re-download or prove science. */
export function separatePublicationEvidence(
  p: RiemannManuscriptPublication | undefined, c: RiemannEvidenceCompanion | undefined,
  expected: { manuscript: string; companion: string; pdf: string; archives: string[] },
) {
  if (!p || !c || p.schema !== 'caos-manuscript-publication-v2'
      || c.schema !== 'separate-zenodo-evidence-publication-v1'
      || p.passed !== true || c.passed !== true || p.status !== 'published' || c.status !== 'published'
      || p.manuscript_only !== true || p.scientific_content_changed !== false || p.external_peer_review !== false
      || c.resource_type !== 'dataset' || c.manuscript_pdf_included !== false
      || p.record_id !== expected.manuscript || c.record_id !== expected.companion
      || p.record_id === c.record_id || c.manuscript_record !== p.record_id
      || p.version_doi !== `10.5281/zenodo.${p.record_id}` || c.doi !== `10.5281/zenodo.${c.record_id}`
      || p.evidence_companion_doi !== c.doi || p.evidence_companion_record_id !== c.record_id
      || p.version !== c.version || p.metadata?.version !== p.version || c.metadata?.version !== c.version
      || p.metadata?.resource_type?.id !== 'publication-preprint' || c.metadata?.resource_type?.id !== 'dataset'
      || !p.metadata.related_identifiers?.some((r) => r.identifier === c.doi && r.relation_type.id === 'issupplementedby')
      || !c.metadata.related_identifiers?.some((r) => r.identifier === p.version_doi && r.relation_type.id === 'issupplementto')
      || p.files?.length !== 1 || c.files?.length !== expected.archives.length
      || p.record_url !== `https://zenodo.org/records/${p.record_id}`) return false;
  const pdf = p.files[0];
  if (!pdf.name.endsWith('.pdf') || pdf.sha256 !== expected.pdf || p.pdf_sha256 !== expected.pdf
      || pdf.live_bytes_verified !== true
      || pdf.url !== `https://zenodo.org/api/records/${p.record_id}/files/${pdf.name}/content`) return false;
  return new Set(c.files.map((f) => f.sha256)).size === expected.archives.length
    && c.files.every((f) => f.name.endsWith('.zip') && f.live_bytes_verified === true
      && expected.archives.includes(f.sha256)
      && f.url === `https://zenodo.org/api/records/${c.record_id}/files/${f.name}/content`);
}
