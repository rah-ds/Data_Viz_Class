"""
Prepare Wikipedia Arbitration data for D3 visualizations.

Reads arb_cases.txt, categorizes each case by topic area and dispute type,
and outputs structured JSON for visualization.
"""

import json
import re
from pathlib import Path
from collections import Counter

# Paths
ROOT = Path(__file__).resolve().parents[3]  # Data_Viz_Class root
DATA_DIR = ROOT / "data" / "raw" / "03_visual_data_analysis"
ARB_CASES_FILE = DATA_DIR / "arb_cases.txt"
OUTPUT_DIR = DATA_DIR

# ---------- Topic Classification Rules ----------
# Each rule: (list_of_keywords, category)

TOPIC_RULES = [
    # Geopolitics & Regional Conflicts
    (["Israel", "Palest", "Gaza", "Arab", "Zion", "antisemit", "Deir Yassin",
      "Liancourt", "Kashmir", "India-Pakistan", "Armenia-Azerbaijan", "Kosovo",
      "Kurdistan", "Kurd", "Ottoman", "Transnistria", "Gibraltar", "Dalmatia",
      "Eastern Europe", "Horn of Africa", "War of the Pacific", "West Bank",
      "Judea", "Senkaku", "Iran", "Iraqi", "Venezuelan", "Canadian politics",
      "American politics", "Baku", "Korean", "Catalonia", "Franco-Mongol",
      "German war", "Historical elections", "Israel-Lebanon", "Israeli apartheid",
      "Tang Dynasty", "Xinjiang"], "Geopolitics"),

    # Science & Medicine
    (["Climate", "COVID", "Vaccine", "Evolution", "Intelligent design",
      "Fringe science", "Pseudoscience", "Acupuncture", "Cold fusion",
      "Depleted uranium", "Genetically modified", "Industrial agriculture",
      "Medicine", "Neuro-linguistic", "Speed of light", "Austrian economics",
      "Socionics", "ADHD"], "Science & Medicine"),

    # Religion
    (["Muhammad", "Scientology", "Mormon", "Christianity", "Falun Gong",
      "Ebionites", "International Churches", "Chabad", "Sathya Sai",
      "Francis Schuckardt", "KJV", "Transcendental Meditation", "Prem Rawat",
      "Waldorf education", "Attachment Therapy", "New World Translation",
      "Historicity of Jesus"], "Religion"),

    # Social & Cultural Issues
    (["Abortion", "Gun control", "GamerGate", "Gender", "Transgender",
      "Sexology", "Sexuality", "Race and", "Critical race", "Waterboarding",
      "Bowling for Columbine", "Brexit", "Tea Party", "Obama",
      "BLP", "Biographies of Living", "Sarah Palin", "Lyndon LaRouche",
      "Boris Stomakhin", "Warren Kinsella", "Manning naming",
      "Asmahan", "Yasuke", "Rajput", "Allegations of apartheid"], "Social & Cultural"),

    # Editor Conduct (personal disputes, sanctions, etc.)
    (["vs", "v.", "appeal", "ban", "block", "sanction", "enforcement",
      "wheel war", "sockpuppet", "civility", "conduct", "Reversion",
      "Reversal", "restriction", "banning", "Arbitration Enforcement",
      "Arbitration enforcement", "Attack sites"], "Editor Conduct"),

    # Content & Policy Disputes
    (["Infobox", "Article titles", "capitalisation", "Template", "Portals",
      "BJAODN", "Episodes and characters", "Date delinking", "Highways",
      "Webcomics", "WikiProject", "Tree shaping", "John Buscema",
      "Honda S2000", "Moby Dick", "Shakespeare authorship",
      "Monty Hall", "Media Viewer", "Motorsports", "Election",
      "Ayn Rand", "Great Irish Famine", "World War II",
      "Robert the Bruce", "Robert I", "Henri Coanda", "Vivaldi",
      "Carl Hewitt", "Longevity", "Hunger", "List of"], "Content & Policy"),

    # User-specific / Named editor disputes  (catch-all for editor names)
    (["User:", "IRC", "CAMERA", "COFS", "PoolGuy", "WikiUser",
      "Wikicology", "Conflict of interest"], "Procedural"),
]


