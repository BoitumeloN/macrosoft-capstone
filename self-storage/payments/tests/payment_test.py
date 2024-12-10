import json
import os
import unittest
from unittest.mock import patch, MagicMock
from payments.src.api.process_payment import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('requests.post')
    @patch.dict(os.environ, {'PAYPAL_CLIENT_ID': 'your_client_id', 'PAYPAL_SECRET': 'your_secret'})
    def test_lambda_handler_success(self, mock_post):
        # Prepare test input event
        event = {
            'body': json.dumps({
                'amount': 100.00
            })
        }

        # Mock the response from PayPal's OAuth2 token endpoint
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {'access_token': 'fake_access_token'}
        mock_post.return_value = mock_token_response

        # Mock the response from PayPal's payment creation endpoint
        mock_payment_response = MagicMock()
        mock_payment_response.status_code = 201
        mock_payment_response.text = json.dumps({'id': 'PAY-12345'})
        mock_post.return_value = mock_payment_response

        # Call the lambda_handler function
        response = lambda_handler(event, None)

        # Validate the response
        self.assertEqual(response['statusCode'], 201)
        self.assertIn('id', json.loads(response['body']))

    @patch('requests.post')
    @patch.dict(os.environ, {'PAYPAL_CLIENT_ID': 'your_client_id', 'PAYPAL_SECRET': 'your_secret'})
    def test_lambda_handler_failure(self, mock_post):
        # Prepare test input event
        event = {
            'body': json.dumps({
                'amount': 100.00
            })
        }

        # Mock the response from PayPal's OAuth2 token endpoint
        mock_token_response = MagicMock()
        mock_token_response.json.return_value = {'access_token': 'fake_access_token'}
        mock_post.return_value = mock_token_response

        # Mock the response from PayPal's payment creation endpoint with failure
        mock_payment_response = MagicMock()
        mock_payment_response.status_code = 400
        mock_payment_response.text = json.dumps({'error': 'invalid_request'})
        mock_post.return_value = mock_payment_response

        # Call the lambda_handler function
        response = lambda_handler(event, None)

        # Validate the response
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('error', json.loads(response['body']))

if __name__ == '__main__':
    unittest.main()
