from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ================= DATA =================
departments = []
roles = []
employees = []

# ================= LOGIN =================
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if data.get('username') == "admin" and data.get('password') == "1234":
        return jsonify({"status": True})
    
    return jsonify({"status": False})


# ================= DEPARTMENT =================
@app.route('/add-department', methods=['POST'])
def add_department():
    data = request.get_json()

    dept = {
        "id": len(departments) + 1,
        "name": data.get('name'),
        "description": data.get('description'),
        "status": True
    }

    departments.append(dept)
    return jsonify({"message": "added"})


@app.route('/all-departments')
def get_departments():
    return jsonify(departments)


@app.route('/delete-department/<int:id>', methods=['PUT'])
def delete_department(id):
    for d in departments:
        if d['id'] == id:
            d['status'] = False
    return jsonify({"message": "deleted"})


@app.route('/restore-department/<int:id>', methods=['PUT'])
def restore_department(id):
    for d in departments:
        if d['id'] == id:
            d['status'] = True
    return jsonify({"message": "restored"})


@app.route('/update-department/<int:id>', methods=['PUT'])
def update_department(id):
    data = request.get_json()

    for d in departments:
        if d['id'] == id:
            d['name'] = data.get('name')
            d['description'] = data.get('description')

    return jsonify({"message": "updated"})


# ================= ROLE =================
@app.route('/add-role', methods=['POST'])
def add_role():
    data = request.get_json()

    role = {
        "id": len(roles) + 1,
        "name": data.get('name'),
        "description": data.get('description'),
        "status": True
    }

    roles.append(role)
    return jsonify({"message": "added"})


@app.route('/all-roles')
def get_roles():
    return jsonify(roles)


@app.route('/delete-role/<int:id>', methods=['PUT'])
def delete_role(id):
    for r in roles:
        if r['id'] == id:
            r['status'] = False
    return jsonify({"message": "deleted"})


@app.route('/restore-role/<int:id>', methods=['PUT'])
def restore_role(id):
    for r in roles:
        if r['id'] == id:
            r['status'] = True
    return jsonify({"message": "restored"})


@app.route('/update-role/<int:id>', methods=['PUT'])
def update_role(id):
    data = request.get_json()

    for r in roles:
        if r['id'] == id:
            r['name'] = data.get('name')
            r['description'] = data.get('description')

    return jsonify({"message": "updated"})


# ================= EMPLOYEE =================
@app.route('/add-employee', methods=['POST'])
def add_employee():
    data = request.get_json()

    emp = {
        "id": len(employees) + 1,
        "firstName": data.get('firstName'),
        "lastName": data.get('lastName'),
        "email": data.get('email'),
        "mobile": data.get('mobile'),
        "department": data.get('department'),
        "role": data.get('role'),
        "manager": data.get('manager'),
        "status": True
    }

    employees.append(emp)
    return jsonify({"message": "added"})


@app.route('/all-employees')
def get_employees():
    return jsonify(employees)


@app.route('/delete-employee/<int:id>', methods=['PUT'])
def delete_employee(id):
    for e in employees:
        if e['id'] == id:
            e['status'] = False
    return jsonify({"message": "deleted"})


@app.route('/restore-employee/<int:id>', methods=['PUT'])
def restore_employee(id):
    for e in employees:
        if e['id'] == id:
            e['status'] = True
    return jsonify({"message": "restored"})


@app.route('/update-employee/<int:id>', methods=['PUT'])
def update_employee(id):
    data = request.get_json()

    for e in employees:
        if e['id'] == id:
            e.update(data)

    return jsonify({"message": "updated"})


# ================= RUN =================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))