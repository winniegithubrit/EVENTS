import os
import requests
import time
import base64
from datetime import datetime
from flask import Blueprint, request, jsonify
from models import Billing, db
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

# M-Pesa credentials
M_PESA_CONSUMER_KEY = os.getenv('M_PESA_CONSUMER_KEY')
M_PESA_CONSUMER_SECRET = os.getenv('M_PESA_CONSUMER_SECRET')
M_PESA_SHORTCODE = os.getenv('M_PESA_SHORTCODE')
M_PESA_LNMO_SHORTCODE = os.getenv('M_PESA_LNMO_SHORTCODE')  # Get LNMO Shortcode from .env
M_PESA_SANDBOX_URL = os.getenv('M_PESA_SANDBOX_URL')

print(f"Consumer Key: {M_PESA_CONSUMER_KEY}")
print(f"Consumer Secret: {M_PESA_CONSUMER_SECRET}")

mpesaBlueprint = Blueprint('mpesa', __name__)

# Cache variables for the access token
access_token_cache = {"token": None, "expires_at": 0}

def get_cached_access_token():
    if access_token_cache["token"] and time.time() < access_token_cache["expires_at"]:
        return access_token_cache["token"]

    api_url = f"{M_PESA_SANDBOX_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=HTTPBasicAuth(M_PESA_CONSUMER_KEY, M_PESA_CONSUMER_SECRET))
    
    # Debugging access token request
    print(f"Access Token Response: {response.status_code} - {response.text}")
    
    if response.status_code == 200:
        json_response = response.json()
        access_token = json_response['access_token']
        expires_in = int(json_response.get('expires_in', 3600))  
        access_token_cache["token"] = access_token
        access_token_cache["expires_at"] = time.time() + expires_in
        return access_token
    else:
        print("Failed to obtain access token.")
        return None


def generate_mpesa_password():
    print("Inside generate_mpesa_password function")  # Confirm function is called
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password_string = f"{M_PESA_SHORTCODE}{M_PESA_LNMO_SHORTCODE}{timestamp}"
    encoded_password = base64.b64encode(password_string.encode()).decode()
    print(f"Generated M-Pesa Password: {encoded_password}")  # Print the generated password
    return encoded_password

@mpesaBlueprint.route('/mpesa/pay', methods=['POST'])
def initiate_payment():
    print("Initiating payment...")  # Added debug statement
    data = request.get_json()
    print(f"Received data: {data}")  # Log the raw data received
    billing_id = data.get('billing_id')

    print(f"Received billing_id: {billing_id}")  # Log the billing ID

    billing = Billing.query.get(billing_id)
    if not billing:
        print("Billing record not found.")  # Log if billing record is missing
        return jsonify({'error': 'Billing record not found'}), 404

    access_token = get_cached_access_token()
    if not access_token:
        print("Failed to obtain access token.")  # Log if token retrieval fails
        return jsonify({'error': 'Failed to obtain access token'}), 500

    # Before generating the password
    print("Generating M-Pesa password...")  # Confirm password generation is about to happen
    
    # Generate the password and print it
    password = generate_mpesa_password()
    
    # Prepare payload for STK push request
    payload = {
        "BusinessShortCode": M_PESA_SHORTCODE,
        "Password": password,  # Use the generated password here
        "Timestamp": datetime.now().strftime('%Y%m%d%H%M%S'),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": billing.amount,
        "PartyA": "254797594751",  
        "PartyB": M_PESA_SHORTCODE,
        "PhoneNumber": "254727316620",  
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": f"Billing-{billing.id}",
        "TransactionDesc": "Payment for billing"
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Send request to M-Pesa
    response = requests.post(f"{M_PESA_SANDBOX_URL}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)

    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")  # Log the full response content

    # Print the generated password directly to the terminal for your testing
    print(f"Generated Password for Testing: {password}")

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        print(f"Failed to initiate payment: {response.text}")  
        return jsonify({'error': 'Failed to initiate payment', 'details': response.text}), 500

@mpesaBlueprint.route('/mpesa/callback', methods=['POST'])
def callback():
    data = request.get_json()
    print(f"Callback received: {data}")
    return jsonify({'message': 'Callback received', 'data': data}), 200
