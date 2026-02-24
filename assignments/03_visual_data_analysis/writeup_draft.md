# What Drives Wikipedia to Its Court of Last Resort?

## A Visual Analysis of 481 Wikipedia Arbitration Committee Cases

**Ryan Healy** | Data Visualization – Homework 3  
**Dataset**: Wikipedia Arbitration Committee (ArbCom) case archive — 481 named cases, classified by topic category, dispute type (content vs. conduct), complexity, and recurrence  
**Source**: Wikipedia Arbitration project data (`arb_cases.txt`, `full_articles.yaml`, dispute resolution lifecycle model)

---

## The Question

**What kinds of disputes reach Wikipedia's final authority, and what does the pattern of escalation reveal about where the collaborative encyclopedia model breaks down?**

Wikipedia's Arbitration Committee (ArbCom) is the elected body that serves as the "court of last resort" for the English-language Wikipedia. Cases arrive at ArbCom only after lower-level dispute resolution mechanisms — talk pages, third opinions, mediation, admin intervention — have failed. This makes the ArbCom case archive a revealing dataset: it is a catalogue of *failures of consensus*, the places where Wikipedia's open-editing model could not self-heal.

By classifying all 481 ArbCom case names by topic category, dispute type, case complexity, and recurrence (cases that returned for a second or third round), I ask: **Where does Wikipedia's graduated dispute resolution system fail, and why?** Are the intractable disputes about controversial topics — or about individual editors? Do some categories resist resolution more stubbornly than others?

---

## Visualization Approaches

I built three D3.js visualizations, each using a fundamentally different spatial and encoding strategy to expose different dimensions of this question.

### Visualization 1: The Escalation Funnel (Sankey Diagram)

**Technique**: A Sankey (alluvial) diagram mapping dispute flow through Wikipedia's six-stage graduated resolution system: Talk Page → Third Opinion / Request for Comment → Dispute Resolution Noticeboard → Administrators' Noticeboard → ArbCom → Resolved.

**How it works**: The horizontal position encodes the *stage* of the dispute resolution pipeline (left = informal, right = formal/binding). The vertical thickness of each flow band encodes the *volume* of disputes traveling that pathway. Color is inherited from the source node, creating visual continuity as flows merge, split, and taper through the system.

**Encoding strategy**: This is fundamentally a *flow-and-funnel* representation. The leftward width of the Talk Page node (which receives all disputes) versus the narrow band that reaches ArbCom creates a visual metaphor for *filtration*. The eye naturally follows the diminishing flow rightward, which mirrors the actual escalation pathway — most disputes resolve early; a small fraction persists to binding arbitration.

**Rules of the layout**: The Sankey enforces a strict left-to-right reading order that maps to the temporal/authority gradient of the system. Nodes cannot be freely repositioned; their vertical extent is determined by the volume passing through them. This means the chart *structurally prevents* showing anything other than flow and volume — it cannot show time, individual cases, or case characteristics.

**Cognitive design**: The Sankey leverages *schema*: readers already understand funnels and pipelines. The graduated narrowing of flow bands activates the intuition that "most things don't make it through." Color continuity reduces *split attention* — you can track a pathway type (content vs. conduct) across stages without consulting a separate legend.

### Visualization 2: The Anatomy of Arbitration (Nested Treemap)

**Technique**: A nested treemap where the outer rectangles represent topic categories (Geopolitics, Science & Medicine, Religion, Social & Cultural, Editor Conduct, Content & Policy, Procedural, Editor Disputes) and inner rectangles subdivide each category by dispute type (Content, Conduct, Hybrid). Area encodes case count.

**How it works**: The treemap algorithm partitions a rectangular canvas into nested rectangles whose areas are proportional to a quantitative variable — here, the number of ArbCom cases. The outer nesting groups cases by topic category; within each category, sub-rectangles show how many cases were Content disputes vs. Conduct disputes vs. Hybrid.

