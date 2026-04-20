const BASE_URL = "https://hrm-system-eu3z.onrender.com";

let employees = [];

// LOAD EMPLOYEES
async function loadEmployees() {
    const res = await fetch(BASE_URL + "/employees");
    employees = await res.json();

    let options = "<option value=''>Select Employee</option>";

    employees.forEach((e, i) => {
        const name = e.fname || e.name || ("Employee " + i);
        options += `<option value="${i}">${name}</option>`;
    });

    document.getElementById("employee").innerHTML = options;
}


// ADD REVIEW
async function addReview() {

    const employeeId = document.getElementById("employee").value;

    if (!employeeId) {
        alert("Please select employee");
        return;
    }

    const data = {
        review_title: document.getElementById("title").value,
        review_date: document.getElementById("date").value,
        employee_id: employeeId,
        reviewed_by: "admin",
        review_period: document.getElementById("period").value,
        rating: document.getElementById("rating").value,
        comments: document.getElementById("comments").value
    };

    await fetch(BASE_URL + "/add-review", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    alert("Review Added");

    document.getElementById("title").value = "";
    document.getElementById("rating").value = "";
    document.getElementById("comments").value = "";

    loadReviews();
}


// LOAD REVIEWS
async function loadReviews() {
    const res = await fetch(BASE_URL + "/reviews");
    const data = await res.json();

    let html = "";

    data.forEach(r => {

        const emp = employees[r.employee_id];
        const empName = emp ? (emp.fname || emp.name) : "Unknown";

        html += `
        <tr>
            <td>${r.review_title}</td>
            <td>${empName}</td>
            <td>${r.review_period}</td>
            <td>${r.rating}</td>
            <td>
                <button onclick="deleteReview(${r.review_id})">Delete</button>
            </td>
        </tr>`;
    });

    document.getElementById("reviewTable").innerHTML = html;
}


// DELETE REVIEW
async function deleteReview(id) {
    await fetch(BASE_URL + "/delete-review/" + id, {
        method: "DELETE"
    });

    loadReviews();
}


// LOAD ON START
window.onload = async function () {
    await loadEmployees();
    loadReviews();
};