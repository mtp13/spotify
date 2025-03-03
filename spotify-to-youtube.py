import json
from typing import Dict, List, Tuple

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import OAuthCredentials, YTMusic


def get_credentials(filename: str) -> Tuple[str, str]:
    """Load OAuth credentials from a JSON file."""
    try:
        with open(filename, "r") as f:
            oauth_data = json.load(f)
        return oauth_data["client_id"], oauth_data["client_secret"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading credentials from {filename}: {str(e)}")


def get_spotify_client() -> spotipy.Spotify:
    """Initialize and return Spotify client."""
    client_id, client_secret = get_credentials("spotify.json")
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost:8888/callback",
            scope="user-library-read",
        )
    )


def get_youtube_client() -> YTMusic:
    """Initialize and return YouTube Music client."""
    client_id, client_secret = get_credentials("youtube.json")
    return YTMusic(
        "oauth.json",
        oauth_credentials=OAuthCredentials(
            client_id=client_id, client_secret=client_secret
        ),
    )


def get_spotify_playlist_tracks(sp: spotipy.Spotify, playlist_id: str) -> List[Dict]:
    """Fetch all tracks from a Spotify playlist."""
    results = sp.playlist_tracks(playlist_id)
    tracks = results["items"] if results else []

    while results and results["next"]:
        results = sp.next(results)
        if results:
            tracks.extend(results["items"])
    return tracks


def create_youtube_playlist(yt: YTMusic, sp: spotipy.Spotify, playlist_id: str) -> str:
    """Create a YouTube Music playlist based on Spotify playlist details."""
    playlist_details = sp.playlist(playlist_id)
    playlist_title = playlist_details["name"] if playlist_details else "New Playlist"
    playlist_description = playlist_details["description"] if playlist_details else ""
    return str(yt.create_playlist(playlist_title, playlist_description))


def transfer_playlist(spotify_playlist_uri: str) -> None:
    """Transfer a Spotify playlist to YouTube Music."""
    sp = get_spotify_client()
    yt = get_youtube_client()

    # Get Spotify playlist tracks
    tracks = get_spotify_playlist_tracks(sp, spotify_playlist_uri)

    # Create YouTube Music playlist
    new_playlist_id = create_youtube_playlist(yt, sp, spotify_playlist_uri)

    # Transfer tracks
    for idx, item in enumerate(tracks, 1):
        track = item["track"]
        query = f"{track['name']} {track['artists'][0]['name']}"
        search_results = yt.search(query, filter="songs", limit=1)

        if search_results:
            print(f"{idx} Adding {track['name']}")
            video_id = search_results[0]["videoId"]
            yt.add_playlist_items(new_playlist_id, [video_id])
        else:
            print(f"{idx} Didn't find {track['name']}")


if __name__ == "__main__":
    PLAYLIST_URI = "spotify:playlist:73vmEitV1vfKQK25m1uCp5"
    transfer_playlist(PLAYLIST_URI)
