/**
 * export_chart39_svg.mjs  –  Export chart 39 as full-page SVG + PNG
 *
 * Same approach as chart 38 but targets the cleaned version
 * (no song quotes in callout annotations).
 */
import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, "../turn_in/final_turn_in");
const URL = "http://localhost:8080/39_key_annotated_clean.html";
const PREFIX = "39_key_annotated_clean";
fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 900, deviceScaleFactor: 2 });
  await page.goto(URL, { waitUntil: "networkidle0", timeout: 30_000 });
  await page.waitForSelector(".cell svg polygon", { timeout: 15_000 });
  await new Promise((r) => setTimeout(r, 1500));

  // Hide interactive-only elements
  await page.evaluate(() => {
    document.querySelectorAll("a.back, .tooltip").forEach((el) => (el.style.display = "none"));
  });

  // Build SVG wrapping the rendered HTML inside a foreignObject
  const svgString = await page.evaluate(() => {
    const body = document.body;
    const w = body.scrollWidth;
    const h = body.scrollHeight;

    // Gather all stylesheets as inline <style>
    let css = "";
    for (const sheet of document.styleSheets) {
      try {
        for (const rule of sheet.cssRules) css += rule.cssText + "\n";
      } catch (_) {}
    }

    // Remove <script> tags — JS has already executed and rendered the DOM,
    // and raw JS breaks XML parsing (bare < and & chars).
    body.querySelectorAll("script").forEach((s) => s.remove());

    // Serialise body HTML
    const html = body.outerHTML;

    return [
      `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">`,
      `<foreignObject width="100%" height="100%">`,
      `<html xmlns="http://www.w3.org/1999/xhtml">`,
      `<head><style>/*<![CDATA[*/\n${css}\n/*]]>*/</style></head>`,
      html,
      `</html>`,
      `</foreignObject>`,
      `</svg>`,
    ].join("\n");
  });

  const svgPath = path.join(OUT_DIR, `${PREFIX}.svg`);
  fs.writeFileSync(svgPath, svgString, "utf-8");
  console.log(`✓ SVG → ${svgPath} (${(fs.statSync(svgPath).size / 1024).toFixed(1)} KB)`);

  // Also save a PNG for reference
  const pngPath = path.join(OUT_DIR, `${PREFIX}.png`);
  await page.screenshot({ path: pngPath, fullPage: true });
  console.log(`✓ PNG → ${pngPath} (${(fs.statSync(pngPath).size / 1024).toFixed(1)} KB)`);

  await browser.close();
}
main().catch((e) => {
  console.error(e);
  process.exit(1);
});