**Encoding strategy**: This uses *area as the primary channel* — the single strongest preattentive cue for quantity comparison. Color hue distinguishes categories, while saturation/brightness variation within each category distinguishes dispute type. Labels are embedded directly in the cells to eliminate split attention between the chart and a legend.

**Rules of the layout**: The treemap's layout algorithm optimizes for *squareness* (reducing long, thin slivers), which means adjacent rectangles are placed to minimize perimeter. This creates a compact, space-filling view — no whitespace is wasted. However, the algorithm determines position, so the spatial relationships between categories are *not* meaningful (unlike a scatterplot). You cannot infer that two adjacent categories are "related" — adjacency is an artifact of the packing algorithm.

**Cognitive design**: The treemap leverages *chunking* — the outer category borders create perceptual groups that the eye can scan as units before diving into sub-category detail. The overwhelming visual dominance of the "Editor Disputes" rectangle (which dwarfs all topic categories) creates an immediate *preattentive pop-out* that delivers the key insight before any reading is required.

### Visualization 3: Which Disputes Come Back? (Heatmap)

**Technique**: A matrix heatmap with topic category on the Y-axis, case complexity (Simple / Complex / Very Complex) on the X-axis, and color saturation encoding the *proportion of recurring cases* — those that came back to ArbCom for a second, third, or later hearing (e.g., "Arbitration enforcement 2", "Palestine-Israel articles 5").

**How it works**: Each cell represents the intersection of one category and one complexity level. The count of cases in that cell is annotated as a number. The fill color uses a sequential yellow-orange-red scale (YlOrRd) where intensity maps to the recurrence rate — the proportion of cases in that cell that have numbered sequels. Darker = more repeat disputes.

**Encoding strategy**: This is a *matrix-comparison* technique. By placing categories and complexity on orthogonal axes, the heatmap enables *structured pairwise comparison*: the eye can scan along a row (how does recurrence vary with complexity within one category?) or down a column (which categories have the highest recurrence at a given complexity?). Color saturation provides a *continuous quantitative channel* that is readable without precise decoding — "darker = more recurring."

**Rules of the layout**: The heatmap enforces a *grid discipline* that creates perfectly aligned comparison slots. Every category gets the same-width columns; every complexity level gets the same-height rows. This makes comparison fair — no category gets more visual weight by accident. The trade-off is that the grid cannot show relationships *between* cells (e.g., it cannot show that Geopolitics-Complex cases escalated from Geopolitics-Simple cases).

**Cognitive design**: The heatmap minimizes *extraneous cognitive load* by reducing the task to color comparison within a familiar grid schema. The dual encoding — number annotation for exact values, color for rapid scanning — allows both *precise* and *approximate* reading modes without switching between chart types.

---

## Insights

### 1. ArbCom is overwhelmingly a behavioral court, not a content court.
The treemap delivers this instantly: **"Editor Disputes" accounts for 309 of 481 cases (64%)**. Most ArbCom cases are named after individual editors (e.g., "Betacommand", "Ryulong", "DreamGuy"), not topics. This reveals that Wikipedia's highest authority spends the majority of its time adjudicating *individual conduct*, not settling substantive content disagreements. Content disputes are largely resolved at lower stages (as the Sankey shows — content pathways taper to thin bands by the time they reach ArbCom).

### 2. Geopolitics is the most arbitration-prone topic area.
Among topic-driven cases, **Geopolitics leads with 37 cases**, followed by Content & Policy (34), Social & Cultural (25), Religion (19), and Science & Medicine (17). The Israel-Palestine conflict alone has generated at least 5 numbered ArbCom cases (Palestine-Israel articles 3, 4, 5), making it the most persistent topic-level dispute on the platform.

### 3. Recurring cases cluster in specific categories and complexity levels.
The heatmap reveals that **recurrence is not uniform** — some categories have dramatically higher rates of repeat arbitration. Geopolitics and Editor Disputes both show high recurrence among Complex and Very Complex cases, indicating that the disputes ArbCom handles in these areas are fundamentally resistant to one-time resolution. By contrast, Science & Medicine cases rarely recur, suggesting that once ArbCom rules on a scientific-topic dispute, the decision tends to stick.

