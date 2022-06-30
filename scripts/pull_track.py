import pandas as pd


def pull_track_info(spotify_conn, basic_info_recent):
    tracks_ids = basic_info_recent['trackID'].tolist()

    track_info = spotify_conn.tracks(tracks_ids)

    artist_and_track = pd.json_normalize(
        data=track_info['tracks'],
        record_path='artists',
        meta=['id'],
        record_prefix='sp_artist_',
        meta_prefix='sp_track_',
        sep="_")

    artist_track = artist_and_track[['sp_artist_id', 'sp_artist_name', 'sp_track_id']]\
        .rename(columns={'sp_artist_id': 'artistID', 'sp_artist_name': 'artistName', 'sp_track_id': 'trackID'}).drop_duplicates()

    return artist_track
