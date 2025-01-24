from flask import Flask, jsonify, request
import requests
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

ACCESS_TOKEN = "660f1622e1665"

@app.route('/api/get_qr', methods=['GET'])
def get_qr():
    # Step 1: Generate instance ID
    instance_response = requests.get(f"https://chat.hopelearning.net/api/create_instance?access_token={ACCESS_TOKEN}")
    if instance_response.status_code != 200:
        return jsonify({"error": "Failed to create instance"}), 500

    instance_data = instance_response.json()
    instance_id = instance_data.get("instance_id")

    if not instance_id:
        return jsonify({"error": "Instance ID not found"}), 500

    # Step 2: Get QR code
    qr_response = requests.get(
        f"https://chat.hopelearning.net/api/get_qrcode?instance_id={instance_id}&access_token={ACCESS_TOKEN}"
    )
    if qr_response.status_code != 200:
        return jsonify({"error": "Failed to get QR code"}), 500

    qr_data = qr_response.json()
    base64_image = qr_data.get("base64")

    if not base64_image:
        return jsonify({"error": "Base64 QR code not found"}), 500

    # Step 3: Return the QR code base64
    return jsonify({"qr_code": base64_image})

if __name__ == '__main__':
    app.run(debug=True)
