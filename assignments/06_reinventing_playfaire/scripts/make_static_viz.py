"""
Generate a clean, annotated static visualization: evidence_trap_static.svg / .pdf
Reads the per-case JSON files, computes 60-bucket evidence fractions,
and draws a publication-ready single-page figure with annotations.
"""

import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.colors import LinearSegmentedColormap
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DATA_DIR  = Path(__file__).resolve().parents[1] / "data" / "processed" / "d3"
OUT_DIR   = Path(__file__).resolve().parents[1] / "static"
BUCKETS   = 60

BG        = "#0d1117"
BORDER    = "#30363d"
TEXT      = "#e6edf3"
MUTED     = "#8b949e"
EV_COLOR  = "#E97500"   # evidence orange
EV_RGB    = (233/255, 117/255, 0/255)

GROUPS = [
    dict(id="politics",    label="Politics",    color="#CC3333", n=12, icon="FAST CLOSE"),
    dict(id="religion",    label="Religion",    color="#9966CC", n=7,  icon="MIXED"),
    dict(id="science",     label="Science",     color="#14866D", n=8,  icon="TRAPPED"),
    dict(id="social",      label="Social",      color="#339966", n=7,  icon="MIXED"),
    dict(id="geopolitics", label="Geopolitics", color="#FF9900", n=11, icon="TRAPPED"),
    dict(id="policy",      label="Policy",      color="#3366CC", n=8,  icon="FAST CLOSE"),
]

CASES_BY_GROUP = {
    "politics": [
        "user:polishpoliticians","election","article_titles_and_capitalisation",
        "race_and_politics","manning_naming_dispute","american_politics",
        "american_politics_2","blp_issues_on_british_politics_articles",
        "canadian_politics","iranian_politics","venezuelan_politics",
        "indian_military_history",
    ],
    "religion": [
        "st_christopher","ebionites","international_churches_of_christ",
        "scientology","ebionites_3","christianity_and_sexuality",
        "world_war_ii_and_the_history_of_jews_in_poland",
    ],
    "science": [
        "theresa_knott_vs._mr-natural-health","mr-natural-health",
        "climate_change_dispute","climate_change_dispute_2","pseudoscience",
        "martinphi-scienceapologist","climate_change","skepticism_and_coordinated_editing",
    ],
    "social": [
        "transnistria","abortion","manipulation_of_blps","racepacket",
        "sexology","civility_in_infobox_discussions",
        "transgender_healthcare_and_people",
    ],
    "geopolitics": [
        "israeli_apartheid","israel-lebanon","kosovo","palestineremembered",
        "india-pakistan","armenia-azerbaijan_2","ottoman_empire-turkey_naming_dispute",
        "palestine-israel_articles_3","palestine-israel_articles_4",
        "armenia-azerbaijan_3","palestine-israel_articles_5",
    ],
    "policy": [
        "civility_enforcement","arbitration_enforcement_sanction_handling",
        "banning_policy","arbitration_enforcement","arbitration_enforcement_2",
        "editor_conduct_in_e-cigs_articles","conduct_of_mister_wiki_editors",
        "conduct_in_deletion-related_editing",
    ],
}

# ---------------------------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------------------------
def load_case(slug):
    p = DATA_DIR / f"{slug}.json"
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)

def compute_evidence_curve(json_data):
    events = json_data.get("events", [])
    if len(events) < 2:
        return None
    times = []
    for e in events:
        try:
            from datetime import datetime
            t = datetime.fromisoformat(e["timestamp"].replace("Z",""))
            times.append(t.timestamp())
        except Exception:
            pass
    if len(times) < 2:
        return None
    t0, t1 = min(times), max(times)
    dur = t1 - t0
    if dur < 86400:
        return None

    buckets = [{} for _ in range(BUCKETS)]
    ev_times = []
    for e in events:
        try:
            from datetime import datetime
            t = datetime.fromisoformat(e["timestamp"].replace("Z","")).timestamp()
        except Exception:
            continue
        frac = max(0, min(0.9999, (t - t0) / dur))
        bi = int(frac * BUCKETS)
        pt = e.get("page_type") or e.get("type") or "main"
        buckets[bi][pt] = buckets[bi].get(pt, 0) + 1

    ev_frac = []
    for bk in buckets:
        tot = sum(bk.values())
        ev  = bk.get("evidence", 0)
        ev_frac.append(ev / tot if tot > 0 else 0.0)
    return ev_frac

