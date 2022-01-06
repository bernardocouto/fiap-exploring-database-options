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
            record = df.to_json(orient='records')
            logger.info('Send record to AWS Kinesis Firehose JSON')
            firehose.put_record(
                delivery_stream_name=delivery_stream_name_json,
                record=record
            )
            logger.info('Send record to AWS Kinesis Firehose Parquet')
            firehose.put_record(
                delivery_stream_name=delivery_stream_name_parquet,
                record=record
            )

    logger.info('End of AWS Lambda run')
