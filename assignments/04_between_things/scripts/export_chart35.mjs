/**
 * export_chart35.mjs  –  Export chart 35 (Lollipop) as PNG
 *
 * Prerequisites:
 *   - viz server running at http://localhost:8765
 *   - `npm install` in this directory (puppeteer)
 *
 * Usage:
 *   node export_chart35.mjs
 */

import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, "../turn_in");
const URL = "http://localhost:8765/35_key_lollipop.html";
const PREFIX = "35_key_lollipop";

fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  console.log("\nLaunching browser…");
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 900, deviceScaleFactor: 2 });

  page.on("console", () => {});
  page.on("pageerror", (e) => console.warn("  page error:", e.message));

  console.log(`Loading ${URL}…`);
  await page.goto(URL, { waitUntil: "networkidle0", timeout: 30_000 });
  await page.waitForSelector("#chart-container svg circle", { timeout: 15_000 });
  await new Promise((r) => setTimeout(r, 1000));

  // Hide nav / tooltip
  await page.evaluate(() => {
    document.querySelectorAll("a.back, .tooltip").forEach((el) => (el.style.display = "none"));
  });

  // ── PNG ──
  const pngPath = path.join(OUT_DIR, `${PREFIX}.png`);
  await page.screenshot({ path: pngPath, fullPage: true });
  const pngKB = (fs.statSync(pngPath).size / 1024).toFixed(1);
  console.log(`✓ PNG  ${pngKB} KB  →  ${pngPath}`);

  await browser.close();
  console.log(`\nDone → ${OUT_DIR}\n`);
}

main().catch((err) => {
  console.error("Export failed:", err);
  process.exit(1);
});
