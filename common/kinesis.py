import boto3
import logging

logger = logging.getLogger(__name__)

class Kinesis:

    def __init__(self):
        self.client = boto3.client('kinesis')

    def put_record(self):
        try:
            self.client.put_record(
                Data='',
                PartitionKey='',
                StreamName=''
            )
        except self.client.exceptions.InvalidArgumentException as exception:
            logger.error(f'Invalid argument: {exception}')
        except self.client.exceptions.KMSAccessDeniedException as exception:
            logger.error(f'KMS access denied: {exception}')
        except self.client.exceptions.KMSDisabledException as exception:
            logger.error(f'KMS disabled: {exception}')
        except self.client.exceptions.KMSInvalidStateException as exception:
            logger.error(f'KMS invalid state: {exception}')
        except self.client.exceptions.KMSNotFoundException as exception:
            logger.error(f'KMS not found: {exception}')
        except self.client.exceptions.KMSOptInRequired as exception:
            logger.error(f'KMS opt in required: {exception}')
        except self.client.exceptions.KMSThrottlingException as exception:
            logger.error(f'KMS throttling: {exception}')
        except self.client.exceptions.ProvisionedThroughputExceededException as exception:
            logger.error(f'Provisioned throughput exceeded: {exception}')
        except self.client.exceptions.ResourceNotFoundException as exception:
            logger.error(f'Resource not found: {exception}')
