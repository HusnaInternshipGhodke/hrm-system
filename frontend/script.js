const API_URL = "https://hrm-system-eu3z.onrender.com";

let editId = null;

// ================= DEPARTMENT =================

// Add / Update Department
function addDepartment() {
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    if (editId !== null) {
        // UPDATE
        fetch(`${API_URL}/update-department/${editId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, description })
        })
        .then(() => {
            alert("Department Updated");
            editId = null;
            getDepartments();
        });

    } else {
        // ADD
        fetch(`${API_URL}/add-department`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, description })
        })
        .then(() => {
            alert("Department Added");
            getDepartments();
        });
    }
}

// Get Departments
function getDepartments() {
    fetch(`${API_URL}/all-departments`)
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("departmentList");

        if (!list) return;

        list.innerHTML = "";

        data.forEach(dep => {
            const li = document.createElement("li");

            if (dep.status) {
                li.innerHTML = `
                    ${dep.name} - ${dep.description}
                    <button onclick="editDepartment(${dep.id}, '${dep.name}', '${dep.description}')">Edit</button>
                    <button onclick="deleteDepartment(${dep.id})">Delete</button>
                `;
            } else {
                li.innerHTML = `
                    ${dep.name} - ${dep.description} (Inactive)
                    <button onclick="restoreDepartment(${dep.id})">Restore</button>
                `;
            }

            list.appendChild(li);
        });
    })
    .catch(err => console.log(err));
}

// Delete Department
function deleteDepartment(id) {
    fetch(`${API_URL}/delete-department/${id}`, {
        method: "PUT"
    })
    .then(() => getDepartments());
}

// Restore Department
function restoreDepartment(id) {
    fetch(`${API_URL}/restore-department/${id}`, {
        method: "PUT"
    })
    .then(() => getDepartments());
}

// Edit Department
function editDepartment(id, name, description) {
    document.getElementById("name").value = name;
    document.getElementById("description").value = description;
    editId = id;
}

// Load Departments
getDepartments();


// ================= ROLE =================

// Get Roles
function getRoles() {
    fetch(`${API_URL}/all-roles`)
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("roleList");

        if (!list) return;

        list.innerHTML = "";

        data.forEach(role => {
            const li = document.createElement("li");

            if (role.status) {
                li.innerHTML = `
                    ${role.name} - ${role.description}
                    <button onclick="deleteRole(${role.id})">Delete</button>
                `;
            } else {
                li.innerHTML = `
                    ${role.name} - ${role.description} (Inactive)
                    <button onclick="restoreRole(${role.id})">Restore</button>
                `;
            }

            list.appendChild(li);
        });
    })
    .catch(err => console.log(err));
}

// Add Role
function addRole() {
    const name = document.getElementById("roleName").value;
    const description = document.getElementById("roleDesc").value;

    fetch(`${API_URL}/add-role`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name, description })
    })
    .then(() => {
        alert("Role Added");
        getRoles();
    });
}

// Delete Role
function deleteRole(id) {
    fetch(`${API_URL}/delete-role/${id}`, {
        method: "PUT"
    })
    .then(() => getRoles());
}

// Restore Role
function restoreRole(id) {
    fetch(`${API_URL}/restore-role/${id}`, {
        method: "PUT"
    })
    .then(() => getRoles());
}

// Load Roles
getRoles();