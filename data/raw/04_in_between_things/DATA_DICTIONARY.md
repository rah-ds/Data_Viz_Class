# Spotify Data Dictionary

> Data export from Spotify covering **14 listeners** (personID 1–15, excluding 13), spanning roughly **2019–2025**.

---

## Core Tables

### `StreamingHistory_music.csv` — 266,388 rows
The backbone: every music stream across all listeners.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener identifier (1–15, no 13) |
| `endTime_UTC` | datetime | UTC timestamp when the stream ended |
| `artistName` | str | Artist name |
| `trackName` | str | Track name |
| `msPlayed` | int | Milliseconds played (0 = instant skip, <30 000 = likely skip) |
| `track.id` | str | Spotify track URI (join key to trackFeatures / trackInfo) |

### `StreamingHistory_podcast.csv` — 2,315 rows
Podcast episode streams.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener identifier |
| `endTime_UTC` | datetime | When the stream ended |
| `podcastName` | str | Show / podcast name |
| `episodeName` | str | Episode title |
| `msPlayed` | int | Milliseconds played |
| `episode.id` | str | Spotify episode URI (often empty) |

### `StreamingHistory_audiobook.csv` — 660 rows
Audiobook chapter streams.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener identifier |
| `endTime_UTC` | datetime | When the stream ended |
| `audiobookName` | str | Audiobook title |
| `chapterName` | str | Chapter title |
| `authorName` | str | Author |
| `msPlayed` | int | Milliseconds played |

---

## Track Metadata

### `trackInfo.csv` — 76,845 rows
Spotify API metadata for tracks (album, artist, popularity).

| Column | Type | Description |
|--------|------|-------------|
| `track.id` | str | **Primary key** — Spotify track URI |
| `track.name` | str | Track title |
| `track.popularity` | int | 0–100 popularity score (current snapshot) |
| `track.explicit` | bool | Whether Spotify flags the track as explicit |
| `track.duration_ms` | int | Full track length in milliseconds |
| `track.disc_number` | int | Disc number on album |
| `track.track_number` | int | Track number on album |
| `artist.id` | str | Primary artist URI (join key to artistInfo) |
| `artist.name` | str | Primary artist name |
| `album.id` | str | Album URI |
| `album.name` | str | Album title |
| `album.type` | str | `album`, `single`, `compilation` |
| `album.release_date` | str | ISO date (YYYY, YYYY-MM, or YYYY-MM-DD) |
| `album.total_tracks` | int | Number of tracks on the album |

### `trackFeatures.csv` — 21,454 rows
Spotify Audio Features API (current-year tracks). *API deprecated Nov 2024.*

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `track.id` | str | — | Join key |
| `danceability` | float | 0–1 | How suitable for dancing (tempo, rhythm stability, beat strength) |
| `energy` | float | 0–1 | Perceptual intensity and activity (loud, fast, noisy → high) |
| `key` | int | 0–11 | Pitch class (0=C, 1=C♯/D♭, …, 11=B). -1 if not detected |
| `loudness` | float | −60–0 dB | Average loudness in decibels |
| `mode` | int | 0 or 1 | 0 = minor, 1 = major |
| `speechiness` | float | 0–1 | Presence of spoken words (>0.66 = speech, 0.33–0.66 = rap/spoken word) |
| `acousticness` | float | 0–1 | Confidence the track is acoustic |
| `instrumentalness` | float | 0–1 | Predicts no vocals (>0.5 = instrumental) |
| `liveness` | float | 0–1 | Detects live audience (>0.8 = probably live) |
| `valence` | float | 0–1 | Musical positiveness (happy/cheerful → high, sad/angry → low) |
| `tempo` | float | BPM | Estimated beats per minute |
| `duration_ms` | float | ms | Track duration |
| `time_signature` | float | 3–7 | Estimated time signature (beats per bar, e.g. 4 = 4/4) |

### `trackFeatures_6yrs.csv` — 235,478 rows
Same schema as `trackFeatures.csv` but covering tracks from **2020–2025** (historical feature snapshots).

---

## Artist Metadata

### `artistInfo.csv` — 21,148 rows
Spotify API artist data.

| Column | Type | Description |
|--------|------|-------------|
| `artist.id` | str | **Primary key** — Spotify artist URI |
| `artist.name` | str | Artist name |
| `artist.genres` | str (Python list repr) | e.g. `['slap house', 'edm']` |
| `artist.popularity` | int | 0–100 popularity score |
| `artist.followers` | int | Follower count |

### `artistInfo_genres.csv` — 25,199 rows
Exploded version: one row per artist–genre pair.

| Column | Type | Description |
|--------|------|-------------|
| `artist.id` | str | Artist URI |
| `artist.name` | str | Artist name |
| `artist.genre` | str | Single genre tag (e.g. `indie pop`) |

---

## Library & Playlists

### `Playlists.csv` — 29,066 rows
All playlist contents across listeners.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener identifier |
| `playlist.name` | str | Playlist title |
| `playlist.lastModifiedDate` | str | Last edit date |
| `playlist.description` | str | Playlist description |
| `playlist.numberOfFollowers` | int | Follower count |
| `track.trackName` | str | Track title |
| `track.artistName` | str | Artist |
| `track.albumName` | str | Album |
| `track.id` | str | Track URI |
| `track.addedDate` | str | When track was added to playlist |
| `episode` | bool | Is this an episode? |
| `audiobook` | bool | Is this an audiobook? |
| `localTrack` | bool | Is this a local file? |
| `localTrack.uri` | str | URI for local tracks |
| `episode.episodeName` | str | Episode name (if episode) |
| `episode.showName` | str | Show name (if episode) |
| `episode.episodeID` | str | Episode URI |
| `track` | bool | Is this a track? |