### 4. The escalation funnel is steeper for conduct than content.
The Sankey shows that content disputes have multiple off-ramps (Third Opinion, RfC, DRN) that bleed volume before reaching admin intervention. Conduct disputes, by contrast, bypass content-focused stages and flow more directly from Talk Page → ANI → ArbCom. This means the system provides fewer "soft" resolution mechanisms for behavioral problems — a structural gap that may explain why ArbCom's docket is dominated by conduct cases.

---

## Critical Comparison of Techniques

### What each reveals that the others cannot:

| Technique | Unique Strength | Blind Spot |
|-----------|----------------|------------|
| **Sankey** | Shows the *process* — how disputes flow and filter through stages. Reveals the structural asymmetry between content and conduct pathways. | Cannot show individual cases, categories, or recurrence. The lifecycle data is modeled, not observed case-by-case. |
| **Treemap** | Shows the *composition* — the part-to-whole relationship of categories and types. The area encoding delivers the "Editor Disputes dominate" insight instantly. | Cannot show process, time, or recurrence. The packing algorithm means spatial position is meaningless — proximity ≠ relatedness. |
| **Heatmap** | Shows *cross-dimensional patterns* — how recurrence varies across both category and complexity simultaneously. The grid layout enables systematic row/column scanning. | Cannot show volume well (small cell counts may have noisy rates). Cannot show process or flow. The uniform grid gives equal visual weight to cells with 2 cases and cells with 250 cases. |

### What each hides:

- **Sankey** hides *heterogeneity*. All disputes are aggregated into flow volumes — you cannot see that a Geopolitics case behaves differently from a Religion case within the same flow.
- **Treemap** hides *temporal dynamics*. You see that Editor Disputes dominate, but not whether this has changed over time. The treemap is a static snapshot.
- **Heatmap** hides *absolute magnitude*. A cell with 3 cases and 67% recurrence looks dramatic in color, but the small sample size makes the rate unreliable. The cell annotations partially mitigate this, but the color still dominates the preattentive read.

### How the rules of layout affect understanding:

The **Sankey's** left-to-right flow rule powerfully reinforces the mental model of escalation, but it *constrains* the analyst to thinking about disputes as a pipeline — which may not be accurate (disputes can skip stages, loop back, or run in parallel across multiple venues simultaneously).

The **Treemap's** space-filling rule is extremely efficient for part-to-whole comparison, but the lack of meaningful spatial arrangement means the analyst cannot form spatial hypotheses ("what's near what?"). This is a strength in one sense — it prevents false spatial inferences — but a weakness in that it wastes the position channel entirely.

The **Heatmap's** grid rule is the most disciplined: every intersection gets exactly one cell, enabling systematic comparison. But the grid assumes that both dimensions are *categorical and independent*. If complexity actually correlates with category (e.g., geopolitical disputes are inherently more complex), the grid treats this as an incidental pattern rather than a structural feature.

### Suggested improvements and next steps:

1. **Add a temporal dimension**: A streamgraph or stacked area chart showing ArbCom cases over time by category would reveal whether the composition of the docket has shifted (e.g., more social/cultural cases in recent years with culture-war topics).
2. **Individual case detail**: A zoomable treemap or sunburst that lets the viewer drill into individual case names within each category would bridge the gap between the aggregate view and case-level specifics.
3. **Network view**: The Wikipedia Arbitration project data includes editor overlap across cases — a force-directed network graph showing editors as nodes and shared ArbCom involvement as edges would reveal *repeat players* in the arbitration system.
4. **Combine recurrence + volume**: The heatmap's recurrence rate could be made more robust by encoding cell *size* proportional to case count (a proportional-symbol heatmap), so that small-N cells with noisy rates don't visually dominate.
5. **Annotation and narrative layer**: Exporting the SVGs and annotating them in Inkscape/Illustrator with callouts for notable cases (e.g., the Palestine-Israel series, the Climate change disputes) would add the interpretive layer that automated tools cannot produce.

