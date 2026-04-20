const API_URL = "https://hrm-system-eu3z.onrender.com";

// =====================
// DEPARTMENT
// =====================
async function addDepartment() {
    const name = document.getElementById("name").value;
    const desc = document.getElementById("description").value;

    await fetch(API_URL + "/departments", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, desc })
    });

    loadDepartments();
}

async function loadDepartments() {
    const res = await fetch(API_URL + "/departments");
    const data = await res.json();

    let html = "";
    let dropdown = "";

    data.forEach((d, i) => {
        html += `<li>${d.name} <button onclick="deleteDepartment(${i})">Delete</button></li>`;
        dropdown += `<option value="${d.name}">${d.name}</option>`;
    });

    document.getElementById("departmentList").innerHTML = html;
    document.getElementById("department").innerHTML = dropdown;
}

async function deleteDepartment(index) {
    await fetch(API_URL + "/departments/delete/" + index, {
        method: "DELETE"
    });
    loadDepartments();
}


// =====================
// ROLE
// =====================
async function addRole() {
    const name = document.getElementById("roleName").value;
    const desc = document.getElementById("roleDesc").value;

    await fetch(API_URL + "/roles", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, desc })
    });

    loadRoles();
}

async function loadRoles() {
    const res = await fetch(API_URL + "/roles");
    const data = await res.json();

    let html = "";
    let dropdown = "";

    data.forEach(r => {
        html += `<li>${r.name}</li>`;
        dropdown += `<option value="${r.name}">${r.name}</option>`;
    });

    document.getElementById("roleList").innerHTML = html;
    document.getElementById("role").innerHTML = dropdown;
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

    data.forEach(e => {
        html += `<li>${e.fname} (${e.department})</li>`;
    });

    document.getElementById("employeeList").innerHTML = html;
}


// =====================
// NAVIGATION
// =====================
function goToTask() {
    window.location.href = "task.html";
}

function logout() {
    localStorage.removeItem("login");
    window.location.href = "index.html";
}


// =====================
// AUTO LOAD
// =====================
window.onload = function () {
    loadDepartments();
    loadRoles();
    loadEmployees();
};