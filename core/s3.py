import boto3

s3 = boto3.client("s3")


CDN_URL = "https://i.bozbalci.me/"


def upload_to_s3(file_obj, bucket_name, key):
    s3.upload_fileobj(file_obj, bucket_name, key)
