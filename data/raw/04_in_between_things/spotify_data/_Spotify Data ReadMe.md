## Spotify Data Readme

Data in this folder are Spotify exports from individuals, which have been de-identified and combined into collections by type.  
Tracks, artists, episodes, and more have then been queried against the Spotify API [https://developer.spotify.com/documentation/web-api](https://developer.spotify.com/documentation/web-api) for detailed information on the objects.  

Data are all in CSV (comma separated value) format for ease of use.  
Additional and more extensive original data are in the companion file spotify_data_extras.zip  

## The Data
In alphabetical order:  

# artistInfo_genres.csv
Musical genres (pop, rock, rap, folk, etc.) for each artist, encoded by artist.name and artist.id.
Many artists have more than one genre and will show up with multiple records.  This format is built for many-to-one relationships, and can be related to tracks, albums, and more.  
fields: artist.genre, artist.id, artist.name  
See [https://developer.spotify.com/documentation/web-api/reference/get-an-artist](https://developer.spotify.com/documentation/web-api/reference/get-an-artist)

# artistInfo.csv
Information about each artist (artist.name, artist.id), including artist.popularity and artist.followers, as well as a single entry list/array ["pop", "rock", "rap", "folk"] of genres.  
fields: artist.genres, artist.id, artist.name, artist.popularity, artist.followers
See [https://developer.spotify.com/documentation/web-api/reference/get-an-artist](https://developer.spotify.com/documentation/web-api/reference/get-an-artist)

# episodeInfo.csv
Podcast Episodes information, on episode.id and episode.name.  
Includes episode.duration_ms, episode.explicit, episode.language, episode.release_date, and episode.description, along with information on the show that it is part of.  
fields: episode.description,episode.duration_ms,episode.explicit,episode.id,episode.language,episode.name,episode.release_date,show.description,show.id,show.name,show.publisher,show.total_episodes
Note that this does not include a comprehensive list of all episodes identified in the StreamingHistory_podcast, because the Search API does not work well for podcast episodes unfortunately.  It did get a lot of them.
See [https://developer.spotify.com/documentation/web-api/reference/get-an-episode](https://developer.spotify.com/documentation/web-api/reference/get-an-episode)

# Follow_counts.csv
Count of followers and following for each personID (each student who contributed data) in the set.
Note: the original Follow data from Spotify includes the usernames of who the user is following, is followed by, and is blocking.  While this might be interesting, it is also potentially identifiable, so I have removed that list in favor of the counts.  There is very little overlap anyway, so the names don't give us much more than an attempt to identify.
fields: personID, userIsFollowing_count, userIsFollowedBy_count, userIsBlocking_count

# Inferences.csv
What Spotify infers about you.  This is a list of their categories (some of which are just identifier codes, so not that useful) and who they've tied these to based on your history and patterns of listening and searching.  This may or may not be that useful, but I'm including it just in case.
fields: personID, inferences

# Marquee.csv
Assessment for each personID and select artists the personIDs are considered "Super Listeners", "Moderate Listeners", "Light Listeners", "Previously Active Listeners", etc.  
fields: personID, artistName, segment

# Playlists.csv
Collection of all tracks in a personID's spotify playlists, by playlist name, including when it was added and updated.
fields: personID, episode, audiobook, localTrack, track.addedDate, track.trackName, track.artistName, track.albumName, playlist.name, playlist.lastModifiedDate, playlist.description, playlist.numberOfFollowers, track, localTrack.uri, episode.episodeName, episode.showName, episode.episodeID, track.id
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# StreamingHistory_audiobook.csv
Same as _music, below, but for audio books.

# StreamingHistory_music.csv
Date/Time playing history of all tracks listened to, by personID and track.id
Note that the time encoding is when the track *finished* playing (not started), and is in UTC time (Coordinated Universal Time zone), so 4- or 5- hours offset from EST / EDT.  Time can be converted with DateTime math in Tableau and elsewhere.  
fields: personID, endTime_UTC, artistName, trackName, msPlayed, track.id
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# StreamingHistory_podcast.csv
Same as _music, but for podcast episides.

# trackFeatures.csv
Detailed audio features (measurements) of each track, for understanding the music's characteristics or how the music feels.  For this year’s tracks, and not all of them at that.  Due to the Spotify audio-features api being deprecated in Nov 2024, not all of our tracks have feature information.
fields: danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, track.id, duration_ms, time_signature  
See [https://developer.spotify.com/documentation/web-api/reference/get-audio-features](https://developer.spotify.com/documentation/web-api/reference/get-audio-features) for explanations of what each measurement means and the scale of values used.

# trackFeatures_6yrs.csv
Detailed audio features (measurements) of each track, for understanding the music's characteristics or how the music feels.  
Same as the above but collected from all of the DataViz classes over the 6 prior years, 2020-2025.  This includes > 235,000 tracks, but a lot of these do not connect to this year’s listening data.  Will be more useful for broader artist and album based analysis, rather than our student listening habits this year.

# trackInfo.csv
Core information about each track, including track.popularity, track.duation_ms, track.explicit, and more.  
Can easily be related (joined) to trackFeatures, StreamingHistory_music, and other files.  
fields: artist.id, artist.name, album.id, album.name, album.type, album.release_date, album.total_tracks, track.disc_number, track.duration_ms, track.explicit, track.id, track.name, track.popularity, track.track_number
See [https://developer.spotify.com/documentation/web-api/reference/get-track](https://developer.spotify.com/documentation/web-api/reference/get-track)

# trackInfo_AvailableMarkets.csv
This file is only available in the spotify_extras download, not the main set, because it is large and likely not as useful to most of you.
Which "Markets" (countries, locations) where this track is available for streaming.  
This is a very long list, organized as a Pivot table, for one-to-many relationships.  
See [https://developer.spotify.com/documentation/web-api/reference/get-track](https://developer.spotify.com/documentation/web-api/reference/get-track)

# YourLibrary_albums.csv
Albums listed in each personID's saved library.  Can be related (joined) to other files in this set for further detail.  
fields: personID, albums_album, albums_artist, albums_id  
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_artists.csv
Artists listed in each personID's saved library.  
fields: personID, artists_name, artists_id  
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_bannedArtists.csv
Artists banned by each personID's saved library.  
fields: personID, bannedArtists_name, bannedArtists_id
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_bannedTracks.csv
Tracks banned by each personID's saved library.  
fields: personID, bannedTracks_album, bannedTracks_artist, bannedTracks_track, bannedTracks_id
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_episodes.csv
Podcast episodes listed in each personID's saved library.  
fields: personID, episodes_name, episodes_show, episodes_id  

See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_other.csv
Other things in your library.  Mostly local tracks not in the main streaming platform, like imports from CDs or otherwise.
fields: personID, other
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_shows.csv
Podcast shows listed in each personID's saved library.  
fields: personID, shows_name, shows_publisher, shows_id  
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)

# YourLibrary_tracks.csv
Music tracks listed in each personID's saved library.  
fields: personID, tracks_album, tracks_artist, tracks_track, tracks_id  
See [https://support.spotify.com/us/article/understanding-my-data/](https://support.spotify.com/us/article/understanding-my-data/)
