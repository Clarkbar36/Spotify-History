from datetime import datetime, date, timedelta
import os
import inspect


def save_csv(streamT, albumT, artistT, trackT):
    to_save = [streamT, albumT, artistT, trackT]
    names = ['streams', 'ablums', 'artists', 'tracks']

    for df, n in zip(to_save, names):
        root = 'C:\\Users\\aclark5\\PycharmProjects\\Spotify-History'
        csv = 'csv'
        subdir = os.path.join(root, csv)
        datesv = n + date.today().strftime('%m-%d-%Y') + '.csv'
        export_path = os.path.join(subdir, datesv)
        df.to_csv(os.path.join(subdir, datesv), index=False)

    return export_path
