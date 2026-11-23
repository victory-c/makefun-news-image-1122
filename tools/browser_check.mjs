// SPDX-License-Identifier: MIT
// Development-only browser acceptance check. Requires Playwright outside the entry.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, join } from 'node:path';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = dirname(dirname(fileURLToPath(import.meta.url)));
const out = join(root, 'out');
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ headless: true });
try {
  const context = await browser.newContext({ viewport: { width: 1100, height: 1250 }, deviceScaleFactor: 1 });
  const page = await context.newPage();
  const errors = [];
  const external = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.route(/^https?:/, async route => {
    external.push(route.request().url());
    await route.abort();
  });
  await page.goto(pathToFileURL(join(root, 'index.html')).href);
  const image = page.locator('img');
  await image.evaluate(i => i.decode());
  const native = await image.evaluate(i => ({ complete: i.complete, width: i.naturalWidth, height: i.naturalHeight, alt: i.alt }));
  assert.equal(native.complete, true);
  assert.equal(native.width, 1024);
  assert.equal(native.height, 1024);
  assert.match(native.alt, /22 November 2026/);
  const imageBox = await image.boundingBox();
  assert.equal(imageBox.width, 1024);
  assert.equal(imageBox.height, 1024);
  await image.screenshot({ path: join(out, 'browser-image.png') });
  await page.screenshot({ path: join(out, 'desktop-final.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  const mobile = await image.boundingBox();
  assert.equal(mobile.width, 390);
  assert.equal(mobile.height, 390);
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
  await page.screenshot({ path: join(out, 'mobile-final.png'), fullPage: true });
  const download = page.locator('a[download]');
  assert.equal(await download.getAttribute('href'), 'entry.png');
  assert.deepEqual(errors, []);
  assert.deepEqual(external, []);
  console.log(JSON.stringify({ status: 'PASS', desktop: '1024x1024', mobile: '390x390', externalRequests: external.length, errors, screenshots: out }));
  await context.close();
} finally {
  await browser.close();
}
