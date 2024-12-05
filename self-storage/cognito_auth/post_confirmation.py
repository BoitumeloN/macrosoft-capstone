import boto3

def lambda_handler(event, context):
    # Get the Cognito User Pool ID and Username from the event
    user_pool_id = event['userPoolId']
    username = event['userName']
    
    # Initialize the Cognito client
    cognito_client = boto3.client('cognito-idp')

    # group user are added to
    group_name = 'TenantsUsersGroup'  

    # Add the user to the specified group
    response = cognito_client.admin_add_user_to_group(
        UserPoolId=user_pool_id,
        Username=username,
        GroupName=group_name
    )

    return event  # Must return the event object to proceed with Cognito post-confirmation flow
