import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# def get_artist()

playlist_url = 'https://open.spotify.com/playlist/51gY6jFMaqpsPFFgVbGcvX?si=19584ccb85d24650'
playlist_id = playlist_url.split('/')[-1]
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# results = spotify.playlist_items(playlist_id)['tracks']['items'][0]['track']
results = spotify.playlist_items(playlist_id)['tracks']['items']

# print(json.dumps(results, indent=4, sort_keys=True))
playlist_dict = {}

for song in results:
    print(song['track']['name'])

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
