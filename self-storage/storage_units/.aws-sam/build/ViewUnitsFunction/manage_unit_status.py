import json
import boto3
import os

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

def lambda_handler(event, context):
    # Get the status from the path parameters dynamically
    status = event['pathParameters']['status']  # e.g., Available, Reserved, Cancelling
    
    try:
        # Scan the table with a dynamic status filter
        response = table.scan(
            FilterExpression="#status = :status_value",
            ExpressionAttributeNames={
                "#status": "Status"  # Alias for the 'Status' attribute to avoid reserved keyword issues
            },
            ExpressionAttributeValues={
                ":status_value": status  # Use the status value from the path
            }
        )

        # Return the filtered items (units with the requested status)
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items']),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    
    except Exception as e:
        # Handle exceptions if any error occurs
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
