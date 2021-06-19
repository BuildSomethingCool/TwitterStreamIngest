import boto3
import creds
import time
import logging
import json
import sys

wait_time = creds.wait
landingTableName = "RawTweets"
logger = logging.getLogger('dynamo')


def create_landing_table(dynamodb=None, table_name=landingTableName):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    dynamo_client = boto3.client('dynamodb')
    existing_tables_map = dynamo_client.list_tables()
    existing_tables = existing_tables_map['TableNames']
    print(f"Table to create: {table_name}")
    print(f"Tables that exist: {existing_tables}")
    logger.info(f"Table to create {table_name}")
    logger.info(f"Tables that exist: {existing_tables}")
    for table in existing_tables:
        if table.lower() == table_name.lower():
            print(f"Table match done, deleting table {table}")
            logger.info(f"Table match done, deleting table {table}")
            response = dynamo_client.delete_table(
                TableName=table
            )
            logger.info(f"Response: {response}")
            print(f"Response: {response}")

    still_exists = True
    while still_exists:
        import time
        time.sleep(5)
        print('table still exists')
        logger.info(f"Table still exists")
        existing_tables_map = dynamo_client.list_tables()
        existing_tables = existing_tables_map['TableNames']
        if table_name not in existing_tables:
            still_exists = False

    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    status = table.table_status
    while status != "ACTIVE":
        time.sleep(3)
        status = table.table_status
    return table


def index_tweet(tweet, table_name):
    if creds.env == 'dev':
        dynamodb = boto3.resource('dynamodb', endpoint_url=f"http://{creds.docker['endpoint']}:{creds.docker['port']}")
        dynamo_client = boto3.client('dynamodb',
                                     endpoint_url=f"http://{creds.docker['endpoint']}:{creds.docker['port']}")
    else:
        dynamodb = boto3.resource('dynamodb')
        dynamo_client = boto3.client('dynamodb')

    table = dynamodb.Table(table_name)
    tables = dynamo_client.list_tables()
    print(f"tables: {tables}")
    logger.info(f"Tables: {tables}")
    response = dynamo_client.describe_table(TableName=table_name)

    status = response['Table']['TableStatus']
    while status != 'ACTIVE':
        time.sleep(5)
        response = dynamo_client.describe_table(TableName=table_name)
        status = response['Table']['TableStatus']

    response = table.put_item(
        Item=tweet
    )
    return response


if __name__ == '__main__':
    landing_table = create_landing_table()
    print("Table status:", landing_table.table_status)
