# Chart 31: Key Signatures — Deviations from Median

## Reading the Chart

### n (Sample Size)

Each radar cell displays **n = X,XXX**, which is the total number of individual music streams that fell into that musical key across all 14 listeners in the dataset. This is the sample size behind each key's averaged audio features. Larger n values mean the averages are more stable and representative; smaller n values mean the profile could be more influenced by a handful of heavily-replayed tracks. For context, the dataset contains roughly 266,000 total music streams.

### Hz (Hertz) — Frequency

**Hz** stands for **Hertz**, the unit of frequency — the number of sound wave cycles per second. Every musical note corresponds to a specific frequency:

| Note | Frequency |
|------|-----------|
| C    | 261.6 Hz  |
| D    | 293.7 Hz  |
| E    | 329.6 Hz  |
| A    | 440.0 Hz  |
| B    | 493.9 Hz  |

A higher Hz value means a higher-pitched note. The standard tuning reference is **A = 440 Hz** — this is the A above middle C, the note orchestras tune to. Each frequency shown on the piano keyboard and radar cells tells you the exact pitch of that key in the fourth octave (the octave starting at middle C).

### The Chromatic Scale

The **chromatic scale** contains all 12 notes in Western music, each separated by a **semitone** (half step) — the smallest interval on a standard piano. Starting from C and going up:

```
C → C♯/D♭ → D → D♯/E♭ → E → F → F♯/G♭ → G → G♯/A♭ → A → A♯/B♭ → B → (C again, one octave higher)
```

**Why the double names?** Notes like C♯/D♭ have two names because of **enharmonic equivalence** — C♯ ("C sharp", raised a half step from C) and D♭ ("D flat", lowered a half step from D) are the same pitch. Which name is used depends on the musical context.

**White vs. black keys on the piano:** The keyboard at the top of the chart mirrors a real piano. The 7 white keys (C, D, E, F, G, A, B) form the C major scale — the simplest scale with no sharps or flats. The 5 black keys (C♯, D♯, F♯, G♯, A♯) fill in the gaps, completing the chromatic scale to 12 notes.

**Frequency relationship:** Each step up the chromatic scale multiplies the frequency by approximately **1.0595** (the twelfth root of 2). After 12 semitones you've exactly doubled the frequency, which is one octave. This is why the chart spans C4 (261.6 Hz) to B4 (493.9 Hz) — one full octave.

### How the Personality Labels Work

Each key's radar shows the average value of 7 Spotify audio features (acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence) for all streams in that key.

The dashed grey polygon is the **median** across all 12 keys. For each key, we compute a **robust z-score** using the median and MAD (median absolute deviation) for each feature. If the highest z-score exceeds 1.0, that feature becomes the key's "personality." If no feature deviates significantly, the key is labeled **Uncategorized**.

The **representative song** shown under each radar is not simply the most-played track in that key — it's the most-played track (among the top 20) that actually scores highest on the key's dominant audio feature, so the example genuinely reflects the personality label.
