from datetime import date, timedelta
import boto3
from io import StringIO


def upload_csv_to_s3(streamT, albumT, artistT, trackT):
    to_save = [streamT, albumT, artistT, trackT]
    names = ['streams', 'ablums', 'artists', 'tracks']
    """Upload extracted .csv file to s3 bucket."""
    s3_client = boto3.client('s3')
    for df, n in zip(to_save, names):
        datesv = n + "/" + date.today().strftime('%m-%d-%Y') + '_' + n + '.csv'
        bucket = "spotifystreaming" # already created on S3
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, datesv).put(Body=csv_buffer.getvalue())



