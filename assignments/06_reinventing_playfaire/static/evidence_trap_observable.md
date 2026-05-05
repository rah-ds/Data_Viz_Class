# The Evidence Trap — Observable Notebook

## How to set this up on observablehq.com

1. Go to https://observablehq.com/new (create a blank notebook)
2. Upload `evidence_trap_data.json` as a file attachment  
   (click the **paperclip icon** in the top-right, or drag it onto the notebook)
3. Paste each cell below **in order** — each is a separate cell

---

## Cell 1 — Title (Markdown cell)

```markdown
# The Evidence Trap
### Why fact-based conflicts never settle

Wikipedia's Arbitration Committee is its court of last resort. Cases only reach it after every lower forum has failed.
When those cases cluster around disputed **facts** rather than disputed **conduct**, they stay open longer —
because the committee cannot rule on what reality is. It can only manage behavior around the disagreement.

*53 arbitration cases · 2004–2025 · Click any group to expand individual cases*
```

---

## Cell 2 — Styles (JavaScript cell)

```javascript
html`<style>
  :root {
    --bg: #0d1117; --surface: #161b22; --border: rgba(48,54,61,.6);
    --text: #e6edf3; --muted: #8b949e; --accent: #E97500;
  }
  .et-wrap { background: var(--bg); color: var(--text); font-family: -apple-system, 'Segoe UI', sans-serif;
    font-size: 13px; padding: 0 0 60px; }
  .et-groups { max-width: 1100px; margin: 0 auto; padding: 0 24px; }
  .et-block { border-top: 1px solid rgba(48,54,61,.4); }
  .et-toggle { display:flex; align-items:center; gap:10px; padding:10px 0; cursor:pointer; user-select:none;
    border-radius:4px; transition:background .12s; }
  .et-toggle:hover { background: rgba(255,255,255,.025); }
  .et-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
  .et-icon { font-size:13px; width:18px; text-align:center; }
  .et-name { font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.08em;
    width:82px; flex-shrink:0; }
  .et-nc { font-size:10px; color:var(--muted); width:50px; flex-shrink:0; }
  .et-dashnum { font-size:10px; color:rgba(139,148,158,.4); width:28px; flex-shrink:0; }
  .et-chev { font-size:14px; color:var(--muted); margin-left:auto; padding-right:4px;
    transition:transform .2s; }
  .et-block.open .et-chev { transform:rotate(90deg); }
  .et-lbl-col { width:148px; flex-shrink:0; text-align:right; padding-right:10px; }
  .et-avg-row { display:flex; align-items:center; height:16px; margin-bottom:3px; }
  .et-avg-lbl { font-size:7.5px; color:rgba(139,148,158,.32); font-style:italic; }
  .et-avg-bar, .et-fp-bar { flex:1; display:flex; height:100%; }
  .et-avg-cell, .et-fp-cell { flex:1; height:100%; }
  .et-fp-row { display:flex; align-items:center; height:10px; margin-bottom:2px; }
  .et-fp-lbl { font-size:7px; color:var(--muted); white-space:nowrap; overflow:hidden;
    text-overflow:ellipsis; cursor:default; }
  .et-fp-cell.ended {
    background: rgba(13,17,23,.4) !important;
    background-image: repeating-linear-gradient(45deg,rgba(255,255,255,.035) 0,
      rgba(255,255,255,.035) 1px,transparent 0,transparent 50%) !important;
    background-size: 4px 4px !important;
  }
  .et-detail { display:none; padding-bottom:10px; }
  .et-block.open .et-detail { display:block; }
  .et-desc { font-size:11px; color:rgba(200,209,219,.45); font-style:italic; line-height:1.6;
    padding:10px 0 4px 148px; max-width:820px; border-top:1px solid rgba(48,54,61,.2); margin-top:8px; }
  .et-recur-head { font-size:8.5px; font-weight:700; text-transform:uppercase; letter-spacing:.1em;
    color:rgba(139,148,158,.35); margin-bottom:7px; padding-left:148px; }
  .et-recur-item { font-size:10.5px; color:rgba(200,209,219,.45); line-height:1.7; padding-left:158px;
    border-left:2px solid rgba(48,54,61,.5); margin-bottom:6px; max-width:720px; }
  .et-recur-item b { color:rgba(200,209,219,.6); font-weight:600; }
</style>`
```

---

## Cell 3 — Constants (JavaScript cell)

```javascript
BUCKETS = 60
```

---

## Cell 4 — Data (JavaScript cell — requires the file attachment)

```javascript
data = FileAttachment("evidence_trap_data.json").json()
```

---

## Cell 5 — Helpers (JavaScript cell)

```javascript
function buildAvgEv(cases) {
  return Array.from({length: BUCKETS}, (_, bi) => {
    const vals = cases.map(c => c.evidencePct[bi] || 0);
    return vals.reduce((a, b) => a + b, 0) / vals.length;
  });
}

function evColor(frac) {
  if (frac <= 0.015) return 'transparent';
  const t = Math.pow(Math.min(frac / 0.40, 1), 0.5);
  return `rgba(233,117,0,${t.toFixed(3)})`;
}
```

---

## Cell 6 — Main visualization (JavaScript cell)

