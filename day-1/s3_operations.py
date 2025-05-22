import boto3
import logging
from datetime import datetime

logging.basicConfig(filename='example.log',
                    encoding='utf-8', level=logging.INFO)


def create_s3_connection():
    session = boto3.Session()
    s3 = session.client("s3")
    return s3


def log_error(action, e):
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.debug(f'Failed action at {timestamp}')
    logger.info(f'Attempted {action}')
    logger.error(f'Error: {e}')


def log_success(action):
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Successfully completed {action} at {timestamp}')


def view_all_active_buckets():
    try:
        s3 = create_s3_connection()
        buckets = s3.list_buckets()
        for bucket in buckets["Buckets"]:
            print(bucket["Name"])
        log_success("Viewing buckets")
    except Exception as e:
        log_error("Viewing buckets", e)


def create_new_bucket():
    try:
        s3 = create_s3_connection()
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M%S")
        bucket_name = f"ethan-test{timestamp}"
        region = "us-east-2"
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                         'LocationConstraint': region})
        log_success(f"Creating new bucket {bucket_name}")
        return bucket_name
    except Exception as e:
        log_error("Creating new bucket", e)


