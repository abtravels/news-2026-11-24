// The World in One Day — 24 November 2026 (Node 22, standard library only).
// Copies the pre-rendered image ./entry.png into the output directory
// the harness reads (MAKEFUN_OUTPUT_DIR, or /output by default).
// No rendering happens here, so the run needs no Python, no Pillow and
// no fonts: the image is drawn once at build time and shipped as-is.
// The copy is byte-identical to the committed entry.png every run.

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = join(here, 'entry.png');
const dest = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
console.log(`entry.png -> ${dest} (${statSync(dest).size} bytes)`);
