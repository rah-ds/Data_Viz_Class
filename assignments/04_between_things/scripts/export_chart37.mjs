/**
 * export_chart37.mjs  –  Export chart 37 (Parallel Coordinates) as PNG
 */
import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, "../turn_in");
const URL = "http://localhost:8765/37_key_parallel.html";
const PREFIX = "37_key_parallel";
fs.mkdirSync(OUT_DIR, { recursive: true });

async function main() {
  const browser = await puppeteer.launch({ headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1100, height: 900, deviceScaleFactor: 2 });
  await page.goto(URL, { waitUntil: "networkidle0", timeout: 30_000 });
  await page.waitForSelector(".chart-wrap svg path", { timeout: 15_000 });
  await new Promise(r => setTimeout(r, 1000));
  await page.evaluate(() => document.querySelectorAll("a.back, .tooltip").forEach(el => el.style.display = "none"));
  const pngPath = path.join(OUT_DIR, `${PREFIX}.png`);
  await page.screenshot({ path: pngPath, fullPage: true });
  console.log(`✓ PNG → ${pngPath} (${(fs.statSync(pngPath).size/1024).toFixed(1)} KB)`);
  await browser.close();
}
main().catch(e => { console.error(e); process.exit(1); });
