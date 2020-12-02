

SPOTIFY_URLS = {
    "playlists_url": 'https://api.spotify.com/v1/users/{spotify_user_id}/playlists',
    "tracks_url": 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks',
}

SPOTIFY_HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    "Authorization": "Bearer {spotify_oauth_token}"
}

ARCLOUD_URLS = {
    'host': '***PUT_HERE_YOUR_ARCLOUD_HOST_URL***'  # could be found here: console.acrcloud.com
}