---

## Extended Visualizations (4–6)

Three additional visualizations push the same dataset through radically different spatial logics.

### Visualization 4: The Dispute Resolution DAG (Directed Acyclic Graph)

**Technique**: A hand-positioned directed acyclic graph that renders the dispute resolution lifecycle as a network rather than a pipeline. Nodes represent resolution stages; directed edges represent valid escalation pathways. Node radius encodes throughput (total disputes flowing through that stage); edge thickness encodes flow volume. Subtle column bands indicate authority level (Informal → Community → Mediation → Admin → Arbitration → Outcome).

**How it differs from the Sankey**: The Sankey compressed the system into a left-to-right pipeline and treated Third Opinion (3O) and Request for Comment (RfC) as separate sequential nodes. The DAG reveals that they are *parallel* — both sit at the same authority level. It also exposes the *topology*: you can see that DRN can feed both ANI *and* ArbCom directly (not just via ANI), and that Talk Pages can short-circuit to ANI when conduct violations are immediate. The DAG's arrowhead markers make directionality explicit — something the Sankey implied but never showed.

**Strengths**: The DAG is the only visualization that preserves the system's *graph structure*. It shows branching, parallelism, and shortcuts that the Sankey's left-to-right bands collapsed. The authority-level column bands provide a geographic metaphor for institutional escalation.

**Weaknesses**: The manual positioning means the layout is editorially determined, not algorithmically derived from data — it cannot scale to new stages without repositioning. The DAG also cannot show *case-level* detail; it is still an aggregate system view.

**Cognitive design**: The DAG leverages spatial reasoning more naturally than the Sankey. Nodes at the same horizontal position are at the same authority level — the eye can compare laterally. The concentric throughput encoding (larger nodes = more traffic) creates a preattentive "mass" impression: you immediately see that Talk Page and Resolved are the heaviest nodes, bookending the system.

### Visualization 5: A Census of Every Case (Beeswarm Strip Plot)

**Technique**: A beeswarm plot that renders every single case as an individual dot, organized into horizontal rows by category. Within each row, dots are spread using a force simulation to avoid overlap. Color encodes dispute type (Content / Conduct / Hybrid); dot radius encodes recurrence depth (larger dots = more ArbCom hearings for that case).

**How it differs from the treemap**: The treemap aggregated cases into area-proportional rectangles. The beeswarm *disaggregates* — every case is individually visible and hoverable. This is the only visualization in the set that lets you find a specific case by name. The sheer visual density of the Editor Disputes row (309 tightly packed gray-orange dots) gives visceral weight to the finding that ArbCom is a conduct court — in a way that a single large rectangle never could.

**Strengths**: The beeswarm preserves *individual identity*. You can hover any dot and see "Rex071404" or "Palestine-Israel articles 5." The force simulation creates organic clustering that visually encodes density without binning — the row fullness *is* the count. The recurrence-sized dots make repeat offenders literally stand out.

**Weaknesses**: The beeswarm is poor at precise quantitative comparison — you cannot easily tell whether Editor Disputes has 309 or 350 cases by counting dots. It also does not encode any structural relationship between cases (e.g., that "Everyking" and "Everyking 2" and "Everyking 3" are the same dispute). Dot overlap, while mitigated by the force simulation, can still obscure dots in dense rows.

**Cognitive design**: The beeswarm leverages the *enumeration* instinct — the brain registers "a lot of dots" as magnitude, even without counting. The color encoding creates immediate layering: scanning across a row, you can see whether a category is dominated by blue (Content) or orange (Conduct) dots. This is a *part-to-whole* cue embedded in a *unit-level* view — a hybrid that neither the treemap (aggregate only) nor the heatmap (matrix only) could provide.

### Visualization 6: The Disputes That Won't Die (Radial Burst)

