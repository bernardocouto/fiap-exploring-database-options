import boto3

class SQS:

    def __init__(self):
        self.client = boto3.client('sqs')

    def send_message(self, message_body, queue_url):
        try:
            self.client.send_message(
                MessageBody=message_body,
                QueueUrl=queue_url
            )
        except self.client.exceptions.InvalidMessageContents as exception:
            print(exception)
        except self.client.exceptions.UnsupportedOperation as exception:
            print(exception)
