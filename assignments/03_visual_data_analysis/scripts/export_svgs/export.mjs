/**
 * export.mjs
 *
 * Uses Puppeteer to:
 *   1. Start a local file server so D3 can fetch the JSON data file
 *      (browsers block fetch() on file:// URLs).
 *   2. Load each target HTML page.
 *   3. Wait for the D3 SVG to finish rendering.
 *   4. Inline all computed styles + the Google Fonts @import so the SVG
 *      is fully self-contained when opened in Inkscape / Illustrator.
 *   5. Write the cleaned SVG to viz/to_refine/.
 *
 * Usage:
 *   node export.mjs
 */

import puppeteer from "puppeteer";
import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// ─── paths ────────────────────────────────────────────────────────────────────

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "../../../.."); // Data_Viz_Class root
const VIZ_RAW = path.join(ROOT, "assignments/03_visual_data_analysis/viz/raw");
const OUT_DIR = path.join(ROOT, "assignments/03_visual_data_analysis/viz/to_refine");

// ─── targets ──────────────────────────────────────────────────────────────────

const TARGETS = [
  {
    page: "index.html",
    svgSelector: "#sankey-container svg",
    waitFor: ".sankey-node rect",
    outFile: "escalation_funnel.svg",
    label: "Escalation Funnel (Sankey)",
  },
  {
    page: "extended.html",
    svgSelector: "#dag-container svg",
    waitFor: ".dag-node circle",
    outFile: "proper_dag.svg",
    label: "Dispute Resolution DAG",
  },
  {
    page: "extended.html",
    svgSelector: "#radial-container svg",
    waitFor: ".radial-spoke",
    outFile: "reoccuring_cases.svg",
    label: "Recurring Case Families (Radial Burst)",
  },
];

// ─── simple static file server ────────────────────────────────────────────────
// Serves the project root so the relative ../../../../data/raw/... fetch works.

function startServer(root, port) {
  const mimeTypes = {
    ".html": "text/html",
    ".js": "application/javascript",
    ".css": "text/css",
    ".json": "application/json",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".txt": "text/plain",
  };

  const server = http.createServer((req, res) => {
    const filePath = path.join(root, decodeURIComponent(req.url.split("?")[0]));
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end(`Not found: ${req.url}`);
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      res.writeHead(200, { "Content-Type": mimeTypes[ext] || "application/octet-stream" });
      res.end(data);
    });
  });

  return new Promise((resolve) => server.listen(port, () => resolve(server)));
}

// ─── SVG post-processing ──────────────────────────────────────────────────────
// Inlines the Google Fonts @import and computed styles into the SVG <defs>
// so it renders correctly when opened outside a browser.

async function extractStyledSVG(page, svgSelector, label) {
  return await page.evaluate(
    async (selector, titleText) => {
      const svgEl = document.querySelector(selector);
      if (!svgEl) throw new Error(`SVG not found: ${selector}`);

      // ── 1. Clone the SVG so we don't mutate the live DOM ──
      const clone = svgEl.cloneNode(true);

      // ── 2. Ensure width/height attributes exist (for Inkscape) ──
      const vb = svgEl.getAttribute("viewBox");
      if (vb && (!clone.getAttribute("width") || !clone.getAttribute("height"))) {
        const parts = vb.split(/[\s,]+/);
        clone.setAttribute("width", parts[2]);
        clone.setAttribute("height", parts[3]);
      }

      // ── 3. Collect all stylesheet text (includes @import for Google Fonts) ──
      let cssText = "";
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            cssText += rule.cssText + "\n";
          }
        } catch (_) {
          // Cross-origin sheets (Google Fonts CDN) — grab the href instead
          if (sheet.href) {
            cssText += `@import url('${sheet.href}');\n`;
          }
        }
      }

      // ── 4. Inline computed styles on every element inside the SVG ──
      //    This makes the SVG self-contained even if the CSS is lost.
      const allEls = Array.from(svgEl.querySelectorAll("*"));
      const cloneEls = Array.from(clone.querySelectorAll("*"));
      const skipProps = new Set(["transition", "animation", "will-change"]);

      allEls.forEach((el, i) => {
        const computed = window.getComputedStyle(el);
        const styles = [];
        for (const prop of computed) {
          if (skipProps.has(prop)) continue;
          const val = computed.getPropertyValue(prop);
          if (val && val !== "initial" && val !== "unset") {
            styles.push(`${prop}:${val}`);
          }
        }
        if (styles.length) {
          cloneEls[i].setAttribute("style", styles.join(";"));
        }
      });

      // ── 5. Add <defs> with a <style> block for fonts ──
      let defs = clone.querySelector("defs");
      if (!defs) {
        defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
        clone.insertBefore(defs, clone.firstChild);
      }
      const styleEl = document.createElementNS("http://www.w3.org/2000/svg", "style");
      styleEl.textContent = cssText;
      defs.insertBefore(styleEl, defs.firstChild);

      // ── 6. Add a <title> element ──
      const existing = clone.querySelector("title");
      if (!existing) {
        const titleEl = document.createElementNS("http://www.w3.org/2000/svg", "title");
        titleEl.textContent = titleText;
        clone.insertBefore(titleEl, clone.firstChild);
      }

      // ── 7. Serialise ──
      const serializer = new XMLSerializer();
      let svgStr = serializer.serializeToString(clone);

      // Ensure XML declaration + proper namespace
      if (!svgStr.startsWith("<?xml")) {
        svgStr =
          '<?xml version="1.0" encoding="utf-8"?>\n' +
          '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" ' +
          '"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n' +
          svgStr;
      }

      return svgStr;
    },
    svgSelector,
    label
  );
}

// ─── main ─────────────────────────────────────────────────────────────────────

async function main() {
  const PORT = 7331;
  console.log(`\nStarting static server on port ${PORT} (serving ${ROOT})…`);
  const server = await startServer(ROOT, PORT);

  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  try {
    for (const target of TARGETS) {
      const url = `http://localhost:${PORT}/assignments/03_visual_data_analysis/viz/raw/${target.page}`;
      console.log(`\n[${target.label}]`);
      console.log(`  Loading ${url}…`);

      const page = await browser.newPage();
      await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });

      // Suppress console noise from the page
      page.on("console", () => {});
      page.on("pageerror", (err) => console.warn("  page error:", err.message));

      await page.goto(url, { waitUntil: "networkidle0", timeout: 30_000 });

      // Wait for D3 to finish rendering the specific SVG elements
      console.log(`  Waiting for selector: ${target.waitFor}…`);
      await page.waitForSelector(target.waitFor, { timeout: 20_000 });

      // Extra settle time for force simulations (beeswarm, radial)
      await new Promise((r) => setTimeout(r, 1200));

      console.log(`  Extracting SVG…`);
      const svgContent = await extractStyledSVG(page, target.svgSelector, target.label);

      const outPath = path.join(OUT_DIR, target.outFile);
      fs.writeFileSync(outPath, svgContent, "utf-8");
      const kb = (fs.statSync(outPath).size / 1024).toFixed(1);
      console.log(`  ✓ Saved ${target.outFile} (${kb} KB)`);

      await page.close();
    }
  } finally {
    await browser.close();
    server.close();
    console.log("\nDone.\n");
  }
}

main().catch((err) => {
  console.error("Export failed:", err);
  process.exit(1);
});
