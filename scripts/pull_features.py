import pandas as pd


def pull_features(spotify_conn, basic_info_recent):
    tracks_ids = basic_info_recent['trackID'].tolist()
    features = spotify_conn.audio_features(tracks_ids)
    norm_features = pd.json_normalize(features)
    track_features = norm_features[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                           'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'id',
                           'time_signature']].rename(columns={'id': 'trackID'})
    trackInfo = basic_info_recent[['trackID', 'trackName', 'trackPopularity', 'durationMs']].drop_duplicates()
    trackTable = trackInfo.merge(track_features, on="trackID", how="inner").drop_duplicates()
    return trackTable
