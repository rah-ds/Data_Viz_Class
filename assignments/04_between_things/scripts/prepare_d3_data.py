"""
Prepare JSON data files for D3 visualizations.
Run from the 04_between_things directory:
    python scripts/prepare_d3_data.py
"""
import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import Counter

DATA_DIR = Path("data/spotify_data")
OUT_DIR  = Path("viz/data")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Load CSVs ────────────────────────────────────────────────────────
streaming = pd.read_csv(DATA_DIR / "StreamingHistory_music.csv", low_memory=False)
features  = pd.read_csv(DATA_DIR / "trackFeatures.csv")
tracks    = pd.read_csv(DATA_DIR / "trackInfo.csv", low_memory=False)
artists   = pd.read_csv(DATA_DIR / "artistInfo.csv")
genres    = pd.read_csv(DATA_DIR / "artistInfo_genres.csv")
marquee   = pd.read_csv(DATA_DIR / "Marquee.csv")

# Drop any rows where the header got duplicated into the data
streaming = streaming[streaming["personID"] != "personID"].copy()
streaming["personID"] = streaming["personID"].astype(int)
streaming["msPlayed"] = pd.to_numeric(streaming["msPlayed"], errors="coerce")
streaming["endTime"] = pd.to_datetime(streaming["endTime_UTC"], errors="coerce")
streaming["min_played"] = streaming["msPlayed"] / 60_000
streaming["hour"] = streaming["endTime"].dt.hour
streaming["dow"]  = streaming["endTime"].dt.dayofweek
streaming["month"] = streaming["endTime"].dt.to_period("M").astype(str)

# Enriched: streaming + features + track info
enriched = streaming.merge(features, on="track.id", how="left")
enriched = enriched.merge(
    tracks[["track.id", "track.popularity", "track.explicit",
            "album.name", "album.release_date"]],
    on="track.id", how="left"
)

FEAT_COLS = ["danceability", "energy", "speechiness", "acousticness",
             "instrumentalness", "liveness", "valence"]

# ══════════════════════════════════════════════════════════════════════
# 1. Mood Space — every stream with energy, valence, personID
# ══════════════════════════════════════════════════════════════════════
mood = enriched.dropna(subset=["energy", "valence"])[
    ["personID", "energy", "valence", "artistName", "trackName"]
].copy()
# Subsample for browser performance (max 20k points)
if len(mood) > 20_000:
    mood = mood.sample(20_000, random_state=42)
mood.to_json(OUT_DIR / "mood_space.json", orient="records")
print(f"mood_space.json: {len(mood):,} records")

# Per-person centroids
centroids = (enriched.dropna(subset=["energy", "valence"])
             .groupby("personID")[["energy", "valence"]].mean()
             .reset_index())
centroids.to_json(OUT_DIR / "mood_centroids.json", orient="records")

# ══════════════════════════════════════════════════════════════════════
# 2. Sonic Fingerprints — per-person mean audio features
# ══════════════════════════════════════════════════════════════════════
profiles = enriched.groupby("personID")[FEAT_COLS].mean().reset_index()
profiles.to_json(OUT_DIR / "sonic_fingerprints.json", orient="records")
print(f"sonic_fingerprints.json: {len(profiles)} persons")

# ══════════════════════════════════════════════════════════════════════
# 3. Taste Distance Matrix
# ══════════════════════════════════════════════════════════════════════
from scipy.spatial.distance import pdist, squareform
prof_matrix = profiles.set_index("personID")[FEAT_COLS]
dist_arr = squareform(pdist(prof_matrix, metric="euclidean"))
persons = prof_matrix.index.tolist()
links = []
for i in range(len(persons)):
    for j in range(i+1, len(persons)):
        links.append({
            "source": int(persons[i]), "target": int(persons[j]),
            "distance": round(float(dist_arr[i][j]), 4)
        })
nodes = [{"id": int(p), "label": f"P{p}"} for p in persons]
json.dump({"nodes": nodes, "links": links}, open(OUT_DIR / "taste_network.json", "w"))
print(f"taste_network.json: {len(nodes)} nodes, {len(links)} links")

