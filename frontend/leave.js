const BASE_URL = "https://hrm-system-eu3z.onrender.com";

let employees = [];

// LOAD EMPLOYEES
async function loadEmployees() {
    const res = await fetch(BASE_URL + "/employees");
    employees = await res.json();

    let opt = "";
    employees.forEach((e,i)=>{
        opt += `<option value="${i}">${e.fname}</option>`;
    });

    document.getElementById("employee").innerHTML = opt;
}


// APPLY LEAVE
async function applyLeave() {

    const data = {
        employee_id: document.getElementById("employee").value,
        leave_type: document.getElementById("type").value,
        start_date: document.getElementById("start").value,
        end_date: document.getElementById("end").value,
        reason: document.getElementById("reason").value
    };

    await fetch(BASE_URL + "/apply-leave", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify(data)
    });

    alert("Leave Applied");
    loadLeaves();
}


// LOAD LEAVES
async function loadLeaves() {
    const res = await fetch(BASE_URL + "/leaves");
    const data = await res.json();

    let html = "";

    data.forEach(l => {

        const emp = employees[l.employee_id];
        const name = emp ? emp.fname : "Unknown";

        html += `
        <tr>
            <td>${name}</td>
            <td>${l.leave_type}</td>
            <td>${l.start_date} - ${l.end_date}</td>
            <td class="${l.status}">${l.status}</td>
            <td>
                ${l.status === "pending" ? `
                <button onclick="approve(${l.leave_id}, 'approved')">Approve</button>
                <button onclick="approve(${l.leave_id}, 'rejected')">Reject</button>
                ` : "Locked"}
            </td>
        </tr>`;
    });

    document.getElementById("table").innerHTML = html;
}


// APPROVE / REJECT
async function approve(id, status) {
    await fetch(BASE_URL + "/approve-leave/" + id, {
        method: "PUT",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({status})
    });

    loadLeaves();
}


// LOAD
window.onload = function() {
    loadEmployees();
    loadLeaves();
};