def classify_case(case_name: str) -> dict:
    """Classify an arbitration case by topic category and infer dispute type."""
    category = "Editor Disputes"  # default for named-editor cases

    for keywords, cat in TOPIC_RULES:
        for kw in keywords:
            if kw.lower() in case_name.lower():
                category = cat
                break
        else:
            continue
        break

    # Determine dispute type (content vs conduct vs hybrid)
    conduct_signals = ["ban", "block", "sanction", "conduct", "civility",
                       "wheel war", "sockpuppet", "enforcement", "appeal",
                       "restriction", "vs", "v."]
    content_signals = ["article", "infobox", "template", "capitalisation",
                       "title", "naming", "portals", "election"]

    is_conduct = any(s.lower() in case_name.lower() for s in conduct_signals)
    is_content = any(s.lower() in case_name.lower() for s in content_signals)

    if is_conduct and is_content:
        dispute_type = "Hybrid"
    elif is_conduct:
        dispute_type = "Conduct"
    elif is_content:
        dispute_type = "Content"
    else:
        # Heuristic: if case name looks like a person's name, it's conduct
        # If it looks like a topic, it's content
        if category in ("Geopolitics", "Science & Medicine", "Religion",
                        "Social & Cultural", "Content & Policy"):
            dispute_type = "Content"
        else:
            dispute_type = "Conduct"

    # Estimate complexity by name features (proxy for number of parties)
    complexity = "Simple"
    if any(x in case_name for x in [" and ", " et al", " 2", " 3", " 4", " 5",
                                     "others", "editors", "articles"]):
        complexity = "Complex"
    if any(x in case_name for x in [" et al", "others", "articles", " 4", " 5"]):
        complexity = "Very Complex"

    # Detect if it's a recurring case (has a number suffix)
    recurrence = 1
    match = re.search(r'\s(\d+)$', case_name)
    if match:
        recurrence = int(match.group(1))

    return {
        "name": case_name,
        "category": category,
        "dispute_type": dispute_type,
        "complexity": complexity,
        "recurrence": recurrence,
        "is_recurring": recurrence > 1,
    }


def build_lifecycle_data():
    """
    Build dispute resolution lifecycle stage data.
    Based on the Wikipedia DR lifecycle model from the project docs.
    """
    stages = [
        {"id": "talk", "label": "Talk Page", "order": 0,
         "description": "Informal discussion between editors on article talk pages"},
        {"id": "3o", "label": "Third Opinion", "order": 1,
         "description": "Request for uninvolved third editor (2-party disputes only)"},
        {"id": "rfc", "label": "Request for Comment", "order": 1,
         "description": "Broader community input solicited for multi-party disputes"},
        {"id": "drn", "label": "Dispute Resolution Noticeboard", "order": 2,
         "description": "Structured mediation by trained volunteers"},
        {"id": "ani", "label": "Administrators' Noticeboard", "order": 3,
         "description": "Admin intervention for conduct violations"},
        {"id": "arbcom", "label": "Arbitration Committee", "order": 4,
         "description": "Binding decisions by elected committee—court of last resort"},
        {"id": "resolved", "label": "Resolved", "order": 5,
         "description": "Dispute concluded via consensus, sanctions, or binding ruling"},
    ]

    # Transition flows (from → to, with type and estimated volume)
    transitions = [
        {"source": "talk", "target": "3o", "type": "content", "value": 35},
        {"source": "talk", "target": "rfc", "type": "content", "value": 45},
        {"source": "talk", "target": "ani", "type": "conduct", "value": 30},
        {"source": "talk", "target": "resolved", "type": "consensus", "value": 60},
        {"source": "3o", "target": "drn", "type": "escalation", "value": 15},
        {"source": "3o", "target": "resolved", "type": "consensus", "value": 20},
        {"source": "rfc", "target": "drn", "type": "escalation", "value": 20},
        {"source": "rfc", "target": "ani", "type": "escalation", "value": 10},
        {"source": "rfc", "target": "resolved", "type": "consensus", "value": 25},
        {"source": "drn", "target": "ani", "type": "escalation", "value": 18},
        {"source": "drn", "target": "arbcom", "type": "escalation", "value": 8},
        {"source": "drn", "target": "resolved", "type": "mediated", "value": 22},
        {"source": "ani", "target": "arbcom", "type": "escalation", "value": 25},
        {"source": "ani", "target": "resolved", "type": "sanctioned", "value": 33},
        {"source": "arbcom", "target": "resolved", "type": "binding", "value": 33},
    ]

    return {"stages": stages, "transitions": transitions}


