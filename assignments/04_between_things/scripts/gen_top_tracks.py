"""Generate top-5 songs per musical key for the appendix in chart 38."""
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "spotify_data"
OUT  = BASE / "viz" / "data" / "key_top_tracks.json"

# Load track features (has key column)
feats = {}
with open(DATA / "trackFeatures.csv") as f:
    for row in csv.DictReader(f):
        tid = row["track.id"]
        try:
            feats[tid] = int(float(row["key"]))
        except Exception:
            pass

# Count plays per track from streaming history
plays = defaultdict(lambda: {"count": 0, "ms": 0, "name": "", "artist": ""})
with open(DATA / "StreamingHistory_music.csv") as f:
    for row in csv.DictReader(f):
        if row.get("personID", "") == "personID":
            continue
        tid = row["track.id"]
        try:
            ms = int(float(row["msPlayed"]))
        except Exception:
            ms = 0
        plays[tid]["count"] += 1
        plays[tid]["ms"] += ms
        plays[tid]["name"] = row["trackName"]
        plays[tid]["artist"] = row["artistName"]

# Build per-key track lists
key_tracks = defaultdict(list)
for tid, info in plays.items():
    if tid in feats and info["count"] > 0 and info["name"]:
        key_tracks[feats[tid]].append(
            {"name": info["name"], "artist": info["artist"], "plays": info["count"]}
        )

# Sort by plays desc, dedupe by name, take top 5
result = {}
for k in range(12):
    tracks = sorted(key_tracks.get(k, []), key=lambda x: -x["plays"])
    seen, deduped = set(), []
    for t in tracks:
        if t["name"] not in seen:
            seen.add(t["name"])
            deduped.append(t)
        if len(deduped) == 5:
            break
    result[str(k)] = deduped

with open(OUT, "w") as f:
    json.dump(result, f, indent=2)

key_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
for k in range(12):
    print(f"\nKey {k} ({key_names[k]}):")
    for t in result[str(k)]:
        print(f"  {t['plays']:>3}x  {t['name']} -- {t['artist']}")
