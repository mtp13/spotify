import json
from ytmusicapi import YTMusic, OAuthCredentials

# Load OAuth credentials from oauth.json
with open("youtube.json", "r") as f:
    oauth_data = json.load(f)

client_id = oauth_data["client_id"]
client_secret = oauth_data["client_secret"]

ytmusic = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=client_id, client_secret=client_secret
    ),
)

playlists = ytmusic.get_library_playlists()
for playlist in playlists:
    print(playlist["title"])
    if playlist["title"] == "test":
        print("found")
        ytmusic.delete_playlist(playlist["playlistId"])
    # ytmusic.delete_playlist(playlist["playlistId"])
    # ytmusic.add_playlist_items(playlist["playlistId"], ["https://www.youtube.com/watch?v=0J2QdDbelmY"])
    # ytmusic.edit_playlist(playlist["playlistId"], "new title", "new description")
    # ytmusic.remove_playlist_items(playlist["playlistId"], [search_results[0]["videoId"]])
