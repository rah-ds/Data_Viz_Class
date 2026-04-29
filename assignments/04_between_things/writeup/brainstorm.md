# Brainstorm — "Between Things" Spotify Visualization

> "I do not paint things, I paint only the differences between things." — Matisse

The assignment asks for a **single, fully developed, static visualization** that uses spatial/visual structure as an *analytic strategy* — not just a chart, but a way of *seeing into* the data. The goal is to expose relationships, not summarize statistics.

Below: ideas organized from strongest (most "between things") to more exploratory.

---

## Tier 1 — High-potential concepts (relationships *between* listeners)

### 1. Sonic Fingerprints — Comparative Radar Overlays
**What:** Small-multiple polar/radar charts — one per person — of their mean audio profile (danceability, energy, valence, acousticness, speechiness, instrumentalness, liveness). Overlay all 14 on a single large chart, or use small multiples with a shared "average" silhouette underneath.  
**Why it works:** Immediately shows *shape* of taste — who skews acoustic vs. energetic, happy vs. dark. The *differences between shapes* are the story.  
**Spatial strategy:** Layered radial geometry turns 7 dimensions into a recognizable silhouette. Distance from the group mean = uniqueness.  
**Refinement idea:** Weight by listening time (not just track count) so heavy-rotation tracks dominate the shape. Highlight the person who is most different from the group centroid.

### 2. Mood Space Map — Energy × Valence Landscape
**What:** Plot every stream on a 2D energy × valence plane. Use density/contours (not just points) per person to show where each listener *lives* in mood space. Overlay contour lines like a topographic map.  
**Why it works:** Energy × valence is a well-known "mood quadrant" (happy/energetic, sad/calm, angry/turbulent, peaceful). By mapping density rather than individual points, you get a landscape — each person's territory in emotional space. The **overlap and gaps** between territories are the insight.  
**Spatial strategy:** Contour density maps with transparency. Show all 14 contours overlaid, or small multiples with a shared grid. Annotate the "no-man's-land" between clusters — what moods does nobody listen to?  
**Refinement idea:** Size or opacity by msPlayed. Draw arrows from each person's centroid to the group centroid. Label the "most unique mood zones."

### 3. Taste Distance Network — Who Sounds Like Whom?
**What:** Compute euclidean (or cosine) distance between each pair of listeners based on their mean audio feature vectors. Draw a network/graph where persons are nodes and edge weight = similarity (thicker = more similar taste). Use force-directed layout so similar listeners pull close together.  
**Why it works:** Directly visualizes the *space between* listeners. You see clusters of like-minded people and outliers. This IS "painting the differences."  
**Spatial strategy:** Force-directed or MDS (multidimensional scaling) layout of the distance matrix. Node size = total listening time. Color = dominant genre.  
**Refinement idea:** Layer in a second distance metric — shared artists (Jaccard overlap) — as a second edge type. Show where feature-similarity agrees/disagrees with artist-similarity. Are some people feature-similar but artist-different (parallel taste, different discovery)?

### 4. Temporal Rhythms — When Do You Listen?
**What:** 24-hour × 7-day heatmap per person (small multiples), showing stream density by hour and day of week. Alternatively, a radial clock visualization.  
**Why it works:** Listening time *is* behavior. Night owls, morning commuters, weekend bingers — these patterns define the person as much as what they listen to. The differences between temporal patterns say something distinct from audio features.  
**Spatial strategy:** Polar/clock layout (24 hours around a circle, days as rings) makes the cyclical nature visible. Or use a strip chart: each person is a row, 168 columns (hours in a week), colored by intensity.  
**Refinement idea:** Overlay average audio features *per time slot* — does someone listen to calm music in the morning and energetic at night? The mood × time intersection is rich.

---

## Tier 2 — Strong supporting concepts

### 5. Artist Loyalty Spectrum — Depth vs. Breadth
**What:** For each person, compute a concentration metric (e.g., Herfindahl index or % of listening from top-5 artists). Plot as a single axis from "loyalist" (few artists, deep listening) to "explorer" (many artists, shallow). Then for each person, fan out their top artists as branches.  
**Why it works:** This is about listening *strategy* — not what, but how. Some students binge one artist; others skim the catalog. The structure of attention is the story.  
**Spatial strategy:** Dendrogram or tree structure branching from each person. Width of branch = time spent. Deep narrow trees = loyalists; wide shallow = explorers.  
**Extraction:** Who are the loyalists? What artists capture that loyalty? Is there a relationship between loyalty and genre or mood?

### 6. Popularity Gradient — Mainstream ↔ Underground
**What:** For each person, plot the distribution of their track popularity scores (0-100) as ridgeline plots or stacked density curves. Sort persons from most mainstream to most obscure.  
**Why it works:** Track popularity is a proxy for cultural centrality. The *spread* (not just center) tells you if someone mixes hits with deep cuts or stays in one lane.  
**Spatial strategy:** Ridgeline (joy plot) — stacked KDE curves sorted by mean popularity. Shows both position and spread. The overlap between curves = shared mainstream core.  
**Extraction:** Who are the outliers? Is there a bimodal listener who has both very popular and very obscure tracks?

