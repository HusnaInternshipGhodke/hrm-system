const API_URL = "https://hrm-system-eu3z.onrender.com";
let editId = null;

// Add / Update Department
function addDepartment() {
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    if (editId !== null) {
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
    });
}

// Delete
function deleteDepartment(id) {
    fetch(`${API_URL}/delete-department/${id}`, {
        method: "PUT"
    }).then(() => getDepartments());
}

// Restore
function restoreDepartment(id) {
    fetch(`${API_URL}/restore-department/${id}`, {
        method: "PUT"
    }).then(() => getDepartments());
}

// Edit
function editDepartment(id, name, description) {
    document.getElementById("name").value = name;
    document.getElementById("description").value = description;
    editId = id;
}

// Load data
getDepartments();


