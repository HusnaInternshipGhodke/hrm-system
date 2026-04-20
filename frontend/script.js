const BASE_URL = "https://hrm-system-eu3z.onrender.com";

// ==============================
// LOGIN
// ==============================
function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(BASE_URL + "/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status) {
            localStorage.setItem("login", "true");
            window.location.href = "department.html";
        } else {
            document.getElementById("error").innerText = data.message;
        }
    })
    .catch(() => {
        document.getElementById("error").innerText = "Server error";
    });
}

// FORGOT PASSWORD NAVIGATION
function goToForgot() {
    window.location.href = "forgot.html";
}


// ==============================
// TASK MODULE
// ==============================

// CREATE TASK
async function createTask() {
    const data = {
        task_title: document.getElementById("task_title").value,
        task_description: document.getElementById("task_description").value,
        task_priority: document.getElementById("task_priority").value,
        start_date: document.getElementById("start_date").value,
        end_date: document.getElementById("end_date").value,
        task_type: document.getElementById("task_type").value,
        employee_id: document.getElementById("employee_id").value
    };

    const res = await fetch(BASE_URL + "/create-task", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.message);

    loadTasks();
}

// LOAD TASKS
async function loadTasks() {
    const res = await fetch(BASE_URL + "/tasks");
    const data = await res.json();

    let html = "";

    data.forEach(t => {
        html += `
        <tr>
            <td>${t.task_title}</td>
            <td>${t.priority}</td>
            <td>${t.status}</td>
            <td>
                <button onclick="updateTaskStatus(${t.assignment_id}, 'Completed')">Complete</button>
            </td>
        </tr>
        `;
    });

    document.getElementById("taskTable").innerHTML = html;
}

// UPDATE STATUS
async function updateTaskStatus(id, status) {
    await fetch(BASE_URL + "/update-status/" + id, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ status })
    });

    loadTasks();
}