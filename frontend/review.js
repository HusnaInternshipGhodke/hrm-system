const BASE_URL = "https://hrm-system-eu3z.onrender.com";

// LOAD EMPLOYEES IN DROPDOWN
async function loadEmployees() {
    const res = await fetch(BASE_URL + "/employees");
    const data = await res.json();

    let options = "";

    data.forEach((e, i) => {
        options += `<option value="${i}">${e.fname}</option>`;
    });

    document.getElementById("employee").innerHTML = options;
}


// ADD REVIEW
async function addReview() {
    const data = {
        review_title: document.getElementById("title").value,
        review_date: document.getElementById("date").value,
        employee_id: document.getElementById("employee").value,
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
    loadReviews();
}


// LOAD REVIEWS
async function loadReviews() {
    const res = await fetch(BASE_URL + "/reviews");
    const data = await res.json();

    let html = "";

    data.forEach(r => {
        html += `
        <tr>
            <td>${r.review_title}</td>
            <td>${r.employee_id}</td>
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
window.onload = function () {
    loadEmployees();
    loadReviews();
};