### `YourLibrary_tracks.csv` — 22,388 rows
Saved/liked tracks.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `tracks_track` | str | Track name |
| `tracks_artist` | str | Artist name |
| `tracks_album` | str | Album name |
| `tracks_id` | str | Track URI |

### `YourLibrary_artists.csv` — 291 rows
Followed artists.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `artists_name` | str | Artist name |
| `artists_id` | str | Artist URI |

### `YourLibrary_albums.csv` — 678 rows
Saved albums.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `albums_album` | str | Album title |
| `albums_artist` | str | Artist name |
| `albums_id` | str | Album URI |

### `YourLibrary_shows.csv` — 72 rows
Followed podcast shows.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `shows_name` | str | Show name |
| `shows_publisher` | str | Publisher |
| `shows_id` | str | Show URI |

### `YourLibrary_episodes.csv` — 169 rows
Saved episodes.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `episodes_name` | str | Episode title |
| `episodes_show` | str | Show name |
| `episodes_id` | str | Episode URI |

### `YourLibrary_bannedArtists.csv` — 11 rows
Blocked artists.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `bannedArtists_name` | str | Artist name |
| `bannedArtists_id` | str | Artist URI |

### `YourLibrary_bannedTracks.csv` — 10 rows
Blocked tracks.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `bannedTracks_track` | str | Track name |
| `bannedTracks_artist` | str | Artist name |
| `bannedTracks_album` | str | Album |
| `bannedTracks_id` | str | Track URI |

### `YourLibrary_other.csv` — 21 rows
Local file URIs (`spotify:local:...`).

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `other` | str | spotify:local URI |

---

## Engagement & Segmentation

### `Marquee.csv` — 14,732 rows
Spotify's internal listener-segment labels for artists.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `artistName` | str | Artist |
| `segment` | str | `"Super Listeners"`, `"Moderate listeners"`, `"Light listeners"`, `"Previously Active Listeners"` |

### `Follow_counts.csv` — 12 rows
Social graph counts per listener.

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `userIsFollowing_count` | int | How many people this person follows |
| `userIsFollowedBy_count` | int | Follower count |
| `userIsBlocking_count` | int | Blocked users |

### `Inferences.csv` — 5,676 rows
Spotify's inferred user attributes (ad targeting etc.).

| Column | Type | Description |
|--------|------|-------------|
| `personID` | int | Listener |
| `inferences` | str | Inference labels (UUIDs and content tags like `content_music`) |

---

## Podcast / Episode Metadata

### `episodeInfo.csv` — 872 rows

| Column | Type | Description |
|--------|------|-------------|
| `episode.id` | str | Episode URI |
| `episode.name` | str | Episode title |
| `episode.description` | str | Description text |
| `episode.duration_ms` | int | Duration in ms |
| `episode.explicit` | bool | Explicit flag |
| `episode.language` | str | Language code |
| `episode.release_date` | str | Release date |
| `show.id` | str | Parent show URI |
| `show.name` | str | Show name |
| `show.description` | str | Show description |
| `show.publisher` | str | Publisher |
| `show.total_episodes` | int | Total episodes in show |

---

## Extras (`data/spotify_extras/`)

| File | Description |
|------|-------------|
| `artistInfo_full.json` | Full Spotify API artist objects (21k) with images, followers, genres |
| `trackInfo_full.json` | Full Spotify API track objects (very large, ~50 MB) |
| `episodeInfo_full.json` | Full episode API objects with images, previews |
| `showInfo_full.json` | Full show API objects with markets, copyrights |
| `trackList_full.csv` | Simple lookup: `track.name`, `artist.name`, `track.id` (53k rows) |
| `trackInfo_AvailableMarkets.csv` | Available markets per track (very large) |
| `tracksNotFoundAfterSearch.json` | 476 tracks not found via Spotify API search |
| `episodesNotFoundAfterSearch.json` | 68 episodes not found |
| `showsNotFound.txt` | 7 shows not found |

---

## Key Join Relationships

```
StreamingHistory_music ──[track.id]──→ trackFeatures
StreamingHistory_music ──[track.id]──→ trackInfo ──[artist.id]──→ artistInfo
StreamingHistory_music ──[track.id]──→ trackInfo ──[artist.id]──→ artistInfo_genres
StreamingHistory_podcast ─[episode.id]→ episodeInfo
Marquee ──[personID + artistName]──→ StreamingHistory_music
```

## Audio Feature Interpretation Guide

| Feature | Low (→ 0) | High (→ 1) |
|---------|-----------|------------|
| **Danceability** | Irregular rhythm, complex | Steady beat, dance-friendly |
| **Energy** | Soft, quiet, sparse | Loud, fast, dense, noisy |
| **Speechiness** | Instrumental / sung | Spoken word / podcast-like |
| **Acousticness** | Electronic / produced | Acoustic instruments |
| **Instrumentalness** | Vocals present | No vocals (instrumental) |
| **Liveness** | Studio recording | Live performance w/ audience |
| **Valence** | Sad, angry, dark | Happy, cheerful, euphoric |
| **Loudness** | −60 dB (very quiet) | 0 dB (very loud) |
| **Tempo** | Slow (~60 BPM) | Fast (~200+ BPM) |
