import pandas as pd


def pull_artist_info(spotify_conn, artist_track):
    artist_ids = artist_track['artistID'].unique().tolist()
    artist = spotify_conn.artists(artist_ids)
    norm_artist = pd.json_normalize(artist['artists'])
    info_artist = norm_artist[['genres', 'id', 'popularity', 'followers.total']] \
        .rename(columns={'id': 'artistID', 'popularity': 'artistPopularity', 'followers.total': 'followers'})
    return info_artist