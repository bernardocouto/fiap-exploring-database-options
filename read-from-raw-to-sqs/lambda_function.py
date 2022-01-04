from common.sqs import SQS

import os

def lambda_handler(event, context):

    # TODO: Sento to SQS
    print(event)

    queue_name = os.environ.get('AWS_SQS_RAW_JSON_TO_FIREHOSE', 'row-json-to-firehose')

    sqs = SQS()
    queue_url = sqs.get_queue_url(queue_name=queue_name)
    sqs.send_message(message_body=None, queue_url=queue_url)
