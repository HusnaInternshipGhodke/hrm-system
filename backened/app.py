from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time
import os

app = Flask(__name__)
CORS(app)

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
# STORAGE
# -------------------------
departments = []
roles = []
employees = []

deleted_departments = []
deleted_roles = []
deleted_employees = []

# -------------------------
# TASK STORAGE
# -------------------------
tasks = []
assignments = []
task_id_counter = 1
assignment_id_counter = 1

# -------------------------
# REVIEW STORAGE (MODULE 5)
# -------------------------
reviews = []
review_id_counter = 1

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

    if username in users and users[username]["password"] == password:
        return jsonify({"status": True, "message": "Login successful"})

    return jsonify({"status": False, "message": "Invalid credentials"})

# -------------------------
# OTP
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

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    username = data.get("username")

    record = otp_store.get(username)

    if not record or not record["verified"]:
        return jsonify({"message": "OTP not verified"}), 400

    users[username]["password"] = "1234"
    del otp_store[username]

    return jsonify({"message": "Password reset to 1234"})

# =====================================================
# DEPARTMENT
# =====================================================
@app.route('/departments', methods=['GET'])
def get_departments():
    return jsonify(departments)

@app.route('/departments', methods=['POST'])
def add_department():
    data = request.json
    departments.append(data)
    return jsonify({"message": "Department added"})

@app.route('/departments/delete/<int:index>', methods=['DELETE'])
def delete_department(index):
    if index < len(departments):
        deleted_departments.append(departments[index])
        departments.pop(index)
    return jsonify({"message": "Deleted"})

@app.route('/departments/restore/<int:index>', methods=['POST'])
def restore_department(index):
    if index < len(deleted_departments):
        departments.append(deleted_departments[index])
        deleted_departments.pop(index)
    return jsonify({"message": "Restored"})

# =====================================================
# ROLE
# =====================================================
@app.route('/roles', methods=['GET'])
def get_roles():
    return jsonify(roles)

@app.route('/roles', methods=['POST'])
def add_role():
    data = request.json
    roles.append(data)
    return jsonify({"message": "Role added"})

@app.route('/roles/delete/<int:index>', methods=['DELETE'])
def delete_role(index):
    if index < len(roles):
        deleted_roles.append(roles[index])
        roles.pop(index)
    return jsonify({"message": "Deleted"})

@app.route('/roles/restore/<int:index>', methods=['POST'])
def restore_role(index):
    if index < len(deleted_roles):
        roles.append(deleted_roles[index])
        deleted_roles.pop(index)
    return jsonify({"message": "Restored"})

# =====================================================
# EMPLOYEE
# =====================================================
@app.route('/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
def add_employee():
    data = request.json
    employees.append(data)
    return jsonify({"message": "Employee added"})

@app.route('/employees/delete/<int:index>', methods=['DELETE'])
def delete_employee(index):
    if index < len(employees):
        deleted_employees.append(employees[index])
        employees.pop(index)
    return jsonify({"message": "Deleted"})

@app.route('/employees/restore/<int:index>', methods=['POST'])
def restore_employee(index):
    if index < len(deleted_employees):
        employees.append(deleted_employees[index])
        deleted_employees.pop(index)
    return jsonify({"message": "Restored"})

# =====================================================
# TASK MODULE
# =====================================================
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

@app.route('/tasks', methods=['GET'])
def get_tasks():
    result = []

    for a in assignments:
        task = next((t for t in tasks if t["task_id"] == a["task_id"]), None)

        if task:
            result.append({
                "assignment_id": a["assignment_id"],
                "task_title": task["task_title"],
                "task_priority": task["task_priority"],
                "status": a["status"],
                "employee_id": a["employee_id"]
            })

    return jsonify(result)

@app.route('/update-status/<int:id>', methods=['PUT'])
def update_status(id):
    data = request.json

    for a in assignments:
        if a["assignment_id"] == id:
            a["status"] = data.get("status")
            return jsonify({"message": "Updated"})

    return jsonify({"message": "Not found"}), 404

# =====================================================
# ✅ MODULE 5: PERFORMANCE REVIEW
# =====================================================
@app.route('/add-review', methods=['POST'])
def add_review():
    global review_id_counter

    data = request.json

    review = {
        "review_id": review_id_counter,
        "review_title": data.get("review_title"),
        "review_date": data.get("review_date"),
        "employee_id": data.get("employee_id"),
        "reviewed_by": data.get("reviewed_by"),
        "review_period": data.get("review_period"),
        "rating": data.get("rating"),
        "comments": data.get("comments"),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    reviews.append(review)
    review_id_counter += 1

    return jsonify({"message": "Review added"})

@app.route('/reviews', methods=['GET'])
def get_reviews():
    return jsonify(reviews)

@app.route('/delete-review/<int:id>', methods=['DELETE'])
def delete_review(id):
    global reviews
    reviews = [r for r in reviews if r["review_id"] != id]
    return jsonify({"message": "Deleted"})

# =====================================================
# ✅ MODULE 6: LEAVE MANAGEMENT
# =====================================================

leaves = []
leave_id_counter = 1

leave_quota = []
quota_id_counter = 1


# APPLY LEAVE
@app.route('/apply-leave', methods=['POST'])
def apply_leave():
    global leave_id_counter

    data = request.json

    leave = {
        "leave_id": leave_id_counter,
        "employee_id": data.get("employee_id"),
        "leave_type": data.get("leave_type"),
        "reason": data.get("reason"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "status": "pending"
    }

    leaves.append(leave)
    leave_id_counter += 1

    return jsonify({"message": "Leave Applied"})


# GET LEAVES
@app.route('/leaves', methods=['GET'])
def get_leaves():
    return jsonify(leaves)


# UPDATE (Employee edit before approval)
@app.route('/update-leave/<int:id>', methods=['PUT'])
def update_leave(id):
    data = request.json

    for l in leaves:
        if l["leave_id"] == id:
            if l["status"] == "pending":
                l["leave_type"] = data.get("leave_type")
                l["reason"] = data.get("reason")
                return jsonify({"message": "Updated"})
            else:
                return jsonify({"message": "Cannot edit approved/rejected"}), 400

    return jsonify({"message": "Not found"}), 404


# APPROVE / REJECT (Manager)
@app.route('/approve-leave/<int:id>', methods=['PUT'])
def approve_leave(id):
    data = request.json

    for l in leaves:
        if l["leave_id"] == id:
            l["status"] = data.get("status")
            return jsonify({"message": "Status Updated"})

    return jsonify({"message": "Not found"}), 404


# ADD LEAVE QUOTA
@app.route('/add-quota', methods=['POST'])
def add_quota():
    global quota_id_counter

    data = request.json

    quota = {
        "quota_id": quota_id_counter,
        "employee_id": data.get("employee_id"),
        "leave_type": data.get("leave_type"),
        "total_quota": data.get("total_quota"),
        "used_quota": 0,
        "remain_quota": data.get("total_quota")
    }

    leave_quota.append(quota)
    quota_id_counter += 1

    return jsonify({"message": "Quota Added"})


# GET QUOTA
@app.route('/quota', methods=['GET'])
def get_quota():
    return jsonify(leave_quota)
# -------------------------
# RUN
# -------------------------
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)