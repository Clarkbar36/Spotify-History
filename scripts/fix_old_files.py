import pandas as pd

old_file = pd.read_csv('csv/06-28-2022.csv')

old_file['trackHashID'] = old_file['hashID']
old_file['hashID'] = old_file['trackHashID'] + old_file['artistID']

cols = old_file.columns.tolist()

cols = ['playedAt', 'albumID', 'albumName', 'albumReleaseDate', 'durationMs', 'trackID', 'trackName', 'trackPopularity',
        'artistID', 'artistName', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'genres', 'artistPopularity', 'followers',
        'trackHashID', 'hashID']

old_file = old_file[cols]

old_file.to_csv('csv/06-28-2022.csv', index=False)
