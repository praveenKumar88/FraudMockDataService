from flask import Flask, jsonify, request
import random
import uuid
import time
from faker import Faker

app = Flask(__name__)
fake = Faker()


# Function to generate a single mock transaction
def generate_mock_transaction(is_fraud=False):
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4()),
        "transaction_amount": round(random.uniform(10, 5000), 2),  # Random amount between $10 and $5000
        "timestamp": time.time(),
        "geolocation": fake.location_on_land()[2],  # Random city location
        "payment_method": random.choice(["credit_card", "paypal", "bank_transfer"]),
        "ip_address": fake.ipv4_public(),
        "device_type": random.choice(["mobile", "desktop", "tablet"]),
        "merchant_id": str(uuid.uuid4()),
        "is_fraud": is_fraud
    }

    # Add fraud characteristics if this transaction is flagged as fraud
    if is_fraud:
        transaction["transaction_amount"] = round(random.uniform(5000, 10000), 2)  # Higher transaction for fraud
        transaction["geolocation"] = "Nigeria"  # Example of a high-risk country
        transaction["ip_address"] = fake.ipv4_public()

    return transaction


# Endpoint to generate mock transactions
@app.route('/generate_transactions', methods=['GET'])
def generate_transactions():
    # Get number of transactions and fraud percentage from the request (or use defaults)
    num_transactions = int(request.args.get('num_transactions', 100))
    fraud_percentage = float(request.args.get('fraud_percentage', 5))

    transactions = []
    for _ in range(num_transactions):
        is_fraud = random.random() < (fraud_percentage / 100)
        transaction = generate_mock_transaction(is_fraud)
        transactions.append(transaction)

    return jsonify(transactions)


# Run the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
