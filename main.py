
import argparse

from logic.processor import MainProcessor

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--folder',
                    action="store",
                    dest="media_folder",
                    type=str,
                    help='Folder with media to import')

parser.add_argument('-p', '--playlist-name',
                    action="store",
                    dest="playlist_name",
                    type=str,
                    help='Playlist name')

parser.add_argument('-e', '--extensions',
                    action="store",
                    dest="extension_list",
                    nargs='*',
                    default=['*.mp3', '*.wav', '*.aac', '*.m4a'],
                    help='Media extensions')

parser.add_argument('-o', '--output-file',
                    action="store",
                    dest="output_file",
                    type=str,
                    default='Output.txt',
                    help='Output file')

# There is only one option for each argument so far
# parser.add_argument('-ars', type=str, help='Audio recognition service')
# parser.add_argument('-msp', type=str, help='Media service provider')


def main():
    console_args = parser.parse_args()
    processor = MainProcessor(console_args)
    processor.process()


if __name__ == '__main__':
    main()
