const API_URL = "https://hrm-system-eu3z.onrender.com";

// =====================
// DEPARTMENT
// =====================
async function addDepartment() {
    const name = document.getElementById("name").value;
    const description = document.getElementById("description").value;

    await fetch(API_URL + "/departments", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    loadDepartments();
}

async function loadDepartments() {
    const res = await fetch(API_URL + "/departments");
    const data = await res.json();

    let html = "";
    data.forEach((d, i) => {
        html += `<li>${d.name}
            <button onclick="deleteDepartment(${i})">Delete</button>
            <button onclick="restoreDepartment(${i})">Restore</button>
        </li>`;
    });

    document.getElementById("departmentList").innerHTML = html;

    let dropdown = "";
    data.forEach(d => {
        dropdown += `<option>${d.name}</option>`;
    });

    document.getElementById("department").innerHTML = dropdown;
}

async function deleteDepartment(i) {
    await fetch(API_URL + "/departments/delete/" + i, { method: "DELETE" });
    loadDepartments();
}

async function restoreDepartment(i) {
    await fetch(API_URL + "/departments/restore/" + i, { method: "POST" });
    loadDepartments();
}

// =====================
// ROLE
// =====================
async function addRole() {
    const name = document.getElementById("roleName").value;
    const description = document.getElementById("roleDesc").value;

    await fetch(API_URL + "/roles", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    loadRoles();
}

async function loadRoles() {
    const res = await fetch(API_URL + "/roles");
    const data = await res.json();

    let html = "";
    let dropdown = "";

    data.forEach((r, i) => {
        html += `<li>${r.name}
            <button onclick="deleteRole(${i})">Delete</button>
        </li>`;
        dropdown += `<option>${r.name}</option>`;
    });

    document.getElementById("roleList").innerHTML = html;
    document.getElementById("role").innerHTML = dropdown;
}

async function deleteRole(i) {
    await fetch(API_URL + "/roles/delete/" + i, { method: "DELETE" });
    loadRoles();
}

// =====================
// EMPLOYEE
// =====================
async function addEmployee() {
    const data = {
        fname: document.getElementById("firstName").value,
        lname: document.getElementById("lastName").value,
        email: document.getElementById("email").value,
        mobile: document.getElementById("mobile").value,
        department: document.getElementById("department").value,
        role: document.getElementById("role").value,
        manager: document.getElementById("manager").value
    };

    await fetch(API_URL + "/employees", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    loadEmployees();
}

async function loadEmployees() {
    const res = await fetch(API_URL + "/employees");
    const data = await res.json();

    let html = "";
    data.forEach((e, i) => {
        html += `<li>${e.fname}
            <button onclick="deleteEmployee(${i})">Delete</button>
        </li>`;
    });

    document.getElementById("employeeList").innerHTML = html;
}

async function deleteEmployee(i) {
    await fetch(API_URL + "/employees/delete/" + i, { method: "DELETE" });
    loadEmployees();
}

// =====================
function logout() {
    localStorage.removeItem("login");
    window.location.href = "index.html";
}

function goToTask() {
    window.location.href = "task.html";
}

// LOAD
window.onload = function () {
    loadDepartments();
    loadRoles();
    loadEmployees();
};