```javascript
{
  const wrap = html`<div class="et-wrap">
    <div class="et-groups" id="et-root"></div>
  </div>`;
  const root = wrap.querySelector('#et-root');

  const tip = wrap.appendChild(Object.assign(document.createElement('div'), {
    style: 'position:fixed;background:#1c2128;border:1px solid rgba(48,54,61,.6);border-radius:5px;padding:8px 11px;font-size:11px;color:#e6edf3;pointer-events:none;display:none;z-index:999;line-height:1.6;max-width:220px'
  }));
  const showTip = (html_, e) => { tip.innerHTML = html_; tip.style.display='block';
    tip.style.left=(e.clientX+14)+'px'; tip.style.top=(e.clientY+14)+'px'; };
  const hideTip = () => { tip.style.display='none'; };

  for (const grp of data.groups) {
    const avgEv = buildAvgEv(grp.cases);
    const block = document.createElement('div');
    block.className = 'et-block';

    // Toggle header
    const toggle = document.createElement('div');
    toggle.className = 'et-toggle';
    toggle.innerHTML = `
      <div class="et-dot" style="background:${grp.baseColor}"></div>
      <div class="et-icon">${grp.icon}</div>
      <div class="et-name" style="color:${grp.baseColor}">${grp.label}</div>
      <div class="et-nc">${grp.cases.length} cases</div>
      <div class="et-dashnum">(${grp.dashNum})</div>
      <div class="et-chev">›</div>`;
    block.appendChild(toggle);

    // Group avg row — always visible
    const avgRow = document.createElement('div');
    avgRow.className = 'et-avg-row';
    avgRow.innerHTML = `<div class="et-lbl-col et-avg-lbl">group avg</div>`;
    const avgBar = document.createElement('div');
    avgBar.className = 'et-avg-bar';
    for (let bi = 0; bi < BUCKETS; bi++) {
      const cell = document.createElement('div');
      cell.className = 'et-avg-cell';
      cell.style.background = evColor(avgEv[bi]);
      cell.addEventListener('mouseenter', e => showTip(
        `<b style="color:${grp.baseColor}">${grp.label}</b> group avg<br>` +
        `Window ${bi+1}/60 · ${Math.round(bi/(BUCKETS-1)*100)}% through<br>` +
        `Evidence: <b style="color:#E97500">${(avgEv[bi]*100).toFixed(0)}%</b>`, e));
      cell.addEventListener('mouseleave', hideTip);
      avgBar.appendChild(cell);
    }
    avgRow.appendChild(avgBar);
    block.appendChild(avgRow);

    // Detail (individual cases) — hidden until click
    const detail = document.createElement('div');
    detail.className = 'et-detail';

    for (const c of grp.cases) {
      const row = document.createElement('div');
      row.className = 'et-fp-row';
      row.innerHTML = `<div class="et-lbl-col et-fp-lbl" title="${c.short}">${c.short}</div>`;
      const bar = document.createElement('div');
      bar.className = 'et-fp-bar';
      for (let bi = 0; bi < BUCKETS; bi++) {
        const ph = c.dominantPhase[bi];
        const ended = bi > c.lastActive;
        const cell = document.createElement('div');
        cell.className = 'et-fp-cell' + (ended ? ' ended' : '');
        if (!ended) cell.style.background = ph === 'evidence' ? '#E97500' : 'transparent';
        cell.addEventListener('mouseenter', e => showTip(
          `<b>${c.short}</b><br>` +
          `Segment ${bi+1}/60 · ${Math.round(bi/(BUCKETS-1)*100)}% through<br>` +
          `Evidence: <b style="color:#E97500">${(c.evidencePct[bi]*100).toFixed(0)}%</b><br>` +
          `<span style="opacity:.5">${c.totalEditors} editors · ${Math.round(c.durationDays)}d total</span>`, e));
        cell.addEventListener('mouseleave', hideTip);
        bar.appendChild(cell);
      }
      row.appendChild(bar);
      detail.appendChild(row);
    }

    // Recurring case notes
    if (grp.recurNotes && grp.recurNotes.length) {
      const head = Object.assign(document.createElement('div'), {className:'et-recur-head'});
      head.textContent = 'Why these cases came back';
      detail.appendChild(head);
      grp.recurNotes.forEach(({title, note}) => {
        const item = Object.assign(document.createElement('div'), {className:'et-recur-item'});
        item.innerHTML = `<b>${title}:</b> ${note}`;
        detail.appendChild(item);
      });
    }

    const desc = Object.assign(document.createElement('div'), {className:'et-desc'});
    desc.textContent = grp.desc;
    detail.appendChild(desc);

    block.appendChild(detail);

    toggle.addEventListener('click', () => {
      const open = block.classList.toggle('open');
      toggle.querySelector('.et-chev').style.transform = open ? 'rotate(90deg)' : '';
    });

    root.appendChild(block);
  }

  return wrap;
}
```

---

## That's it

You should have 6 cells total. The notebook will be fully interactive — click any group header to expand individual cases.

**Tips:**
- To share: click **Publish** in Observable, or use **Share → Embed** for an iframe
- The tooltip follows your cursor; hover over any cell to see evidence %
- To pre-expand a group on load, add `block.classList.add('open')` after `root.appendChild(block)` for the groups you want open
