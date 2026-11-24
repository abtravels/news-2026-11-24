// The World in One Day — 24 November 2026 (Node 22, standard library only).
// Runs the Python renderer beside this file, which draws the front page
// with Pillow and writes entry.png to /output (or $MAKEFUN_OUTPUT_DIR).
// Deterministic: the same drawing runs twice and writes identical bytes.
// After rendering, the program checks the file exists and reports its size.

import { execFileSync } from 'node:child_process';
import { existsSync, statSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const outFile = join(outDir, 'entry.png');

execFileSync('python3', [join(here, 'draw.py')], {
  cwd: here,
  stdio: 'inherit',
  env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
});

if (!existsSync(outFile)) {
  throw new Error(`renderer did not write ${outFile}`);
}
console.log(`entry.png: ${statSync(outFile).size} bytes`);
