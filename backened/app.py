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

    # -------------------------
# TASK STORAGE
# -------------------------
tasks = []
task_assignments = []
task_id_counter = 1
assignment_id_counter = 1


# -------------------------
# CREATE TASK
# -------------------------
@app.route('/create-task', methods=['POST'])
def create_task():
    global task_id_counter, assignment_id_counter

    data = request.json

    task = {
        "task_id": task_id_counter,
        "task_title": data.get("task_title"),
        "task_description": data.get("task_description"),
        "task_priority": data.get("task_priority"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "task_type": data.get("task_type"),
        "created_at": time.time(),
        "updated_at": time.time()
    }

    tasks.append(task)

    assignment = {
        "assignment_id": assignment_id_counter,
        "task_id": task_id_counter,
        "employee_id": data.get("employee_id"),
        "assigned_by": "admin",
        "assigned_date": time.time(),
        "status": "Pending",
        "completed_at": None
    }

    task_assignments.append(assignment)

    task_id_counter += 1
    assignment_id_counter += 1

    return jsonify({"message": "Task created successfully"})


# -------------------------
# GET TASKS
# -------------------------
@app.route('/tasks', methods=['GET'])
def get_tasks():
    result = []

    for a in task_assignments:
        task = next((t for t in tasks if t["task_id"] == a["task_id"]), None)

        result.append({
            "assignment_id": a["assignment_id"],
            "task_title": task["task_title"],
            "task_priority": task["task_priority"],
            "status": a["status"],
            "employee_id": a["employee_id"]
        })

    return jsonify(result)


# -------------------------
# UPDATE TASK STATUS
# -------------------------
@app.route('/update-status/<int:assignment_id>', methods=['PUT'])
def update_status(assignment_id):
    data = request.json

    for a in task_assignments:
        if a["assignment_id"] == assignment_id:
            a["status"] = data.get("status")

            if a["status"] == "Completed":
                a["completed_at"] = time.time()

            return jsonify({"message": "Status updated"})

    return jsonify({"message": "Not found"}), 404


# -------------------------
# DELETE TASK
# -------------------------
@app.route('/delete-task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["task_id"] != task_id]

    return jsonify({"message": "Task deleted"})