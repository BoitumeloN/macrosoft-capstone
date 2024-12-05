import json
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

# Prepare DynamoDB client
UNITS_TABLE = os.getenv('TABLE_NAME')
if not UNITS_TABLE:
    raise RuntimeError("Environment variable 'TABLE_NAME' is not set")

dynamodb = boto3.resource('dynamodb')
ddbTable = dynamodb.Table(UNITS_TABLE)

def lambda_handler(event, context):
    response_body = {'Message': 'Unsupported route'}
    status_code = 400
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    }

    try:
        # Validate request body
        if 'body' not in event or not event['body']:
            raise ValueError("Request body is missing")
        
        body = json.loads(event['body'])
        unitid = body.get("unitid")

        if not unitid:
            raise ValueError("Missing 'unitid' in request")

        print(f"Fetching unit with ID: {unitid}")
        
        # Fetch the unit details
        try:
            ddb_response = ddbTable.get_item(Key={'unitid': unitid})
        except ClientError as e:
            raise ValueError(f"DynamoDB error: {e.response['Error']['Message']}")
        
        unit = ddb_response.get('Item')
        
        if not unit:
            raise ValueError(f"Unit with ID {unitid} does not exist.")
        
        if unit['Status'] != 'Available':
            raise ValueError(f"Unit {unitid} is not available for booking.")
        
        # Update the unit status to 'unavailable'
        print(f"Booking unit: {unitid}")
        update_response = ddbTable.update_item(
            Key={"unitid": unitid},
            UpdateExpression="SET #Status = :unavailable, #bookingTime = :time",
            ExpressionAttributeNames={
                '#Status': 'Status',
                '#bookingTime': 'bookingTimestamp'
            },
            ExpressionAttributeValues={
                ':unavailable': 'Unavailable',
                ':time': datetime.now().isoformat(),
                ':Available': 'Available'
            },
            ConditionExpression="attribute_exists(unitid) AND #Status = :Available",
            ReturnValues="ALL_NEW"
        )

        # Respond with the updated item
        response_body = update_response.get('Attributes', {})
        status_code = 200

    except ValueError as ve:
        status_code = 400
        response_body = {'error': 'ValidationError', 'message': str(ve)}
    except ClientError as ce:
        status_code = 500
        response_body = {'error': 'DynamoDBError', 'message': str(ce)}
    except Exception as err:
        status_code = 500
        response_body = {'error': 'ServerError', 'message': str(err)}
        print(str(err))

    return {
        'statusCode': status_code,
        'body': json.dumps(response_body),
        'headers': headers
    }