def build_category_network():
    """Build a network showing connections between categories via shared patterns."""
    # Cross-topic connections based on arb cases that span categories
    connections = [
        {"source": "Geopolitics", "target": "Editor Conduct",
         "strength": 45, "reason": "Edit wars on geopolitical articles trigger conduct cases"},
        {"source": "Science & Medicine", "target": "Editor Conduct",
         "strength": 30, "reason": "Climate/COVID disputes lead to editor sanctions"},
        {"source": "Religion", "target": "Social & Cultural",
         "strength": 20, "reason": "Religious topics intersect social issues"},
        {"source": "Religion", "target": "Editor Conduct",
         "strength": 25, "reason": "Religious article edit wars"},
        {"source": "Social & Cultural", "target": "Editor Conduct",
         "strength": 35, "reason": "BLP and social issue disputes escalate"},
        {"source": "Content & Policy", "target": "Procedural",
         "strength": 15, "reason": "Policy disputes generate procedural cases"},
        {"source": "Geopolitics", "target": "Social & Cultural",
         "strength": 18, "reason": "Geopolitical topics intersect social issues"},
        {"source": "Science & Medicine", "target": "Content & Policy",
         "strength": 12, "reason": "Scientific sourcing disputes"},
    ]
    return connections


def main():
    # Read arb cases
    with open(ARB_CASES_FILE, "r") as f:
        cases = [line.strip() for line in f if line.strip()]

    print(f"Read {len(cases)} arbitration cases")

    # Classify each case
    classified = [classify_case(c) for c in cases]

    # Build category summary
    cat_counts = Counter(c["category"] for c in classified)
    type_counts = Counter(c["dispute_type"] for c in classified)
    complexity_counts = Counter(c["complexity"] for c in classified)
    recurring = sum(1 for c in classified if c["is_recurring"])

    print(f"\nCategory distribution:")
    for cat, count in cat_counts.most_common():
        print(f"  {cat}: {count}")

    print(f"\nDispute type distribution:")
    for t, count in type_counts.most_common():
        print(f"  {t}: {count}")

    print(f"\nComplexity distribution:")
    for comp, count in complexity_counts.most_common():
        print(f"  {comp}: {count}")

    print(f"\nRecurring cases: {recurring}")

    # Build lifecycle data
    lifecycle = build_lifecycle_data()

    # Build network connections
    network = build_category_network()

    # Category × type crosstab
    crosstab = {}
    for c in classified:
        key = c["category"]
        if key not in crosstab:
            crosstab[key] = {"Content": 0, "Conduct": 0, "Hybrid": 0}
        crosstab[key][c["dispute_type"]] += 1

    # ---- Build recurring case families ----
    # Group cases that share a base name (e.g., "Rex071404", "Rex071404 2", etc.)
    families = {}
    for c in classified:
        # Strip trailing number to find the base name
        base = re.sub(r'\s+\d+$', '', c["name"])
        if base not in families:
            families[base] = []
        families[base].append(c)

    # Only keep families with 2+ cases
    recurring_families = []
    for base, members in sorted(families.items()):
        if len(members) >= 2:
            recurring_families.append({
                "base_name": base,
                "category": members[0]["category"],
                "dispute_type": members[0]["dispute_type"],
                "count": len(members),
                "max_recurrence": max(m["recurrence"] for m in members),
                "cases": [m["name"] for m in members],
            })

    recurring_families.sort(key=lambda f: f["count"], reverse=True)

    # ---- Build alphabetical index for beeswarm ----
    # Assign each case a stable index within its category for layout
    by_category = {}
    for c in classified:
        by_category.setdefault(c["category"], []).append(c)
    for cat in by_category:
        by_category[cat].sort(key=lambda x: x["name"].lower())
        for i, c in enumerate(by_category[cat]):
            c["index_in_category"] = i

    # Assemble full dataset
    dataset = {
        "cases": classified,
        "summary": {
            "total_cases": len(classified),
            "categories": dict(cat_counts),
            "dispute_types": dict(type_counts),
            "complexity": dict(complexity_counts),
            "recurring_cases": recurring,
            "crosstab": crosstab,
        },
        "lifecycle": lifecycle,
        "network": network,
        "recurring_families": recurring_families,
    }

    # Write JSON
    output_file = OUTPUT_DIR / "arb_cases_classified.json"
    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)

    print(f"\nWrote dataset to {output_file}")


if __name__ == "__main__":
    main()
