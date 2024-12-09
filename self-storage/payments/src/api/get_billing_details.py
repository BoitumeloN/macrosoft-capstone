import json
import boto3

def lambda_handler(event, context):
    user_id = event['requestContext']['identity']['cognitoIdentityId']  # Get user ID from Cognito
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('BillingDetails')

    response = table.get_item(Key={'UserId': user_id})
    
    if 'Item' in response:
        return {
            'statusCode': 200,
            'body': json.dumps(response['Item'])
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Billing details not found'})
        }