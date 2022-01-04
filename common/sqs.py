import boto3

class SQS:

    def __init__(self):
        self.client = boto3.client('sqs')

    def send_message(self):
        pass