### 7. Genre Bridges — Artists That Connect Worlds
**What:** Many artists are tagged with multiple genres. Build a bipartite graph: genres on one side, artists on the other, edges = membership. Weight by total stream time. Show which genres are close (connected through shared artists) and which are isolated.  
**Why it works:** Genres are social constructs; the boundaries are interesting. Artists that span genres are *bridges* — they sit "between things."  
**Spatial strategy:** Force-directed bipartite layout, or a chord diagram showing genre-to-genre co-occurrence (how often the same artist is in both).  
**Extraction:** What genre combinations are common? Which are rare and surprising?

### 8. Shared vs. Unique — The Venn of Taste
**What:** Categorize each artist (or track) as: shared by almost everyone (universal), shared by a few, or unique to one person. Visualize as concentric rings or zones: center = universal, edges = personal.  
**Why it works:** The "between" here is between common and personal. What makes you *you* in this group?  
**Spatial strategy:** Target/bullseye diagram. Or: one ring per person, with arcs colored by artist, and connecting lines for shared artists (chord diagram).  
**Extraction:** What % of your listening is shared with others? Who is most unique?

---

## Tier 3 — Experimental / niche ideas

### 9. Listening Arc — Mood Over Time
For each person, plot a time-series of rolling-average valence (or energy) across their streaming history. Does their mood drift? Are there seasonal patterns? Do exam periods show up as shifts?  
**Spatial approach:** Sparkline-style small multiples. Annotate with external events (exam weeks, holidays).

### 10. Danceability × Tempo × Energy 3D Landscape
A 3D scatter or projected 2D hexbin of danceability, tempo, and energy. Each hexbin colored by dominant genre. Shows the "physics" of the music.  
**Spatial approach:** Hexbin density with genre-labeled clusters.

### 11. Explicit Content Map
What fraction of each person's listening is explicit tracks? Cross-reference with genre and time-of-day. Is explicit content more common at night?  
**Spatial approach:** Small-multiple bar charts or a single stacked bar, sorted by explicit ratio.

### 12. The Skip Pattern — Short Plays as Signal
Many `msPlayed` values are very short (< 30 seconds = likely skips). Map skip rate per person, per artist, per hour. Who gives up on songs? When?  
**Spatial approach:** Strip chart with each stream as a dot, y-axis = msPlayed, colored by skip/complete threshold. Show the "skip floor."

### 13. Album vs. Single Culture
Using `album.type` and `album.total_tracks`, distinguish album-listening from single-track cherry-picking. Who listens to albums front-to-back?  
**Spatial approach:** Sort by album completion rate. Show sequential track numbers listened per album as a "staircase" — complete albums make full stairs.

### 14. Playlist Composition DNA
Each person's playlists as a horizontal bar, subdivided by genre proportion. Compare playlist structures side by side.  
**Spatial approach:** Stacked bar chart or Marimekko chart. Width = playlist size, color blocks = genre.

### 15. Follower × Listening Asymmetry
Cross-reference `Follow_counts` with listening intensity. Do social listeners (many followers/following) listen differently than solo listeners?  
**Spatial approach:** Bubble chart — x=followers, y=total_hours, size=unique_artists, color=mean_valence.

---

## What the EDA Revealed (summary from eda.ipynb)

| Signal | What it showed |
|--------|---------------|
| **Audio feature correlations** | Energy↔loudness strong positive; acousticness↔energy strong negative. Valence somewhat independent — good axis. |
| **Per-person profiles** | Real, visible differences in radar shapes. Some are very acoustic-heavy, others very energetic. |
| **Mood space centroids** | Persons cluster mostly in the high-energy, mid-valence zone but with genuine spread. |
| **Temporal patterns** | Different peak-listening hours across persons. Some are clearly night listeners. |
| **Popularity distributions** | Wide range — some persons average 50+ popularity, others ~30. Genuine personality here. |
| **Shared artists** | Some pairs share 200+ artists; others share <20. The overlap structure is non-trivial. |
| **Taste distance** | Euclidean distance on feature means shows clear clusters AND outliers. |

---

## My Top 3 Picks (to develop into a final static visualization)

1. **Mood Space Topography** (#2) — The energy × valence density contour map is spatially rich, analytically clear, and deeply "between things." Each person's mood territory has borders, and the spaces between them are meaningful.

2. **Taste Distance Network** (#3) — Force-directed layout of listener similarity makes the abstract concrete. Could be refined in Illustrator with thoughtful annotation.

3. **Sonic Fingerprints** (#1) — The radar overlay is visually striking and immediately readable. The challenge is making 14 layers legible — may need to cluster or highlight extremes.

---

## Tools to Consider
- **Tableau / RAWGraphs** for initial spatial layouts
- **Illustrator / Inkscape** for refinement, annotation, labeling
- **D3.js / Observable** if interactive exploration helps find the right static frame
- **Python (matplotlib/seaborn)** for analytic exploration (this notebook)
- **Figma** for layout polish

## What NOT to do (per assignment)
- Don't just dump a statistical summary to screen
- Don't let the tool drive — be intentional about spatial decisions
- Don't try to show everything — pick one focused question
- Don't posterize — use density, range, and texture as richness
