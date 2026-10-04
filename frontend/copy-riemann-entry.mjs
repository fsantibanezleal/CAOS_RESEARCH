// Give the published Riemann route a real Pages entry instead of a 404 bounce.
// Root-relative assets/data let it reuse the exact existing app HTML.
import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const frontend = dirname(fileURLToPath(import.meta.url));
const dist = join(frontend, 'dist');
const entry = join(dist, 'problems', 'riemann-hypothesis');
mkdirSync(entry, { recursive: true });
copyFileSync(join(dist, 'index.html'), join(entry, 'index.html'));
console.log('[copy-riemann-entry] root HTML -> Riemann static entry');
