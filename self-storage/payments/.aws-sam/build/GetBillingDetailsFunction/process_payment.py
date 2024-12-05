import json
import os
import requests

def lambda_handler(event, context):
    payment_info = json.loads(event['body'])
    amount = payment_info.get('amount')
    
    client_id = os.environ['PAYPAL_CLIENT_ID']
    secret = os.environ['PAYPAL_SECRET']
    
    # Get access token
    auth = (client_id, secret)
    response = requests.post('https://api.sandbox.paypal.com/v1/oauth2/token', 
                             auth=auth, data={'grant_type': 'client_credentials'})
    access_token = response.json().get('access_token')

    # Create payment request
    payment = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "USD"
            },
            "description": "Payment for self-storage rental"
        }],
        "redirect_urls": {
            "return_url": "https://your-return-url.com",
            "cancel_url": "https://your-cancel-url.com"
        }
    }

    payment_response = requests.post('https://api.sandbox.paypal.com/v1/payments/payment',
                                      json=payment, headers={'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'})

    return {
        'statusCode': payment_response.status_code,
        'body': payment_response.text
    }