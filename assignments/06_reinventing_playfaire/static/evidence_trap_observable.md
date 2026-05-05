# The Evidence Trap — Observable Notebook

## Setup

1. Go to https://observablehq.com/new
2. Upload `evidence_trap_data.json` as a file attachment (paperclip icon, top-right)
3. Create one **JavaScript** cell, paste the code below, run it

---

## The Cell

```javascript
{
  const BUCKETS = 60;
  const data = await FileAttachment("evidence_trap_data.json").json();

  // ── helpers ──────────────────────────────────────────────────────────────
  const buildAvgEv = cases => Array.from({length: BUCKETS}, (_, bi) => {
    const v = cases.map(c => c.evidencePct[bi] || 0);
    return v.reduce((a, b) => a + b, 0) / v.length;
  });
  const evColor = frac => {
    if (frac <= 0.015) return 'transparent';
    return `rgba(233,117,0,${Math.pow(Math.min(frac / 0.40, 1), 0.5).toFixed(3)})`;
  };

  // ── root ─────────────────────────────────────────────────────────────────
  const el = document.createElement('div');

  // ── styles ───────────────────────────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    .et-root { background:#0d1117; color:#e6edf3;
      font-family:system-ui,-apple-system,'Segoe UI',sans-serif; font-size:13px; }
    .et-header {
      background:
        radial-gradient(circle at 14% 0%,rgba(233,117,0,.13),transparent 28%),
        radial-gradient(circle at 86% 6%,rgba(51,102,204,.08),transparent 24%),
        #0d1117;
      padding:60px 52px 44px; max-width:1420px; margin:0 auto;
    }
    .et-ph-label { font-size:11px; font-weight:700; text-transform:uppercase;
      letter-spacing:.14em; color:rgba(233,117,0,.6); margin-bottom:14px; }
    .et-ph-title { font-size:clamp(34px,4.5vw,56px); font-weight:800; line-height:1.05;
      letter-spacing:-.04em; margin-bottom:8px; }
    .et-ph-title em { color:#E97500; font-style:normal; }
    .et-ph-sub { font-size:16px; color:#8b949e; margin-bottom:22px; }
    .et-ph-cols { display:grid; grid-template-columns:1fr 1fr; gap:32px;
      max-width:1040px; margin-top:4px; }
    .et-ph-block { font-size:13.5px; color:rgba(200,209,219,.72); line-height:1.85;
      border-left:2px solid rgba(233,117,0,.28); padding-left:15px; }
    .et-ph-blkhead { font-size:10px; font-weight:700; text-transform:uppercase;
      letter-spacing:.1em; color:rgba(233,117,0,.5); margin-bottom:6px; }
    .et-ph-block strong { color:rgba(230,218,200,.9); font-weight:600; }
    .et-divider { width:100px; height:2px; border-radius:999px;
      background:linear-gradient(90deg,#E97500,transparent); margin:30px 0 0; }
    .et-groups { max-width:1420px; margin:0 auto; padding:0 52px 72px; }
    .et-block { border-top:1px solid rgba(48,54,61,.4); }
    .et-toggle { display:flex; align-items:center; gap:12px; padding:11px 0;
      cursor:pointer; user-select:none; border-radius:4px; transition:background .12s; }
    .et-toggle:hover { background:rgba(255,255,255,.025); }
    .et-dot { width:9px; height:9px; border-radius:50%; flex-shrink:0; }
    .et-icon { font-size:13px; width:18px; flex-shrink:0; text-align:center; }
    .et-name { font-size:11.5px; font-weight:700; text-transform:uppercase;
      letter-spacing:.08em; width:80px; flex-shrink:0; }
    .et-nc { font-size:10.5px; color:#8b949e; width:52px; flex-shrink:0; }
    .et-dashnum { font-size:10px; color:rgba(139,148,158,.45); width:28px; flex-shrink:0; }
    .et-chev { font-size:14px; color:#8b949e; margin-left:auto; padding-right:4px;
      transition:transform .2s; }
    .et-lbl-col { width:168px; flex-shrink:0; text-align:right; padding-right:10px; }
    .et-avg-row { display:flex; align-items:center; height:18px; margin-bottom:4px; }
    .et-avg-lbl { font-size:8px; color:rgba(139,148,158,.35); font-style:italic; }
    .et-avg-bar, .et-fp-bar { flex:1; display:flex; height:100%; }
    .et-avg-cell, .et-fp-cell { flex:1; height:100%; }
    .et-detail { display:none; padding-bottom:12px; }
    .et-block.open .et-detail { display:block; }
    .et-fp-row { display:flex; align-items:center; height:11px; margin-bottom:2px; }
    .et-fp-lbl { font-size:7.5px; color:#8b949e; white-space:nowrap;
      overflow:hidden; text-overflow:ellipsis; cursor:default; line-height:1; }
    .et-fp-cell.ended {
      background:rgba(13,17,23,.4)!important;
      background-image:repeating-linear-gradient(
        45deg,rgba(255,255,255,.035) 0,rgba(255,255,255,.035) 1px,transparent 0,transparent 50%
      )!important;
      background-size:4px 4px!important;
    }
    .et-desc { font-size:11px; color:rgba(200,209,219,.45); font-style:italic;
      line-height:1.6; padding:10px 0 4px 168px; max-width:860px;
      border-top:1px solid rgba(48,54,61,.2); margin-top:8px; }
    .et-recur-head { font-size:9px; font-weight:700; text-transform:uppercase;
      letter-spacing:.1em; color:rgba(139,148,158,.35); margin-bottom:8px;
      padding:12px 0 0 168px; border-top:1px solid rgba(48,54,61,.25); }
    .et-recur-item { font-size:11px; color:rgba(200,209,219,.45); line-height:1.7;
      padding-left:178px; border-left:2px solid rgba(48,54,61,.5);
      margin-bottom:7px; max-width:680px; }
    .et-recur-item b { color:rgba(200,209,219,.65); font-weight:600; }
    .et-footer { max-width:1420px; margin:0 auto; padding:24px 52px 40px;
      border-top:1px solid #30363d; }
    .et-footer-label { font-size:11px; color:rgba(139,148,158,.28); }
    .et-tip { position:fixed; background:rgba(13,17,23,.97);
      border:1px solid rgba(48,54,61,.8); border-radius:10px;
      padding:10px 14px; font-size:12px; line-height:1.7; color:#e6edf3;
      max-width:300px; pointer-events:none; display:none; z-index:999;
      box-shadow:0 8px 32px rgba(0,0,0,.55); }
  `;
  el.appendChild(style);
  el.className = 'et-root';

  // ── header ───────────────────────────────────────────────────────────────
  const hdr = document.createElement('div');
  hdr.className = 'et-header';
  hdr.innerHTML = `
    <div class="et-ph-label">53 Cases · 2004 to 2025</div>
    <div class="et-ph-title">The <em>Evidence</em> Trap</div>
    <div class="et-ph-sub">Why fact-based conflicts never settle</div>
    <div class="et-ph-cols">
      <div class="et-ph-block">
        <div class="et-ph-blkhead">The pattern</div>
        In political cases, the committee gathers evidence, rules, and moves on.
        The evidence phase clears within the first third of the timeline.
        In science and geopolitics, the evidence phase never fully releases.
        The argument loops back, demands more proof, and the case starves
        for a decision that facts alone cannot deliver.
      </div>
      <div class="et-ph-block">
        <div class="et-ph-blkhead">What Wikipedia's last resort reveals</div>
        The Arbitration Committee is Wikipedia's court of <strong>last resort</strong>.
        Cases only reach it after every lower forum has failed.
        When those cases cluster around disputed <strong>facts</strong> rather than
        disputed <strong>conduct</strong>, they stay open longer because the committee
        cannot rule on what reality is. It can only manage behavior around
        the disagreement. The evidence trap is not a process failure.
        It is a signal that some conflicts are structurally beyond arbitration's reach.
      </div>
    </div>
    <div class="et-divider"></div>
  `;
  el.appendChild(hdr);

  // ── tooltip ──────────────────────────────────────────────────────────────
  const tip = document.createElement('div');
  tip.className = 'et-tip';
  el.appendChild(tip);
  const showTip = (markup, e) => {
    tip.innerHTML = markup; tip.style.display = 'block';
    const x = e.clientX+14, y = e.clientY+14;
    tip.style.left = (x + tip.offsetWidth > window.innerWidth ? x - tip.offsetWidth - 28 : x) + 'px';
    tip.style.top  = (y + tip.offsetHeight > window.innerHeight ? y - tip.offsetHeight - 28 : y) + 'px';
  };
  const hideTip = () => { tip.style.display = 'none'; };

  // ── groups ───────────────────────────────────────────────────────────────
  const root = document.createElement('div');
  root.className = 'et-groups';
  el.appendChild(root);

  for (const grp of data.groups) {
    const avgEv = buildAvgEv(grp.cases);
    const block = document.createElement('div');
    block.className = 'et-block';

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

    const detail = document.createElement('div');
    detail.className = 'et-detail';

    for (const c of grp.cases) {
      const row = document.createElement('div');
      row.className = 'et-fp-row';
      row.innerHTML = `<div class="et-lbl-col et-fp-lbl" title="${c.short}">${c.short}</div>`;
      const bar = document.createElement('div');
      bar.className = 'et-fp-bar';
      for (let bi = 0; bi < BUCKETS; bi++) {
        const ended = bi > c.lastActive;
        const cell = document.createElement('div');
        cell.className = 'et-fp-cell' + (ended ? ' ended' : '');
        if (!ended) cell.style.background = c.dominantPhase[bi] === 'evidence' ? '#E97500' : 'transparent';
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

    if (grp.recurNotes && grp.recurNotes.length) {
      const rHead = document.createElement('div');
      rHead.className = 'et-recur-head';
      rHead.textContent = 'Why these cases came back';
      detail.appendChild(rHead);
      grp.recurNotes.forEach(({title, note}) => {
        const item = document.createElement('div');
        item.className = 'et-recur-item';
        item.innerHTML = `<b>${title}:</b> ${note}`;
        detail.appendChild(item);
      });
    }

    const desc = document.createElement('div');
    desc.className = 'et-desc';
    desc.textContent = grp.desc;
    detail.appendChild(desc);

    block.appendChild(detail);

    toggle.addEventListener('click', () => {
      const open = block.classList.toggle('open');
      toggle.querySelector('.et-chev').style.transform = open ? 'rotate(90deg)' : '';
    });

    root.appendChild(block);
  }

  // ── footer ───────────────────────────────────────────────────────────────
  const footer = document.createElement('div');
  footer.className = 'et-footer';
  footer.innerHTML = `<span class="et-footer-label">SARC 5400 · UVA Data Viz · Final Project</span>`;
  el.appendChild(footer);

  return el;
}
```

---

**To share:** Publish the notebook, then use **Share → Embed** for an iframe, or **Download code** to export as a standalone HTML file.
