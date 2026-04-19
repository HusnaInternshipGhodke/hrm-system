from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():
    try:

        
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if username == "admin" and password == "1234":
            return jsonify({"status": True}), 200
        else:
            return jsonify({"status": False}), 200

    except Exception as e:
        return jsonify({"status": False}), 500


# ================= DEPARTMENT =================

departments = [
    {"id": 1, "name": "HR", "description": "Human Resource", "status": True},
    {"id": 2, "name": "IT", "description": "Tech Department", "status": True}
]

@app.route('/all-departments', methods=['GET'])
def all_departments():
    return jsonify(departments)

@app.route('/add-department', methods=['POST'])
def add_department():
    data = request.get_json()

    new_dept = {
        "id": len(departments) + 1,
        "name": data.get("name"),
        "description": data.get("description"),
        "status": True
    }

    departments.append(new_dept)
    return jsonify({"message": "Department added"})

@app.route('/update-department/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.get_json()

    for d in departments:
        if d['id'] == id:
            d['name'] = data.get("name")
            d['description'] = data.get("description")

    return jsonify({"message": "Updated"})

@app.route('/delete-department/<int:id>', methods=['PUT'])
def delete_department(id):
    for d in departments:
        if d['id'] == id:
            d['status'] = False
    return jsonify({"message": "Deleted"})

@app.route('/restore-department/<int:id>', methods=['PUT'])
def restore_department(id):
    for d in departments:
        if d['id'] == id:
            d['status'] = True
    return jsonify({"message": "Restored"})


# ================= ROLE =================

roles = [
    {"id": 1, "name": "Admin", "description": "Full Access", "status": True},
    {"id": 2, "name": "Manager", "description": "Manage Team", "status": True}
]

@app.route('/all-roles', methods=['GET'])
def all_roles():
    return jsonify(roles)

@app.route('/add-role', methods=['POST'])
def add_role():
    data = request.get_json()

    new_role = {
        "id": len(roles) + 1,
        "name": data.get("name"),
        "description": data.get("description"),
        "status": True
    }

    roles.append(new_role)
    return jsonify({"message": "Role added"})

@app.route('/delete-role/<int:id>', methods=['PUT'])
def delete_role(id):
    for r in roles:
        if r['id'] == id:
            r['status'] = False
    return jsonify({"message": "Role deleted"})

@app.route('/restore-role/<int:id>', methods=['PUT'])
def restore_role(id):
    for r in roles:
        if r['id'] == id:
            r['status'] = True
    return jsonify({"message": "Role restored"})
# ---------------- EMPLOYEE ---------------- #

employees = []

# Get all employees
@app.route('/all-employees', methods=['GET'])
def all_employees():
    return jsonify(employees)

# Add employee
@app.route('/add-employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    new_emp = {
        "id": len(employees) + 1,
        "first_name": data.get("first_name"),
        "last_name": data.get("last_name"),
        "email": data.get("email"),
        "mobile": data.get("mobile"),
        "department": data.get("department"),
        "role": data.get("role"),
        "manager": data.get("manager"),
        "status": True
    }

    employees.append(new_emp)
    return jsonify({"message": "Employee added"})

# Update employee
@app.route('/update-employee/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()

    for e in employees:
        if e['id'] == id:
            e['first_name'] = data.get("first_name")
            e['last_name'] = data.get("last_name")
            e['email'] = data.get("email")
            e['mobile'] = data.get("mobile")
            e['department'] = data.get("department")
            e['role'] = data.get("role")
            e['manager'] = data.get("manager")

    return jsonify({"message": "Employee updated"})

# Delete employee
@app.route('/delete-employee/<int:id>', methods=['PUT'])
def delete_employee(id):
    for e in employees:
        if e['id'] == id:
            e['status'] = False
    return jsonify({"message": "Employee deleted"})

# Restore employee
@app.route('/restore-employee/<int:id>', methods=['PUT'])
def restore_employee(id):
    for e in employees:
        if e['id'] == id:
            e['status'] = True
    return jsonify({"message": "Employee restored"})

# ================= RUN =================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    # employee module added


