import json
import boto3
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('UNITS_TABLE'))

def lambda_handler(event, context):
    http_method = event['httpMethod']
    path_parameters = event['pathParameters']
    
    if http_method == "GET":
        # Handle GetUnitStatus
        status = path_parameters['status']
        return get_units_by_status(status)
    elif http_method == "PUT":
        # Handle UpdateUnitStatus
        unitid = path_parameters['unitid']
        new_status = path_parameters['status']
        return update_unit_status(unitid, new_status)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

def get_units_by_status(status):
    try:
        # Query storage units by status
        response = table.scan(
            FilterExpression="#status = :status_value",
            ExpressionAttributeNames={"#status": "Status"},
            ExpressionAttributeValues={":status_value": status}
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items']),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return handle_error(e)

def update_unit_status(unitid, new_status):
    try:
        # Update the status of a specific storage unit
        response = table.update_item(
            Key={'unitid': unitid},
            UpdateExpression="SET #status = :new_status",
            ExpressionAttributeNames={"#status": "Status"},
            ExpressionAttributeValues={":new_status": new_status},
            ReturnValues="ALL_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes']),
            'headers': {'Content-Type': 'application/json'}
        }
    except Exception as e:
        return handle_error(e)

def handle_error(exception):
    return {
        'statusCode': 500,
        'body': json.dumps({'error': str(exception)}),
        'headers': {'Content-Type': 'application/json'}
    }
