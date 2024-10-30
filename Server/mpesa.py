import base64
import os  
import requests
from flask import Blueprint, request, jsonify
from datetime import datetime
from models import Billing, db  

mpesaBlueprint = Blueprint('mpesa', __name__)

# Load credentials from environment variables
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
BUSINESS_SHORTCODE = os.getenv('BUSINESS_SHORTCODE')
LIPA_NA_MPESA_PASSKEY = os.getenv('LIPA_NA_MPESA_PASSKEY')

# Helper function to generate OAuth token
def generate_token():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth_string = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded_string = base64.b64encode(auth_string.encode()).decode('utf-8')
    headers = {"Authorization": f"Basic {encoded_string}"}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to generate token")

# Function to initiate an STK push
STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

def lipa_na_mpesa_online(amount, phone_number, account_reference, transaction_desc):
    token = generate_token()
    headers = {"Authorization": f"Bearer {token}"}
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(f"{BUSINESS_SHORTCODE}{LIPA_NA_MPESA_PASSKEY}{timestamp}".encode()).decode("utf-8")
    
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": 254797594751,  
        "CallBackURL": "https://7e55-197-237-171-180.ngrok-free.app/callback",
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }
    
    response = requests.post(STK_PUSH_URL, json=payload, headers=headers)
    return response.json()

# Route to initiate payment
@mpesaBlueprint.route('/pay', methods=['POST'])
def pay():
    data = request.get_json()
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    account_reference = data.get("account_reference")
    transaction_desc = data.get("transaction_desc", "Payment for event")

    if not phone_number or not amount or not account_reference:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        response = lipa_na_mpesa_online(amount, phone_number, account_reference, transaction_desc)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Callback route for payment confirmation
@mpesaBlueprint.route('/callback', methods=['POST'])
def callback():
    payment_data = request.json
    result_code = payment_data['Body']['stkCallback']['ResultCode']
    if result_code == 0:
        billing_id = payment_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
        billing_record = Billing.query.get(billing_id)
        if billing_record:
            billing_record.status = "Paid"
            db.session.commit()
    return jsonify({"Result": "Success"}), 200
