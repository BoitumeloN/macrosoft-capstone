import json
import boto3
from botocore.exceptions import ClientError

# Initialize SNS client
sns_client = boto3.client('sns', region_name='eu-west-1')  # Modify the region if necessary

# SNS that you created
SNS_TOPIC_ARN = 'arn:aws:sns:eu-west-1:820242915645:StorageNotification'

def send_notification(subject, message):
    try:
        # Send notification to SNS topic
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        print(f"Notification sent! Message ID: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': json.dumps(f'Notification sent: {response["MessageId"]}')
        }
    except ClientError as e:
        print(f"Error sending notification: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }

def lambda_handler(event, context):
    # Retrieve subject and message from the event
    subject = event.get('subject', 'Self-Storage Notification')
    message = event.get('message', 'Your self-storage unit has been successfully booked!')

    # Send the notification
    return send_notification(subject, message)
