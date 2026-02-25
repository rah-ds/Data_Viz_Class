```yaml
name: Ryan Healy
userid: rah5ff
semester: Spring 2026
```

# Visual Data Analysis

This is assignment 3 for the semester, with [instructions here](https://canvas.its.virginia.edu/courses/162865/assignments/816728).


>There are two foci for this assignment:
>1) To explore and test out different approaches and techniques toward visual structure, differentiation, encoding, and analysis that are out there amidst available tools.  There are some novel approaches here.  Try them.
>2) To use these techniques to critically analyze graphical, structural, organizational, and representational approaches for their strengths and weaknesses at gaining insight into information.

The SVGs are in document and also will attach so easy to see.

## Table of Contents
- [Visual Data Analysis](#visual-data-analysis)
  - [Table of Contents](#table-of-contents)
  - [The Data](#the-data)
  - [The Connecting Question](#the-connecting-question)
  - [Figure 1 - The Wikipedia Escalation Funnel](#figure-1---the-wikipedia-escalation-funnel)
    - [How It Works](#how-it-works)
    - [What It Hides](#what-it-hides)
    - [Why I like it](#why-i-like-it)
  - [Figure 2 - The Anatomy of the Dispute Lifecyle](#figure-2---the-anatomy-of-the-dispute-lifecyle)
    - [How It Works](#how-it-works-1)
    - [What It Hides](#what-it-hides-1)
    - [Why I like it](#why-i-like-it-1)
  - [Figure 3 - The Disputes That Won't Die (Reoccurance)](#figure-3---the-disputes-that-wont-die-reoccurance)
    - [How It Works](#how-it-works-2)
    - [What it Hides](#what-it-hides-2)
    - [Why I like it](#why-i-like-it-2)
  - [Some other improvements](#some-other-improvements)


 

**Sorry, for the delay in getting this assignment out.**

## The Data

The data is from my [Capstone](https://github.com/rah-ds/Wikipedia_Dispute_Models). Anyone can run my code, just like anyone can edit Wikipedia. 

While anyone can edit Wikipedia and there is an escalating pathway to disolve disputes. The final and highest level for English Wikipedia is Arbitration, which is settled by its namesake committee. Wikipedia's Arbitration Committee (ArbCom) is the elected body that serves as the "court of last resort" for the English-language Wikipedia. Cases arrive at ArbCom only after lower-level dispute resolution mechanisms (talk pages, third opinions, mediation, admin intervention) have failed. This makes the ArbCom case archive a revealing dataset. It is a catalogue of failures of consensus, the places where Wikipedia's open-editing model could not self-heal.

The dataset is Wikipedia Arbitration Committee (ArbCom) case archive with 481 named cases, classified by topic category, dispute type (content vs. conduct), complexity, and recurrence. 

 Broadly, what we are trying to do is take all the [Wikipedia Arbitration cases](https://en.wikipedia.org/wiki/Category:Wikipedia_arbitration_cases) and map them their path to arbititration.



---

## The Connecting Question

What kinds of disputes reach Wikipedia's final authority, and what does the pattern of escalation reveal about where the collaborative encyclopedia model breaks down?

By classifying all 481 ArbCom case names by topic category, dispute type, case complexity, and recurrence (zombie cases that returned for a second or third round), I ask one question. Where does Wikipedia's graduated dispute resolution system fail, and why? Can we see it graphically? 

I played with and built three D3.js visualizations, each using a fundamentally different spatial and encoding strategy, then exported and refined the following SVGs. Each figure below is followed by a direct critique of what the technique reveals, what it hides, and how the rules of layout shape understanding.

---

## Figure 1 - The Wikipedia Escalation Funnel

**Figure 1** : A [Sankey (Alluvial) Diagram](https://en.wikipedia.org/wiki/Sankey_diagram) How disputes flow and filter through Wikipedia's six-stage graduated resolution system.

* **Insight:** The vast majority of Wikipedia disputes never reach ArbCom. The system filters aggressively at every stage, and the tapering flow makes this visible at a glance before a single label is read.

![Escalation Funnel](viz/zz_final/escalation_funnel.svg)

### How It Works

This is a Sankey (or alluvial) diagram mapping dispute flow through Wikipedia's resolution pipeline. We start at the talk page of Wikipedia then flow through. Left is informal and low-authority; right is formal and binding. 

The vertical thickness of each flow band encodes the volume of disputes traveling that pathway. Color is inherited from the source node, creating visual continuity as flows merge, split, and taper across stages.

This is a flow-and-funnel representation. The layout enforces a strict left-to-right reading order that maps directly to the temporal and authority gradient of Wikipedia's dispute resolution system.

Reading the chart left to right is the same cognitive motion as following a case through escalation. The leftward width of the Talk Page node, which receives all disputes, versus the narrow band reaching ArbCom creates a visual metaphor for filtration. The eye naturally follows the diminishing flow and registers "most disputes don't make it this far" before any text is read.

The chart structurally prevents showing anything other than flow and volume. It cannot show time within a stage, individual cases, or case-level characteristics.


### What It Hides

The Sankey hides heterogeneity. All disputes are aggregated into flow volumes. You cannot see that a Geopolitics case behaves differently from a Religion case within the same flow band.

It also hides the topology of the system. Third Opinion and RfC appear as sequential nodes on the same horizontal tier, but they are actually parallel pathways at the same authority level. The *left-to-right * pipeline rule flattens the system's graph structure into a single ordered sequence. The lifecycle data is also partially modeled rather than observed *case-by-case*, which means the flows represent a structural inference rather than traced case histories. Perhaps most importantly, the Sankey hides time. It cannot show whether the composition of disputes reaching ArbCom has shifted across the decades Wikipedia has operated.

The pipeline metaphor is powerful but constraining. Disputes can skip stages, loop back, or run simultaneously across multiple venues. The Sankey cannot represent any of that without losing its core legibility. A natural next step would be to add a temporal overlay. Encoding node color or width by year-range would reveal whether the proportions are stable or shifting. Pairing this chart with a network view (as in [Figure 2](#figure-2---the-anatomy-of-the-dispute-lifecyle)) addresses the topology problem directly. The two views are genuinely complementary, not redundant.

### Why I like it 

The tapering is emotionally legible. I feeling of the flow is persuasive and visible in a way that a table wouldn't be. 

---

## Figure 2 - The Anatomy of the Dispute Lifecyle

**Figure 2**:  A [Directed Acyclic Graph (DAG)](https://en.wikipedia.org/wiki/Directed_acyclic_graph) that shows the dispute resolution lifecycle rendered as a network, revealing parallelism, branching, and authority levels.

> **Insight:** Wikipedia's dispute system is not a pipeline but a branching network.

![Dispute Resolution DAG](viz/zz_final/proper_dag.svg)

### How It Works

This is a hand-positioned directed acyclic graph (DAG) where nodes represent resolution stages and directed edges represent valid escalation pathways. Node radius encodes throughput, meaning total disputes flowing through that stage. Edge thickness encodes flow volume. Subtle column bands in the background indicate authority level (Informal, Community, Mediation, Admin, Arbitration, Outcome), creating a geographic metaphor for institutional escalation. Arrowhead markers make directionality explicit on every edge.

The DAG uses position as its primary structural channel. Nodes at the same horizontal column are at the same institutional authority level. The viewer can compare laterally without any decoding step. The concentric throughput encoding (larger nodes = more traffic) creates a preattentive "mass" impression, you immediately register that Talk Page and Resolved are the heaviest nodes. The arrowheads do work that the Sankey's left-to-right flow only implied. Directionality is now explicit, readable at a glance even on edges that run at oblique angles.

The column band background applies the [Gestalt law of common region](https://en.wikipedia.org/wiki/Principles_of_grouping#Common_region). Nodes sharing a band are grouped by that shared background, reducing the need to read axis labels to understand which tier a node belongs to. This is chunking applied spatially. The brain parses the diagram as a sequence of zones, not as an undifferentiated scatter of circles.

The manual positioning is the key design decision here. Unlike a force-directed layout that would optimize for aesthetic properties (edge crossing minimization, uniform spacing), this layout was editorially determined to enforce the authority-level columns.

The column banding is a strong cognitive scaffold. It converts an abstract graph into something that reads more like an organizational chart with geographic authority zones. This is precisely where the DAG outperforms the Sankey. By making the system's topology the visual object rather than its flow volumes, it enables a different analytical question ("what paths exist?") rather than only ("how much flows through each path?"). Used together, [Figure 1](#figure-1---the-wikipedia-escalation-funnel) and [Figure 2](#figure-2---the-anatomy-of-the-dispute-lifecyle) are genuinely complementary. [Figure 1](#figure-1---the-wikipedia-escalation-funnel) shows the quantity, [Figure 2](#figure-2---the-anatomy-of-the-dispute-lifecyle) shows the structure.

The DAG reveals topology that the Sankey collapsed. Third Opinion (3O) and Request for Comment (RfC) are parallel, not sequential. Both sit at the same authority tier. Dispute Resolution Noticeboard (DRN) can feed both ANI *and* ArbCom directly, not only via ANI as the Sankey implied. Talk Pages can short-circuit to ANI when conduct violations are immediate. These are structural features of the system, not edge cases, and none of them are visible in [Figure 1](#figure-1---the-wikipedia-escalation-funnel). The difference between "a pipeline" and "a network with branching and parallelism" is not a cosmetic distinction. It changes the diagnosis of where and why the system fails.

### What It Hides

The editorial nature of the positioning means the layout cannot scale or adapt. It hides case-level detail entirely. All disputes are abstracted into node throughput and edge volume. It cannot show time, cannot distinguish categories within a flow, and cannot reveal whether specific edge pathways are more or less common for certain dispute types. The DAG also implies that the system operates in a clean directed-acyclic fashion, when in practice disputes can loop, be reopened, or run on multiple tracks simultaneously. The "acyclic" constraint is an abstraction.

A small-multiples version showing the same DAG structure for different time periods would address the temporal blindspot. 

### Why I like it

This rewards a second look. The first chart gives you the flow at a glance and this really reveals some of the exceptions in the process.

---

## Figure 3 - The Disputes That Won't Die (Reoccurance)

**Figure 3**: A [Radial Burst (Polar Spoke Chart)](https://en.wikipedia.org/wiki/Pie_chart#Polar_area_diagram0) where every recurring case family rendered as a spoke, grouped by topic category, with spoke length encoding depth of recurrence.

> **Insight:** Recurrence is concentrated, not spread evenly. Editor Disputes produces the most recurring families by count, but Geopolitics produces the deepest reoccurance. Palestine-Israel articles returned five times, the longest spoke in the chart.

![Recurring Case Families](viz/zz_final/reoccuring_cases.svg)


### How It Works

This is a radial layout centered on a hub, with spokes radiating outward, one per recurring case family. Each family is a dispute that returned to ArbCom for at least one sequel (e.g., "Rex071404" with 4 hearings, "Palestine-Israel articles" with 5 hearings). Spokes are grouped into angular sectors by topic category. Spoke length encodes the maximum recurrence number. Dots along each spoke mark individual hearings. Filled dots indicate a case exists at that depth; the spoke extends to the maximum hearing number for that family. Concentric reference circles at 1×, 2×, 3×, 4×, and 5× provide a calibrated ruler for reading depth.

This is the only visualization in the set that focuses exclusively on recurrence, the failure of finality. It answers a question neither [Figure 1](#figure-1---the-wikipedia-escalation-funnel) nor [Figure 2](#figure-2---the-anatomy-of-the-dispute-lifecyle) can. Not "how does the system work?" but "which specific disputes resisted permanent resolution, and how severely?" The angular grouping by category achieves categorical partitioning without a grid. Sectors function like treemap regions but in polar space, making the visual distribution across categories immediately scannable.

The spoke-and-dot encoding is information-dense in the manner Tufte values. A single spoke conveys the family name, category, number of hearings, and any gaps in the sequence. Spoke length as the primary channel leverages length comparison, one of the most accurate preattentive judgment tasks the visual system can perform. The radial layout adds a magnitude metaphor. Long spokes radiating outward suggest force, tension, unresolved energy. This aligns with the semantic content of the data. These are disputes that could not be contained.

The polar rule forces the viewer to scan angularly. The eye follows the circumference, comparing sector fullness, before drilling into individual spokes. This scanning motion is the opposite of the grid-scanning motion activated by a heatmap, and it naturally integrates categorical and quantitative information, as you scan around the wheel, you simultaneously register "which category" (sector color/position) and "how deep" (spoke length). The reference circles convert the otherwise ambiguous radial extent into a calibrated scale. Without them, the chart would be dramatic but not analytically useful. The circles are the mechanism that makes spoke length a readable quantity rather than just a visual impression.

The chart reveals an asymmetry that neither the flow-based nor the structural views could surface that recurrence is not uniformly distributed. Editor Disputes dominates in raw count of recurring families. The density of spokes in the Editor Disputes sector is immediately visible as the fullest portion of the wheel. But the deepest recurrence belongs to Geopolitics where the Palestine-Israel articles family reaches spoke length 5, the longest single spoke in the chart.

The radial layout sacrifices comparison precision for visual drama. Angular extents are harder to judge than linear lengths, so sector size (which represents the count of recurring families per category) is less accurately readable than it would be in a bar chart. The chart also hides the non-recurring majority. 


### What it Hides

The 400+ cases that went through ArbCom exactly once do not appear at all. by zooming in on recurrence, it achieves depth at the cost of population context. A viewer who only sees [Figure 3](#figure-3---the-disputes-that-wont-die-reoccurance) would not know how large the non-recurring baseline is.

The most direct improvement would be making the sector angular width proportional to the number of cases in each category, not just the number of recurring families. This would reintroduce the population context that the radial form currently discards. 

A second potential improvement, encoding spoke width by dispute type (content vs. conduct) would layer the type dimension onto the recurrence view without requiring a separate chart.

### Why I like it

This was based on a question my sponsor asked directly, and I didn't want to just do a bar chart. This radial layout makes you work a bit for the insight but I like it, the plot has personality.

---

## Some other improvements 

These are off the top of my head but worth putting on paper.

* Add a temporal dimension
* Combine recurrence and volume
* Annotate the SVGs more. I ran out of time a bit but they could really use somre more informative labels in Figure 3 in particular. 