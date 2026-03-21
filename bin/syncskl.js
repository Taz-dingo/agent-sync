#!/usr/bin/env node
/* syncskl: SSOT facts CLI (repo-local)
 * Usage:
 *   node syncskl/bin/syncskl.js check
 *   node syncskl/bin/syncskl.js get <key>
 *   node syncskl/bin/syncskl.js search <query>
 *   node syncskl/bin/syncskl.js set <key> --value <json> [--source <text>] [--confidence confirmed|likely|tentative]
 */

const fs = require('fs');
const path = require('path');

function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function repoRoot() {
  // This script lives at syncskl/bin/syncskl.js
  return path.resolve(__dirname, '..', '..');
}

function syncsklRoot() {
  return path.resolve(__dirname, '..');
}

function listFactFiles() {
  const dir = path.join(syncsklRoot(), 'facts');
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith('.json'))
    .map((f) => path.join(dir, f));
}

function readJson(file) {
  const raw = fs.readFileSync(file, 'utf8');
  if (!raw.trim()) die(`Empty JSON file: ${file}`);
  try {
    return JSON.parse(raw);
  } catch (e) {
    die(`Failed to parse JSON: ${file}\n${e.message}`);
  }
}

function loadAllFacts() {
  const files = listFactFiles();
  const all = [];
  for (const f of files) {
    const j = readJson(f);
    const facts = j.facts || {};
    for (const [key, entry] of Object.entries(facts)) {
      all.push({ key, entry, file: f });
    }
  }
  return all;
}

function nowDate() {
  // Asia/Shanghai date is fine; we just store YYYY-MM-DD from local time.
  const d = new Date();
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd}`;
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const k = a.slice(2);
      const v = argv[i + 1];
      if (v == null || v.startsWith('--')) args[k] = true;
      else {
        args[k] = v;
        i++;
      }
    } else {
      args._.push(a);
    }
  }
  return args;
}

function cmdGet(key) {
  const all = loadAllFacts();
  const hit = all.find((x) => x.key === key);
  if (!hit) die(`Not found: ${key}`);
  process.stdout.write(JSON.stringify(hit.entry.value, null, 2) + '\n');
}

function cmdSearch(query) {
  const q = query.toLowerCase();
  const all = loadAllFacts();
  const hits = all.filter(({ key, entry }) => {
    const blob = JSON.stringify({ key, entry }).toLowerCase();
    return blob.includes(q);
  });
  const out = hits.map(({ key, entry, file }) => ({
    key,
    value: entry.value,
    meta: entry.meta,
    file: path.relative(repoRoot(), file)
  }));
  process.stdout.write(JSON.stringify(out, null, 2) + '\n');
}

function cmdSet(key, opts) {
  const valueRaw = opts.value;
  if (!valueRaw) die('Missing --value (must be valid JSON, e.g. "\"<name>\"" or "{\"a\":1}")');

  let value;
  try {
    value = JSON.parse(valueRaw);
  } catch (e) {
    die(`--value is not valid JSON: ${e.message}`);
  }

  const source = opts.source || 'manual';
  const confidence = opts.confidence || 'confirmed';
  if (!['confirmed', 'likely', 'tentative'].includes(confidence)) {
    die('Invalid --confidence. Use confirmed|likely|tentative');
  }

  // Default file strategy: put everything into syncskl/facts/user.json unless user sets --file
  const file = opts.file
    ? path.resolve(repoRoot(), opts.file)
    : path.join(syncsklRoot(), 'facts', 'user.json');

  const j = readJson(file);
  if (!j.facts) j.facts = {};
  j.facts[key] = {
    value,
    meta: {
      source,
      confidence,
      updated_at: nowDate()
    }
  };

  fs.writeFileSync(file, JSON.stringify(j, null, 2) + '\n', 'utf8');
  process.stdout.write(`OK set ${key} -> ${path.relative(repoRoot(), file)}\n`);
}

function cmdCheck() {
  // Minimal checks without dependencies:
  // - every facts file parses
  // - each entry has meta.source/meta.confidence/meta.updated_at
  // - no duplicate keys across files
  const all = loadAllFacts();
  const seen = new Map();
  let ok = true;

  for (const { key, entry, file } of all) {
    if (seen.has(key)) {
      ok = false;
      console.error(`DUPLICATE KEY: ${key}\n  - ${path.relative(repoRoot(), seen.get(key))}\n  - ${path.relative(repoRoot(), file)}`);
    } else {
      seen.set(key, file);
    }

    if (!entry || typeof entry !== 'object') {
      ok = false;
      console.error(`INVALID ENTRY (not object): ${key} in ${path.relative(repoRoot(), file)}`);
      continue;
    }
    if (!('value' in entry)) {
      ok = false;
      console.error(`MISSING value: ${key} in ${path.relative(repoRoot(), file)}`);
    }
    const m = entry.meta;
    if (!m || typeof m !== 'object') {
      ok = false;
      console.error(`MISSING meta: ${key} in ${path.relative(repoRoot(), file)}`);
    } else {
      if (!m.source) {
        ok = false;
        console.error(`MISSING meta.source: ${key} in ${path.relative(repoRoot(), file)}`);
      }
      if (!m.confidence) {
        ok = false;
        console.error(`MISSING meta.confidence: ${key} in ${path.relative(repoRoot(), file)}`);
      }
      if (!m.updated_at) {
        ok = false;
        console.error(`MISSING meta.updated_at: ${key} in ${path.relative(repoRoot(), file)}`);
      }
    }
  }

  if (!listFactFiles().length) {
    ok = false;
    console.error('No facts files found under syncskl/facts/*.json');
  }

  if (!ok) process.exit(1);
  process.stdout.write('OK\n');
}

function main() {
  const argv = process.argv.slice(2);
  if (!argv.length) {
    die('Usage: syncskl <check|get|search|set> ...');
  }

  const cmd = argv[0];
  const args = parseArgs(argv.slice(1));

  if (cmd === 'get') {
    const key = args._[0];
    if (!key) die('Usage: syncskl get <key>');
    return cmdGet(key);
  }
  if (cmd === 'search') {
    const q = args._[0];
    if (!q) die('Usage: syncskl search <query>');
    return cmdSearch(q);
  }
  if (cmd === 'set') {
    const key = args._[0];
    if (!key) die('Usage: syncskl set <key> --value <json> [--source <text>]');
    return cmdSet(key, args);
  }
  if (cmd === 'check') {
    return cmdCheck();
  }

  die(`Unknown command: ${cmd}`);
}

main();
