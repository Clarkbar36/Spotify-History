import pandas as pd

history = pd.read_csv("/csv/final_history.csv", parse_dates=['playedAt'])

streamTable = history[['playedAt', 'albumID', 'trackID', 'trackHashID']].rename(
    columns={'trackHashID': 'hashID'}).drop_duplicates()
albumTable = history[['albumID', 'albumName', 'albumReleaseDate']].drop_duplicates()
trackTable = history[
    ['trackID', 'trackName', 'trackPopularity', 'durationMs', 'danceability', 'energy', 'key', 'loudness',
     'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
     'time_signature']].drop_duplicates()

artistTable = history[['artistID', 'artistName', 'trackID', 'artistPopularity', 'genres', 'followers']]
artistTable['genres'] = artistTable['genres'].astype('str')
artistTable['genres'] = artistTable['genres'].str.strip('[]')
artistTable['genres'] = artistTable['genres'].str.replace(r'\'', '', regex=True)
genres = artistTable['genres'].str.split(',', n =5, expand=True).add_prefix('genre').fillna('').drop('genre5', axis=1)
artistTable = artistTable.join(genres).drop('genres', axis=1)
artistTable = artistTable.drop_duplicates()
artistTable['uniqArtID'] = artistTable['artistID'] + artistTable['trackID']

streamTable.to_sql('stg.spotifyStream', engine, index=False, dtype={'playedAt': sa.DateTime()})
albumTable.to_sql('stg.spotifyAlbums', engine, index=False)
trackTable.to_sql('stg.spotifyTracks', engine, index=False)
artistTable.to_sql('prd.spotifyArtist', engine, index=False)
