from common.sqs import SQS

import json
import os

def lambda_handler(event, context):

    queue_name = os.environ.get('AWS_SQS_RAW_JSON_TO_FIREHOSE', 'raw-json-to-firehose')

    sqs = SQS()

    queue_url = sqs.get_queue_url(queue_name=queue_name)

    if 'Records' in event:
        for record in event['Records']:
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            message_body = json.dumps({
                'bucket': bucket,
                'key': key
            })
            sqs.send_message(message_body=message_body, queue_url=queue_url)