# ══════════════════════════════════════════════════════════════════════
# 4. Temporal Patterns — hour × dow × personID heatmap data
# ══════════════════════════════════════════════════════════════════════
temporal = (streaming.groupby(["personID", "dow", "hour"])
            .size().reset_index(name="count"))
temporal.to_json(OUT_DIR / "temporal_patterns.json", orient="records")
print(f"temporal_patterns.json: {len(temporal):,} records")

# ══════════════════════════════════════════════════════════════════════
# 5. Top Artists per Person — stream count + total minutes
# ══════════════════════════════════════════════════════════════════════
artist_person = (streaming.groupby(["personID", "artistName"])
                 .agg(streams=("trackName", "size"),
                      total_min=("min_played", "sum"))
                 .reset_index()
                 .sort_values(["personID", "total_min"], ascending=[True, False]))
# Top 15 per person
top_per_person = artist_person.groupby("personID").head(15)
top_per_person["total_min"] = top_per_person["total_min"].round(1)
top_per_person.to_json(OUT_DIR / "top_artists_per_person.json", orient="records")
print(f"top_artists_per_person.json: {len(top_per_person):,} records")

# ══════════════════════════════════════════════════════════════════════
# 6. Genre Distribution per Person
# ══════════════════════════════════════════════════════════════════════
# Map artists → genres, then join with streaming
artist_genre_first = genres.drop_duplicates(subset="artist.name")[["artist.name", "artist.genre"]]
artist_genre_first.columns = ["artistName", "genre"]
streaming_genre = streaming.merge(artist_genre_first, on="artistName", how="left").dropna(subset=["genre"])
genre_person = (streaming_genre.groupby(["personID", "genre"])
                .agg(streams=("trackName", "size"),
                     total_min=("min_played", "sum"))
                .reset_index()
                .sort_values(["personID", "total_min"], ascending=[True, False]))
# Top 10 genres per person
top_genres = genre_person.groupby("personID").head(10)
top_genres["total_min"] = top_genres["total_min"].round(1)
top_genres.to_json(OUT_DIR / "genre_per_person.json", orient="records")
print(f"genre_per_person.json: {len(top_genres):,} records")

