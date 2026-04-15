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
departments = [
    {"id": 1, "name": "HR", "description": "Human Resource", "status": True},
    {"id": 2, "name": "IT", "description": "Tech Department", "status": True}
]

# Get all departments
@app.route('/all-departments', methods=['GET'])
def all_departments():
    return jsonify(departments)

# Add department
@app.route('/add-department', methods=['POST'])
def add_department():
    data = request.json

    new_dept = {
        "id": len(departments) + 1,
        "name": data['name'],
        "description": data['description'],
        "status": True
    }

    departments.append(new_dept)
    return jsonify({"message": "Department added"})

# Soft delete
@app.route('/delete-department/<int:id>', methods=['PUT'])
def delete_department(id):
    for d in departments:
        if d['id'] == id:
            d['status'] = False
    return jsonify({"message": "Deleted"})

# Restore
@app.route('/restore-department/<int:id>', methods=['PUT'])
def restore_department(id):
    for d in departments:
        if d['id'] == id:
            d['status'] = True
    return jsonify({"message": "Restored"})

@app.route('/update-department/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.get_json()

    for d in departments:
        if d['id'] == id:
            d['name'] = data.get("name")
            d['description'] = data.get("description")

    return jsonify({"message": "Updated"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

    # Login API
