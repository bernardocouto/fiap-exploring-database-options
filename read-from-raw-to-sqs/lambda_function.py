from common.sqs import SQS

import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info('Start of running AWS Lambda')

    sqs = SQS()
    queue_name = os.environ.get('AWS_SQS_RAW_JSON_TO_FIREHOSE', 'raw-json-to-firehose')
    queue_url = sqs.get_queue_url(queue_name=queue_name)

    if 'Records' in event:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            message_body = json.dumps({
                'bucket': bucket,
                'key': key
            })
            logger.info('Sending the message to AWS SQS')
            sqs.send_message(message_body=message_body, queue_url=queue_url)

    logger.info('End of AWS Lambda run')
