import json
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import urllib.request

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

    return get_playlist_list


def get_youtube_search_join(raw_search_string):
    search_string_split = raw_search_string.split(" ")
    search_string_joined = "+".join(search_string_split)

    return search_string_joined


def get_youtube_url(search_list):
    searh_params = "+".join(search_list)
    search_results = urllib.request.urlopen("https://www.youtube.com/results?search_query={0}".format(searh_params))

    video_ids = re.findall(r"watch\?v=(\S{11})", search_results.read().decode())
    youtube_link = "https://www.youtube.com/watch?v=" + video_ids[0]

    return youtube_link


playlist_url = 'https://open.spotify.com/playlist/51gY6jFMaqpsPFFgVbGcvX?si=19584ccb85d24650'
playlist_id = playlist_url.split('/')[-1]
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.playlist_items(playlist_id)['tracks']['items'][0]['track']
results = spotify.playlist_items(playlist_id)

playlist_results = get_playlist_song_artist(results)

print(json.dumps(playlist_results, indent=4, sort_keys=True))

for track in playlist_results:
    print(get_youtube_url(track))
# print(playlist_dict)

# print(json.dumps(playlist_dict, indent=4, sort_keys=True))
# song_title = results['name']

# artists_list = results['artists']
# print(artists_list)
# for artist in artists_list:
#     print(artist['name'])
# albums = results['items']
# while results['next']:
#     results = spotify.next(results)
#     albums.extend(results['items'])
#
# for album in albums:
#     print(album['name'])


# url = 'https://www.youtube.com/watch?v=5T0utQ-XWGY'
# dest_path = '/mnt/c/Users/adamr/My Documents/My Music/Downloaded_Music/Ready_To_Stumble'
# yt_dl_cmd = 'youtube-dl -v -f bestaudio {0} ' \
#             '--external-downloader ffmpeg --external-downloader-args "-ss starttime -to endtime" -o ' \
#             '"{1}/%(title)s-%(id)s.%(ext)s"'.format(url, dest_path)
#
# print(yt_dl_cmd)
#
# os.system(yt_dl_cmd)