def build_group_averages():
    group_curves = {}
    for g in GROUPS:
        curves = []
        for slug in CASES_BY_GROUP[g["id"]]:
            data = load_case(slug)
            if data is None:
                continue
            curve = compute_evidence_curve(data)
            if curve is not None:
                curves.append(curve)
        if curves:
            avg = np.mean(curves, axis=0)
        else:
            avg = np.zeros(BUCKETS)
        group_curves[g["id"]] = avg
        print(f"  {g['label']:12s}: {len(curves)} cases loaded")
    return group_curves

# ---------------------------------------------------------------------------
# PER-CASE DATA
# ---------------------------------------------------------------------------
def load_all_case_curves():
    """Return dict: group_id → list of (short_label, ev_frac[60], lastActive)"""
    SHORTS = {
        # politics
        "user:polishpoliticians": "Polish 2004", "election": "Election 2006",
        "article_titles_and_capitalisation": "Titles 2012", "race_and_politics": "Race 2013",
        "manning_naming_dispute": "Manning 2013", "american_politics": "AmPol 2014",
        "american_politics_2": "AmPol 2015", "blp_issues_on_british_politics_articles": "BritBLP 2018",
        "canadian_politics": "Canada 2019", "iranian_politics": "Iran 2021",
        "venezuelan_politics": "Venezuela 2024", "indian_military_history": "IndMil 2025",
        # religion
        "st_christopher": "StChris 2006", "ebionites": "Ebionites 2007",
        "international_churches_of_christ": "ICC 2008", "scientology": "Sciento 2009",
        "ebionites_3": "Ebionites 2013", "christianity_and_sexuality": "C&S 2015",
        "world_war_ii_and_the_history_of_jews_in_poland": "WWII Jews 2023",
        # science
        "theresa_knott_vs._mr-natural-health": "Theresa 2004",
        "mr-natural-health": "MrNatural 2004", "climate_change_dispute": "Climate 2005",
        "climate_change_dispute_2": "Climate2 2005", "pseudoscience": "Pseudosci 2006",
        "martinphi-scienceapologist": "SciApp 2007", "climate_change": "Climate 2010",
        "skepticism_and_coordinated_editing": "Skepticism 2022",
        # social
        "transnistria": "Transnistria 2007", "abortion": "Abortion 2011",
        "manipulation_of_blps": "BLPs 2011", "racepacket": "Racepacket 2011",
        "sexology": "Sexology 2013", "civility_in_infobox_discussions": "Infobox 2018",
        "transgender_healthcare_and_people": "TransHealth 2025",
        # geopolitics
        "israeli_apartheid": "IsrApart 2006", "israel-lebanon": "IsrLebanon 2006",
        "kosovo": "Kosovo 2006", "palestineremembered": "PalRemem 2007",
        "india-pakistan": "India-Pak 2007", "armenia-azerbaijan_2": "ArmAze 2007",
        "ottoman_empire-turkey_naming_dispute": "Ottoman 2013",
        "palestine-israel_articles_3": "PalIsrael 2015",
        "palestine-israel_articles_4": "PalIsrael 2019",
        "armenia-azerbaijan_3": "ArmAze 2023",
        "palestine-israel_articles_5": "PalIsrael 2024",
        # policy
        "civility_enforcement": "Civility 2011",
        "arbitration_enforcement_sanction_handling": "ArbSanctns 2011",
        "banning_policy": "Banning 2014", "arbitration_enforcement": "ArbEnf 2015",
        "arbitration_enforcement_2": "ArbEnf2 2015",
        "editor_conduct_in_e-cigs_articles": "E-cigs 2015",
        "conduct_of_mister_wiki_editors": "MisterWiki 2017",
        "conduct_in_deletion-related_editing": "Deletion 2022",
    }

    result = {g["id"]: [] for g in GROUPS}
    for g in GROUPS:
        for slug in CASES_BY_GROUP[g["id"]]:
            data = load_case(slug)
            if data is None:
                continue
            curve = compute_evidence_curve(data)
            if curve is None:
                continue
            # compute lastActive
            events = data.get("events", [])
            from datetime import datetime
            times = []
            for e in events:
                try:
                    times.append(datetime.fromisoformat(e["timestamp"].replace("Z","")).timestamp())
                except Exception:
                    pass
            if len(times) < 2:
                continue
            t0, t1 = min(times), max(times)
            dur = t1 - t0
            buckets = [{} for _ in range(BUCKETS)]
            for e in events:
                try:
                    t = datetime.fromisoformat(e["timestamp"].replace("Z","")).timestamp()
                except Exception:
                    continue
                frac = max(0, min(0.9999, (t - t0) / dur))
                bi = int(frac * BUCKETS)
                pt = e.get("page_type") or e.get("type") or "main"
                buckets[bi][pt] = buckets[bi].get(pt, 0) + 1
            last_active = -1
            for i in range(BUCKETS - 1, -1, -1):
                if buckets[i]:
                    last_active = i
                    break
            short = SHORTS.get(slug, slug[:14])
            result[g["id"]].append((short, curve, last_active))
    return result


