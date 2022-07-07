from datetime import date, timedelta
import boto3

def upload_csv_to_s3(export_file_path: str) -> None:
    """Upload extracted .csv file to s3 bucket."""
    s3_client = boto3.client('s3')
    dateMinusOne = (date.today() - timedelta(days=1)).strftime('%m-%d-%Y') + '.csv'
    s3_client.upload_file(export_file_path, "spotifystreaming", dateMinusOne)
