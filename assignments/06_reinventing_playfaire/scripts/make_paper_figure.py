"""
Generate a print-ready paper figure: evidence_trap_paper.pdf
Focused 3-case-per-side comparison, large enough to read at 6.5" wide.

Left:  3 Science/Geopolitics cases (persistent orange) + group averages
Right: 3 Politics/Policy cases (orange clears early) + group averages

Designed for: width=\linewidth in A4 paper (≈6.5 inches at 11pt/1.25in margins)
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "processed" / "d3"
OUT_DIR  = Path(__file__).resolve().parents[1] / "static"
BUCKETS  = 60

BG     = "#0d1117"
BORDER = "#30363d"
TEXT   = "#e6edf3"
MUTED  = "#8b949e"
EV_COLOR = "#E97500"
EV_RGB   = (233/255, 117/255, 0/255)


def load_and_compute(slug):
    p = DATA_DIR / f"{slug}.json"
    if not p.exists():
        return None
    with open(p) as f:
        data = json.load(f)
    events = data.get("events", [])
    if len(events) < 2:
        return None
    times = []
    for e in events:
        try:
            times.append(datetime.fromisoformat(e["timestamp"].replace("Z","")).timestamp())
        except Exception:
            pass
    if len(times) < 2:
        return None
    t0, t1 = min(times), max(times)
    dur = t1 - t0
    if dur < 86400:
        return None

    buckets = [{} for _ in range(BUCKETS)]
    for e in events:
        try:
            t = datetime.fromisoformat(e["timestamp"].replace("Z","")).timestamp()
        except Exception:
            continue
        bi = int(max(0, min(0.9999, (t - t0) / dur)) * BUCKETS)
        pt = e.get("page_type") or e.get("type") or "main"
        buckets[bi][pt] = buckets[bi].get(pt, 0) + 1

    ev_frac = []
    for bk in buckets:
        tot = sum(bk.values())
        ev_frac.append(bk.get("evidence", 0) / tot if tot > 0 else 0.0)

    last_active = max((i for i in range(BUCKETS) if buckets[i]), default=-1)
    return ev_frac, last_active


def ev_color(ev, gamma=0.50):
    if ev < 0.005:
        return (0.09, 0.10, 0.13)
    t = min(ev / 0.40, 1.0) ** gamma
    return (EV_RGB[0]*t + 0.09*(1-t),
            EV_RGB[1]*t + 0.10*(1-t),
            EV_RGB[2]*t + 0.13*(1-t))


# ── Select representative cases ──────────────────────────────────────────────
# FACT side: maximum persistent orange examples
FACT_CASES = [
    # (slug, label, color)
    ("climate_change",              "Climate Change  2010",      "#14866D"),
    ("skepticism_and_coordinated_editing", "Skepticism  2022",   "#14866D"),
    ("palestine-israel_articles_4", "Palestine–Israel  2019",    "#FF9900"),
    ("armenia-azerbaijan_3",        "Armenia–Azer.  2023",       "#FF9900"),
]

# CONDUCT side: maximum early-clear examples
CONDUCT_CASES = [
    ("american_politics",                          "American Politics  2014", "#CC3333"),
    ("american_politics_2",                        "American Politics  2015", "#CC3333"),
    ("arbitration_enforcement",                    "Arb. Enforcement  2015",  "#3366CC"),
    ("arbitration_enforcement_sanction_handling",  "Arb. Sanctions  2011",    "#3366CC"),
]

# Group averages for all 6 groups
GROUP_AVGS = [
    ("geopolitics", "Geopolitics avg", "#FF9900",
     ["israeli_apartheid","israel-lebanon","kosovo","palestineremembered","india-pakistan",
      "armenia-azerbaijan_2","ottoman_empire-turkey_naming_dispute",
      "palestine-israel_articles_3","palestine-israel_articles_4",
      "armenia-azerbaijan_3","palestine-israel_articles_5"]),
    ("science",     "Science avg",     "#14866D",
     ["theresa_knott_vs._mr-natural-health","mr-natural-health","climate_change_dispute",
      "climate_change_dispute_2","pseudoscience","martinphi-scienceapologist",
      "climate_change","skepticism_and_coordinated_editing"]),
    ("religion",    "Religion avg",    "#9966CC",
     ["st_christopher","ebionites","international_churches_of_christ","scientology",
      "ebionites_3","christianity_and_sexuality",
      "world_war_ii_and_the_history_of_jews_in_poland"]),
    ("social",      "Social avg",      "#339966",
     ["transnistria","abortion","manipulation_of_blps","racepacket",
      "sexology","civility_in_infobox_discussions","transgender_healthcare_and_people"]),
    ("politics",    "Politics avg",    "#CC3333",
     ["user:polishpoliticians","election","article_titles_and_capitalisation",
      "race_and_politics","manning_naming_dispute","american_politics","american_politics_2",
      "blp_issues_on_british_politics_articles","canadian_politics","iranian_politics",
      "venezuelan_politics","indian_military_history"]),
    ("policy",      "Policy avg",      "#3366CC",
     ["civility_enforcement","arbitration_enforcement_sanction_handling",
      "banning_policy","arbitration_enforcement","arbitration_enforcement_2",
      "editor_conduct_in_e-cigs_articles","conduct_of_mister_wiki_editors",
      "conduct_in_deletion-related_editing"]),
]


def compute_avg(slugs):
    curves = [c for s in slugs if (c := load_and_compute(s)) is not None]
    if not curves:
        return np.zeros(BUCKETS)
    return np.mean([c[0] for c in curves], axis=0)


def draw(out_path):
    # Load data
    fact_data    = [(lbl, col, load_and_compute(slug)) for slug, lbl, col in FACT_CASES]
    conduct_data = [(lbl, col, load_and_compute(slug)) for slug, lbl, col in CONDUCT_CASES]
    avg_data     = [(lbl, col, compute_avg(slugs)) for _, lbl, col, slugs in GROUP_AVGS]

    fact_data    = [(l, c, d) for l, c, d in fact_data    if d is not None]
    conduct_data = [(l, c, d) for l, c, d in conduct_data if d is not None]

    # ── Layout constants ────────────────────────────────────────────────────
    # Figure sized for letterhead/A4 embedded: 10" × 7.5"
    FIG_W, FIG_H = 12, 8.5

    # Row heights (in data units, y-axis 0..N)
    IND_H  = 0.60    # individual case row height
    AVG_H  = 0.55    # group-average row height
    GAP    = 0.25    # gap between individual rows
    GRP_G  = 0.40    # gap between groups in avg section
    SPACER = 0.65    # space between comparison rows and avg strip

    # Horizontal label offset (in BUCKETS units, negative = left of bar)
    LBL_X = -2.0

    # Compute row y positions (bottom → top) for comparison panel
    def make_rows(cases):
        rows, y = [], 0.0
        for lbl, col, (ev, la) in cases:
            rows.append((y, IND_H, lbl, col, ev, la))
            y += IND_H + GAP
        return rows, y - GAP

    fact_rows, fact_top    = make_rows(fact_data)
    conduct_rows, cond_top = make_rows(conduct_data)
    comp_top = max(fact_top, cond_top)

    # Avg strip starts above comparison rows
    avg_y0 = comp_top + SPACER
    # Both columns get 3 avg rows at IDENTICAL y positions
    left_avg_data  = avg_data[:3]   # Geopolitics, Science, Religion
    right_avg_data = avg_data[3:]   # Social, Politics, Policy

    left_avgs  = [(avg_y0 + i*(AVG_H+GRP_G), AVG_H, lbl, col, ev)
                  for i, (lbl, col, ev) in enumerate(left_avg_data)]
    right_avgs = [(avg_y0 + i*(AVG_H+GRP_G), AVG_H, lbl, col, ev)
                  for i, (lbl, col, ev) in enumerate(right_avg_data)]
    total_h = avg_y0 + 3*(AVG_H + GRP_G)

    # ── Figure ──────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor=BG)

    # Fractional layout
    TITLE_TOP = 0.96
    LGND_BOT  = 0.04
    AX_TOP    = TITLE_TOP - 0.12
    AX_BOT    = LGND_BOT  + 0.065

    # Two comparison columns
    L_MARGIN = 0.055
    R_MARGIN = 0.015
    COL_GAP  = 0.025
    col_w    = (1 - L_MARGIN - R_MARGIN - COL_GAP) / 2
    ax_h     = AX_TOP - AX_BOT

    # Left: FACT column (Geopolitics + Science)
    axL = fig.add_axes([L_MARGIN,              AX_BOT, col_w, ax_h])
    # Right: CONDUCT column (Politics + Policy)
    axR = fig.add_axes([L_MARGIN + col_w + COL_GAP, AX_BOT, col_w, ax_h])

    for ax in (axL, axR):
        ax.set_facecolor(BG)
        ax.set_xlim(LBL_X - 0.5, BUCKETS + 0.5)
        ax.set_ylim(-0.3, total_h + 0.1)
        ax.axis("off")

    # ── draw helper ─────────────────────────────────────────────────────────
    def draw_bar_row(ax, y, h, ev_curve, last_active, hatch_ended=True):
        for bi, ev in enumerate(ev_curve):
            ended = bi > last_active if last_active >= 0 else False
            if ended and hatch_ended:
                fc = (0.08, 0.08, 0.09)
                ax.add_patch(mpatches.Rectangle(
                    (bi, y - h/2), 1, h, facecolor=fc,
                    hatch="///", edgecolor=(0.14, 0.14, 0.15),
                    linewidth=0, zorder=2))
            else:
                ax.add_patch(mpatches.Rectangle(
                    (bi, y - h/2), 1, h,
                    facecolor=ev_color(ev), linewidth=0, zorder=2))

    def draw_avg_band(ax, y_bot, y_top, color, alpha=0.03):
        ax.add_patch(mpatches.Rectangle(
            (0, y_bot), BUCKETS, y_top - y_bot,
            linewidth=0, facecolor=(*[c for c in (
                int(color[1:3],16)/255, int(color[3:5],16)/255, int(color[5:7],16)/255
            )], alpha), zorder=0))

    # ── Individual case rows ─────────────────────────────────────────────────
    def draw_cases(ax, rows):
        for y, h, lbl, col, ev_curve, last_active in rows:
            # Subtle band
            draw_avg_band(ax, y - h/2 - 0.05, y + h/2 + 0.05, col, alpha=0.04)
            draw_bar_row(ax, y, h, ev_curve, last_active)
            ax.text(LBL_X - 0.3, y, lbl,
                    ha="right", va="center",
                    color=col, fontsize=7.5, fontweight="bold",
                    fontfamily="monospace")

    draw_cases(axL, fact_rows)
    draw_cases(axR, conduct_rows)

    # ── Group average strip (both axes) ─────────────────────────────────────
    # First 3 avgs on left axis; last 3 on right axis — SAME y positions in both
    left_avgs  = left_avgs   # already computed above
    right_avgs = right_avgs

    def draw_avg_rows(ax, rows):
        for y, h, lbl, col, avg_ev in rows:
            ax.add_patch(mpatches.Rectangle(
                (0, y - h/2 - 0.04), BUCKETS, h + 0.08,
                linewidth=0, facecolor=(0.11, 0.12, 0.16), zorder=1))
            draw_bar_row(ax, y, h, avg_ev, last_active=BUCKETS-1, hatch_ended=False)
            ax.text(LBL_X - 0.3, y, lbl,
                    ha="right", va="center",
                    color=col, fontsize=7.0, alpha=0.75)
            ax.text(LBL_X - 0.3, y - h*0.6, "all cases",
                    ha="right", va="top",
                    color=MUTED, fontsize=5.5, alpha=0.45)

    draw_avg_rows(axL, left_avgs)
    draw_avg_rows(axR, right_avgs)

    # ── Divider line between comparison rows and avg strip ──────────────────
    for ax in (axL, axR):
        ax.axhline(avg_y0 - SPACER/2, color=BORDER, linewidth=0.5,
                   alpha=0.4, linestyle=":")

    # ── ⅓ and ⅔ reference lines ────────────────────────────────────────────
    third  = BUCKETS / 3
    twoths = BUCKETS * 2 / 3
    for ax in (axL, axR):
        for xv, alpha in [(third, 0.55), (twoths, 0.30)]:
            ax.axvline(xv, color=EV_COLOR, linewidth=0.8,
                       linestyle="--", alpha=alpha, zorder=5)
        # tick labels at bottom
        ax.text(0,       -0.25, "start", ha="left",  va="top", color=MUTED, fontsize=7, alpha=0.6)
        ax.text(BUCKETS, -0.25, "end",   ha="right", va="top", color=MUTED, fontsize=7, alpha=0.6)
        ax.text(third,   -0.25, "⅓",     ha="center",va="top", color=EV_COLOR, fontsize=7, alpha=0.5)
        ax.text(twoths,  -0.25, "⅔",     ha="center",va="top", color=EV_COLOR, fontsize=7, alpha=0.35)

    # ── Annotation arrows ────────────────────────────────────────────────────
    # Left: point to late-stage orange in Armenia-Azer 2023 (last row = highest y)
    if len(fact_rows) >= 4:
        y_arm = fact_rows[3][0]   # Armenia-Azer 2023 (top individual case)
        axL.annotate(
            "evidence record\nstill growing at ⅔",
            xy=(twoths + 1, y_arm),
            xytext=(twoths - 18, y_arm + 0.9),
            color=EV_COLOR, fontsize=7, alpha=0.9,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color=EV_COLOR, lw=0.9, alpha=0.8),
            fontfamily="monospace"
        )
    # Left: point to persistent orange in Palestine-Israel 2019
    if len(fact_rows) >= 2:
        y_pal = fact_rows[2][0]   # Palestine-Israel 2019
        axL.annotate(
            "5 separate cases\nover 2 decades",
            xy=(5, y_pal),
            xytext=(16, y_pal + 0.85),
            color="#FF9900", fontsize=6.5, alpha=0.85,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color="#FF9900", lw=0.8, alpha=0.7),
            fontfamily="monospace"
        )

    # Right: point to dark zone after ⅓ in AmPol 2014 (bottom row)
    if len(conduct_rows) >= 1:
        y_ampol = conduct_rows[0][0]  # AmPol 2014
        axR.annotate(
            "dark after ⅓:\ncommittee decides",
            xy=(third + 4, y_ampol),
            xytext=(third + 16, y_ampol + 0.85),
            color="#CC3333", fontsize=7, alpha=0.9,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color="#CC3333", lw=0.9, alpha=0.8),
            fontfamily="monospace"
        )
    # Right: point to the single burst in ArbEnforcement 2015
    if len(conduct_rows) >= 3:
        y_arb = conduct_rows[2][0]   # ArbEnforcement 2015
        axR.annotate(
            "one burst of\nevidence, then done",
            xy=(10, y_arb),
            xytext=(22, y_arb + 0.85),
            color="#3366CC", fontsize=6.5, alpha=0.85,
            ha="center", va="bottom",
            arrowprops=dict(arrowstyle="->", color="#3366CC", lw=0.8, alpha=0.7),
            fontfamily="monospace"
        )

    # ── "avg strip" label ────────────────────────────────────────────────────
    # Label sits just above the dotted separator
    axL.text(0, avg_y0 - SPACER * 0.20, "Group averages — all cases:",
             ha="left", va="bottom",
             color=MUTED, fontsize=6.5, alpha=0.55, fontstyle="italic")

    # ── Column headers ───────────────────────────────────────────────────────
    def col_header(ax, header, sub, color):
        ax.text(BUCKETS / 2, total_h + 0.05, header,
                ha="center", va="bottom",
                color=color, fontsize=10, fontweight="bold", fontfamily="monospace")
        ax.text(BUCKETS / 2, total_h - 0.25, sub,
                ha="center", va="bottom",
                color=MUTED, fontsize=7.5, fontstyle="italic", alpha=0.75)

    col_header(axL, "FACT DISPUTES",
               "Geopolitics + Science  ·  orange persists throughout",
               EV_COLOR)
    col_header(axR, "CONDUCT DISPUTES",
               "Politics + Policy  ·  orange clears in first ⅓",
               "#CC3333")

    # ── Title ────────────────────────────────────────────────────────────────
    fig.text(0.04, TITLE_TOP + 0.01, "The ", ha="left", va="bottom",
             color=TEXT, fontsize=19, fontweight="bold", transform=fig.transFigure)
    fig.text(0.115, TITLE_TOP + 0.01, "Evidence", ha="left", va="bottom",
             color=EV_COLOR, fontsize=19, fontweight="bold", transform=fig.transFigure)
    fig.text(0.255, TITLE_TOP + 0.01, "Trap", ha="left", va="bottom",
             color=TEXT, fontsize=19, fontweight="bold", transform=fig.transFigure)

    fig.text(0.04, TITLE_TOP - 0.025,
             "Why fact-based conflicts never settle  ·  "
             "Wikipedia ArbCom · 53 cases · 2004–2025",
             ha="left", va="bottom", transform=fig.transFigure,
             color=MUTED, fontsize=8, fontstyle="italic")

    fig.add_artist(plt.Line2D(
        [0.04, 0.98], [TITLE_TOP - 0.030, TITLE_TOP - 0.030],
        transform=fig.transFigure,
        color=EV_COLOR, linewidth=0.8, alpha=0.4
    ))

    # Vertical divider
    mid_x = L_MARGIN + col_w + COL_GAP / 2
    fig.add_artist(plt.Line2D(
        [mid_x, mid_x], [AX_BOT, AX_TOP],
        transform=fig.transFigure,
        color=BORDER, linewidth=0.7, alpha=0.5
    ))

    # ── Legend ───────────────────────────────────────────────────────────────
    leg_items = [("none", 0.0), ("low", 0.08), ("mid", 0.22),
                 ("high", 0.42), ("peak", 0.85)]
    fig.text(0.04, LGND_BOT + 0.030, "Evidence fraction:",
             ha="left", va="bottom", transform=fig.transFigure,
             color=MUTED, fontsize=7, alpha=0.7)
    for xi, (lbl, ev_val) in enumerate(leg_items):
        x = 0.145 + xi * 0.058
        fig.add_artist(plt.Rectangle(
            (x, LGND_BOT + 0.010), 0.046, 0.020,
            transform=fig.transFigure,
            facecolor=ev_color(ev_val), edgecolor=BORDER,
            linewidth=0.4, clip_on=False))
        fig.text(x + 0.023, LGND_BOT + 0.007, lbl,
                 ha="center", va="top", transform=fig.transFigure,
                 color=MUTED, fontsize=6.5, alpha=0.7)

    fig.text(0.44, LGND_BOT + 0.030,
             "╱╱╱ = after last edit (case closed).   "
             "Thin rows = individual cases.   Thick rows = all-case group average.",
             ha="left", va="bottom", transform=fig.transFigure,
             color=MUTED, fontsize=6.5, alpha=0.55)

    plt.savefig(str(out_path), dpi=200, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    pdf_path = OUT_DIR / "evidence_trap_paper.pdf"
    svg_path = OUT_DIR / "evidence_trap_paper.svg"
    draw(pdf_path)
    draw(svg_path)
    print("Done.")
