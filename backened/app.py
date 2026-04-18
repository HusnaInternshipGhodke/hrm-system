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


# ================= RUN =================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    