
const API_BASE = "http://127.0.0.1:8000";

const signupForm = document.getElementById("signupForm");
const signupMessage = document.getElementById("signupMessage");
const signupButton = document.getElementById("signupButton");

signupForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    signupMessage.textContent = "";

    if (!name || !email || !phone || !password || !confirmPassword) {
        signupMessage.style.color = "red";
        signupMessage.textContent = "Please fill all fields.";
        return;
    }

    if (password !== confirmPassword) {
        signupMessage.style.color = "red";
        signupMessage.textContent = "Passwords do not match.";
        return;
    }

    if (password.length < 8) {
        signupMessage.style.color = "red";
        signupMessage.textContent = "Password must be at least 8 characters.";
        return;
    }

    signupButton.disabled = true;
    signupButton.textContent = "Creating Account...";

    try {

        // STEP 1: CREATE ACCOUNT

        const signupResponse = await fetch(`${API_BASE}/users`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name,
                email,
                phone,
                password
            })
        });

        const signupData = await signupResponse.json();

        if (!signupResponse.ok) {
            const detail = signupData.detail;

            throw new Error(
                Array.isArray(detail)
                    ? detail.map(item => item.msg).join(", ")
                    : detail || "Signup failed."
            );
        }

        // STEP 2: AUTOMATIC LOGIN

        signupButton.textContent = "Logging in...";

        const loginResponse = await fetch(`${API_BASE}/users/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const loginData = await loginResponse.json();

        if (!loginResponse.ok) {
            throw new Error(
                loginData.detail || "Account created, but automatic login failed."
            );
        }

        // STEP 3: SAVE JWT TOKEN

        sessionStorage.setItem(
            "access_token",
            loginData.access_token
        );

        // STEP 4: OPEN DASHBOARD

        signupMessage.style.color = "green";
        signupMessage.textContent = "Account created! Opening Dashboard...";

        window.location.replace("dashboard.html");

    } catch (error) {

        signupMessage.style.color = "red";
        signupMessage.textContent = error.message;

    } finally {

        signupButton.disabled = false;
        signupButton.textContent = "Create Account";

    }

});
