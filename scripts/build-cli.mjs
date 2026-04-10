import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, '..');
const packageJsonPath = path.join(projectRoot, 'package.json');
const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf-8'));

let esbuild;
try {
  esbuild = await import('esbuild');
} catch (error) {
  console.error('Missing dependency: esbuild');
  console.error('Run: npm install -D esbuild');
  process.exit(1);
}

const version = process.env.CLAUDE_CODE_VERSION || packageJson.version || '0.0.0-dev';
const buildTime = process.env.CLAUDE_CODE_BUILD_TIME || new Date().toISOString();
const packageUrl = process.env.CLAUDE_CODE_PACKAGE_URL || packageJson.name || '@anthropic-ai/claude-code';
const nativePackageUrl = process.env.CLAUDE_CODE_NATIVE_PACKAGE_URL || null;
const feedbackChannel =
  process.env.CLAUDE_CODE_FEEDBACK_CHANNEL || 'https://github.com/anthropics/claude-code/issues';
const issuesExplainer =
  process.env.CLAUDE_CODE_ISSUES_EXPLAINER ||
  'run /bug or open an issue at https://github.com/anthropics/claude-code/issues';
const versionChangelog = process.env.CLAUDE_CODE_VERSION_CHANGELOG || '';

const macroDefine = JSON.stringify({
  VERSION: version,
  BUILD_TIME: buildTime,
  PACKAGE_URL: packageUrl,
  NATIVE_PACKAGE_URL: nativePackageUrl,
  FEEDBACK_CHANNEL: feedbackChannel,
  ISSUES_EXPLAINER: issuesExplainer,
  VERSION_CHANGELOG: versionChangelog,
});

const srcAliasPlugin = {
  name: 'src-alias',
  setup(build) {
    build.onResolve({ filter: /^src\// }, (args) => ({
      path: path.join(projectRoot, args.path),
    }));
  },
};

const bunBundlePlugin = {
  name: 'bun-bundle-shim',
  setup(build) {
    build.onResolve({ filter: /^bun:bundle$/ }, () => ({
      path: 'bun:bundle',
      namespace: 'bun-bundle',
    }));

    build.onLoad({ filter: /.*/, namespace: 'bun-bundle' }, () => ({
      contents: `
const featureSet = new Set(
  (process.env.CLAUDE_CODE_FEATURES || '')
    .split(',')
    .map((x) => x.trim())
    .filter(Boolean)
);

export function feature(name) {
  return featureSet.has(name);
}
`,
      loader: 'js',
    }));
  },
};

const banner =
  '#!/usr/bin/env node\n' +
  '// (c) Anthropic PBC. All rights reserved. Use is subject to the Legal Agreements outlined here: https://code.claude.com/docs/en/legal-and-compliance.\n';

await esbuild.build({
  absWorkingDir: projectRoot,
  entryPoints: ['src/entrypoints/cli.tsx'],
  outfile: 'cli.js',
  bundle: true,
  format: 'esm',
  platform: 'node',
  target: ['node18'],
  sourcemap: true,
  legalComments: 'inline',
  logLevel: 'info',
  banner: { js: banner },
  define: {
    MACRO: macroDefine,
  },
  plugins: [srcAliasPlugin, bunBundlePlugin],
});

console.log(`Built cli.js from source (version=${version})`);
