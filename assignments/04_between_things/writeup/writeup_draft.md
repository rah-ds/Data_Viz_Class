```yaml
name: Ryan Healy
userid: rah5ff
Semester: Spring 2026
assignment: In Between Things
```


# Objective

Write up on the [Spotify dataset](https://canvas.its.virginia.edu/courses/162865/files/18466068/download?download_frd=1).

## Question
>What is your question?  What do you want to know?  What measures, orders, benchmarks, intersections, or contradictions might you organize around?

**Do musical keys have audible personalities, and can we see them?**

Spotify's Audio Features API assigns every track a key (0 = C through 11 = B) based on the [chromatic scale](https://en.wikipedia.org/wiki/Chromatic_scale), the 12 semitone steps that make up one octave on a piano. Each step multiplies the frequency by the twelfth root of two (≈ 1.0595), so after 12 steps the frequency doubles exactly. On the chart, the octave runs from C4 (261.6 Hz) to B4 (493.9 Hz), the octave starting at middle C.

This is a natural physical ordering, not an arbitrary one. I wanted to lay out the 12 keys along this scale and ask: *does the music people actually stream in each key differ on Spotify's seven audio features?* If so, how? Are certain keys consistently more acoustic, more danceable, more energetic than others, or is it all noise?

The seven features I compare are danceability, energy, speechiness, acousticness, instrumentalness, liveness, and [valence](https://en.wikipedia.org/wiki/Valence_(psychology)), all floats on [0, 1] from the Spotify Audio Features API. The data spans roughly 266,000 music streams across 14 listeners (2019–2025), joined to track-level audio features via the track URI. For each key I compute the mean of each feature across all streams, then compare keys against the overall median using a robust z-score (median + [MAD × 1.4826](https://en.wikipedia.org/wiki/Median_absolute_deviation)) to identify significant deviations.

The organizing principle is a **benchmark comparison**: the median across all 12 keys is the baseline, and the question is which keys deviate from it, on which features, and by how much. The physical ordering of the chromatic scale (Hz) gives the layout its backbone, while the z-score gives the analytical threshold.

## Strategy
>What is your visual / organizational strategy?  

The visualization, titled *Chromatic Personalities*, uses three interlocking spatial structures:

**1. Piano keyboard as an index.** Across the top, a literal piano keyboard spans one octave (C4–B4), with white keys for the natural notes and black keys for the sharps/flats. Each key is colored by its assigned "personality" label, indicating the audio feature that deviates most above the median. This gives the viewer an immediate chromatic map: which keys cluster together, which stand alone. The keyboard serves double-duty as a navigational element (click to isolate) and a spatial legend.

**2. Grouped small-multiple [radar charts](https://en.wikipedia.org/wiki/Radar_chart).** Below the keyboard, each of the 12 keys gets a card with a 7-axis radar showing its audio-feature profile. Instead of laying the cards out in chromatic order (which would scatter visually similar keys), they are *grouped by personality*: all "Groover" keys (high danceability) sit together, all "Powerhouse" keys (high energy) sit together, and so on. Within each group, cards are sorted by pitch (ascending Hz). This dual sort (first by analytic category, then by physical frequency) lets the eye compare shape *within* a personality and contrast shape *between* personalities.

Each radar overlays two polygons:
- A **dashed grey median polygon**, the benchmark across all 12 keys.
- A **colored data polygon**, this key's actual profile, filled with the personality's color.

Where the colored polygon exceeds the grey one, the key is above median on that feature. Significant deviations (|z| ≥ 1) are marked with filled dots (above) or ring dots (below); non-significant points are dimmed. This encoding means the viewer does not have to read axis values; the *shape difference* between the two polygons is the signal.

**3. Personality labels as semantic anchors.** Rather than showing raw feature names, each key receives a human-readable label (*The Groover*, *The Powerhouse*, *The Unplugged*, etc.) based on its dominant feature. These labels are defined from the data dictionary:

| Label | Dominant Feature | Interpretation (from Spotify) |
|-------|-----------------|-------------------------------|
| The Unplugged | Acousticness | Acoustic instruments, less electronic production |
| The Groover | Danceability | Steady beat, groove-friendly rhythms |
| The Powerhouse | Energy | Loud, fast, dense, noisy |
| The Silent Type | Instrumentalness | No vocals: ambient, classical, lo-fi |
| The Stage Lover | Liveness | Live performance, audience noise, stage energy |
| The Storyteller | Speechiness | Spoken or rapped content, word-heavy |
| The Optimist | Valence | Happy, cheerful, euphoric |

Keys where no feature exceeds z = 1 are grouped as *Uncategorized* because they sit near the median on everything. A glossary table at the bottom of the visualization defines each label so the chart is self-contained.

**Additional detail layers:**
- **Representative song**: rather than just showing the most-played track per key, the script selects the most-played track (among the top 20) that *scores highest on the key's dominant feature*, so the example genuinely reflects the personality.
- **Sig-tags**: small pill badges below each radar call out which features are significantly above (+) or below (−) median, providing a textual summary alongside the visual one.
- **Tooltip on hover** (in the interactive version): exact feature values, z-scores, and stream counts.

The color palette uses seven hues spaced ≈ 51° apart on the color wheel for maximum perceptual contrast, set against a dark (#0d1117) background.

## So What?
>Extract.  So what?  

Musical keys are not neutral containers, at least not in this dataset.

The most striking finding is that **keys cluster into recognizable personalities**, and the clusters are not random. The chart reveals that:

- **Instrumentalness dominates certain "sharp" keys.** C♯/D♭, F♯/G♭, G♯/A♭, D♯/E♭, and A♯/B♭ (all sharps/flats) are assigned *The Silent Type*. This could reflect that instrumental and ambient music (film scores, lo-fi beats, classical piano) is disproportionately composed in these keys. The enharmonic/sharp keys are less common in pop songwriting but prevalent in instrumental composition, which would pull their instrumentalness average above the median.

- **Danceability concentrates in G, E, and A**, all common guitar keys. These are among the most popular keys in pop and dance music, which could explain the elevated groove factor.

- **Liveness clusters in D, F, and A♯/B♭.** The "Stage Lover" label appears for keys associated with live recordings and concert staples.

- **No key received the Storyteller (speechiness) or Unplugged (acousticness) label in the primary grouping**, suggesting that those features do not vary enough across keys to cross the z = 1 threshold consistently. Speech and acoustic content appear more evenly distributed than energy or instrumentalness.

- **The Uncategorized keys are the "average" keys.** They sit near the median on every dimension, meaning they have no distinguishing audio personality. These are the "vanilla" keys that host the broadest mix of content.

The benchmark comparison makes the "so what" visually immediate: if a key's colored polygon is nearly identical to the grey median polygon, there's nothing interesting to say about it. The moment the polygons diverge, the deviation jumps out. The grouping-by-personality layout means the viewer does not have to hunt for patterns because they are pre-sorted.

One deeper implication: **key choice is not independent of musical style.** Composers and producers tend to write certain *kinds* of music in certain keys, whether for physical reasons (guitar tunings favor E, A, G; piano pieces often sit in C, F, B♭) or cultural convention. This visualization makes that latent structure visible through the lens of 266,000 real listening events.

## What would you change?

If I were to iterate further:

1. **Weight by listening time, not stream count.** Currently each stream counts equally regardless of `msPlayed`. A 5-second skip and a full 4-minute listen contribute the same to the key's feature average. Weighting by `msPlayed` would better reflect what listeners actually *heard*, not just what they clicked on. Streams under 30 seconds (likely skips) could be excluded entirely.

2. **Separate listeners.** The current chart aggregates all 14 listeners. A natural extension would be small multiples *per person* — do individual listeners show the same key-personality patterns, or is the pattern an artifact of aggregation? If Person 3's heavy rotation of instrumental hip-hop in C♯ is driving the "Silent Type" label, that's a different story than if all 14 listeners independently skew instrumental in that key.

3. **Test for statistical significance more rigorously.** The z = 1 threshold is a reasonable heuristic, but a formal [permutation test](https://en.wikipedia.org/wiki/Permutation_test) or bootstrap confidence interval would give stronger evidence that the deviations are not just noise from unequal sample sizes across keys.

4. **Add a second octave or mode dimension.** The chart only shows one octave and ignores [mode](https://en.wikipedia.org/wiki/Mode_(music)) (major vs. minor). Since each key can be played in either mode, splitting into 24 categories (12 keys × 2 modes) might reveal that the major/minor distinction, not the pitch class, is what actually drives the personality differences. Minor keys are famously associated with sadness (low valence), and major keys with brightness (high valence).

5. **Explore causality vs. convention.** Is C♯ "The Silent Type" because something about that pitch naturally encourages instrumental music, or because cultural songwriting conventions happen to cluster instrumental genres there? A cross-dataset comparison (e.g., against the [Million Song Dataset](https://en.wikipedia.org/wiki/Million_Song_Dataset) or a classical music corpus) could help distinguish physical acoustics from cultural habit.

6. **Refine the representative song selection.** The current approach picks the highest-scoring track among the top 20 by play count. An alternative would be to pick the track closest to the *centroid* of the key's feature vector, selecting the most "typical" song rather than the most extreme.