**Technique**: A radial layout centered on a hub, with 33 spokes radiating outward — one per recurring case family. Each family is a dispute that returned to ArbCom for at least one sequel (e.g., "Rex071404" → 4 hearings). Spokes are grouped into angular sectors by topic category. Spoke length encodes the maximum recurrence number (how many times the case returned). Dots along each spoke mark individual hearings (filled = case exists, hollow = gap in numbering).

**How it differs from everything else**: This is the only visualization that focuses exclusively on *recurrence* — the failure of finality. The Sankey and DAG showed the system; the treemap and beeswarm showed the population; the heatmap showed aggregate recurrence rates. The radial burst shows *which specific disputes resisted permanent resolution*, and how deeply. The angular grouping by category reveals that Editor Disputes dominates in count, but Geopolitics produces the deepest recurrence — Palestine-Israel articles reached case #5.

**Strengths**: The radial layout is inherently dramatic — long spokes "punch outward" from the center, creating visual emphasis proportional to the severity of the recurrence. The sector grouping enables category comparison without a grid. The spoke-and-dot encoding is information-dense: in one glyph, you can read the family name, category, number of hearings, and any gaps in the sequence.

**Weaknesses**: The radial layout sacrifices comparison precision — angular differences are harder to judge than linear differences. Spoke labels crowd each other in dense sectors (Editor Disputes), requiring only the most-recurrent families to be labeled. The circular form also wastes the central area (though this is mitigated by using it for a summary annotation).

**Cognitive design**: The radial burst leverages the *explosion metaphor* — spokes radiating from a center suggest force, tension, unresolved energy. This aligns with the semantic content: these are disputes that *could not be contained*. The concentric reference circles (1×, 2×, 3×, 4×, 5×) provide a ruler for reading depth, reducing the decoding effort. The category color sectors use *color as grouping* rather than color as quantity — a more natural use of the hue channel.

---

## Cross-Comparison: All Six Visualizations

| # | Technique | Spatial Logic | What It Shows Best | What It Hides |
|---|-----------|--------------|-------------------|---------------|
| 1 | Sankey | Left→right pipeline | Flow volume & filtration | Network topology, individual cases |
| 2 | Treemap | Space-filling area | Part-to-whole composition | Time, process, individuals |
| 3 | Heatmap | Grid matrix | Cross-dimensional rates | Volume reliability, relationships |
| 4 | DAG | Network graph | System topology & parallelism | Individual cases, time |
| 5 | Beeswarm | Force-packed strips | Every individual case | Precise counts, relationships |
| 6 | Radial | Polar burst | Recurrence families & depth | Non-recurring cases, volume |
| 7 | Parallel Coordinates | Multi-axis polylines | Multivariate co-occurrence | Density (overplotting), hierarchy |
| 8 | Unit / Waffle | Grid of individual squares | Exact counts, magnitude | Relationships, process, time |
| 9 | Sunburst | Concentric radial rings | Hierarchical drill-down | Precise comparison, flat views |

The progression from Viz 1→9 moves from *system-level abstraction* (how does the pipeline work?) to *case-level specificity* (which exact disputes keep coming back?) to *multivariate exploration* (how do all four attributes interact?). Each successive visualization sacrifices one kind of clarity to gain another. The Sankey and DAG show the *machine*; the treemap and heatmap show the *statistics*; the beeswarm and radial burst show the *individuals*; the parallel coordinates show the *attribute space*; the unit chart shows the *population as individuals*; and the sunburst provides *zoomable hierarchy*.

---

## Experimental Visualizations (7–9)

Three final visualizations test fundamentally different spatial logics against the same 481-case dataset.

### Visualization 7: Multivariate Threads (Parallel Coordinates)

**Technique**: A parallel coordinates plot with four vertical axes — Category, Dispute Type, Complexity, and Recurrence — where each of 481 cases is drawn as a polyline threading through all four. Color encodes category. Axes support brushing for interactive filtering.

**How it works**: Each axis is a categorical or ordinal scale laid out vertically. A single case creates a polyline connecting its value on each axis, left to right. When hundreds of lines overlap, they create visible *bundles* — thick bands of coincident paths that reveal dominant attribute combinations. Brushing an axis region filters the view to only those lines passing through the selected values.

