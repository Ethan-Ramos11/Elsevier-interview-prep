import boto3
import logging


def create_s3_connection():
    session = boto3.Session()
    s3 = session.client("s3")
    return s3


