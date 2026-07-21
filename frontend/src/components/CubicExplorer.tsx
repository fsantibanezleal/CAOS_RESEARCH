import { useEffect, useRef, useState } from 'react';
import { useT } from '../lib/i18n';

// The fiber cubic W(w) = 4 Phi(w) - w BC + A C^2, Phi = w^2 - w^3 (EXP-002/007): the preimages
// of a target are exactly its roots; a multiple root is an escape. Live evaluation of one cubic
// per input change (no loops); the DEFAULT target is the engineered collision target (-16, -16, 1) with three rational preimages.
const PX_W = 560;
const PX_H = 300;

export default function CubicExplorer() {
  const t = useT();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [A, setA] = useState(-16);
  const [B, setB] = useState(-16);
  const [C, setC] = useState(1);

  const W = (w: number) => 4 * (w * w - w * w * w) - w * B * C + A * C * C;

  // Count sign changes of W on a fine grid (real roots up to grid resolution).
  const roots: number[] = [];
  {
    let scale = 1e-9;
    for (let i = 0; i <= 200; i++) scale = Math.max(scale, Math.abs(W(-3 + (6 * i) / 200)));
    let prev = W(-3);
    for (let i = 1; i <= 900; i++) {
      const w = -3 + (6 * i) / 900;
      const cur = W(w);
      if ((prev < 0 && cur >= 0) || (prev > 0 && cur <= 0)) roots.push(w);
      else if (Math.abs(cur) < scale * 1.5e-4 && Math.abs(prev) >= Math.abs(cur)
               && Math.abs(W(w + 6 / 900)) > Math.abs(cur)) roots.push(w);  // touching root
      prev = cur;
    }
  }

  useEffect(() => {
    const cv = canvasRef.current;
    const ctx = cv?.getContext('2d');
    if (!cv || !ctx) return;
    const styles = getComputedStyle(document.documentElement);
    const fg = styles.getPropertyValue('--rs-subtle') || '#5c6875';
    ctx.clearRect(0, 0, PX_W, PX_H);
    const xOf = (w: number) => ((w + 3) / 6) * PX_W;
    let ymax = 1e-9;
    for (let i = 0; i <= 200; i++) ymax = Math.max(ymax, Math.abs(W(-3 + (6 * i) / 200)));
    const yOf = (v: number) => PX_H / 2 - (v / ymax) * (PX_H / 2 - 12);
    ctx.strokeStyle = fg.trim() || '#5c6875';
    ctx.globalAlpha = 0.45;
    ctx.beginPath(); ctx.moveTo(0, yOf(0)); ctx.lineTo(PX_W, yOf(0)); ctx.stroke();
    ctx.globalAlpha = 1;
    ctx.strokeStyle = '#0969da';
    ctx.lineWidth = 2.2;
    ctx.beginPath();
    for (let i = 0; i <= 560; i++) {
      const w = -3 + (6 * i) / 560;
      const y = yOf(W(w));
      if (i === 0) ctx.moveTo(xOf(w), y); else ctx.lineTo(xOf(w), y);
    }
    ctx.stroke();
    ctx.fillStyle = '#b02e0c';
    for (const r of roots) {
      ctx.beginPath(); ctx.arc(xOf(r), yOf(0), 5, 0, 2 * Math.PI); ctx.fill();
    }
  });

  return (
    <div className="rs-panel">
      <canvas ref={canvasRef} width={PX_W} height={PX_H}
              aria-label={t('Fiber cubic with its real roots marked', 'Cubica de fibra con sus raices reales marcadas')} />
      <div className="rs-controls">
        <label>A = <b className="rs-readout">{A.toFixed(2)}</b>
          <input type="range" min={-20} max={20} step={0.25} value={A} onChange={(e) => setA(Number(e.target.value))} /></label>
        <label>B = <b className="rs-readout">{B.toFixed(2)}</b>
          <input type="range" min={-20} max={20} step={0.25} value={B} onChange={(e) => setB(Number(e.target.value))} /></label>
        <label>C = <b className="rs-readout">{C.toFixed(2)}</b>
          <input type="range" min={-3} max={3} step={0.05} value={C} onChange={(e) => setC(Number(e.target.value))} /></label>
        <span className="rs-readout">
          {t('real roots detected', 'raices reales detectadas')}: <b>{roots.length}</b>
          {' '}({t('each root reconstructs one preimage; a double root is an escape', 'cada raiz reconstruye una preimagen; una raiz doble es un escape')})
        </span>
      </div>
    </div>
  );
}
