import spotipy
from spotipy.oauth2 import SpotifyOAuth
import configparser
import pandas as pd


config = configparser.ConfigParser()
config.read('spotify.ini')

cache_handler = spotipy.cache_handler.CacheFileHandler()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config["Spotify"]["SPOTIFY_CLIENT_ID"],
                                               client_secret=config["Spotify"]["SPOTIFY_CLIENT_SECRET"],
                                               redirect_uri=config["Spotify"]["SPOTIFY_REDIRECT_URI"],
                                               scope="user-read-recently-played",
                                               cache_handler=cache_handler,
                                               show_dialog=True))

recently_played = sp.current_user_recently_played(10)

initial_pull = pd.json_normalize(
    data=recently_played['items'],
    sep="_")

basic_info = initial_pull[['played_at', 'track_album_id', 'track_album_name', 'track_album_release_date',
                           'track_duration_ms', 'track_id', 'track_name', 'track_popularity']] \
    .rename(columns={'played_at': 'playedAt', 'track_album_id': 'albumID', 'track_album_name': 'albumName',
                     'track_album_release_date': 'albumReleaseDate', 'track_duration_ms': 'durationMs',
                     'track_id': 'trackID', 'track_name': 'trackName', 'track_popularity': 'trackPopularity'})

tracks_ids = basic_info['trackID'].tolist()

track_info = sp.tracks(tracks_ids)

artist_and_track = pd.json_normalize(
    data=track_info['tracks'],
    record_path='artists',
    meta=['id'],
    record_prefix='sp_artist_',
    meta_prefix='sp_track_',
    sep="_")

artist_track_info = artist_and_track[['sp_artist_id', 'sp_artist_name', 'sp_track_id']] \
    .rename(columns={'sp_artist_id': 'artistID', 'sp_artist_name': 'artistName', 'sp_track_id': 'trackID'})

artist_ids = artist_track_info['artistID'].unique().tolist()

features = sp.audio_features(tracks_ids)
norm_features = pd.json_normalize(features)
track_features = norm_features[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                                'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'id',
                                'time_signature']].rename(columns={'id': 'trackID'})

artist = sp.artists(artist_ids)
norm_artist = pd.json_normalize(artist['artists'])
artist_info = norm_artist[['genres', 'id', 'popularity', 'followers.total']] \
    .rename(columns={'id': 'artistID', 'popularity': 'artistPopularity', 'followers.total': 'followers'})

all_info = basic_info.merge(artist_track_info, on="trackID", how="inner").merge(track_features, on="trackID",
                                                                                how="inner").merge(artist_info,
                                                                                                   on="artistID",
                                                                                                   how="inner")
all_info['hashID'] = all_info['playedAt'] + all_info['trackID']
