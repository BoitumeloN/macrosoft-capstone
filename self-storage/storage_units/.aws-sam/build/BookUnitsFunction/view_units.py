# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import uuid
import os
import boto3
from datetime import datetime

# Prepare DynamoDB client
UNITS_TABLE = os.getenv('UNITS_TABLE', None)
dynamodb = boto3.resource('dynamodb')
ddbTable = dynamodb.Table(UNITS_TABLE)
  


def lambda_handler(event, context):
   
    # Set default response, override with data from DynamoDB if any
    response_body = {'Message': 'Unsupported route'}
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
        }
    try:
        # Get a list of all Users
        ddb_response = ddbTable.scan(Select='ALL_ATTRIBUTES')
        # return list of items instead of full DynamoDB response
        response_body = ddb_response['Items']
        status_code = 200
       
      
    except Exception as err:
        status_code = 400
        response_body = {'Error:': str(err)}
        print(str(err))
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body),
        'headers': headers
    }        