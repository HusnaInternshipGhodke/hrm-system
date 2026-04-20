<script>
const API_URL = "https://hrm-system-eu3z.onrender.com";

function login() {
    fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.status) {
            localStorage.setItem("login", "true");
            window.location = "department.html";
        } else {
            error.innerText = "Invalid login";
        }
    });
}

// ✅ THIS WAS MISSING
function goToForgot() {
    window.location.href = "forgot.html";
}
</script>