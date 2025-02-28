import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth


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

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read",
    )
)

rwh_uri = "spotify:playlist:73vmEitV1vfKQK25m1uCp5"
results = sp.playlist_tracks(rwh_uri)
tracks = []

if results is not None:
    tracks = results["items"]
    while results and results["next"]:
        results = sp.next(results)
        if results is not None:
            tracks.extend(results["items"])

if tracks:
    num = 1
    for track in tracks:
        track_info = track["track"]
        track_name = track_info["name"]
        album_name = track_info["album"]["name"]
        artist_name = track_info["artists"][0]["name"]
        print(f"{num}. Track name: {track_name}")
        # print(f"Album name: {album_name}")
        # print(f"Artist name: {artist_name}\n")
        num += 1
else:
    print("No results found.")
