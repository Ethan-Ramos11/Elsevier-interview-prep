import boto3
import logging
from datetime import datetime
import os
import questionary 
logging.basicConfig(filename='aws.log',
                    encoding='utf-8', level=logging.INFO)


def create_s3_connection():
    """
    Creates and returns an S3 client using boto3.

    Returns:
        boto3.client: Configured S3 client instance
    """
    session = boto3.Session()
    s3 = session.client("s3")
    return s3


def log_error(action, e):
    """
    Logs errors to aws.log file

    Args:
        action (str): Description of the action that failed
        e (Exception): The exception that was raised
    """
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.debug(f'Failed action at {timestamp}')
    logger.info(f'Attempted {action}')
    logger.error(f'Error: {e}')


def log_success(action):
    """
    Logs success to aws.log file

    Args:
        action (str): Description of the action that was completed 
    """
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Successfully completed {action} at {timestamp}')


def view_all_active_buckets():
    try:
        s3 = create_s3_connection()
        buckets = s3.list_buckets()
        bucket_names = []
        for bucket in buckets["Buckets"]:
            print(bucket["Name"])
            bucket_names.append(bucket["Name"])
        log_success("Viewing buckets")
        return bucket_names
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


def generate_object_name(file_type, file_path):
    """
    Generates S3 object name based on file type and path.
    Organizes files into type-specific folders (docs/, texts/, pdfs/).

    Args:
        file_type (str): Type of file (doc, docx, txt, pdf)
        file_path (str): Full path to the file

    Returns:
        str: S3 object name with appropriate folder prefix
    """
    split_path = file_path.split("/")
    if file_type == "docx" or file_type == "doc":
        return f"docs/{split_path[-1]}"
    elif file_type == "txt":
        return f"texts/{split_path[-1]}"
    else:
        return f"pdfs/{split_path[-1]}"


def upload_file(bucket_name, file_path, file_type, bucket_list):
    """
    Uploads a file to specified S3 bucket

    Args:
        bucket_name (str): Name of the S3 bucket
        file_path (str): Path to the file to upload
        file_type (str): Type of file (txt, pdf, doc, docx)

    Raises:
        ValueError: If file type is invalid
        FileNotFoundError: If file doesn't exist
    """
    if file_type not in ["txt", "pdf", "doc", "docx"]:
        raise ValueError("Must be a document file type")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if bucket_name not in bucket_list:
        raise ValueError("Bucket name is not in buckets")
    object_name = generate_object_name(file_type, file_path)
    try:
        s3 = create_s3_connection()
        s3.upload_file(file_path, bucket_name, object_name)
        log_success(f"Uploading {file_path} to bucket {bucket_name}")
    except Exception as e:
        log_error("Upoading bucket", e)

def view_objects(bucket_name):
    try:
        s3 = create_s3_connection()
        objects = s3.list_objects(Bucket=bucket_name)
        object_key = []
        if "Contents" in objects and objects["Contents"]:
            print("---------")
            print(f"{bucket_name} content: ")
            for obj in objects["Contents"]:
                object_key.append(obj["Key"])
                print(obj["Key"])
        else:
            print(f'No objects in {bucket_name}')
        log_success(f"Displayed {bucket_name} content")
        return object_key
    except Exception as e:
        log_error("Could not view bucket content", e)

def delete_object(bucket_name, object_key):
    try:
        s3 = create_s3_connection()
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        log_success(f"Deleted {object_key} from {bucket_name}")
    except Exception as e:
        log_error("Deleting object", e)

def delete_bucket(bucket_name):
    try:
        s3 = create_s3_connection()
        objects = s3.list_objects(Bucket=bucket_name)
        if objects["Contents"]:
            for obj in objects["Contents"]:
                delete_object(bucket_name, obj["Key"])

        s3.delete_bucket(Bucket=bucket_name)
        log_success(f"Deleted bucket {bucket_name}")
    except Exception as e:
        log_error("Deleting bucket", e)
