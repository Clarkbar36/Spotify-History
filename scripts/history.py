import ast
from typing import List
from os import listdir
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import exceptions
import configparser
import datetime
from datetime import timedelta
from pytz import timezone


def get_streamings(path: str = 'json') -> List[dict]:
    files = ['json/' + x for x in listdir(path)
             if x.split('.')[0][:-1] == 'StreamingHistory']

    all_streamings = []

    for file in files:
        with open(file, 'r', encoding='UTF-8') as f:
            new_streamings = ast.literal_eval(f.read())
            all_streamings += [streaming for streaming
                               in new_streamings]
    return all_streamings


test = get_streamings()

history = pd.json_normalize(test)

history['secondsPlayed'] = round(history['msPlayed'] / 1000).astype(int)
history['minutesPlayed'] = round(history['msPlayed'] / 60000).astype(int)
history_reduced = history[(history['secondsPlayed'] > 30) & (history['minutesPlayed'] < 10)].copy()
history_reduced['playedAt'] = pd.to_datetime(history_reduced['endTime'], format='%Y-%m-%dT%H:%M:%S') \
                                  .dt.tz_localize('US/Eastern') - history_reduced['msPlayed'].astype('timedelta64[ms]')

unique_plays = history_reduced.drop_duplicates(subset=['artistName', 'trackName'])
unique_plays = unique_plays[['artistName', 'trackName']]

config = configparser.ConfigParser()
config.read('spotify.ini')

cache_handler = spotipy.cache_handler.CacheFileHandler()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["Spotify"]["SPOTIFY_CLIENT_ID"],
                                               client_secret=config["Spotify"]["SPOTIFY_CLIENT_SECRET"],
                                               redirect_uri=config["Spotify"]["SPOTIFY_REDIRECT_URI"],
                                               scope="user-read-recently-played",
                                               cache_handler=cache_handler,
                                               show_dialog=True))

basic_info = []
for a, b in unique_plays.itertuples(index=False):
    q = str("artist:%s track:%s" % (a, b))
    try:
        track_search = sp.search(q, type="track", limit=1)
        basic_track_info = pd.json_normalize(track_search, ['tracks', 'items'])
        basic_info.append(basic_track_info)
    except spotipy.exceptions.SpotifyException as e:
        continue

streaming_history = pd.concat(basic_info)

# Load file
streaming_history = pd.read_csv('csv\history.csv')
streaming_history = streaming_history.rename(
    columns={'id': 'trackID', 'name': 'trackName', 'popularity': 'trackPopularity',
             'album.id': 'albumID', 'album.name': 'albumName',
             'album.release_date': 'albumReleaseDate', 'duration_ms': 'durationMs'})
# rename columns for joining and rest of process
streaming_history = streaming_history[['albumID', 'albumName', 'albumReleaseDate',
                                       'durationMs', 'trackID', 'trackName', 'trackPopularity']]

stream_history_joined = history_reduced.merge(streaming_history, on=["artistName", "trackName"], how="left")
# streaming_history.to_csv(os.path.join(subdir, 'history.csv'), index=False)
# TODO: need ini file to run the trackIDs through to find the artist, then I can merge to the history file
# TODO: Take IDs and run through the rest of the process to fill in gaps
