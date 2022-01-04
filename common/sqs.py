import boto3
import logging

logger = logging.getLogger(__name__)

class SQS:

    def __init__(self):
        self.client = boto3.client('sqs')

    def get_queue_url(self, queue_name):
        try:
            queue_url = self.client.get_queue_url(
                QueueName=queue_name
            )
            return queue_url.get('QueueUrl')
        except self.client.exceptions.QueueDoesNotExist as exception:
            logger.error(f'Queue does not exist: {exception}')

    def send_message(self, message_body, queue_url):
        try:
            self.client.send_message(
                MessageBody=message_body,
                QueueUrl=queue_url
            )
        except self.client.exceptions.InvalidMessageContents as exception:
            logger.error(f'Invalid message contents: {exception}')
        except self.client.exceptions.UnsupportedOperation as exception:
            logger.error(f'Unsupported operation: {exception}')
