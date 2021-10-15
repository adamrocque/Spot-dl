import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import urllib.request

sys.path
sys.path.append('E:\Repos\Spotify_DL')

FAIL_DICT = {}

PLAYLIST_LENGTH = 0

# Change working directory so logs can hit the logging folder
os.chdir('../')

# Check if the logging directory exists, create if not
if not os.path.isdir('Logging/spotify_downloader/'):
    os.mkdir('Logging/spotify_downloader/')

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


def get_youtube_url(search_list):
    logger.info("Received this search string: ".format(search_list))
    search_params = "+".join(search_list)

    logger.info("Searching with the following link: "
                "\nhttps://www.youtube.com/results?search_query={0}".format(search_params))
    search_results = urllib.request.urlopen("https://www.youtube.com/results?search_query={0}".format(search_params))

    # Using RegEx to search for all video results that have an 11 AlphaNumeric code, revealing the video URL suffix
    video_ids = re.findall(r"watch\?v=(\S{11})", search_results.read().decode())
    video_ids[0]

    return video_ids, search_params


playlist_url = 'https://open.spotify.com/playlist/51gY6jFMaqpsPFFgVbGcvX?si=19584ccb85d24650'
playlist_id = playlist_url.split('/')[-1]
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.playlist_items(playlist_id)

playlist_results = get_playlist_song_artist(results)

print(json.dumps(playlist_results, indent=4, sort_keys=True))

for track_count, track in enumerate(playlist_results):
    try:
        # print(get_youtube_url(track))
        video_ids_get, search_params_get = get_youtube_url(track)
        for vid_trial_count, video in enumerate(video_ids_get):
            # video_suffix = get_youtube_url(track)
            url = "https://www.youtube.com/watch?v=" + video

            dest_path = '/Downloaded_Music'
            yt_dl_cmd = 'youtube-dl -v -f bestaudio {0} ' \
                        '--external-downloader ffmpeg --external-downloader-args "-ss starttime -to endtime" -o ' \
                        '"{1}/%(title)s.%(ext)s"'.format(url, dest_path)
            try:
                print("Downloading song {0} of {1}".format(track_count+1, len(playlist_results)))
                logger.info("Downloading song {0} of {1}".format(track_count+1, len(playlist_results)))
                os.system(yt_dl_cmd)
                break
            except Exception as e:
                logger.exception("Encountered an issue: {0}".format(e))
                FAIL_DICT[search_params_get[vid_trial_count]] = e

    except Exception as e:
        logger.exception("Encountered an issue: {0}".format(e))

    finally:
        logger.info("These are the files which had issues: {0}".format(json.dumps(FAIL_DICT, indent=4, sort_keys=True)))
