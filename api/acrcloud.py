
from config.const import ARCLOUD_URLS
from config.tokens import ACCESS_KEY, ACCESS_SECRET

from acrcloud.recognizer import ACRCloudRecognizer


class ARCloudApi:

    name = 'acrcloud'

    @classmethod
    def __get_acrcloud(cls):
        return ACRCloudRecognizer(cls.__get_acrcloud_config())

    @staticmethod
    def __get_acrcloud_config():
        return {
            'host': ARCLOUD_URLS['host'],
            'access_key': ACCESS_KEY,
            'access_secret': ACCESS_SECRET,
            'debug': False,
            'timeout': 10
        }

    @classmethod
    def get_song_info(cls, filename: str):
        return cls.__get_acrcloud().recognize_by_file(filename, 0)