# ---------------------------------------------------------------------------
# DRAWING
# ---------------------------------------------------------------------------
def draw_static(group_curves, out_path, case_curves=None):
    """
    Two-column comparison layout showing individual cases for the key groups.

    Left column:  FACT DISPUTES (Geopolitics + Science) — all individual cases expanded
    Right column: CONDUCT DISPUTES (Politics + Policy) — all individual cases expanded
    Bottom strip: Religion + Social group averages (reference)

    The argument: orange is scattered throughout the LEFT column;
                  orange concentrates in the FIRST THIRD of the RIGHT column, then goes dark.
    """
    GAMMA    = 0.50    # power curve: low ev values still glow slightly
    AVG_H    = 0.85    # height of group-average row in y-units
    IND_H    = 0.45    # height of individual case row in y-units
    IND_GAP  = 0.06    # gap between individual rows
    GRP_GAP  = 0.55    # extra gap between groups
    LABEL_X  = -2.5    # x-position of labels (relative to bar start=0)

    def ev_color(ev):
        if ev < 0.005:
            return (0.09, 0.10, 0.13)
        t = min(ev / 0.40, 1.0) ** GAMMA
        return (EV_RGB[0]*t + 0.09*(1-t),
                EV_RGB[1]*t + 0.10*(1-t),
                EV_RGB[2]*t + 0.13*(1-t))

    # ── compute row layout ─────────────────────────────────────────────────
    def build_layout(group_ids):
        """Return list of (y_center, height, label, color, type, data) from bottom up."""
        rows = []
        y = 0.0
        for gid in group_ids:
            g_meta = next(g for g in GROUPS if g["id"] == gid)
            cases = case_curves[gid] if case_curves else []

            # Individual case rows (drawn first so avg is on top)
            case_rows = []
            for short, ev_curve, last_active in reversed(cases):
                case_rows.append((y, IND_H, short, g_meta["color"], "case",
                                  (ev_curve, last_active)))
                y += IND_H + IND_GAP
            y += 0.1  # gap before avg row

            # Group average row
            avg_curve = group_curves[gid]
            rows.append((y, AVG_H, g_meta["label"].upper(), g_meta["color"],
                         "avg", avg_curve))
            y += AVG_H

            # Add the case rows above the avg
            rows.extend(case_rows)

            y += GRP_GAP

        return rows, y  # rows (bottom-up), total height

    # Fact groups: Geopolitics + Science
    fact_ids    = ["geopolitics", "science"]
    conduct_ids = ["politics", "policy"]

    fact_rows,    fact_h    = build_layout(fact_ids)
    conduct_rows, conduct_h = build_layout(conduct_ids)
    max_h = max(fact_h, conduct_h)

    # ── figure ─────────────────────────────────────────────────────────────
    # Use a tall landscape figure
    scale = 0.55   # points-per-y-unit → inches
    data_h_in = max_h * scale
    fig_h = max(9.0, data_h_in + 3.2)   # title + legend margins
    fig_w = 16.0
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor=BG)

    # Two axes side by side
    # margins in figure fraction
    left_margin  = 0.04
    right_margin = 0.02
    col_gap      = 0.03
    mid          = (1 - left_margin - right_margin - col_gap) / 2

    title_top    = 0.94
    legend_bot   = 0.04
    ax_top       = title_top - 0.10   # below subtitle
    ax_bot       = legend_bot + 0.07

    # Column x positions
    ax_left_x0  = left_margin
    ax_left_x1  = left_margin + mid
    ax_right_x0 = left_margin + mid + col_gap
    ax_right_x1 = 1.0 - right_margin

    ax_h_frac = ax_top - ax_bot

    def make_ax(x0, x1):
        ax = fig.add_axes([x0, ax_bot, x1 - x0, ax_h_frac])
        ax.set_facecolor(BG)
        ax.set_xlim(-3.5, BUCKETS + 0.5)
        ax.set_ylim(-0.5, max_h + 0.2)
        ax.axis("off")
        return ax

    axL = make_ax(ax_left_x0, ax_left_x1)
    axR = make_ax(ax_right_x0, ax_right_x1)

    def draw_rows(ax, rows):
        for (y, h, label, color, kind, data) in rows:
            y_bot = y - h / 2
            if kind == "avg":
                # Slightly lighter background band
                ax.add_patch(mpatches.Rectangle(
                    (0, y_bot - 0.04), BUCKETS, h + 0.08,
                    linewidth=0, facecolor=(0.12, 0.13, 0.17), zorder=1))
                # Draw buckets
                for bi, ev in enumerate(data):
                    ax.add_patch(mpatches.Rectangle(
                        (bi, y_bot), 1, h,
                        linewidth=0, facecolor=ev_color(ev), zorder=2))
                # Group label — bold
                ax.text(LABEL_X, y, label,
                        ha="right", va="center",
                        color=color, fontsize=8.5, fontweight="bold",
                        fontfamily="monospace")
                ax.text(LABEL_X, y - h * 0.52, "group avg",
                        ha="right", va="top",
                        color=MUTED, fontsize=5.5, alpha=0.5)
            else:
                # Individual case row
                ev_curve, last_active = data
                for bi, ev in enumerate(ev_curve):
                    ended = bi > last_active
                    if ended:
                        fc = (0.08, 0.08, 0.09)
                        patch = mpatches.Rectangle(
                            (bi, y_bot), 1, h,
                            facecolor=fc,
                            hatch="///", edgecolor=(0.15, 0.15, 0.15),
                            linewidth=0, zorder=2)
                    else:
                        patch = mpatches.Rectangle(
                            (bi, y_bot), 1, h,
                            linewidth=0, facecolor=ev_color(ev), zorder=2)
                    ax.add_patch(patch)
                # Case label — dim
                ax.text(LABEL_X, y, label,
                        ha="right", va="center",
                        color=color, fontsize=5.8, alpha=0.65)

    draw_rows(axL, fact_rows)
    draw_rows(axR, conduct_rows)

    # ── vertical reference lines & labels ─────────────────────────────────
    third  = BUCKETS / 3
    twoths = BUCKETS * 2 / 3
    for ax in (axL, axR):
        for xv, lbl, alpha in [(third, "⅓", 0.45), (twoths, "⅔", 0.25)]:
            ax.axvline(xv, color=EV_COLOR, linewidth=0.7,
                       linestyle="--", alpha=alpha, zorder=5)
            ax.text(xv, max_h + 0.05, lbl,
                    ha="center", va="bottom",
                    color=EV_COLOR, fontsize=7, alpha=alpha * 1.5)
        ax.text(0, -0.45, "start", ha="left", va="top",
                color=MUTED, fontsize=7, alpha=0.6)
        ax.text(BUCKETS, -0.45, "end", ha="right", va="top",
                color=MUTED, fontsize=7, alpha=0.6)

    # ── column headers ─────────────────────────────────────────────────────
    def col_header(x_frac, header, sub, color):
        fig.text(x_frac, ax_top + 0.01, header,
                 ha="center", va="bottom", transform=fig.transFigure,
                 color=color, fontsize=11, fontweight="bold", fontfamily="monospace")
        fig.text(x_frac, ax_top - 0.025, sub,
                 ha="center", va="bottom", transform=fig.transFigure,
                 color=MUTED, fontsize=8, alpha=0.7, fontstyle="italic")

    col_mid_L = (ax_left_x0  + ax_left_x1)  / 2
    col_mid_R = (ax_right_x0 + ax_right_x1) / 2

    col_header(col_mid_L,
               "FACT DISPUTES",
               "Geopolitics + Science (n=19 cases)",
               EV_COLOR)
    col_header(col_mid_R,
               "CONDUCT DISPUTES",
               "Politics + Policy (n=20 cases)",
               "#CC3333")

    # ── annotations: arrows pointing at the pattern difference ────────────
    # Left ax: arrow pointing to persistent orange past 2/3
    axL.annotate(
        "orange persists\npast midpoint →",
        xy=(twoths + 2, fact_h * 0.55),
        xytext=(twoths + 8, fact_h * 0.62),
        color=EV_COLOR, fontsize=6.5, alpha=0.85,
        ha="center", va="center",
        arrowprops=dict(arrowstyle="->", color=EV_COLOR, lw=0.8, alpha=0.7),
        fontfamily="monospace"
    )

    # Right ax: arrow pointing to dark silence after 1/3
    axR.annotate(
        "← dark after ⅓:\nevidence released,\ncommittee decides",
        xy=(third + 3, conduct_h * 0.50),
        xytext=(third + 12, conduct_h * 0.62),
        color="#CC3333", fontsize=6.5, alpha=0.85,
        ha="center", va="center",
        arrowprops=dict(arrowstyle="->", color="#CC3333", lw=0.8, alpha=0.7),
        fontfamily="monospace"
    )

    # ── vertical divider between columns ──────────────────────────────────
    fig.add_artist(plt.Line2D(
        [(ax_left_x1 + ax_right_x0) / 2] * 2,
        [ax_bot, ax_top],
        transform=fig.transFigure,
        color=BORDER, linewidth=0.8, alpha=0.5
    ))

    # ── reference strip: Religion + Social group averages ─────────────────
    # Draw them as a compact note below the title — actually skip for space,
    # instead show them in a small inset text note
    fig.text((col_mid_L + col_mid_R) / 2, ax_bot - 0.025,
             "Religion & Social (n=14) show mixed patterns — some cases clear early, some do not.",
             ha="center", va="top", transform=fig.transFigure,
             color=MUTED, fontsize=7, fontstyle="italic", alpha=0.65)

    # ── title ──────────────────────────────────────────────────────────────
    fig.text(0.03, title_top + 0.02, "The ", ha="left", va="bottom",
             color=TEXT, fontsize=22, fontweight="bold",
             transform=fig.transFigure)
    fig.text(0.11, title_top + 0.02, "Evidence", ha="left", va="bottom",
             color=EV_COLOR, fontsize=22, fontweight="bold",
             transform=fig.transFigure)
    fig.text(0.245, title_top + 0.02, "Trap", ha="left", va="bottom",
             color=TEXT, fontsize=22, fontweight="bold",
             transform=fig.transFigure)

    fig.text(0.03, title_top - 0.015,
             "Why fact-based conflicts never settle  ·  "
             "Wikipedia Arbitration Committee · 53 cases · 2004–2025",
             ha="left", va="bottom", transform=fig.transFigure,
             color=MUTED, fontsize=8.5, fontstyle="italic")

    fig.add_artist(plt.Line2D(
        [0.03, 0.97], [title_top - 0.022, title_top - 0.022],
        transform=fig.transFigure,
        color=EV_COLOR, linewidth=0.9, alpha=0.4
    ))

    # ── legend ─────────────────────────────────────────────────────────────
    leg_items = [("none", 0.0), ("low", 0.08), ("mid", 0.22),
                 ("high", 0.42), ("peak", 0.85)]
    fig.text(0.03, legend_bot + 0.026, "Evidence fraction:",
             ha="left", va="bottom", color=MUTED, fontsize=7,
             transform=fig.transFigure, alpha=0.7)
    for xi, (lbl, ev_val) in enumerate(leg_items):
        x = 0.145 + xi * 0.062
        fc = ev_color(ev_val)
        fig.add_artist(plt.Rectangle(
            (x, legend_bot + 0.006), 0.050, 0.020,
            transform=fig.transFigure,
            facecolor=fc, edgecolor=BORDER, linewidth=0.4, clip_on=False))
        fig.text(x + 0.025, legend_bot + 0.002, lbl,
                 ha="center", va="top", transform=fig.transFigure,
                 color=MUTED, fontsize=6.5, alpha=0.7)

    # Hatching note
    fig.text(0.48, legend_bot + 0.020,
             "╱╱╱ = after last recorded edit (case effectively closed)",
             ha="left", va="bottom", transform=fig.transFigure,
             color=MUTED, fontsize=6.5, alpha=0.55)

    plt.savefig(str(out_path), dpi=180, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    print(f"Saved: {out_path}")


# Also save PDF
def main():
    print("Loading case data...")
    group_curves = build_group_averages()

    print("Loading individual case curves...")
    case_curves = load_all_case_curves()
    for gid, cases in case_curves.items():
        print(f"  {gid}: {len(cases)} cases")

    svg_path = OUT_DIR / "evidence_trap_static.svg"
    pdf_path = OUT_DIR / "evidence_trap_static.pdf"

    print("Drawing SVG...")
    draw_static(group_curves, svg_path, case_curves)

    print("Drawing PDF...")
    draw_static(group_curves, pdf_path, case_curves)

    print("Done.")

if __name__ == "__main__":
    main()
