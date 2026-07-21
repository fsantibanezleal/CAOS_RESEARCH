// Prebuild: copy the committed CONTRACT-2 artifacts (../data/derived) into public/ so the
// static site replays them. Canonical copies live in ../data; public/data is a build-time
// overlay (git-ignored).
import { cpSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const derived = join(HERE, '..', 'data', 'derived');
const pub = join(HERE, 'public', 'data');
if (!existsSync(derived)) {
  console.error('[copy-data] no data/derived; run: python -m researchlab.pipeline all');
  process.exit(1);
}
mkdirSync(pub, { recursive: true });
cpSync(derived, pub, { recursive: true });
console.log('[copy-data] data/derived -> public/data');
