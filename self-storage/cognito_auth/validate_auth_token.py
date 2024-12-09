import os
import json
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    # Extract the JWT token from the event
    token = event['headers'].get('Authorization')
    if not token:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Authorization token is missing'}),
        }

    # Initialize the Cognito client
    cognito_client = boto3.client('cognito-idp')

    try:
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
            return {
                'statusCode': 403,
                'body': json.dumps({'message': 'User is not authorized to book units'}),
                'groups': user_groups['Groups']
            }

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User is authorized'}),
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'NotAuthorizedException':
            return {
                'statusCode': 401,
                'body': json.dumps({'message': 'Unauthorized', 'error': 'Invalid Access Token'}),
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': 'Internal server error', 'error': str(e)}),
            }