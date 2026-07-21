import { useEffect, useRef, useState } from 'react';
import { useT } from '../lib/i18n';

// The exact escape wall (EXP-007) and real census (EXP-011), replayed from the baked equation:
// bracket(A, B, C) = 27 A^2 C^2 - 18 A B C + 16 A + B^3 C - B^2; bracket < 0 <=> 3 real
// preimages, bracket > 0 <=> 1; the wall itself is the non-properness locus. Redrawn only on
// input change (no animation loops).
const bracket = (A: number, B: number, C: number) =>
  27 * A * A * C * C - 18 * A * B * C + 16 * A + B * B * B * C - B * B;

const LIM = 24;
const PX = 460;

export default function WallCanvas() {
  const t = useT();
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [C, setC] = useState(1);
  const [hover, setHover] = useState<{ A: number; B: number } | null>(null);

  useEffect(() => {
    const cv = canvasRef.current;
    if (!cv) return;
    const ctx = cv.getContext('2d');
    if (!ctx) return;
    const img = ctx.createImageData(PX, PX);
    const sign = new Int8Array(PX * PX);
    for (let py = 0; py < PX; py++) {
      const A = LIM - (2 * LIM * py) / (PX - 1);
      for (let px = 0; px < PX; px++) {
        const B = -LIM + (2 * LIM * px) / (PX - 1);
        sign[py * PX + px] = bracket(A, B, C) < 0 ? -1 : 1;
      }
    }
    for (let py = 0; py < PX; py++) {
      for (let px = 0; px < PX; px++) {
        const k = py * PX + px;
        const i = 4 * k;
        const s0 = sign[k];
        const edge =
          (px > 0 && sign[k - 1] !== s0) || (py > 0 && sign[k - PX] !== s0) ||
          (px < PX - 1 && sign[k + 1] !== s0) || (py < PX - 1 && sign[k + PX] !== s0);
        if (edge) {
          img.data[i] = 176; img.data[i + 1] = 46; img.data[i + 2] = 12; img.data[i + 3] = 255;
        } else if (s0 < 0) {
          img.data[i] = 253; img.data[i + 1] = 236; img.data[i + 2] = 228; img.data[i + 3] = 255;
        } else {
          img.data[i] = 230; img.data[i + 1] = 240; img.data[i + 2] = 253; img.data[i + 3] = 255;
        }
      }
    }
    ctx.putImageData(img, 0, 0);
  }, [C]);

  const onMove = (ev: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = ev.currentTarget.getBoundingClientRect();
    const B = -LIM + (2 * LIM * (ev.clientX - rect.left)) / rect.width;
    const A = LIM - (2 * LIM * (ev.clientY - rect.top)) / rect.height;
    setHover({ A, B });
  };

  const d = hover ? bracket(hover.A, hover.B, C) : null;
  return (
    <div className="rs-panel">
      <canvas
        ref={canvasRef}
        width={PX}
        height={PX}
        onMouseMove={onMove}
        onMouseLeave={() => setHover(null)}
        aria-label={t('Real census map: 3 preimages (warm) vs 1 (blue), wall in dark red', 'Mapa del censo real: 3 preimagenes (calido) vs 1 (azul), muro en rojo oscuro')}
      />
      <div className="rs-controls">
        <label>
          C = <b className="rs-readout">{C.toFixed(2)}</b>
          <input type="range" min={-3} max={3} step={0.05} value={C}
                 onChange={(e) => setC(Number(e.target.value))} />
        </label>
        <span className="rs-readout">
          {hover && d !== null
            ? <>A = <b>{hover.A.toFixed(1)}</b>, B = <b>{hover.B.toFixed(1)}</b>: {t('bracket', 'corchete')} {d < 0 ? '< 0' : '> 0'}, <b>{d < 0 ? 3 : 1}</b> {t('real preimages', 'preimagenes reales')}</>
            : t('Hover the map to read the census at a target; slide C to move the slice.', 'Pase el cursor para leer el censo en un objetivo; deslice C para mover el corte.')}
        </span>
      </div>
    </div>
  );
}
