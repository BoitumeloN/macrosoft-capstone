import os
import json
import boto3
from unittest.mock import patch, MagicMock
import pytest

# Mock values
UUID_MOCK_VALUE_UNIT2 = "1"
SUNIT_MOCK_TABLE_NAME = "mock-units-table"
USER_POOL_ID = "mock-user-pool-id"
VALID_AUTH_TOKEN = "valid-auth-token"

# Test the booking function
@patch.dict(os.environ, {
    "UNITS_TABLE": SUNIT_MOCK_TABLE_NAME,
    "USER_POOL_ID": USER_POOL_ID
})
@patch("boto3.resource")
@patch("boto3.client")
def test_book_unit(mock_boto_client, mock_boto_resource):
    """Tests the lambda handler for booking a storage unit."""

    # Mock DynamoDB table
    mock_table = MagicMock()
    mock_boto_resource.return_value.Table.return_value = mock_table

    # Mock Cognito client
    mock_cognito_client = MagicMock()
    mock_boto_client.return_value = mock_cognito_client

    # Cognito user response
    mock_cognito_client.get_user.return_value = {
        "Username": "mock-user"
    }
    mock_cognito_client.admin_list_groups_for_user.return_value = {
        "Groups": [{"GroupName": "TenantsUsersGroup"}]
    }

    # Mock DynamoDB responses
    mock_table.get_item.return_value = {
        "Item": {"unitid": UUID_MOCK_VALUE_UNIT2, "Status": "Available"}
    }
    mock_table.update_item.return_value = {
        "Attributes": {
            "unitid": UUID_MOCK_VALUE_UNIT2,
            "Status": "Reserved",
            "bookingTimestamp": "2024-12-09T12:00:00Z"
        }
    }

    # Prepare event
    event = {
        'httpMethod': 'PUT',
        'path': f'/storage_units/{UUID_MOCK_VALUE_UNIT2}',
        'resource': '/storage_units/{unitid}',
        'pathParameters': {'unitid': UUID_MOCK_VALUE_UNIT2},
        'headers': {
            'Content-Type': 'application/json',
            'Authorization': VALID_AUTH_TOKEN
        }
    }

    # Import and call the lambda handler
    from src.api.book_units import lambda_handler
    response = lambda_handler(event, None)

    # Assertions
    assert response["statusCode"] == 200
    response_body = json.loads(response["body"])
    assert response_body["unitid"] == UUID_MOCK_VALUE_UNIT2
    assert response_body["Status"] == "Reserved"
    assert "bookingTimestamp" in response_body

    # Validate mocks were called correctly
    mock_table.get_item.assert_called_once_with(Key={"unitid": UUID_MOCK_VALUE_UNIT2})
    mock_table.update_item.assert_called_once()
    mock_cognito_client.get_user.assert_called_once_with(AccessToken=VALID_AUTH_TOKEN)
    mock_cognito_client.admin_list_groups_for_user.assert_called_once_with(
        UserPoolId=USER_POOL_ID,
        Username="mock-user"
    )
