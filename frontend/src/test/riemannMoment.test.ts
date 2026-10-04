import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import type { RiemannData } from '../api/data';
import { shortWindowMomentEvidence } from '../lib/riemannMoment';

const replay = (): RiemannData => JSON.parse(readFileSync(join(__dirname, '../../../data/derived/research/riemann.json'), 'utf8'));
describe('short-window analytic evidence admission', () => {
  it('admits the reviewed published moment independently of old conditional flags', () => {
    const m = shortWindowMomentEvidence(replay());
    expect(m?.onset).toBe('0.5339');
    expect(m?.arithmetic_alone_proves_theorem).toBe(false);
    expect(m?.external_peer_review).toBe(false);
  });
  it('supports older replay deployments without fabricating the new result', () => {
    expect(shortWindowMomentEvidence(null)).toBeNull();
    const data = replay(); delete data.short_window_moment;
    expect(shortWindowMomentEvidence(data)).toBeNull();
  });
  it('rejects missing review, false scope, unpublished files and mismatched provenance', () => {
    for (const corrupt of [
      (d: RiemannData) => { d.short_window_moment!.analytic_moment_reviewed = false; },
      (d: RiemannData) => { d.short_window_moment!.arithmetic_alone_proves_theorem = true; },
      (d: RiemannData) => { d.short_window_moment!.eta = '0'; },
      (d: RiemannData) => { d.short_window_moment!.publication.status = 'draft'; },
      (d: RiemannData) => { d.short_window_moment!.publication.files[0].live_bytes_verified = false; },
      (d: RiemannData) => { d.short_window_moment!.source_sha256.moment_mellin = 'changed'; },
      (d: RiemannData) => { d.provenance = d.provenance.filter((p) => p.role !== 'moment_review'); },
      (d: RiemannData) => { d.short_window_moment!.external_peer_review = true; },
    ]) {
      const data = replay(); corrupt(data); expect(shortWindowMomentEvidence(data)).toBeNull();
    }
  });
});
