import ast
from typing import List
import os
from os import listdir
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser


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

from scripts.spotify_connect import connect_spotify

spotify_conn = connect_spotify()
tracks_ids = streaming_history['trackID'].unique().tolist()

track_history = []


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


for group in chunker(tracks_ids, 50):
    track_info = spotify_conn.tracks(group)

    artist_and_track = pd.json_normalize(
        data=track_info['tracks'],
        record_path='artists',
        meta=['id'],
        record_prefix='sp_artist_',
        meta_prefix='sp_track_',
        sep="_")

    artist_track = artist_and_track[['sp_artist_id', 'sp_artist_name', 'sp_track_id']] \
        .rename(
        columns={'sp_artist_id': 'artistID', 'sp_artist_name': 'artistName',
                 'sp_track_id': 'trackID'}).drop_duplicates()
    track_history.append(artist_track)

track_history = pd.concat(track_history)

uni_track_history = track_history.drop_duplicates(subset=['trackID'])
uni_track_history = uni_track_history[['artistName', 'trackID']]
streaming_history = streaming_history.merge(uni_track_history, on=["trackID", "trackID"], how="left")

stream_history_joined = history_reduced.merge(streaming_history, on=["artistName", "trackName"],
                                              how="left").drop_duplicates()
stream_history_joined = stream_history_joined[stream_history_joined['albumID'].notna()].drop('artistName', 1)
stream_history_joined_artist = stream_history_joined.merge(track_history, on=["trackID", "trackID"], how="left")

features = []
tracks_ids = stream_history_joined_artist['trackID'].unique().tolist()
for group in chunker(tracks_ids, 50):
    features_pull = spotify_conn.audio_features(group)
    norm_features = pd.json_normalize(features_pull)
    track = norm_features[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                           'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'id',
                           'time_signature']].rename(columns={'id': 'trackID'})
    features.append(track)

feature_history = pd.concat(features)

stream_history_joined_artist_features = stream_history_joined_artist.merge(feature_history, on=["trackID", "trackID"],
                                                                           how="left")

artists = []
artist_ids = stream_history_joined_artist_features['artistID'].unique().tolist()
for group in chunker(artist_ids, 50):
    artist = spotify_conn.artists(group)
    norm_artist = pd.json_normalize(artist['artists'])
    info_artist = norm_artist[['genres', 'id', 'popularity', 'followers.total']] \
        .rename(columns={'id': 'artistID', 'popularity': 'artistPopularity', 'followers.total': 'followers'})
    artists.append(info_artist)
artist_history = pd.concat(artists)

all_info = stream_history_joined_artist_features.merge(artist_history, on=["artistID", "artistID"], how="left")

all_info['trackHashID'] = all_info['playedAt'].dt.strftime("%Y%m%d%H%M%S").astype(str) + all_info['trackID']
all_info['hashID'] = all_info['trackHashID'] + all_info['artistID']
all_info = all_info.drop_duplicates(subset=['hashID'])

all_info = all_info[
    ["playedAt", "albumID", "albumName", "albumReleaseDate", "durationMs", "trackID", "trackName", "trackPopularity",
     "artistID", "artistName", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
     "instrumentalness", "liveness", "valence", "tempo", "time_signature", "genres", "artistPopularity", "followers",
     "trackHashID", "hashID"]]

root = 'C:\\Users\\aclark5\\PycharmProjects\\Spotify-History'
csv = 'csv'
subdir = os.path.join(root, csv)
all_info.to_csv(os.path.join(subdir, "final_history.csv"), index=False)