**Encoding strategy**: The parallel coordinates plot is the only technique in this set that uses *position on multiple axes simultaneously* as its primary encoding channel. The polyline connecting axis values creates a visual *thread* — the eye can trace a single case across all four dimensions. Where many threads coincide, the bundle density functions as an implicit frequency encoding.

**Rules of the layout**: The axes are uniformly spaced horizontally, and each has its own independent vertical scale. The left-to-right axis order is editorially chosen (Category → Type → Complexity → Recurrence), and reordering the axes would reveal different patterns. This is both a strength (the analyst can explore) and a weakness (the visualization's story depends on axis arrangement). The parallel coordinate chart also assumes that each axis is *independent* — it does not enforce or reveal structural relationships between dimensions.

**Cognitive design**: The "thread" metaphor leverages the eye's ability to follow continuous lines — a preattentive process that requires no decoding. The heavy bundle from Editor Disputes → Conduct → Simple → 1× is immediately visible as the *dominant pathway*. The thin, divergent threads (Geopolitics → Content → Very Complex → 5×) are visually salient *because* they deviate from the main bundle. Brushing adds progressive disclosure: the analyst narrows focus without losing context.

**Key insight**: The plot reveals that **the dominant attribute combination (Editor Disputes / Conduct / Simple / non-recurring) accounts for the vast majority of cases**, creating a single thick bundle. The interesting analytical stories live in the thin threads that deviate — particularly the Geopolitics cases that thread through Content and Very Complex before reaching high recurrence numbers.

### Visualization 8: Counting Every Case (Unit / Waffle Chart)

**Technique**: A unit chart where every case is a single small colored square, grouped by category in labeled rows, colored by dispute type (Content / Conduct / Hybrid). Recurring cases are marked with a white center dot. Cases are sorted by dispute type and then by recurrence depth within each category group.

**How it works**: Each of the 481 cases gets one square — no aggregation, no abstraction. Squares are packed 50 per row within each category block. The visual weight of each block is determined purely by how many squares it contains. This is the data visualization equivalent of *counting on your fingers* — maximally concrete, minimally abstract.

**Encoding strategy**: The unit chart uses *position as grouping* (vertical blocks = category), *color as category* (within a group, hue = dispute type), and *presence as quantity* (each square = exactly one case). The marking of recurring cases with a white dot adds a binary overlay without requiring a separate visualization.

**Rules of the layout**: The grid is strictly ordered — squares are packed left-to-right, top-to-bottom within each group. The fixed cell size means that visual area is perfectly proportional to case count (unlike a bar chart, where width is arbitrary). The 50-column layout width is a design choice that balances density against readability.

**Cognitive design**: This is the most Tufte-esque visualization in the entire set — maximum data-ink ratio, zero chartjunk, no aggregation. Tufte's principle of *small multiples* is applied at the individual-case level. The 309 orange squares in the Editor Disputes block create an overwhelming visual mass that no bar chart or percentage could match — you *see* the imbalance by sheer volume of ink. The cognitive load is minimal: count squares, compare blocks, notice the dots.

**Key insight**: The chart makes **the Editor Disputes dominance viscerally felt** rather than intellectually understood. The massive orange block dwarfing all other categories is an immediate preattentive pop-out. The white dots reveal that recurring cases are scattered throughout Editor Disputes and Geopolitics but nearly absent from Procedural and Science & Medicine.

### Visualization 9: Drilling Into the Hierarchy (Zoomable Sunburst)

**Technique**: A sunburst (radial partition) diagram with three concentric rings: inner = category, middle = dispute type, outer = complexity. Arc length (angular extent) encodes case count. Clicking any segment zooms to show only its descendants, re-proportioning the arcs to fill the full 360°. The center displays the count and label of the currently focused node.

**How it works**: The sunburst uses `d3.partition()` to lay out a hierarchy on a radial basis. Each level of the hierarchy gets a concentric ring, with the innermost ring showing the coarsest grouping (category) and the outermost ring showing the finest (complexity). The angular extent of each arc is proportional to the number of cases in that segment of the hierarchy. Clicking a segment triggers an animated transition that zooms into that subtree, making it fill the full circle.

**Encoding strategy**: The sunburst combines the treemap's *part-to-whole area encoding* with a radial layout that naturally suggests hierarchical depth — inner = broader grouping, outer = finer detail. The zoom interaction lets the reader smoothly transition between overview (all 481 cases) and detail (just the 17 Science & Medicine cases) without losing spatial context.

**Rules of the layout**: The radial partition enforces that all arcs at the same depth occupy the same ring width, making depth comparisons fair. Angular extent is strictly proportional to case count at every level. The layout is deterministic — the same data always produces the same chart. The zoom animation preserves angular relationships (segments shrink or expand but don't jump positions), which maintains spatial memory across transitions.

**Cognitive design**: The concentric ring structure leverages the *nested container* mental model: the inner ring "contains" the middle ring, which "contains" the outer ring. This maps naturally to the hierarchical data structure (a category contains dispute types, which contain complexity levels). The zoom interaction adds *progressive disclosure* — the initial view delivers the overview, and clicks reveal detail on demand. The breadcrumb trail above the chart provides a textual anchor during navigation.

**Key insight**: The sunburst reveals that **within the Editor Disputes category, the Conduct type completely dominates** — when you zoom into Editor Disputes, the Conduct arc fills nearly the entire ring. By contrast, zooming into Geopolitics reveals a more balanced split between Content and Conduct, with a notable Complex/Very Complex presence in the outer ring. The zoom lets the analyst compare the *internal composition* of each category, something the treemap showed only at the aggregate level.

---

## Cross-Comparison: All Nine Visualizations

| # | Technique | Spatial Logic | What It Shows Best | What It Hides |
|---|-----------|--------------|-------------------|---------------|
| 1 | Sankey | Left→right pipeline | Flow volume & filtration | Network topology, individual cases |
| 2 | Treemap | Space-filling area | Part-to-whole composition | Time, process, individuals |
| 3 | Heatmap | Grid matrix | Cross-dimensional rates | Volume reliability, relationships |
| 4 | DAG | Network graph | System topology & parallelism | Individual cases, time |
| 5 | Beeswarm | Force-packed strips | Every individual case | Precise counts, relationships |
| 6 | Radial | Polar burst | Recurrence families & depth | Non-recurring cases, volume |
| 7 | Parallel Coordinates | Multi-axis polylines | Multivariate co-occurrence | Density (overplotting), hierarchy |
| 8 | Unit / Waffle | Grid of individual squares | Exact counts, magnitude | Relationships, process, time |
| 9 | Sunburst | Concentric radial rings | Hierarchical drill-down | Precise comparison, flat views |

---

## Tools and Process

- **Data preparation**: Python script (`scripts/prepare_data.py`) that reads the raw `arb_cases.txt` file from the Wikipedia Arbitration project, classifies each case by topic category and dispute type using keyword rules, and outputs structured JSON.
- **Visualization**: D3.js v7 with the `d3-sankey` plugin. All three visualizations are rendered client-side in a single HTML file (`viz/index.html`).
- **Dataset**: 481 Wikipedia Arbitration Committee case names from the project's artifact archive, supplemented by the dispute resolution lifecycle model from the project documentation.

---

## Files

| File | Description |
|------|-------------|
| `viz/index.html` | Interactive D3 visualizations 1–3 (Sankey, Treemap, Heatmap) |
| `viz/extended.html` | Interactive D3 visualizations 4–6 (DAG, Beeswarm, Radial Burst) |
| `viz/experimental.html` | Interactive D3 visualizations 7–9 (Parallel Coordinates, Unit Chart, Sunburst) |
| `data/arb_cases_classified.json` | Classified case data (JSON) |
| `scripts/prepare_data.py` | Data preparation script |
| `writeup.md` | This analysis document |
