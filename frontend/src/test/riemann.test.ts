import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { renderToString } from 'katex';
import type { RiemannData } from '../api/data';
import { decimalCenter, parityEvidence, pressureWinner } from '../lib/riemannReplay';
import { riemannArchitecture } from '../lib/riemannArchitecture';
import { ARCHITECTURE } from '../lib/architecture';
import { CITATIONS } from '../data/citations';

const repo = join(__dirname, '..', '..', '..');
const replay = (): RiemannData => JSON.parse(readFileSync(join(repo, 'data/derived/research/riemann.json'), 'utf8'));
const pageSource = readFileSync(join(repo, 'frontend/src/pages/RiemannHypothesis.tsx'), 'utf8');

function parityFixture(): RiemannData {
  const data = replay();
  const roles = ['parity_result', 'parity_hypothesis', 'parity_proof', 'parity_audit', 'parity_verdict'] as const;
  const sourceSha256 = Object.fromEntries(roles.map((role) => [role, `${role}-hash`])) as Record<typeof roles[number], string>;
  data.schema = 'riemann-replay-v3';
  data.parity_result = {
    schema: 'riemann-exp004-results-v1', experiment: 'EXP-004-parity-density-transfer',
    arithmetic_status: 'verified',
    scope: 'exact controls',
    provenance: {
      declaration_commit: 'declaration',
      hypothesis: { path: 'hypothesis.md', sha256: sourceSha256.parity_hypothesis, source_commit: 'declaration' },
      inputs: [], runner: { path: 'run.py', sha256: 'runner-hash' },
    },
    threshold: { classical_a: null, kappa: null, theta0_numeric: null, theta1_decimal: null },
  } as unknown as RiemannData['parity_result'];
  data.parity_review = {
    schema: 'riemann-exp004-proof-review-v1', scientific_verdict: 'confirmed',
    universal_finite_proof_reviewed: true, asymptotic_transfer_reviewed: true,
    numerical_exponent_claimed: false, declaration_commit: 'declaration', reviewed_utc: 'now',
    confirmed_conclusion: 'fixed exponent range extension', review_scope: 'automated',
    novelty_scope: 'bounded', imported_inputs: [], unquantified: ['kappa'], source_sha256: sourceSha256,
  };
  data.provenance = roles.map((role) => ({
    role, source_exp: 'EXP-004-parity-density-transfer', path: role, source_commit: 'declaration', bytes: 0,
    sha256: sourceSha256[role],
  }));
  return data;
}

describe('Riemann pressure replay presentation', () => {
  it('selects the confirmed replay while preserving unrun outcomes and original evidence', () => {
    const data = replay();
    const saved = JSON.stringify(data);
    const winner = pressureWinner(data);
    expect(winner?.candidate).toBe(1);
    expect(winner?.improved.display).toContain('0.419087888170111727959091183775');
    expect(winner?.distinct.display).toContain('0.709543944085055863979545591887');
    expect(data.result.improved.display).toContain('0.419076828425303996736665787527');
    expect(data.pressure_result.stage_a.improved.display).toContain('0.419077736020568836833221725071');
    expect(data.pressure_result.stage_b.outcomes.slice(1).map((o) => o.status))
      .toEqual(['not_run_after_higher_ranked_success', 'not_run_after_higher_ranked_success']);
    expect(JSON.stringify(data)).toBe(saved);
  });

  it('does not surface a pressure winner when the stage is unconfirmed', () => {
    const data = replay();
    data.pressure_result.stage_b.arithmetic_status = 'not_confirmed';
    expect(pressureWinner(data)).toBeUndefined();
    expect(pressureWinner(null)).toBeUndefined();
  });

  it('surfaces EXP-004 only when the finite and asymptotic review gates agree', () => {
    const data = parityFixture();
    expect(parityEvidence(data)?.review.scientific_verdict).toBe('confirmed');
    data.parity_review.numerical_exponent_claimed = true as never;
    expect(parityEvidence(data)).toBeUndefined();
  });

  it('rejects an invented numerical seed or a source-hash mismatch', () => {
    const data = parityFixture();
    data.parity_result.threshold.kappa = '1/2' as never;
    expect(parityEvidence(data)).toBeUndefined();
    const clean = parityFixture();
    clean.provenance[0].sha256 = '0'.repeat(64);
    expect(parityEvidence(clean)).toBeUndefined();
  });

  it.each(['unverified', 'missing-second-evaluator', 'wrong-certificate'] as const)(
    'does not surface a pressure winner with %s evidence',
    (failure) => {
      const data = replay();
      const candidate = pressureWinner(data)!;
      if (failure === 'unverified') candidate.audit.verified = false;
      if (failure === 'missing-second-evaluator') candidate.audit.independent_sinc_taylor = false;
      if (failure === 'wrong-certificate') candidate.audit.certificate_sha256 = '0'.repeat(64);
      expect(pressureWinner(data)).toBeUndefined();
    },
  );

  it('preserves small scientific-notation gains and long decimal centers exactly', () => {
    const winner = pressureWinner(replay())!;
    expect(decimalCenter(winner.gain.display))
      .toBe('1.28751946873942245375730769810018160378953296e-5');
    expect(decimalCenter(winner.improved.display))
      .toBe('0.419087888170111727959091183775223467981706544');
  });

  it('all authored mathematical expressions parse in KaTeX', () => {
    const expressions = [...pageSource.matchAll(/tex=\{String\.raw`([^`]*)`\}/g)].map((m) => m[1]);
    expect(expressions.length).toBeGreaterThan(10);
    for (const expression of expressions) {
      expect(() => renderToString(expression, { throwOnError: true })).not.toThrow();
    }
  });

  it('every inline Riemann citation resolves to the source catalogue', () => {
    const ids = [...pageSource.matchAll(/<Cite id="([^"]+)"/g)].map((m) => m[1]);
    for (const id of ids) expect(CITATIONS.some((citation) => citation.id === id)).toBe(true);
    expect(CITATIONS.find((citation) => citation.id === 'riemann-refinement2026')?.doi)
      .toBe('10.5281/zenodo.22727389');
    expect(pageSource).toContain('10.5281/zenodo.22823615');
  });
});

describe('Riemann contextual architecture', () => {
  it.each(['en', 'es'] as const)('binds the %s proof and replay routes without changing other shared tabs', (lang) => {
    const config = riemannArchitecture(lang);
    expect(config.tabs.map((tab) => tab.id)).toEqual(ARCHITECTURE.tabs.map((tab) => tab.id));
    for (const original of ARCHITECTURE.tabs) {
      const tab = config.tabs.find((item) => item.id === original.id)!;
      if (original.id !== 'science' && original.id !== 'method') expect(tab).toEqual(original);
    }
    const science = config.tabs.find((tab) => tab.id === 'science')!;
    const method = config.tabs.find((tab) => tab.id === 'method')!;
    expect(science.svg).toContain('EXP-004-parity-density-transfer/mathematical-proof.md');
    expect(science.svg).toContain(lang === 'en' ? 'Classical odd-zero seed' : 'Densidad clásica de ceros impares');
    expect(method.svg).toContain('docs/guides/riemann-replay.md');
    expect(method.svg).toContain('EXP-001 · EXP-002 · EXP-003 · EXP-004');
    expect(method.svg).toContain(lang === 'en' ? 'Audit parity and pressure' : 'Auditar paridad y presión');
    expect(science.body_en).toContain('not overlapping triples');
    expect(science.body_es).toContain('no entre ternas superpuestas');
  });
});
