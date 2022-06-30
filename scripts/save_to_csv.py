from datetime import datetime, date, timedelta
import os


def save_csv(most_recent):
    root = 'C:\\Users\\aclark5\\PycharmProjects\\Spotify-History'
    csv = 'csv'
    subdir = os.path.join(root, csv)
    dateMinusOne = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y') + '.csv'
    most_recent.to_csv(os.path.join(subdir, dateMinusOne), index=False)
