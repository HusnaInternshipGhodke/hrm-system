from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# -------------------------
# USERS
# -------------------------
users = {
    "admin": {
        "password": "1234"
    }
}

# -------------------------
# OTP STORAGE
# -------------------------
otp_store = {}
OTP_EXPIRY = 300


# -------------------------
# TASK STORAGE
# -------------------------
tasks = []
assignments = []
task_id_counter = 1
assignment_id_counter = 1


# -------------------------
# HOME
# -------------------------
@app.route('/')
def home():
    return "HRM Backend Running"


# -------------------------
# LOGIN
# -------------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
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

    return jsonify({"message": "OTP sent", "otp": otp})


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
        return jsonify({"message": "OTP not found"}), 400

    if time.time() - record["time"] > OTP_EXPIRY:
        del otp_store[username]
        return jsonify({"message": "OTP expired"}), 400

    if record["otp"] != otp:
        return jsonify({"message": "Invalid OTP"}), 400

    record["verified"] = True
    return jsonify({"message": "OTP verified"})


# -------------------------
# RESET PASSWORD
# -------------------------
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
   @app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    username = data.get("username")

    record = otp_store.get(username)

    if not record or not record["verified"]:
        return jsonify({"message": "OTP not verified"}), 400

    # Always set password to 1234
    users[username]["password"] = "1234"

    # Clear OTP
    del otp_store[username]

    return jsonify({"message": "Password reset to 1234"})
    

# =====================================================
# TASK MODULE (PDF BASED)
# =====================================================

# CREATE TASK
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
        "task_type": data.get("task_type")
    }

    tasks.append(task)

    assignment = {
        "assignment_id": assignment_id_counter,
        "task_id": task_id_counter,
        "employee_id": data.get("employee_id"),
        "status": "Pending"
    }

    assignments.append(assignment)

    task_id_counter += 1
    assignment_id_counter += 1

    return jsonify({"message": "Task created"})


# GET TASKS WITH FILTER
@app.route('/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get("status")
    employee = request.args.get("employee_id")

    result = []

    for a in assignments:
        if status and a["status"] != status:
            continue
        if employee and str(a["employee_id"]) != employee:
            continue

        task = next((t for t in tasks if t["task_id"] == a["task_id"]), None)

        if task:
            result.append({
                "assignment_id": a["assignment_id"],
                "task_title": task["task_title"],
                "priority": task["task_priority"],
                "status": a["status"],
                "employee_id": a["employee_id"]
            })

    return jsonify(result)


# UPDATE STATUS
@app.route('/update-status/<int:id>', methods=['PUT'])
def update_status(id):
    data = request.json

    for a in assignments:
        if a["assignment_id"] == id:
            a["status"] = data.get("status")
            return jsonify({"message": "Updated"})

    return jsonify({"message": "Not found"}), 404


# DELETE TASK
@app.route('/delete-task/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks, assignments

    assignments = [a for a in assignments if a["task_id"] != id]
    tasks = [t for t in tasks if t["task_id"] != id]

    return jsonify({"message": "Deleted"})


# TASK STATS
@app.route('/task-stats', methods=['GET'])
def task_stats():
    stats = {"Pending": 0, "In Progress": 0, "Completed": 0}

    for a in assignments:
        stats[a["status"]] += 1

    return jsonify(stats)


# -------------------------
# RUN APP
# -------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)