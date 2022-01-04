import awswrangler as wr
import datetime
import json
import logging
import os

logger = logging.getLogger(__name__)

def lambda_handler(event, context):

    logger.info('Start of running AWS Lambda')

    bucket = os.environ.get('AWS_S3_RAW_JSON', 'fiap-exploring-database-options-raw-json')

    columns_names = [
        'id',
        'name'
    ]

    if 'Records' in event:
        for record in event['Records']:
            body = json.loads(record['body'])
            logger.info(f'Reading the CSV on AWS S3: s3://{body["bucket"]}/{body["key"]}')
            df = wr.s3.read_csv(
                names=columns_names,
                path=[f's3://{body["bucket"]}/{body["key"]}'],
                sep=';'
            )
            logger.info(f'Converting from CSV to JSON and persisting to AWS S3: s3://{bucket}')
            key = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.json'
            wr.s3.to_json(
                df=df,
                lines=True,
                orient='records',
                path=f's3://{bucket}/{key}'
            )

    logger.info('End of AWS Lambda run')
