import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import OAuthCredentials, YTMusic


def get_credentials(filename):
    with open(filename, "r") as f:
        oauth_data = json.load(f)
    client_id = oauth_data["client_id"]
    client_secret = oauth_data["client_secret"]
    return client_id, client_secret


client_id, client_secret = get_credentials("spotify.json")
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read",
    )
)

client_id, client_secret = get_credentials("youtube.json")
yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=client_id, client_secret=client_secret
    ),
)

rwh_uri = "spotify:playlist:73vmEitV1vfKQK25m1uCp5"

# Get Spotify playlist details
playlist_id = rwh_uri
results = sp.playlist_tracks(playlist_id)
tracks = results["items"] if results else []

while results and results["next"]:
    results = sp.next(results)
    if results:
        tracks.extend(results["items"])

# Create a new YouTube Music playlist
playlist_details = sp.playlist(playlist_id)
playlist_title = playlist_details["name"] if playlist_details else "New Playlist"
playlist_description = playlist_details["description"] if playlist_details else ""
new_playlist_id = str(yt.create_playlist(playlist_title, playlist_description))

# Search for each track on YouTube Music and add to the new playlist
num = 0
for item in tracks:
    num += 1
    track = item["track"]
    query = f"{track['name']} {track['artists'][0]['name']}"
    search_results = yt.search(query, filter="songs", limit=1)
    if search_results:
        print(f"{num} Adding {track['name']}")
        video_id = search_results[0]["videoId"]
        yt.add_playlist_items(new_playlist_id, [video_id])
    else:
        print(f"{num} Didn't find {track['name']}")
