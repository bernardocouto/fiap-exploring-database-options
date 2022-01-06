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
        'VendorID',
        'tpep_pickup_datetime',
        'tpep_dropoff_datetime',
        'passenger_count',
        'trip_distance',
        'pickup_longitude',
        'pickup_latitude',
        'RateCodeID',
        'store_and_fwd_flag',
        'dropoff_longitude',
        'dropoff_latitude',
        'payment_type',
        'fare_amount',
        'extra',
        'mta_tax',
        'tip_amount',
        'tolls_amount',
        'improvement_surcharge',
        'total_amount'
    ]

    columns_dtype = {
        'VendorID': int,
        'tpep_pickup_datetime': str,
        'tpep_dropoff_datetime': str,
        'passenger_count': int,
        'trip_distance': float,
        'pickup_longitude': float,
        'pickup_latitude': float,
        'RateCodeID': int,
        'store_and_fwd_flag': str,
        'dropoff_longitude': float,
        'dropoff_latitude': float,
        'payment_type': int,
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'improvement_surcharge': float,
        'total_amount': float
    }

    if 'Records' in event:
        for record in event['Records']:
            body = json.loads(record['body'])
            logger.info(f'Reading the CSV on AWS S3: s3://{body["bucket"]}/{body["key"]}')
            df = wr.s3.read_csv(
                dtype=columns_dtype,
                header=1,
                names=columns_names,
                path=[f's3://{body["bucket"]}/{body["key"]}'],
                sep=','
            )
            # df = df.iloc[1:, :]
            logger.info(f'Converting from CSV to JSON and persisting to AWS S3: s3://{bucket}')
            key = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.json'
            wr.s3.to_json(
                df=df,
                date_format='epoch',
                orient='records',
                path=f's3://{bucket}/{key}'
            )

    logger.info('End of AWS Lambda run')
