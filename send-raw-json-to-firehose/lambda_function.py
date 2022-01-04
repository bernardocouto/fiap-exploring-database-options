import awswrangler as wr
import datetime
import json
import logging
import os

logger = logging.getLogger(__name__)

def lambda_handler(event, context):

    logger.info('Start of running AWS Lambda')

    delivery_stream_name = os.environ.get('AWS_FIREHOSE_INGEST_JSON', 'firehose-ingest-json')

    if 'Records' in event:
        for record in event['Records']:
            body = json.loads(record['body'])
            logger.info(f'Reading the JSON on AWS S3: s3://{body["bucket"]}/{body["key"]}')
            df = wr.s3.read_json(
                path=[f's3://{body["bucket"]}/{body["key"]}']
            )
            for index, row in df.iterrows():
                print(f'Index: {index} - Row: {row}')

    logger.info('End of AWS Lambda run')
