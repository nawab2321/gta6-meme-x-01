const { mkdirSync, readFileSync, writeFileSync } = require('node:fs');
const { join } = require('node:path');

const input = join(process.env.MAKEFUN_BOT_DIR || '/bot', 'POST.json');
const outputDirectory = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const output = join(outputDirectory, 'POST.json');

try {
  // Read first so a missing source leaves the output untouched.
  const post = readFileSync(input);
  mkdirSync(outputDirectory, { recursive: true });
  writeFileSync(output, post);
} catch (error) {
  console.error('Unable to export POST.json:', error.message);
  process.exitCode = 1;
}
