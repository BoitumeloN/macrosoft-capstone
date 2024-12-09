import os
import json
import boto3
from unittest.mock import patch
from moto import mock_dynamodb
import pytest
from contextlib import contextmanager

# Mock DynamoDB table name and UUID values
SUNIT_MOCK_TABLE_NAME = "SUnit"
UUID_MOCK_VALUE_UNIT1 = "1"
UUID_MOCK_VALUE_UNIT2 = "2"


@contextmanager
def my_test_environment():
    """Context manager to mock DynamoDB and set up test data."""
    with mock_dynamodb():
        set_up_dynamodb()
        put_data_dynamodb()
        yield


def set_up_dynamodb():
    conn = boto3.client(
        'dynamodb'
    )
    conn.create_table(
        TableName= SUNIT_MOCK_TABLE_NAME,
        KeySchema=[
            {'AttributeName': 'unitid', 'KeyType': 'HASH'},
        ],
        AttributeDefinitions=[
            {'AttributeName': 'unitid', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )


def put_data_dynamodb():
    """Insert test data into the DynamoDB table."""
    conn = boto3.client('dynamodb', region_name='eu-west-1')
    conn.put_item(
        TableName=SUNIT_MOCK_TABLE_NAME,
        Item={
            'unitid': {'S': UUID_MOCK_VALUE_UNIT1},
            'location': {'S': 'Downtown'},
            'timestamp': {'S': '2023-12-08T10:00:00Z'},
            'Status' : {'S': 'Reserved'}
        }
    )
    conn.put_item(
        TableName=SUNIT_MOCK_TABLE_NAME,
        Item={
            'unitid': {'S': UUID_MOCK_VALUE_UNIT2},
            'location': {'S': 'Uptown'},
            'timestamp': {'S': '2023-12-08T11:00:00Z'},
            'Status' : {'S': 'Available'}
        }
    )


@pytest.fixture
def test_environment():
    """Fixture to set up and tear down test environment."""
    with my_test_environment():
        yield


@patch.dict(os.environ, {"UNITS_TABLE": SUNIT_MOCK_TABLE_NAME})
def test_environment_variable():
    """Test that the UNITS_TABLE environment variable is set correctly."""
    assert os.getenv("UNITS_TABLE") == SUNIT_MOCK_TABLE_NAME


@patch.dict(os.environ, {"UNITS_TABLE": SUNIT_MOCK_TABLE_NAME})
def test_list_units(test_environment):
    """Tests the lambda handler for retrieving a list of all units."""
    from src.api.view_units import lambda_handler

    # Mock API Gateway event for a GET request to list units
    event = {
        "httpMethod": "GET",
        "resource": "/storage_units",
        "path": "/storage_units"
    }

    # Call the Lambda function handler
    response = lambda_handler(event, None)

    # Assertions to verify the response
    assert response["statusCode"] == 200
    response_body = json.loads(response["body"])
    assert len(response_body) == 2
    assert response_body[0]["unitid"] == UUID_MOCK_VALUE_UNIT1
    assert response_body[1]["unitid"] == UUID_MOCK_VALUE_UNIT2


@patch.dict(os.environ, {"UNITS_TABLE": SUNIT_MOCK_TABLE_NAME})
def test_list_units_by_status(test_environment):
    """Tests the lambda handler for retrieving a list of all units."""
    from src.api.manage_unit_status import lambda_handler

    # Mock API Gateway event for a GET request to list units
    event = {
        'httpMethod': 'GET',
        'path': '/storage_units/status/Available',
        'pathParameters': {'status': 'Available'},
        'resource': '/storage_units/status/Available'
    }

    # Call the Lambda function handler
    response = lambda_handler(event, None)

    # Assertions to verify the response
    assert response["statusCode"] == 200
    response_body = json.loads(response["body"])
    assert len(response_body) == 1


@patch.dict(os.environ, {"UNITS_TABLE": SUNIT_MOCK_TABLE_NAME})
def test_cancel_unit(test_environment):
    """Tests the lambda handler for retrieving a list of all units."""
    from src.api.cancel_units import lambda_handler

    # Mock API Gateway event for a GET request to list units
    event = {
        'httpMethod': 'PUT',
        'path': f'/storage_units/{UUID_MOCK_VALUE_UNIT1}/cancel',
        'pathParameters': {'unitid': UUID_MOCK_VALUE_UNIT1},
        'resource': '/storage_units/{unitid}/cancel',
        'headers': {
            'Content-Type': 'application/json',
        }
    }

    # Call the Lambda function handler
    response = lambda_handler(event, None)

    # Assertions to verify the response
    assert response["statusCode"] == 200
    response_body = json.loads(response["body"])
    assert response_body["unitid"] == UUID_MOCK_VALUE_UNIT1
    assert response_body["Status"] == "Cancelling"   

