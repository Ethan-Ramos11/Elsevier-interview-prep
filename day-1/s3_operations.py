import boto3
import logging
from datetime import datetime

logging.basicConfig(filename='example.log',
                    encoding='utf-8', level=logging.DEBUG)


def create_s3_connection():
    session = boto3.Session()
    s3 = session.client("s3")
    return s3


def log(action, e):
    logger = logging.getLogger(__name__)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.debug(f'Failed action at {timestamp}')
    logger.info(f'Attempted {action}')
    logger.error(f'Error: {e}')


