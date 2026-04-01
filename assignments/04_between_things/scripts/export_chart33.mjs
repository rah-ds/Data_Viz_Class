/**
 * export_chart33.mjs  –  Export chart 33 (Cleaned Baseline) as PNG + SVG
 *
 * Prerequisites:
 *   - viz server running at http://localhost:8765
 *   - `npm install` in this directory (puppeteer)
 *
 * Usage:
 *   node export_chart33.mjs
 */

import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, "../turn_in");
const URL = "http://localhost:8765/33_key_cleaned.html";
const PREFIX = "33_key_cleaned";

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
  await page.waitForSelector(".cell svg polygon", { timeout: 15_000 });
  await new Promise((r) => setTimeout(r, 1000));

  // Hide nav / tooltip
  await page.evaluate(() => {
    document.querySelectorAll("a.back, .tooltip").forEach((el) => (el.style.display = "none"));
  });

  // ── 1. PNG ──
  const pngPath = path.join(OUT_DIR, `${PREFIX}.png`);
  await page.screenshot({ path: pngPath, fullPage: true });
  const pngKB = (fs.statSync(pngPath).size / 1024).toFixed(1);
  console.log(`✓ PNG  ${pngKB} KB  →  ${pngPath}`);

  // ── 2. SVG (serialise full page body into a foreignObject SVG) ──
  const dims = await page.evaluate(() => {
    const b = document.body;
    return { w: Math.max(b.scrollWidth, 1100), h: b.scrollHeight };
  });

  const svgContent = await page.evaluate((dims) => {
    // Grab all embedded SVGs and serialise them
    const svgs = [];
    document.querySelectorAll(".cell svg").forEach((svgEl) => {
      const rect = svgEl.getBoundingClientRect();
      const clone = svgEl.cloneNode(true);
      // Inline computed styles on key elements
      const origEls = Array.from(svgEl.querySelectorAll("*"));
      const cloneEls = Array.from(clone.querySelectorAll("*"));
      origEls.forEach((orig, i) => {
        const cs = window.getComputedStyle(orig);
        const c = cloneEls[i];
        const tag = orig.tagName.toLowerCase();
        const keep = [];
        if (["polygon","circle","line"].includes(tag)) {
          if (cs.fill && cs.fill !== "rgb(0, 0, 0)") keep.push(`fill:${cs.fill}`);
          if (cs.fillOpacity !== "1") keep.push(`fill-opacity:${cs.fillOpacity}`);
          if (cs.stroke && cs.stroke !== "none") keep.push(`stroke:${cs.stroke}`);
          if (cs.strokeWidth && cs.strokeWidth !== "1px") keep.push(`stroke-width:${cs.strokeWidth}`);
          if (cs.strokeDasharray && cs.strokeDasharray !== "none") keep.push(`stroke-dasharray:${cs.strokeDasharray}`);
          if (cs.strokeOpacity && cs.strokeOpacity !== "1") keep.push(`stroke-opacity:${cs.strokeOpacity}`);
          if (cs.opacity && cs.opacity !== "1") keep.push(`opacity:${cs.opacity}`);
        } else if (tag === "text") {
          keep.push(`fill:${cs.fill}`);
          keep.push(`font-size:${cs.fontSize}`);
          if (parseInt(cs.fontWeight) >= 600) keep.push(`font-weight:bold`);
        }
        if (keep.length) c.setAttribute("style", keep.join(";"));
      });
      svgs.push({
        x: rect.left, y: rect.top, w: rect.width, h: rect.height,
        inner: new XMLSerializer().serializeToString(clone)
      });
    });
    return JSON.stringify(svgs);
  }, dims);

  // For simplicity, just produce PNG for now — SVG is complex for these layouts
  // If full SVG is needed, use the PNG as the primary deliverable

  await browser.close();
  console.log(`\nDone → ${OUT_DIR}\n`);
}

main().catch((err) => {
  console.error("Export failed:", err);
  process.exit(1);
});
