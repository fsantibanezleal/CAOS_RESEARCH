import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

// The baked artifacts the site replays parse and carry the expected keys.
describe('baked artifacts', () => {
  const root = join(__dirname, '..', '..', '..', 'data', 'derived', 'research');
  it('jacobian payload has the exact anchors', () => {
    const jac = JSON.parse(readFileSync(join(root, 'jacobian.json'), 'utf-8'));
    expect(jac.map.det).toBe(-2);
    expect(jac.family.length).toBe(5);
    expect(jac.landscape.length).toBe(5);
  });
  it('experiments registry is non-empty with verdicts', () => {
    const ex = JSON.parse(readFileSync(join(root, 'experiments.json'), 'utf-8'));
    expect(ex.experiments.length).toBeGreaterThanOrEqual(12);
    expect(ex.experiments.every((e: { verdict: string }) => typeof e.verdict === 'string')).toBe(true);
  });
});
