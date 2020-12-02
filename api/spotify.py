
import json

import requests
from config.const import SPOTIFY_HEADERS, SPOTIFY_URLS
from config.tokens import SPOTIFY_OAUTH_TOKEN, SPOTIFY_USER_ID


class SpotifyAPI:

    name = 'spotify'

    @staticmethod
    def __get_request_headers():
        headers = SPOTIFY_HEADERS
        headers["Authorization"] = headers["Authorization"].format(spotify_oauth_token=SPOTIFY_OAUTH_TOKEN)
        return headers

    @staticmethod
    def __get_playlists_url():
        return SPOTIFY_URLS["playlists_url"]

    @staticmethod
    def __get_tracks_url():
        return SPOTIFY_URLS["tracks_url"]

    @classmethod
    def _ARS_retrieve_track_info(cls, song_info):
        try:
            track_id = song_info['metadata']['music'][0]['external_metadata']['spotify']['track']['id']
        except (KeyError, IndexError):
            return None
        return 'spotify:track:{}'.format(track_id)

    @classmethod
    def retrieve_track_info(cls, ARS_name, song_info):
        if ARS_name == 'acrcloud':
            return cls._ARS_retrieve_track_info(song_info)
        # raise ARS_NOT_RECOGNISED but who cares

    @classmethod
    def _retrieve_playlist_id(cls, playlist_request):
        return json.loads(playlist_request.text)['id']

    @classmethod
    def get_playlist_id(cls, playlist_request):
        return cls._retrieve_playlist_id(playlist_request)

    @classmethod
    def create_playlist(cls, playlist_name: str, description="", public=False):
        playlists_url = cls.__get_playlists_url().format(spotify_user_id=SPOTIFY_USER_ID)
        request_body = {
            "name": playlist_name,
            "description": description,
            "public": public
        }
        payload = json.dumps(request_body)
        return requests.post(playlists_url, data=payload, headers=cls.__get_request_headers())

    @classmethod
    def add_tracks_to_playlist(cls, tracks_ids: str, playlist_id: str):
        tracks_url = cls.__get_tracks_url().format(playlist_id=playlist_id)
        params = {
            "uris": ",".join(tracks_ids)
        }
        return requests.post(tracks_url, params=params, headers=cls.__get_request_headers())
