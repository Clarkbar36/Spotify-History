import pandas as pd


def pull_artist_info(spotify_conn, basic_info_recent):

    tracks_ids = basic_info_recent['trackID'].tolist()

    track_info = spotify_conn.tracks(tracks_ids)

    artist_and_track = pd.json_normalize(
        data=track_info['tracks'],
        record_path='artists',
        meta=['id'],
        record_prefix='sp_artist_',
        meta_prefix='sp_track_',
        sep="_")

    artist_track = artist_and_track[['sp_artist_id', 'sp_artist_name', 'sp_track_id']] \
        .rename(columns={'sp_artist_id': 'artistID', 'sp_artist_name': 'artistName',
                         'sp_track_id': 'trackID'}).drop_duplicates()
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
    artistTable = artist_track.merge(info_artist, on="artistID", how="inner")
    artistTable['genres'] = artistTable['genres'].astype('str')
    artistTable['genres'] = artistTable['genres'].str.strip('[]')
    artistTable['genres'] = artistTable['genres'].str.replace(r'\'', '', regex=True)
    genres = artistTable['genres'].str.split(',', n=5, expand=True).add_prefix('genre').fillna('').drop('genre5',
                                                                                                        axis=1)
    artistTable = artistTable.join(genres).drop('genres', axis=1)
    artistTable['uniqArtID'] = artistTable['artistID'] + artistTable['trackID']
    return artistTable

