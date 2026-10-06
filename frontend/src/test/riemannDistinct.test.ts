import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import type { RiemannData } from '../api/data';
import { distinctZeroEvidence } from '../lib/riemannDistinct';

const replay = (): RiemannData => JSON.parse(readFileSync(join(__dirname, '../../../data/derived/research/riemann.json'), 'utf8'));

describe('completed distinct-zero evidence admission', () => {
  it('admits only the two completed source-bound results', () => {
    const d = distinctZeroEvidence(replay());
    expect(d?.vector.fraction).toBe('30945470743359/36955122080000');
    expect(d?.local.completed_shards).toBe(96);
    expect(d?.vector.external_local_formalization_rebuilt_here).toBe(false);
    expect(d?.incomplete_experiments).toEqual(['019', '023']);
  });
  it('preserves compatibility with an older or missing replay', () => {
    expect(distinctZeroEvidence(null)).toBeNull();
    const data = replay(); delete data.distinct_zero;
    expect(distinctZeroEvidence(data)).toBeNull();
  });
  it('rejects incomplete cover, fabricated formal rebuild, changed source and unpublished files', () => {
    for (const corrupt of [
      (d: RiemannData) => { d.distinct_zero!.local.completed_shards = 95; },
      (d: RiemannData) => { d.distinct_zero!.vector.external_local_formalization_rebuilt_here = true; },
      (d: RiemannData) => { d.distinct_zero!.vector.source_sha256 = 'changed'; },
      (d: RiemannData) => { d.distinct_zero!.publication.files[0].live_download_exact_match = false; },
      (d: RiemannData) => { d.distinct_zero!.publication.files.push(d.distinct_zero!.evidence_companion.files[0]); },
      (d: RiemannData) => { d.distinct_zero!.evidence_companion.files.pop(); },
      (d: RiemannData) => { d.distinct_zero!.evidence_companion.files[0].sha256 = 'changed'; },
      (d: RiemannData) => { d.distinct_zero!.evidence_companion.metadata.related_identifiers = []; },
      (d: RiemannData) => { d.distinct_zero!.evidence_companion.record_id = '23128663'; },
      (d: RiemannData) => { d.provenance = d.provenance.filter((p) => p.role !== 'distinct_native'); },
      (d: RiemannData) => { d.provenance = d.provenance.filter((p) => p.role !== 'distinct_companion'); },
      (d: RiemannData) => { d.distinct_zero!.vector.fraction = '2340938143167/2795532013000'; },
    ]) {
      const data = replay(); corrupt(data); expect(distinctZeroEvidence(data)).toBeNull();
    }
  });
});
