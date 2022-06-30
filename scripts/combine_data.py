import pandas as pd


def combine_data(basic_info_recent, artist_track, track, info_artist):
    all_info = basic_info_recent.merge(artist_track, on="trackID", how="inner") \
        .merge(track, on="trackID", how="inner") \
        .merge(info_artist, on="artistID", how="inner")
    all_info['playedAt'] = pd.to_datetime(all_info['playedAt'], format='%Y-%m-%dT%H:%M:%S.%f').dt.tz_convert(
        'US/Eastern')
    all_info['trackHashID'] = all_info['playedAt'].dt.strftime("%Y%m%d%H%M%S").astype(str) + all_info['trackID']
    all_info['hashID'] = all_info['trackHashID'] + all_info['artistID']
    all_info = all_info.drop_duplicates(subset=['hashID'])
    return all_info
