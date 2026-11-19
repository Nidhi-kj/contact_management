// ======================================
// 1. API CONFIGURATION
// ======================================

 const API_BASE = "http://127.0.0.1:8000";
// const API_BASE = "https://contact-management-r4in.onrender.com";


// ======================================
// 2. LOGIN FORM ELEMENTS
// ======================================

const loginForm = document.getElementById("loginForm");

const emailInput = document.getElementById("email");

const passwordInput = document.getElementById("password");

const togglePassword = document.getElementById("togglePassword");

const loginMessage = document.getElementById("loginMessage");

const loginButton = document.getElementById("loginButton");


// ======================================
// 3. SHOW / HIDE PASSWORD
// ======================================

togglePassword.addEventListener("click", function () {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        togglePassword.textContent = "Hide";

    } else {

        passwordInput.type = "password";

        togglePassword.textContent = "Show";

    }

});


// ======================================
// 4. LOGIN FORM SUBMIT
// ======================================

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const email = emailInput.value.trim();

    const password = passwordInput.value;


    // Clear previous message
    loginMessage.textContent = "";

    loginMessage.style.color = "#d93025";


    // Basic validation
    if (!email || !password) {

        loginMessage.textContent = "Please enter email and password.";

        return;

    }


    // Disable button
    loginButton.disabled = true;

    loginButton.textContent = "Logging in...";


    try {

        // Send login request to FastAPI
        const response = await fetch(`${API_BASE}/users/login`, {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                email: email,

                password: password

            })

        });


        // Get API response
        const data = await response.json();


        // Check login error
        if (!response.ok) {

            let errorMessage = "Invalid email or password.";

            if (typeof data.detail === "string") {

                errorMessage = data.detail;

            } else if (Array.isArray(data.detail)) {

                errorMessage = data.detail
                    .map(error => error.msg)
                    .join(", ");

            }

            throw new Error(errorMessage);

        }


        // Check access token
        if (!data.access_token) {

            throw new Error("Access token not received from server.");

        }


        // Save JWT token in session storage
        sessionStorage.setItem("access_token", data.access_token);


        // Show success message
        loginMessage.style.color = "green";

        loginMessage.textContent = "Login successful! Redirecting...";


        // Redirect to Dashboard
        window.location.replace("dashboard.html");


    } catch (error) {

        loginMessage.style.color = "#d93025";

        loginMessage.textContent = error.message;


    } finally {

        loginButton.disabled = false;

        loginButton.textContent = "Login";

    }

});