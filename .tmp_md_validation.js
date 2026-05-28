const fs = require('node:fs');
const cp = require('node:child_process');
const path = require('node:path');

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full, out);
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      out.push(full);
    }
  }
  return out;
}

const root = process.cwd();
const allMd = walk(root).sort();
const crlfFiles = allMd.filter((file) => fs.readFileSync(file, 'utf8').includes('\r'));
let tracked = [];
try {
  tracked = cp.execFileSync('git', ['ls-files', '*.md'], { encoding: 'utf8' }).split(/\r?\n/).filter(Boolean);
} catch {}

const normalizedOnly = [];
const substantive = [];
const headMissing = [];

for (const rel of tracked) {
  const work = fs.readFileSync(rel, 'utf8');
  let head;
  try {
    head = cp.execFileSync('git', ['show', `HEAD:${rel}`], { encoding: 'utf8' });
  } catch {
    headMissing.push(rel);
    continue;
  }

  if (head === work) continue;
  if (head.replace(/\r\n/g, '\n') === work.replace(/\r\n/g, '\n')) {
    normalizedOnly.push(rel);
  } else {
    substantive.push(rel);
  }
}

const trackedMarkdownDiffs = cp
  .execFileSync('git', ['diff', '--name-only', '--', '*.md'], { encoding: 'utf8' })
  .split(/\r?\n/)
  .filter(Boolean);

console.log(
  JSON.stringify(
    {
      markdownFileCount: allMd.length,
      crlfMarkdownFiles: crlfFiles.map((file) => path.relative(root, file).replace(/\\/g, '/')),
      trackedMarkdownDiffs,
      normalizedOnlyCount: normalizedOnly.length,
      normalizedOnly,
      substantiveCount: substantive.length,
      substantive,
      headMissing,
    },
    null,
    2,
  ),
);
