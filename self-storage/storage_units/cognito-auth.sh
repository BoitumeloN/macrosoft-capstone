#!/bin/bash
#this scripts use aws cli to log in to Cognito using below user details and return the idToken
#this idToken can be used as the Bearer token value for API calls that are autenticated with Cognito
#NOTE: this script adds an extra return (\n) at end of idToken, so if you paste it in as the Bearer token, backspace to remove that return character
#
# Steps:
# 1. first install AWS CLI tools, and setup your AWS Key and Secret credentials as a profile
# 2. Create a  user manually in your cognito user pool (make sure this is the one speciifed for use for authentication by the API Gateway endpoints)
# 3. fill in your test user details below (and do not commit the details to a repo)
#
username="bngwenya023@student.wethinkcode.co.za"
password="Phumzile1@"
clientid="44t95jhbmn74mjqh99tn2lbhih"
region="eu-west-1" #check this matches the region you deploy to
aws_profile="default"
# Authenticate with Cognito

echo "Authenticating with Cognito..."
echo "Authenticating with Cognito..."
token_request=$(aws cognito-idp initiate-auth \
    --auth-flow USER_PASSWORD_AUTH \
    --output json \
    --region "$region" \
    --client-id "$clientid" \
    --auth-parameters USERNAME="$username",PASSWORD="$password" \
    --profile "$aws_profile" --query 'AuthenticationResult.IdToken' --output text)

# Debugging: Output the raw response to check if IdToken is present
echo "Raw Response: $token_request"

# Check if the command executed successfully
if [ $? -ne 0 ]; then
    echo "Failed to authenticate. Check your credentials and AWS configuration."
    exit 1
fi

# Check if ID Token was parsed correctly
if [ -z "$token_request" ]; then
    echo "Failed to retrieve ID Token. Verify Cognito configuration and inputs."
    exit 1
fi

# Export the ID Token as an environment variable
export ID_TOKEN="$token_request"

# Output the ID Token
echo "ID Token: $ID_TOKEN"

# Optionally copy the ID Token to clipboard (if xclip is available)
if command -v xclip &>/dev/null; then
    echo "$ID_TOKEN" | xclip -selection clipboard
    echo "ID Token copied to clipboard."
else
    echo "xclip not found. Token not copied to clipboard."
fi
