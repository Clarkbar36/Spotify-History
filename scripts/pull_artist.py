import pandas as pd


def pull_artist_info(spotify_conn, artist_track):
    artist_ids = artist_track['artistID'].unique().tolist()
    if len(artist_ids) > 50:
        artist_a = spotify_conn.artists(artist_ids[0:49])
        norm_artist_a = pd.json_normalize(artist_a['artists'])
        artist_b = spotify_conn.artists(artist_ids[49:])
        norm_artist_b = pd.json_normalize(artist_b['artists'])
        norm_artist = pd.concat([norm_artist_a, norm_artist_b])

    else:
        artist = spotify_conn.artists(artist_ids)
        norm_artist = pd.json_normalize(artist['artists'])

    info_artist = norm_artist[['genres', 'id', 'popularity', 'followers.total']] \
        .rename(columns={'id': 'artistID', 'popularity': 'artistPopularity', 'followers.total': 'followers'})
    return info_artist

