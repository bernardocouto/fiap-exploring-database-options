from common.firehose import Firehose

import awswrangler as wr
import json
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info('Start of running AWS Lambda')

    firehose = Firehose()
    delivery_stream_name_json = os.environ.get('AWS_FIREHOSE_INGEST_JSON', 'firehose-ingest-json')
    delivery_stream_name_parquet = os.environ.get('AWS_FIREHOSE_INGEST_PARQUET', 'firehose-ingest-parquet')

    if 'Records' in event:
        for record in event['Records']:
            body = json.loads(record['body'])
            logger.info(f'Reading the JSON on AWS S3: s3://{body["bucket"]}/{body["key"]}')
            df = wr.s3.read_json(
                orient='records',
                path=[f's3://{body["bucket"]}/{body["key"]}']
            )
            data = df.to_json(lines=True, orient='records')
            data = data.split('\n')
            for item in data:
                logger.info(f'Send record to AWS Kinesis Firehose JSON: {df}')
                firehose.put_record(
                    delivery_stream_name=delivery_stream_name_json,
                    record=data
                )
                logger.info(f'Send record to AWS Kinesis Firehose Parquet: {df}')
                firehose.put_record(
                    delivery_stream_name=delivery_stream_name_parquet,
                    record=data
                )

    logger.info('End of AWS Lambda run')
