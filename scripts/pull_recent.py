import pandas as pd

pd.options.mode.chained_assignment = None


def pull_recently_played(spotify_conn):
    recently_played = spotify_conn.current_user_recently_played(50)

    initial_pull = pd.json_normalize(
        data=recently_played['items'],
        sep="_")

    basic_info_recent = initial_pull[['played_at', 'track_album_id', 'track_album_name', 'track_album_release_date',
                                      'track_duration_ms', 'track_id', 'track_name', 'track_popularity']] \
        .rename(columns={'played_at': 'playedAt', 'track_album_id': 'albumID', 'track_album_name': 'albumName',
                         'track_album_release_date': 'albumReleaseDate', 'track_duration_ms': 'durationMs',
                         'track_id': 'trackID', 'track_name': 'trackName', 'track_popularity': 'trackPopularity'})

    streamTable = basic_info_recent[['playedAt', 'albumID', 'trackID']]
    streamTable['playedAt'] = pd.to_datetime(streamTable['playedAt'], format='%Y-%m-%dT%H:%M:%S.%f').dt.tz_convert(
        'US/Eastern')
    streamTable['hashID'] = streamTable['playedAt'].dt.strftime("%Y%m%d%H%M%S").astype(str) + streamTable[
        'trackID']
    albumTable = basic_info_recent[['albumID', 'albumName', 'albumReleaseDate']].drop_duplicates()

    return basic_info_recent, streamTable, albumTable
