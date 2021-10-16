import json
import logging
import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import urllib.request

DEST_PATH = 'E:\Repos\Downloaded_Music'

dir = os.getcwd()
# print(dir)

os.chdir('../')
dir = os.getcwd()
# print(dir)

logger = logging.getLogger('[Python Spotify Downloader]')
logger.setLevel(logging.DEBUG)
logname = 'Logging/spotify_downloader/spotify_downloader.log'
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.FileHandler(logname)
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_playlist_song_artist(playlist_raw):
    get_playlist_list = []
    playlist_get = playlist_raw['tracks']['items']

    for song in playlist_get:
        detail_list = []
        song_title = song['track']['name']
        detail_list.append(get_youtube_search_join(song_title))
        for artist in song['track']['artists']:
            detail_list.append(get_youtube_search_join(artist['name']))
        get_playlist_list.append(detail_list)
        logger.info("Adding the following song and artist to our list: \n {0}".format(detail_list))

    return get_playlist_list


def get_youtube_search_join(raw_search_string):
    logger.info("Processing this raw search string, into a suffix for a YouTube search: {0}".format(raw_search_string))
    search_string_split = raw_search_string.split(" ")
    search_string_joined = "+".join(search_string_split)

    logger.info("Processed string {0}".format(search_string_joined))
    return search_string_joined


sys.path
sys.path.append('E:\Repos\Spotify_DL')

# print(sys.path)
search_list = "I+Believe+in+a+Thing+Called+Love+The+Darkness"
search_list_found = "Fergalicious+Fergie+will.i.am"


playlist_url = 'https://open.spotify.com/playlist/51gY6jFMaqpsPFFgVbGcvX?si=19584ccb85d24650'
playlist_id = playlist_url.split('/')[-1]
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.playlist_items(playlist_id)
print(results)
print(len(results))
print(results['next'])

# # Loops to ensure I get every track of the playlist
# while results['next']:
#     results = self.sp.next(results)
#     tracks.extend(results['items'])

# playlist_results = get_playlist_song_artist(results)

# print(json.dumps(playlist_results, indent=4, sort_keys=True))


# def check_song_exists(search_list):
# for filename in os.listdir(DEST_PATH):
#     print(filename)
#         # for file in directory:"
# #             split the file name on spaces into a list
#     #         iterate on the file name list to see if any matches
# #         Check if a file matches the sear
#
