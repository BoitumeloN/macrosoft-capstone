import json
import boto3
import os

# Initialize SNS client
sns_client = boto3.client('sns')

# Get the SNS Topic ARN from environment variables
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    # Parse the incoming event (e.g., when a storage unit is accessed)
    unit_id = event.get('unit_id', 'N/A')
    customer_id = event.get('customer_id', 'N/A')
    status = event.get('status', 'N/A')
    
    # Create the message
    message = f"Storage Unit {unit_id} has been {status}. (Customer ID: {customer_id})"
    subject = f"Notification for Storage Unit {unit_id}"

    # Send the notification to the SNS topic
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        print(f"Notification sent successfully: {response['MessageId']}")
        return {
            'statusCode': 200,
            'body': json.dumps('Notification sent successfully!')
        }
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending notification.')
        }
