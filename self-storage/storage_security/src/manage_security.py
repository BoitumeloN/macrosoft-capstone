import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime

# Initialize SNS and DynamoDB clients
sns_client = boto3.client('sns', region_name='eu-west-1')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StorageUnitAccessLogs')

# SNS Topic ARN
SNS_TOPIC_ARN = 'arn:aws:sns:eu-west-1:820242915645:StorageSecurityNotifications'

def publish_notification(message, subject):
    """Send a notification to the customer via SNS"""
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        print(f"Notification sent! Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending notification: {e}")

def record_access(unit_id, user_id, access_type, start_date, end_date):
    """Record access in DynamoDB"""
    try:
        response = table.put_item(
            Item={
                'unit_id': unit_id,
                'access_time': datetime.now().isoformat(),
                'user_id': user_id,
                'access_type': access_type,
                'start_date': start_date,
                'end_date': end_date
            }
        )
        print(f"Access logged: {response}")
    except ClientError as e:
        print(f"Error logging access: {e}")

def lambda_handler(event, context):
    # Extract input data
    body = json.loads(event['body'])
    action = body.get('action')
    unit_id = body.get('unit_id')
    user_id = body.get('user_id')
    
    if action == 'unlock-storage':
        # Unlock storage logic
        message = f"Storage unit {unit_id} has been unlocked for user {user_id}."
        publish_notification(message, 'Storage Unit Unlocked')
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }
    
    elif action == 'grant-access':
        # Grant access logic
        access_type = body.get('access_type')
        start_date = body.get('start_date')
        end_date = body.get('end_date')
        
        record_access(unit_id, user_id, access_type, start_date, end_date)
        
        message = f"Access granted to user {user_id} for unit {unit_id} (Access Type: {access_type})."
        publish_notification(message, 'Access Granted')
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }
    
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid action'})
        }
