/**
 * export_chart31.mjs  –  Presentation-quality export
 *
 * Captures chart 31 ("Chromatic Personalities") from the running viz server as:
 *   1. High-res PNG  (2× retina, full page incl. glossary)
 *   2. Vector PDF     (print-ready, dark background, incl. glossary)
 *   3. Self-contained SVG  (piano + radars + legend + glossary table, no clipping)
 *
 * Prerequisites:
 *   - viz server running at http://localhost:8080
 *   - `npm install` in this directory (puppeteer)
 *
 * Usage:
 *   node export_chart31.mjs
 */

import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.resolve(__dirname, "../imgs");
const URL = "http://localhost:8080/31_key_differences.html";

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

  // ── Hide ONLY nav / tooltip — glossary & legend stay visible ────────────────
  await page.evaluate(() => {
    document.querySelectorAll("a.back, .tooltip").forEach((el) => (el.style.display = "none"));
  });

  // ── 1. PNG (full page including glossary) ──────────────────────────────────
  const pngPath = path.join(OUT_DIR, "31_chromatic_personalities.png");
  await page.screenshot({ path: pngPath, fullPage: true });
  const pngKB = (fs.statSync(pngPath).size / 1024).toFixed(1);
  console.log(`✓ PNG  ${pngKB} KB`);

  // ── 2. PDF (vector, with glossary) ─────────────────────────────────────────
  const pdfPath = path.join(OUT_DIR, "31_chromatic_personalities.pdf");
  await page.pdf({
    path: pdfPath,
    width: "1100px",
    printBackground: true,
    margin: { top: "10px", bottom: "10px", left: "10px", right: "10px" },
  });
  const pdfKB = (fs.statSync(pdfPath).size / 1024).toFixed(1);
  console.log(`✓ PDF  ${pdfKB} KB`);

  // ── 3. Self-contained SVG with glossary ────────────────────────────────────
  console.log("Building SVG…");
  const svgContent = await page.evaluate(() => {
    /* ── helpers ── */
    const esc = (s) =>
      String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;")
        .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    const cs = (el, prop) => window.getComputedStyle(el).getPropertyValue(prop);

    const PAGE_W  = 1100;
    const BG      = "#0d1117";
    const ACCENT  = "#58a6ff";
    const TXT     = "#c9d1d9";
    const SUB     = "#8b949e";
    const DIM     = "#484f58";
    const BORDER  = "#30363d";

    function wrapText(text, maxChars) {
      const words = text.split(/\s+/);
      const lines = []; let cur = "";
      words.forEach((w) => {
        if (cur && (cur + " " + w).length > maxChars) { lines.push(cur); cur = w; }
        else cur = cur ? cur + " " + w : w;
      });
      if (cur) lines.push(cur);
      return lines;
    }

    /* Track bottom-most Y of the radar section */
    let radarBottom = 0;

    /* ── Title ── */
    const h1 = document.querySelector("h1");
    const h1B = h1?.getBoundingClientRect();

    /* ── Subtitle ── */
    const pSub = document.querySelector("p.sub");
    const pSubB = pSub?.getBoundingClientRect();

    /* ── Piano keys ── */
    const whiteKeys = [], blackKeys = [];
    document.querySelectorAll(".key-white, .key-black").forEach((el) => {
      const r = el.getBoundingClientRect();
      const s = window.getComputedStyle(el);
      const note = el.querySelector(".note");
      const freq = el.querySelector(".freq");
      const isB = el.classList.contains("key-black");
      const d = {
        x: r.left, y: r.top, w: r.width, h: r.height,
        bg: s.backgroundColor,
        border: s.borderTopColor || s.borderColor,
        rx: parseFloat(s.borderBottomLeftRadius) || 4,
        noteText: note?.textContent || "",
        noteColor: note ? cs(note, "color") : TXT,
        noteWeight: note ? cs(note, "font-weight") : "700",
        freqText: freq?.textContent || "",
      };
      (isB ? blackKeys : whiteKeys).push(d);
      radarBottom = Math.max(radarBottom, r.bottom);
    });

    /* ── Group headers ── */
    const gHeaders = [];
    document.querySelectorAll(".group-hdr").forEach((el) => {
      const r = el.getBoundingClientRect();
      const dot = el.querySelector(".gdot");
      const name = el.querySelector(".gname");
      const dim = el.querySelector(".gdim");
      gHeaders.push({
        y: r.top + r.height * 0.65,
        dotCx: r.left + 8, dotCy: r.top + r.height / 2, dotR: 5,
        dotColor: dot ? cs(dot, "background-color") : DIM,
        nameText: name?.textContent || "",
        nameColor: name ? cs(name, "color") : TXT,
        nameX: r.left + 18,
        dimText: dim?.textContent || "",
        dimX: name ? r.left + 18 + name.textContent.length * 8.5 + 4 : r.left + 80,
      });
      radarBottom = Math.max(radarBottom, r.bottom);
    });

    /* ── Radar cards ── */
    const cards = [];
    document.querySelectorAll(".cell").forEach((cell) => {
      const r = cell.getBoundingClientRect();
      const s = window.getComputedStyle(cell);
      const h3 = cell.querySelector("h3");
      const persona = cell.querySelector(".persona");
      const metaEl = cell.children[2];

      // SVG — clone and selectively inline only paint/text styles
      const svgEl = cell.querySelector("svg");
      let cleanInner = "", svgW = 0, svgH = 0, svgOX = 0, svgOY = 0;
      if (svgEl) {
        const sb = svgEl.getBoundingClientRect();
        svgOX = sb.left; svgOY = sb.top; svgW = sb.width; svgH = sb.height;

        const clone = svgEl.cloneNode(true);
        const origEls = Array.from(svgEl.querySelectorAll("*"));
        const cloneEls = Array.from(clone.querySelectorAll("*"));
        origEls.forEach((orig, i) => {
          const c = cloneEls[i];
          const tag = orig.tagName.toLowerCase();
          const ecs = window.getComputedStyle(orig);
          c.removeAttribute("style");

          const keep = [];
          if (tag === "polygon" || tag === "circle" || tag === "line") {
            const fill = ecs.fill, stroke = ecs.stroke;
            if (fill && fill !== "rgb(0, 0, 0)") keep.push(`fill:${fill}`);
            if (ecs.fillOpacity !== "1") keep.push(`fill-opacity:${ecs.fillOpacity}`);
            if (stroke && stroke !== "none") keep.push(`stroke:${stroke}`);
            if (ecs.strokeWidth !== "1px") keep.push(`stroke-width:${ecs.strokeWidth}`);
            if (ecs.strokeDasharray && ecs.strokeDasharray !== "none") keep.push(`stroke-dasharray:${ecs.strokeDasharray}`);
            if (ecs.strokeOpacity !== "1") keep.push(`stroke-opacity:${ecs.strokeOpacity}`);
            if (ecs.opacity !== "1") keep.push(`opacity:${ecs.opacity}`);
          } else if (tag === "text") {
            keep.push(`fill:${ecs.fill}`);
            keep.push(`font-size:${ecs.fontSize}`);
            if (parseInt(ecs.fontWeight) >= 600) keep.push(`font-weight:bold`);
          }
          if (keep.length) c.setAttribute("style", keep.join(";"));
        });

        const raw = new XMLSerializer().serializeToString(clone);
        cleanInner = raw.replace(/<svg[^>]*>/, "").replace(/<\/svg>\s*$/, "");
      }

      // Song + sig-tags
      const songTitle  = cell.querySelector(".top-song .ts-title")?.textContent || "";
      const songArtist = cell.querySelector(".top-song .ts-artist")?.textContent || "";
      const tags = [];
      cell.querySelectorAll(".sig-tag").forEach((t) => {
        tags.push({
          text: t.textContent,
          bg: cs(t, "background-color"),
          color: cs(t, "color"),
        });
      });

      cards.push({
        x: r.left, y: r.top, w: r.width, h: r.height,
        bg: s.backgroundColor,
        border: s.borderTopColor || s.borderColor,
        rx: parseFloat(s.borderRadius) || 8,
        keyName: h3?.textContent || "",
        keyColor: h3 ? cs(h3, "color") : TXT,
        persona: persona?.textContent || "",
        personaColor: persona ? cs(persona, "color") : SUB,
        meta: metaEl?.textContent?.trim() || "",
        cleanInner, svgW, svgH, svgOX, svgOY,
        songTitle, songArtist, tags,
      });
      radarBottom = Math.max(radarBottom, r.bottom);
    });

    /* ── Glossary table data (from live DOM) ── */
    const glossaryEl = document.querySelector("#glossary");
    const glossRows = [];
    glossaryEl?.querySelectorAll("tr").forEach((tr) => {
      const cells = Array.from(tr.querySelectorAll("th, td"));
      glossRows.push(
        cells.map((c) => ({
          text: c.textContent.trim(),
          color: cs(c, "color"),
          bold: parseInt(cs(c, "font-weight")) >= 600,
          isHeader: c.tagName === "TH",
        }))
      );
    });

    /* ── Layout constants for legend + glossary ── */
    const LEGEND_Y   = radarBottom + 18;
    const LEGEND_H   = 14;
    const GLOSS_TOP  = LEGEND_Y + LEGEND_H + 28;
    const GLOSS_LX   = 60;   // left margin
    const COL1_W     = 165;   // Label
    const COL2_W     = 145;   // Feature
    const COL3_W     = PAGE_W - GLOSS_LX - COL1_W - COL2_W - 60; // Description
    const ROW_H      = 26;
    const GLOSS_HDR  = 58;    // heading + explainer lines

    // Pre-compute wrapped rows + total glossary height
    let glossH = GLOSS_HDR;
    const glossLayout = [];
    glossRows.forEach((row) => {
      const desc = row.length >= 3 ? row[2].text : "";
      const lines = row[0]?.isHeader ? [desc] : wrapText(desc, 72);
      const rowH = Math.max(ROW_H, lines.length * 16 + 10);
      glossLayout.push({ row, lines, rowH, yOff: glossH });
      glossH += rowH;
    });
    glossH += 20; // bottom padding

    const TOTAL_H = GLOSS_TOP + glossH + 30;

    /* ════════════════════ ASSEMBLE SVG ════════════════════ */
    let svg = `<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="${PAGE_W}" height="${TOTAL_H}"
     viewBox="0 0 ${PAGE_W} ${TOTAL_H}">
<defs>
  <style>
    text { font-family: "Helvetica Neue", Arial, sans-serif; }
    .sub   { fill: ${SUB}; font-size: 12px; }
    .kn    { font-size: 12px; font-weight: bold; }
    .pers  { font-size: 9px; }
    .meta  { fill: ${DIM}; font-size: 8px; }
    .stit  { fill: ${SUB}; font-size: 7.5px; }
    .sart  { fill: ${DIM}; font-size: 7px; }
    .tag   { font-size: 7px; }
    .gn    { font-size: 13px; font-weight: bold; }
    .gd    { fill: ${SUB}; font-size: 11px; }
    .leg   { fill: ${SUB}; font-size: 9.5px; }
    .gh    { fill: ${ACCENT}; font-size: 17px; font-weight: bold; }
    .gexp  { fill: ${SUB}; font-size: 10.5px; }
    .gtxt  { font-size: 11px; }
    .gth   { font-size: 11px; font-weight: bold; fill: ${SUB}; }
  </style>
</defs>

<!-- Background -->
<rect width="100%" height="100%" fill="${BG}"/>

`;

    /* Title */
    if (h1B) {
      svg += `<text x="${PAGE_W / 2}" y="${h1B.top + h1B.height * 0.72}" fill="${ACCENT}" font-size="24" font-weight="bold" text-anchor="middle">${esc(h1.textContent)}</text>\n`;
    }

    /* Subtitle (word-wrapped) */
    if (pSubB && pSub) {
      const lines = wrapText(pSub.textContent, 100);
      lines.forEach((ln, i) => {
        svg += `<text class="sub" x="${PAGE_W / 2}" y="${pSubB.top + 14 + i * 15}" text-anchor="middle">${esc(ln)}</text>\n`;
      });
    }

    /* Piano keyboard */
    svg += `\n<!-- Piano Keyboard -->\n`;
    const drawKey = (k, isBlk) => {
      svg += `<rect x="${k.x}" y="${k.y}" width="${k.w}" height="${k.h}" rx="${k.rx}" fill="${k.bg}" stroke="${k.border}" stroke-width="1"/>\n`;
      if (k.noteText) {
        const ny = isBlk ? k.y + k.h - 14 : k.y + k.h - 18;
        svg += `<text x="${k.x + k.w / 2}" y="${ny}" fill="${k.noteColor}" font-size="${isBlk ? 9 : 11}" font-weight="${k.noteWeight}" text-anchor="middle">${esc(k.noteText)}</text>\n`;
      }
      if (k.freqText) {
        const fy = isBlk ? k.y + k.h - 4 : k.y + k.h - 6;
        svg += `<text x="${k.x + k.w / 2}" y="${fy}" fill="${SUB}" font-size="${isBlk ? 6 : 7}" text-anchor="middle">${esc(k.freqText)}</text>\n`;
      }
    };
    whiteKeys.forEach((k) => drawKey(k, false));
    blackKeys.forEach((k) => drawKey(k, true));

    /* Group headers */
    svg += `\n<!-- Personality Groups -->\n`;
    gHeaders.forEach((g) => {
      svg += `<circle cx="${g.dotCx}" cy="${g.dotCy}" r="${g.dotR}" fill="${g.dotColor}"/>\n`;
      svg += `<text class="gn" x="${g.nameX}" y="${g.y}" fill="${g.nameColor}">${esc(g.nameText)}</text>\n`;
      svg += `<text class="gd" x="${g.dimX}" y="${g.y}">${esc(g.dimText)}</text>\n`;
    });

    /* Radar cards */
    svg += `\n<!-- Radar Cards -->\n`;
    cards.forEach((c) => {
      svg += `<g>\n`;
      svg += `  <rect x="${c.x}" y="${c.y}" width="${c.w}" height="${c.h}" rx="${c.rx}" fill="${c.bg}" stroke="${c.border}" stroke-width="1"/>\n`;
      if (c.keyName)  svg += `  <text class="kn" x="${c.x + c.w / 2}" y="${c.y + 16}" fill="${c.keyColor}" text-anchor="middle">${esc(c.keyName)}</text>\n`;
      if (c.persona)  svg += `  <text class="pers" x="${c.x + c.w / 2}" y="${c.y + 28}" fill="${c.personaColor}" text-anchor="middle">${esc(c.persona)}</text>\n`;
      if (c.meta)     svg += `  <text class="meta" x="${c.x + c.w / 2}" y="${c.y + 38}" text-anchor="middle">${esc(c.meta)}</text>\n`;

      // Radar SVG (overflow visible so labels aren't clipped)
      if (c.cleanInner && c.svgW) {
        svg += `  <svg x="${c.svgOX}" y="${c.svgOY}" width="${c.svgW}" height="${c.svgH}" viewBox="0 0 ${c.svgW} ${c.svgH}" overflow="visible">\n`;
        svg += c.cleanInner;
        svg += `  </svg>\n`;
      }

      // Song
      if (c.songTitle) {
        const sy = c.y + c.h - 22;
        svg += `  <text class="stit" x="${c.x + c.w / 2}" y="${sy}" text-anchor="middle">${esc(c.songTitle)}</text>\n`;
        if (c.songArtist) svg += `  <text class="sart" x="${c.x + c.w / 2}" y="${sy + 10}" text-anchor="middle">${esc(c.songArtist)}</text>\n`;
      }

      // Sig tags
      if (c.tags.length) {
        let tx = c.x + 4; const ty = c.y + c.h - 4;
        c.tags.forEach((t) => {
          const tw = t.text.length * 5.5 + 8;
          svg += `  <rect x="${tx}" y="${ty - 10}" width="${tw}" height="13" rx="3" fill="${t.bg}"/>\n`;
          svg += `  <text class="tag" x="${tx + tw / 2}" y="${ty}" fill="${t.color}" text-anchor="middle">${esc(t.text)}</text>\n`;
          tx += tw + 3;
        });
      }
      svg += `</g>\n`;
    });

    /* ── Legend row ── */
    svg += `\n<!-- Legend -->\n`;
    const legItems = [
      { fill: SUB, op: .3, stroke: null, label: "Dashed polygon = median" },
      { fill: ACCENT, op: 1,  stroke: null, label: "Filled dot = above median (z > 1)" },
      { fill: "none", op: 1,  stroke: ACCENT, label: "Ring dot = below median (z < −1)" },
      { fill: BORDER, op: 1,  stroke: null, label: "Dim dot = within normal range" },
    ];
    let lx = 75;
    legItems.forEach(({ fill, op, stroke, label }) => {
      const attrs = stroke
        ? `fill="none" stroke="${stroke}" stroke-width="1.5"`
        : `fill="${fill}" opacity="${op}"`;
      svg += `<circle cx="${lx}" cy="${LEGEND_Y}" r="4.5" ${attrs}/>\n`;
      svg += `<text class="leg" x="${lx + 10}" y="${LEGEND_Y + 3.5}">${esc(label)}</text>\n`;
      lx += label.length * 6.2 + 38;
    });

    /* ── Glossary table ── */
    svg += `\n<!-- Personality Glossary -->\n`;
    // Divider
    svg += `<line x1="${GLOSS_LX}" y1="${GLOSS_TOP - 12}" x2="${PAGE_W - GLOSS_LX}" y2="${GLOSS_TOP - 12}" stroke="#21262d" stroke-width="1"/>\n`;
    // Heading
    svg += `<text class="gh" x="${GLOSS_LX}" y="${GLOSS_TOP + 16}">Personality Label Glossary</text>\n`;
    // Explanation
    const expl = "Each key receives a personality based on the audio feature with the highest z-score above the overall median (z > 1). Keys with no significant deviation are Uncategorized.";
    wrapText(expl, 120).forEach((ln, i) => {
      svg += `<text class="gexp" x="${GLOSS_LX}" y="${GLOSS_TOP + 34 + i * 14}">${esc(ln)}</text>\n`;
    });

    // Table
    const tblTop = GLOSS_TOP + GLOSS_HDR;
    const colX = [GLOSS_LX, GLOSS_LX + COL1_W, GLOSS_LX + COL1_W + COL2_W];

    glossLayout.forEach(({ row, lines, rowH, yOff }) => {
      const rowY = tblTop + yOff - GLOSS_HDR;

      if (row[0]?.isHeader) {
        // Header row bottom border
        svg += `<line x1="${GLOSS_LX}" y1="${rowY + rowH}" x2="${PAGE_W - GLOSS_LX}" y2="${rowY + rowH}" stroke="${BORDER}" stroke-width="1"/>\n`;
        row.forEach((c, ci) => {
          svg += `<text class="gth" x="${colX[ci]}" y="${rowY + 17}">${esc(c.text)}</text>\n`;
        });
      } else {
        // Data row separator
        svg += `<line x1="${GLOSS_LX}" y1="${rowY}" x2="${PAGE_W - GLOSS_LX}" y2="${rowY}" stroke="#21262d" stroke-width="0.5"/>\n`;
        row.forEach((c, ci) => {
          const fw = c.bold ? ' font-weight="bold"' : "";
          if (ci < 2) {
            svg += `<text class="gtxt" x="${colX[ci]}" y="${rowY + 18}" fill="${c.color}"${fw}>${esc(c.text)}</text>\n`;
          } else {
            // Description — word wrapped
            lines.forEach((ln, li) => {
              svg += `<text class="gtxt" x="${colX[ci]}" y="${rowY + 18 + li * 16}" fill="${c.color}">${esc(ln)}</text>\n`;
            });
          }
        });
      }
    });

    svg += `\n</svg>`;
    return svg;
  });

  const svgPath = path.join(OUT_DIR, "31_chromatic_personalities.svg");
  fs.writeFileSync(svgPath, svgContent, "utf-8");
  const svgKB = (fs.statSync(svgPath).size / 1024).toFixed(1);
  console.log(`✓ SVG  ${svgKB} KB`);

  await browser.close();
  console.log(`\nDone → ${OUT_DIR}\n`);
}

main().catch((err) => {
  console.error("Export failed:", err);
  process.exit(1);
});
