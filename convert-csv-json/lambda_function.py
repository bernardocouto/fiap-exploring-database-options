import awswrangler as wr
import json
import os

def lambda_handler(event, context):

    bucket = os.environ.get('AWS_S3_RAW_JSON', 'fiap-exploring-database-options-raw-json')

    if 'Records' in event:
        for record in event['Records']:
            body = json.loads(record['body'])
            print('**********')
            print('**********')
            print(type(body))
            print(body)
            print('**********')
            print('**********')
            df = wr.s3.read_csv(
                f's3://{body["bucket"]/{body["key"]}}',
                dataset=True
            )
            print('**********')
            print('**********')
            print(df.head())
            print('**********')
            print('**********')
            wr.s3.to_json(
                database='raw',
                dataset=True,
                df=df,
                path=f's3://{bucket}',
                table='raw'
            )
