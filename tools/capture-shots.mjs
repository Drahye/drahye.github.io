/**
 * Capture the four linked sites for the workbench hover previews.
 *
 *   npm i playwright-core
 *   npx playwright@1.49.1 install chromium
 *   PW_EXE="$(find ~/Library/Caches/ms-playwright/chromium-* -name Chromium -type f | head -1)" \
 *     node tools/capture-shots.mjs
 *
 * Then: python3 tools/grade-shots.py
 *
 * Why Playwright and not the system browser: headless Chrome/Brave does not work
 * on macOS 13. `--headless=new` hangs indefinitely and `--headless=old` exits 0
 * without writing a file, failing on CVDisplayLinkCreateWithActiveCGDisplays.
 * Current Playwright also dropped macOS 13, hence the 1.49.1 pin above.
 */

import { chromium } from "playwright-core";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { mkdirSync } from "node:fs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(HERE, "shots");
mkdirSync(OUT, { recursive: true });

const SITES = [
  ["scholr", "https://getscholr.vercel.app/"],
  ["learningforest", "https://www.learningforest.co/"],
  ["agencymart", "https://drahye.github.io/claude-project-1/#/"],
  ["tourstack", "https://drahye.github.io/tourstack-preview/tourstack-landing.html"],
];

const browser = await chromium.launch({ executablePath: process.env.PW_EXE });

for (const [name, url] of SITES) {
  const ctx = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 1,
    reducedMotion: "reduce", // freeze entrance animations mid-flight
  });
  const page = await ctx.newPage();
  try {
    await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
  } catch {
    // networkidle never settles on sites with long-polling or looping media
    try {
      await page.goto(url, { waitUntil: "load", timeout: 30000 });
    } catch {}
  }
  await page.waitForTimeout(3500); // let hero animations land
  await page.screenshot({ path: path.join(OUT, `${name}.png`) });
  console.log(`${name.padEnd(16)} ${(await page.title().catch(() => "?")).slice(0, 50)}`);
  await ctx.close();
}

await browser.close();
