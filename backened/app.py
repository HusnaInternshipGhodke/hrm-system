from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Login API
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        print("Login attempt:", username, password)

        if username == "admin" and password == "1234":
            return jsonify({"status": True}), 200
        else:
            return jsonify({"status": False}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": False}), 500



# In-memory data
# In-memory data
departments = [
    {"id": 1, "name": "HR", "description": "Human Resource", "status": True},
    {"id": 2, "name": "IT", "description": "Tech Department", "status": True}
]

# ---------------- ROLE MANAGEMENT ---------------- #

roles = [
    {"id": 1, "name": "Admin", "description": "Full Access", "status": True},
    {"id": 2, "name": "Manager", "description": "Manage Team", "status": True}
]
# Get all roles
@app.route('/all-roles', methods=['GET'])
def all_roles():
    return jsonify(roles)

# Add role
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

# Delete role (soft delete)
@app.route('/delete-role/<int:id>', methods=['PUT'])
def delete_role(id):
    for r in roles:
        if r['id'] == id:
            r['status'] = False
    return jsonify({"message": "Role deleted"})

# Restore role
@app.route('/restore-role/<int:id>', methods=['PUT'])
def restore_role(id):
    for r in roles:
        if r['id'] == id:
            r['status'] = True
    return jsonify({"message": "Role restored"})