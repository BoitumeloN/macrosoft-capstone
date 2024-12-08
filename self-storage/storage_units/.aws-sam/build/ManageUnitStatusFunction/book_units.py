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
        unitid = event['pathParameters'].get('unitid')
    
        if not unitid:
            raise ValueError("Missing 'unitid' in request")

        # Extract the JWT token from the event
        token = event['headers'].get('Authorization')
        if not token:
            raise ValueError("Authorization token is missing")

        # Initialize the Cognito client
        cognito_client = boto3.client('cognito-idp')

        # Get the user information from the token
        user_info = cognito_client.get_user(
            AccessToken=token
        )

        # Check if the user is in the TenantsUsersGroup
        user_groups = cognito_client.admin_list_groups_for_user(
            UserPoolId=os.getenv('USER_POOL_ID'),
            Username=user_info['Username']
        )

        is_tenant = any(group['GroupName'] == 'TenantsUsersGroup' for group in user_groups['Groups'])
        if not is_tenant:
            raise ValueError("User is not authorized to book units")
        
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
            UpdateExpression="SET #Status = :reserved, #bookingTime = :time",
            ExpressionAttributeNames={
                '#Status': 'Status',
                '#bookingTime': 'bookingTimestamp'
            },
            ExpressionAttributeValues={
                ':reserved': 'Reserved',
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
