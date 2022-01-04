from common.sqs import SQS

import awswrangler as wr
import json
import logging
import os

logger = logging.getLogger(__name__)

def lambda_handler(event, context):

    logger.info('Start of running AWS Lambda')

    bucket = os.environ.get('AWS_S3_RAW_JSON', 'fiap-exploring-database-options-raw-json')

    sqs = SQS()
    queue_name = os.environ.get('AWS_SQS_RAW_JSON_TO_FIREHOSE', 'raw-json-to-firehose')
    queue_url = sqs.get_queue_url(queue_name=queue_name)

    columns_names = [
        'id',
        'name'
    ]

    if 'Records' in event:
        for record in event['Records']:
            body = json.loads(record['body'])
            receipt_handle = record['receiptHandle']
            logger.info(f'Reading the CSV on AWS S3: s3://{body["bucket"]}/{body["key"]}')
            dfs = wr.s3.read_csv(
                names=columns_names,
                path=[f's3://{body["bucket"]}/{body["key"]}'],
                sep=';'
            )
            logger.info(f'Converting from CSV to JSON and persisting to AWS S3: s3://{bucket}')
            print(dfs)
            for df in dfs:
                print(df)
                wr.s3.to_json(
                    dataset=True,
                    df=df,
                    index=False,
                    path=f's3://{bucket}'
                )
            sqs.delete_message(
                queue_url=queue_url,
                receipt_handle=receipt_handle
            )

    logger.info('End of AWS Lambda run')
