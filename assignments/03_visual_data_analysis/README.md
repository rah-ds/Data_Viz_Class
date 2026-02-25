# Assignment 3 — Visual Data Analysis

Three D3.js visualizations of the Wikipedia ArbCom case archive (481 cases), each using a different spatial encoding strategy to explore where Wikipedia's dispute resolution system fails.

See [`write_up.md`](writeup/write_up.md) for the full analysis.

---

## Figures

| Figure | Type | File |
|--------|------|------|
| 1 — The Wikipedia Escalation Funnel | Sankey / Alluvial Diagram | `viz/zz_final/escalation_funnel.svg` |
| 2 — The Anatomy of the Dispute Lifecycle | Directed Acyclic Graph (DAG) | `viz/zz_final/proper_dag.svg` |
| 3 — The Disputes That Won't Die | Radial Burst / Polar Spoke Chart | `viz/zz_final/reoccuring_cases.svg` |

---

## How to Reproduce

### 1. Prepare the data

```bash
uv run python assignments/03_visual_data_analysis/scripts/prepare_data.py
```

Reads `data/raw/03_visual_data_analysis/arb_cases.txt`, classifies each case by topic, dispute type, and recurrence, and writes `arb_cases_classified.json` to the same directory.

### 2. Serve the visualizations locally

```bash
uv run python assignments/03_visual_data_analysis/scripts/serve.py
```

Opens the D3 charts at `http://localhost:8000`. The three charts live in:
- `viz/raw/index.html` — Sankey (Figure 1)
- `viz/raw/extended.html` — DAG + Radial Burst (Figures 2 & 3)

### 3. Export SVGs

```bash
cd assignments/03_visual_data_analysis/scripts/export_svgs
npm install
node export.mjs
```

Uses Puppeteer to headlessly render each chart, inline all computed styles, and write self-contained SVGs to `viz/to_refine/`. Final refined versions are in `viz/zz_final/`.

---

## Prompts used to generate the graphics

The D3 charts were built with AI assistance (Claude 4.6). The following prompts produced the core of each chart

**Figure 1 — Sankey**
> Build a D3 v7 Sankey diagram showing Wikipedia dispute flow through six resolution stages: Talk Page → Third Opinion / RfC / DRN → ANI → Mediation → ArbCom → Resolved/Declined. Node width encodes total dispute volume. Flow band thickness encodes volume along each pathway. Color flows from the source node. Read the case data from `arb_cases_classified.json`. Export as a self-contained SVG.

**Figure 2 — DAG**
> Build a D3 v7 directed acyclic graph of the same Wikipedia dispute resolution system. Hand-position nodes into authority-level columns: Informal, Community, Mediation, Admin, Arbitration, Outcome. Node radius encodes throughput. Edge thickness encodes flow volume. Add arrowhead markers on all edges. Draw subtle background column bands using the Gestalt law of common region to group nodes by authority tier. Export as a self-contained SVG.

**Figure 3 — Radial Burst**
> Build a D3 v7 radial spoke chart of recurring ArbCom case families. One spoke per family, grouped into angular sectors by topic category. Spoke length encodes max recurrence depth (1–5). Place a dot at each hearing depth along the spoke. Add concentric reference circles at 1×–5× labeled with multipliers. Rotate spoke labels to follow the spoke angle. Color sectors by category. Read data from `arb_cases_classified.json`. Export as a self-contained SVG.