# ══════════════════════════════════════════════════════════════════════
# 7. Popularity Distribution per Person (binned)
# ══════════════════════════════════════════════════════════════════════
pop_data = enriched.dropna(subset=["track.popularity"])[["personID", "track.popularity"]].copy()
pop_data["pop_bin"] = (pop_data["track.popularity"] // 5 * 5).astype(int)
pop_binned = pop_data.groupby(["personID", "pop_bin"]).size().reset_index(name="count")
pop_binned.to_json(OUT_DIR / "popularity_dist.json", orient="records")
print(f"popularity_dist.json: {len(pop_binned):,} records")

# ══════════════════════════════════════════════════════════════════════
# 8. Shared Artists Matrix
# ══════════════════════════════════════════════════════════════════════
person_artists = enriched.groupby("personID")["artistName"].apply(set)
shared_data = []
for p1 in person_artists.index:
    for p2 in person_artists.index:
        shared_data.append({
            "personA": int(p1), "personB": int(p2),
            "shared": len(person_artists[p1] & person_artists[p2]),
            "onlyA": len(person_artists[p1] - person_artists[p2]),
            "onlyB": len(person_artists[p2] - person_artists[p1]),
        })
json.dump(shared_data, open(OUT_DIR / "shared_artists.json", "w"))
print(f"shared_artists.json: {len(shared_data)} cells")

# ══════════════════════════════════════════════════════════════════════
# 9. Genre Chord — co-occurrence of genres through shared artists
# ══════════════════════════════════════════════════════════════════════
# Build artist → [genre list]
artist_genres_map = genres.groupby("artist.name")["artist.genre"].apply(list).to_dict()
# Stream-weighted genre co-occurrence
cooccurrence = Counter()
for _, row in streaming.iterrows():
    g_list = artist_genres_map.get(row["artistName"], [])
    for i in range(len(g_list)):
        for j in range(i+1, len(g_list)):
            pair = tuple(sorted([g_list[i], g_list[j]]))
            cooccurrence[pair] += 1

# Top genres for the chord diagram
top_genre_names = genres["artist.genre"].value_counts().head(20).index.tolist()
chord_links = []
for (g1, g2), count in cooccurrence.most_common(500):
    if g1 in top_genre_names and g2 in top_genre_names:
        chord_links.append({"source": g1, "target": g2, "value": count})
json.dump({"genres": top_genre_names, "links": chord_links},
          open(OUT_DIR / "genre_chord.json", "w"))
print(f"genre_chord.json: {len(top_genre_names)} genres, {len(chord_links)} links")

# ══════════════════════════════════════════════════════════════════════
# 10. Listening Arcs — rolling valence/energy per person over time
# ══════════════════════════════════════════════════════════════════════
arcs = (enriched.dropna(subset=["valence", "energy"])
        .sort_values(["personID", "endTime"])
        .groupby("personID")
        .apply(lambda g: g[["endTime", "valence", "energy"]]
               .set_index("endTime")
               .resample("W").mean()
               .reset_index(), include_groups=False)
        .reset_index(level=0))
arcs["endTime"] = arcs["endTime"].dt.strftime("%Y-%m-%d")
arcs = arcs.dropna(subset=["valence"])
arcs.to_json(OUT_DIR / "listening_arcs.json", orient="records")
print(f"listening_arcs.json: {len(arcs):,} records")

# ══════════════════════════════════════════════════════════════════════
# 11. Feature distributions per person (for beeswarm / strip)
# ══════════════════════════════════════════════════════════════════════
strip = enriched.dropna(subset=FEAT_COLS)[["personID"] + FEAT_COLS].copy()
if len(strip) > 15_000:
    strip = strip.sample(15_000, random_state=42)
strip.to_json(OUT_DIR / "feature_strip.json", orient="records")
print(f"feature_strip.json: {len(strip):,} records")

# ══════════════════════════════════════════════════════════════════════
# Person summary stats
# ══════════════════════════════════════════════════════════════════════
summary = (streaming.groupby("personID")
           .agg(total_streams=("trackName", "size"),
                total_hours=("min_played", lambda x: round(x.sum()/60, 1)),
                unique_artists=("artistName", "nunique"),
                unique_tracks=("trackName", "nunique"))
           .reset_index())
summary.to_json(OUT_DIR / "person_summary.json", orient="records")
print(f"person_summary.json: {len(summary)} persons")

print("\n── Original 13 files done ─────────────────────────────────────")

# ══════════════════════════════════════════════════════════════════════
#  NEW VIZ 11–20  (aggregate / holistic — NOT per-person)
# ══════════════════════════════════════════════════════════════════════

# Also load podcast + audiobook streaming
streaming_pod = pd.read_csv(DATA_DIR / "StreamingHistory_podcast.csv", low_memory=False)
streaming_pod = streaming_pod[streaming_pod["personID"] != "personID"].copy()
streaming_pod["personID"] = streaming_pod["personID"].astype(int)
streaming_pod["msPlayed"] = pd.to_numeric(streaming_pod["msPlayed"], errors="coerce")
streaming_pod["endTime"] = pd.to_datetime(streaming_pod["endTime_UTC"], errors="coerce")

streaming_ab = pd.read_csv(DATA_DIR / "StreamingHistory_audiobook.csv", low_memory=False)
streaming_ab = streaming_ab[streaming_ab["personID"] != "personID"].copy()
streaming_ab["personID"] = streaming_ab["personID"].astype(int)
streaming_ab["msPlayed"] = pd.to_numeric(streaming_ab["msPlayed"], errors="coerce")
streaming_ab["endTime"] = pd.to_datetime(streaming_ab["endTime_UTC"], errors="coerce")

# ══════════════════════════════════════════════════════════════════════
# 11. Release Year Archaeology — what decades is the music from?
# ══════════════════════════════════════════════════════════════════════
yr = enriched.dropna(subset=["album.release_date"]).copy()
yr["release_year"] = yr["album.release_date"].str[:4].astype(int)
yr = yr[(yr["release_year"] >= 1950) & (yr["release_year"] <= 2025)]
yr_agg = yr.groupby("release_year").agg(
    streams=("trackName", "size"),
    total_hours=("min_played", lambda x: round(x.sum()/60, 1)),
    unique_tracks=("trackName", "nunique"),
    unique_artists=("artistName", "nunique"),
).reset_index()
yr_agg.to_json(OUT_DIR / "release_year_archaeology.json", orient="records")
print(f"release_year_archaeology.json: {len(yr_agg)} years")

# ══════════════════════════════════════════════════════════════════════
# 12. Tempo Landscape — BPM distribution with genre annotations
# ══════════════════════════════════════════════════════════════════════
tempo_data = enriched.dropna(subset=["tempo"]).copy()
tempo_data["tempo_bin"] = (tempo_data["tempo"] // 2 * 2).astype(int)
tempo_data = tempo_data[(tempo_data["tempo_bin"] >= 40) & (tempo_data["tempo_bin"] <= 220)]
tempo_agg = tempo_data.groupby("tempo_bin").size().reset_index(name="count")
# also get avg features per tempo bin for coloring
tempo_feat = tempo_data.groupby("tempo_bin")[["energy", "danceability", "valence"]].mean().reset_index()
tempo_feat = tempo_feat.round(3)
tempo_merged = tempo_agg.merge(tempo_feat, on="tempo_bin")
tempo_merged.to_json(OUT_DIR / "tempo_landscape.json", orient="records")
print(f"tempo_landscape.json: {len(tempo_merged)} tempo bins")

# ══════════════════════════════════════════════════════════════════════
# 13. Key Signatures — musical keys × mode (major/minor)
# ══════════════════════════════════════════════════════════════════════
key_data = enriched.dropna(subset=["key", "mode"]).copy()
key_data = key_data[key_data["key"] >= 0]
key_data["key"] = key_data["key"].astype(int)
key_data["mode"] = key_data["mode"].astype(int)
key_names = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F",
             "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
key_agg = key_data.groupby(["key", "mode"]).agg(
    streams=("trackName", "size"),
    avg_energy=("energy", "mean"),
    avg_valence=("valence", "mean"),
).reset_index()
key_agg["key_name"] = key_agg["key"].map(dict(enumerate(key_names)))
key_agg["mode_name"] = key_agg["mode"].map({0: "Minor", 1: "Major"})
key_agg["avg_energy"] = key_agg["avg_energy"].round(3)
key_agg["avg_valence"] = key_agg["avg_valence"].round(3)
key_agg.to_json(OUT_DIR / "key_signatures.json", orient="records")
print(f"key_signatures.json: {len(key_agg)} key×mode combos")

# ══════════════════════════════════════════════════════════════════════
# 14. Skip Map — play duration as % of track length
# ══════════════════════════════════════════════════════════════════════
skip = enriched.dropna(subset=["duration_ms"]).copy()
skip = skip[skip["duration_ms"] > 0]
skip["play_pct"] = (skip["msPlayed"] / skip["duration_ms"] * 100).clip(0, 150)
skip["pct_bin"] = (skip["play_pct"] // 5 * 5).astype(int)
skip_agg = skip.groupby("pct_bin").agg(
    count=("trackName", "size"),
    avg_popularity=("track.popularity", "mean"),
).reset_index()
skip_agg["avg_popularity"] = skip_agg["avg_popularity"].round(1)
# also compute overall skip stats
total_streams = len(skip)
skips_under_30s = len(skip[skip["msPlayed"] < 30_000])
full_plays = len(skip[skip["play_pct"] >= 90])
skip_stats = {
    "total_streams": int(total_streams),
    "skips_under_30s": int(skips_under_30s),
    "skip_rate": round(skips_under_30s / total_streams * 100, 1),
    "full_play_rate": round(full_plays / total_streams * 100, 1),
    "bins": json.loads(skip_agg.to_json(orient="records"))
}
json.dump(skip_stats, open(OUT_DIR / "skip_map.json", "w"))
print(f"skip_map.json: {len(skip_agg)} bins, {skip_stats['skip_rate']}% skip rate")

# ══════════════════════════════════════════════════════════════════════
# 15. Dancefloor Clock — avg danceability/energy/valence by hour
# ══════════════════════════════════════════════════════════════════════
clock = enriched.dropna(subset=["danceability", "energy", "valence"]).copy()
clock_agg = clock.groupby("hour").agg(
    streams=("trackName", "size"),
    danceability=("danceability", "mean"),
    energy=("energy", "mean"),
    valence=("valence", "mean"),
    acousticness=("acousticness", "mean"),
    tempo=("tempo", "mean"),
).reset_index()
for c in ["danceability", "energy", "valence", "acousticness", "tempo"]:
    clock_agg[c] = clock_agg[c].round(4)
clock_agg.to_json(OUT_DIR / "dancefloor_clock.json", orient="records")
print(f"dancefloor_clock.json: {len(clock_agg)} hours")

# ══════════════════════════════════════════════════════════════════════
# 16. Loudness vs Energy — scatter showing the relationship
# ══════════════════════════════════════════════════════════════════════
loud = enriched.dropna(subset=["loudness", "energy"]).copy()
# Bin loudness into 0.5 dB steps for manageable size
loud["loud_bin"] = (loud["loudness"] * 2).round() / 2
loud_agg = loud.groupby("loud_bin").agg(
    count=("trackName", "size"),
    avg_energy=("energy", "mean"),
    avg_valence=("valence", "mean"),
    avg_dance=("danceability", "mean"),
).reset_index()
loud_agg = loud_agg.round(4)
loud_agg.to_json(OUT_DIR / "loudness_energy.json", orient="records")
print(f"loudness_energy.json: {len(loud_agg)} loudness bins")

# ══════════════════════════════════════════════════════════════════════
# 17. The Long Tail — cumulative artist concentration (Lorenz-like)
# ══════════════════════════════════════════════════════════════════════
artist_streams = (streaming.groupby("artistName")
                  .agg(streams=("trackName", "size"),
                       total_min=("min_played", "sum"))
                  .reset_index()
                  .sort_values("streams", ascending=False))
artist_streams["rank"] = range(1, len(artist_streams) + 1)
artist_streams["cum_pct"] = (artist_streams["streams"].cumsum()
                              / artist_streams["streams"].sum() * 100).round(2)
artist_streams["artist_pct"] = (artist_streams["rank"]
                                 / len(artist_streams) * 100).round(2)
# Subsample for chart (every Nth + top 50)
n_artists = len(artist_streams)
step = max(1, n_artists // 500)
sampled = pd.concat([
    artist_streams.head(50),
    artist_streams.iloc[50::step],
    artist_streams.tail(1)
]).drop_duplicates(subset="rank")
long_tail = sampled[["rank", "artistName", "streams", "total_min",
                      "cum_pct", "artist_pct"]].copy()
long_tail["total_min"] = long_tail["total_min"].round(1)
long_tail_meta = {
    "total_artists": int(n_artists),
    "total_streams": int(artist_streams["streams"].sum()),
    "top10_pct": round(float(artist_streams.head(10)["streams"].sum()
                              / artist_streams["streams"].sum() * 100), 1),
    "top50_pct": round(float(artist_streams.head(50)["streams"].sum()
                              / artist_streams["streams"].sum() * 100), 1),
    "data": json.loads(long_tail.to_json(orient="records"))
}
json.dump(long_tail_meta, open(OUT_DIR / "long_tail.json", "w"))
print(f"long_tail.json: {n_artists} artists, top 10 = {long_tail_meta['top10_pct']}%")

# ══════════════════════════════════════════════════════════════════════
# 18. Explicit Content Over Time
# ══════════════════════════════════════════════════════════════════════
explicit_data = enriched.dropna(subset=["track.explicit"]).copy()
explicit_data["track.explicit"] = explicit_data["track.explicit"].astype(str).str.lower().map({"true": 1, "false": 0, "1": 1, "0": 0, "1.0": 1, "0.0": 0}).fillna(0).astype(int)
explicit_data["month"] = explicit_data["endTime"].dt.to_period("M").astype(str)
explicit_monthly = explicit_data.groupby("month").agg(
    total=("trackName", "size"),
    explicit_count=("track.explicit", "sum"),
).reset_index()
explicit_monthly["explicit_pct"] = (explicit_monthly["explicit_count"]
                                     / explicit_monthly["total"] * 100).round(1)
explicit_monthly.to_json(OUT_DIR / "explicit_timeline.json", orient="records")
print(f"explicit_timeline.json: {len(explicit_monthly)} months")

# ══════════════════════════════════════════════════════════════════════
# 19. Song Length Eras — track duration vs release year
# ══════════════════════════════════════════════════════════════════════
dur = enriched.dropna(subset=["album.release_date", "duration_ms"]).copy()
dur["release_year"] = dur["album.release_date"].str[:4].astype(int)
dur = dur[(dur["release_year"] >= 1960) & (dur["release_year"] <= 2025)]
dur["duration_sec"] = dur["duration_ms"] / 1000
dur_agg = dur.groupby("release_year").agg(
    median_sec=("duration_sec", "median"),
    mean_sec=("duration_sec", "mean"),
    p25=("duration_sec", lambda x: x.quantile(0.25)),
    p75=("duration_sec", lambda x: x.quantile(0.75)),
    count=("trackName", "size"),
).reset_index()
dur_agg = dur_agg.round(1)
dur_agg.to_json(OUT_DIR / "song_length_eras.json", orient="records")
print(f"song_length_eras.json: {len(dur_agg)} years")

# ══════════════════════════════════════════════════════════════════════
# 20. Audio Feature Correlations — heatmap of all features
# ══════════════════════════════════════════════════════════════════════
ALL_FEAT = FEAT_COLS + ["loudness", "tempo"]
corr_data = enriched.dropna(subset=ALL_FEAT)[ALL_FEAT]
corr_matrix = corr_data.corr()
corr_records = []
for f1 in ALL_FEAT:
    for f2 in ALL_FEAT:
        corr_records.append({
            "feature1": f1, "feature2": f2,
            "r": round(float(corr_matrix.loc[f1, f2]), 3)
        })
json.dump(corr_records, open(OUT_DIR / "feature_correlations.json", "w"))
print(f"feature_correlations.json: {len(corr_records)} cells ({len(ALL_FEAT)}×{len(ALL_FEAT)})")

# ══════════════════════════════════════════════════════════════════════
# 21. Marquee Segments — Super / Moderate / Light listener breakdown
# ══════════════════════════════════════════════════════════════════════
marquee_clean = marquee[marquee["personID"] != "personID"].copy()
marquee_clean["personID"] = marquee_clean["personID"].astype(int)
marquee_agg = marquee_clean.groupby("segment").size().reset_index(name="count")
# also get top artists per segment
marquee_artists = (marquee_clean.groupby(["segment", "artistName"])
                   .size().reset_index(name="count")
                   .sort_values(["segment", "count"], ascending=[True, False]))
marquee_top = marquee_artists.groupby("segment").head(15)
marquee_out = {
    "segments": json.loads(marquee_agg.to_json(orient="records")),
    "top_artists": json.loads(marquee_top.to_json(orient="records")),
}
json.dump(marquee_out, open(OUT_DIR / "marquee_segments.json", "w"))
print(f"marquee_segments.json: {len(marquee_agg)} segments")

# ══════════════════════════════════════════════════════════════════════
# 22. Media Mix — music vs podcast vs audiobook over time
# ══════════════════════════════════════════════════════════════════════
music_monthly = streaming.groupby(streaming["endTime"].dt.to_period("M")).agg(
    hours=("min_played", lambda x: round(x.sum()/60, 1))
).reset_index()
music_monthly["endTime"] = music_monthly["endTime"].astype(str)
music_monthly["type"] = "Music"

pod_monthly = streaming_pod.groupby(streaming_pod["endTime"].dt.to_period("M")).agg(
    hours=("msPlayed", lambda x: round(x.sum()/3_600_000, 1))
).reset_index()
pod_monthly["endTime"] = pod_monthly["endTime"].astype(str)
pod_monthly["type"] = "Podcast"

ab_monthly = streaming_ab.groupby(streaming_ab["endTime"].dt.to_period("M")).agg(
    hours=("msPlayed", lambda x: round(x.sum()/3_600_000, 1))
).reset_index()
ab_monthly["endTime"] = ab_monthly["endTime"].astype(str)
ab_monthly["type"] = "Audiobook"

media_mix = pd.concat([music_monthly, pod_monthly, ab_monthly], ignore_index=True)
media_mix.to_json(OUT_DIR / "media_mix.json", orient="records")
print(f"media_mix.json: {len(media_mix)} records")

# ══════════════════════════════════════════════════════════════════════
# 23. Tempo × Skip — how does tempo relate to skip behavior?
# ══════════════════════════════════════════════════════════════════════
tempo_skip = enriched.dropna(subset=["tempo", "duration_ms"]).copy()
tempo_skip = tempo_skip[(tempo_skip["duration_ms"] > 0) & (tempo_skip["tempo"] >= 40) & (tempo_skip["tempo"] <= 220)]
tempo_skip["play_pct"] = (tempo_skip["msPlayed"] / tempo_skip["duration_ms"] * 100).clip(0, 150)
tempo_skip["tempo_bin"] = (tempo_skip["tempo"] // 4 * 4).astype(int)
tempo_skip["skipped"] = (tempo_skip["msPlayed"] < 30_000).astype(int)
tempo_skip["full_play"] = (tempo_skip["play_pct"] >= 90).astype(int)

ts_agg = tempo_skip.groupby("tempo_bin").agg(
    streams=("trackName", "size"),
    avg_play_pct=("play_pct", "mean"),
    skip_rate=("skipped", "mean"),
    full_play_rate=("full_play", "mean"),
    avg_energy=("energy", "mean"),
    avg_danceability=("danceability", "mean"),
    avg_valence=("valence", "mean"),
).reset_index()
for c in ["avg_play_pct","skip_rate","full_play_rate","avg_energy","avg_danceability","avg_valence"]:
    ts_agg[c] = (ts_agg[c] * (100 if c in ["skip_rate","full_play_rate"] else 1)).round(2)
ts_agg.to_json(OUT_DIR / "tempo_skip.json", orient="records")
print(f"tempo_skip.json: {len(ts_agg)} tempo bins")

# ══════════════════════════════════════════════════════════════════════
# 24 & 29. Mood Ring / Vocal Compass — hourly avg of ALL features
# ══════════════════════════════════════════════════════════════════════
mr = enriched.dropna(subset=FEAT_COLS)
mr_f = mr.groupby("hour")[FEAT_COLS + ["loudness", "tempo"]].mean().round(4).reset_index()
mr_c = mr.groupby("hour").size().reset_index(name="streams")
mood_ring_out = mr_c.merge(mr_f, on="hour")
mood_ring_out.to_json(OUT_DIR / "mood_ring.json", orient="records")
print(f"mood_ring.json: {len(mood_ring_out)} hours")

# ══════════════════════════════════════════════════════════════════════
# 25. Weekly Vibe DNA — day-of-week avg features
# ══════════════════════════════════════════════════════════════════════
wk = enriched.dropna(subset=FEAT_COLS).copy()
wk["dow"] = wk["endTime"].dt.dayofweek
wk_f = wk.groupby("dow")[FEAT_COLS].mean().round(4).reset_index()
wk_c = wk.groupby("dow").size().reset_index(name="streams")
weekly_out = wk_c.merge(wk_f, on="dow")
weekly_out["day_name"] = weekly_out["dow"].map(dict(enumerate(
    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])))
weekly_out.to_json(OUT_DIR / "weekly_vibe.json", orient="records")
print(f"weekly_vibe.json: {len(weekly_out)} days")

# ══════════════════════════════════════════════════════════════════════
# 26 & 28. Key Features — per-key avg of 7 features (radars + flowers)
# ══════════════════════════════════════════════════════════════════════
kf = enriched.dropna(subset=FEAT_COLS + ["key"]).copy()
kf = kf[kf["key"] >= 0]; kf["key"] = kf["key"].astype(int)
kf_f = kf.groupby("key")[FEAT_COLS].mean().round(4).reset_index()
kf_c = kf.groupby("key").size().reset_index(name="streams")
key_feat_out = kf_c.merge(kf_f, on="key")
_kn2 = ["C","C♯/D♭","D","D♯/E♭","E","F","F♯/G♭","G","G♯/A♭","A","A♯/B♭","B"]
key_feat_out["key_name"] = key_feat_out["key"].map(dict(enumerate(_kn2)))

# Compute per-key dominant feature (highest z-score above median) so we can
# pick a representative song that actually matches the personality label.
import statistics as _stats
_medians_kf = {}; _mads_kf = {}
for _f in FEAT_COLS:
    _vals = sorted(key_feat_out[_f].tolist())
    _med = _stats.median(_vals)
    _medians_kf[_f] = _med
    _ad = sorted(abs(v - _med) for v in _vals)
    _mads_kf[_f] = _stats.median(_ad) * 1.4826 or 0.001

def _dominant_feat(row):
    zscores = {f: (row[f] - _medians_kf[f]) / _mads_kf[f] for f in FEAT_COLS}
    best = max(zscores, key=zscores.get)
    return best if zscores[best] >= 1.0 else None

key_feat_out["_dom"] = key_feat_out.apply(_dominant_feat, axis=1)

# Per-key song plays with per-song average of each feature
song_plays = (
    kf.groupby(["key", "trackName", "artistName"])
    .agg(_plays=("trackName", "size"), **{f: (f, "mean") for f in FEAT_COLS})
    .reset_index()
)

# For each key: among top-20 by plays, pick the one that scores highest on the
# key's dominant feature.  For uncategorized keys (no z>1), just use most-played.
rep_rows = []
for _, kr in key_feat_out.iterrows():
    k = kr["key"]
    dom = kr["_dom"]
    sub = song_plays[song_plays["key"] == k].sort_values("_plays", ascending=False).head(20)
    if dom and len(sub) > 0:
        best = sub.sort_values(dom, ascending=False).iloc[0]
    elif len(sub) > 0:
        best = sub.iloc[0]
    else:
        rep_rows.append({"key": k, "top_track": None, "top_artist": None, "top_plays": 0})
        continue
    rep_rows.append({
        "key": k,
        "top_track": best["trackName"],
        "top_artist": best["artistName"],
        "top_plays": int(best["_plays"]),
    })

top_songs = pd.DataFrame(rep_rows)
key_feat_out = key_feat_out.drop(columns=["_dom"]).merge(top_songs, on="key", how="left")

key_feat_out.to_json(OUT_DIR / "key_features.json", orient="records")
print(f"key_features.json: {len(key_feat_out)} keys")

# ══════════════════════════════════════════════════════════════════════
# 27. Monthly Features — calendar month avg features (seasonal energy)
# ══════════════════════════════════════════════════════════════════════
mf = enriched.dropna(subset=FEAT_COLS).copy()
mf["cal_month"] = mf["endTime"].dt.month
mf_f = mf.groupby("cal_month")[FEAT_COLS].mean().round(4).reset_index()
mf_c = mf.groupby("cal_month").size().reset_index(name="streams")
monthly_out = mf_c.merge(mf_f, on="cal_month")
monthly_out["month_name"] = monthly_out["cal_month"].map(dict(zip(
    range(1, 13), ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])))
monthly_out.to_json(OUT_DIR / "monthly_features.json", orient="records")
print(f"monthly_features.json: {len(monthly_out)} months")

# ══════════════════════════════════════════════════════════════════════
# 30. Loudness by Key — loudness distribution per key (wind rose)
# ══════════════════════════════════════════════════════════════════════
lk = enriched.dropna(subset=["loudness", "key"]).copy()
lk = lk[lk["key"] >= 0]; lk["key"] = lk["key"].astype(int)
lk["loud_bin"] = pd.cut(lk["loudness"],
    bins=[-60, -20, -15, -10, -7, -5, -3, 0],
    labels=["<-20dB", "-20 to -15", "-15 to -10", "-10 to -7", "-7 to -5", "-5 to -3", ">-3dB"])
lk = lk.dropna(subset=["loud_bin"])
lk_agg = lk.groupby(["key", "loud_bin"]).size().reset_index(name="count")
lk_agg["key_name"] = lk_agg["key"].map(dict(enumerate(_kn2)))
lk_agg["loud_bin"] = lk_agg["loud_bin"].astype(str)
lk_agg.to_json(OUT_DIR / "loudness_by_key.json", orient="records")
print(f"loudness_by_key.json: {len(lk_agg)} key×loudness combos")

print("\n✅ All data files written to", OUT_DIR.resolve())
