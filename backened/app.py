from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------------
# SAMPLE USER DATA
# -------------------------
users = {
    "admin": {
        "password": "1234"
    }
}

# -------------------------
# OTP STORAGE (in-memory)
# -------------------------
otp_store = {}
OTP_EXPIRY = 300  # 5 minutes


# -------------------------
# HOME ROUTE (for Render check)
# -------------------------
@app.route('/')
def home():
    return "HRM Backend Running"


# -------------------------
# LOGIN API
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username]["password"] == password:
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401


# -------------------------
# SEND OTP
# -------------------------
@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.json
    username = data.get("username")

    if username not in users:
        return jsonify({"message": "User not found"}), 404

    otp = str(random.randint(100000, 999999))

    otp_store[username] = {
        "otp": otp,
        "time": time.time(),
        "verified": False
    }

    # For testing (no email/SMS)
    return jsonify({
        "message": "OTP sent successfully",
        "otp": otp
    }), 200


# -------------------------
# VERIFY OTP
# -------------------------
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    username = data.get("username")
    otp = data.get("otp")

    record = otp_store.get(username)

    if not record:
        return jsonify({"message": "OTP not requested"}), 400

    # Check expiry
    if time.time() - record["time"] > OTP_EXPIRY:
        del otp_store[username]
        return jsonify({"message": "OTP expired"}), 400

    if record["otp"] != otp:
        return jsonify({"message": "Invalid OTP"}), 400

    record["verified"] = True

    return jsonify({"message": "OTP verified"}), 200


# -------------------------
# RESET PASSWORD
# -------------------------
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    username = data.get("username")
    new_password = data.get("new_password")

    record = otp_store.get(username)

    if not record or not record.get("verified"):
        return jsonify({"message": "OTP not verified"}), 400

    users[username]["password"] = new_password

    # Clear OTP after success
    del otp_store[username]

    return jsonify({"message": "Password reset successful"}), 200


# -------------------------
# RUN APP (Render compatible)
# -------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)