import json
import boto3
import logging

logger = logging.getLogger(__name__)


class Firehose:

    def __init__(self):
        self.client = boto3.client('firehose')

    def put_record(self, delivery_stream_name, record):
        try:
            self.client.put_record(
                DeliveryStreamName=delivery_stream_name,
                Record={'Data': record}
            )
        except self.client.exceptions.InvalidArgumentException as exception:
            logger.error(f'Invalid argument: {exception}')
        except self.client.exceptions.InvalidKMSResourceException as exception:
            logger.error(f'Invalid KMS resource: {exception}')
        except self.client.exceptions.ResourceNotFoundException as exception:
            logger.error(f'Resource not found: {exception}')
        except self.client.exceptions.ServiceUnavailableException as exception:
            logger.error(f'Service unavailable: {exception}')
