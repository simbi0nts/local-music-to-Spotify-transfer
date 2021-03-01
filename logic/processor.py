
import json
import os
from pathlib import Path

from api.acrcloud import ARCloudApi
from api.spotify import SpotifyAPI
from mutagen.mp3 import MP3
from pydub import AudioSegment


def get_audio_recognition_service_cls():
    return ARCloudApi


def get_media_service_provider_cls():
    return SpotifyAPI


class MainProcessor:

    def __init__(self, console_args, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cwd = os.getcwd()

        self.media_folder = console_args.media_folder
        self.playlist_name = console_args.playlist_name
        self.extension_list = console_args.extension_list
        self.output_file_name = console_args.output_file

        self.output_file = None
        if self.output_file_name:
            self.output_file = self.cwd + os.sep + self.output_file_name

        self.temp_file_name = 'TEMP_sample.mp3'
        self.temp_file = self.cwd + os.sep + self.temp_file_name

        self.batch_size = 10
        self.max_track_len = 600  # in seconds
        self.track_begin_cut = 20  # in seconds
        self.track_end_cut = 100  # in seconds

    @property
    def AudioRecognitionService(self):
        return get_audio_recognition_service_cls()

    @property
    def MediaServiceProvider(self):
        return get_media_service_provider_cls()

    def _is_file_valid(self, track):
        if track[-3:].upper() == 'MP3' and MP3(track).info.length > self.max_track_len:
            return False
        return True

    def _make_sample(self, track):
        return track[self.track_begin_cut * 1000: self.track_end_cut * 1000]

    def _retrieve_track_info(self, song_info):
        return self.MediaServiceProvider.retrieve_track_info(self.AudioRecognitionService.name, song_info)

    def process(self, **args):
        playlist_request = self.MediaServiceProvider.create_playlist(self.playlist_name)
        playlist_id = self.MediaServiceProvider.get_playlist_id(playlist_request)

        tracks_ids = []
        not_found_tracks = []

        os.chdir(self.media_folder)
        for extension in self.extension_list:
            for item in Path().rglob(extension):
                track = str(item)
                if not self._is_file_valid(track):
                    continue

                song = AudioSegment.from_file(track)
                song_sample = self._make_sample(song)
                song_sample.export(self.temp_file)

                song_info = self.AudioRecognitionService.get_song_info(self.temp_file)

                track_info = self._retrieve_track_info(json.loads(song_info))
                if track_info:
                    tracks_ids.append(track_info)
                else:
                    not_found_tracks.append(track)

                if len(tracks_ids) >= self.batch_size:
                    self.MediaServiceProvider.add_tracks_to_playlist(tracks_ids, playlist_id)
                    tracks_ids = []

        if len(tracks_ids):
            self.MediaServiceProvider.add_tracks_to_playlist(tracks_ids, playlist_id)

        def save_output():
            if self.output_file:
                with open(self.output_file, 'w+') as f:
                    f.write('Tracks that were not found: \n')
                    for track in not_found_tracks:
                        f.write("%s\n" % track)

        save_output()
        print("Nicely Done!")
