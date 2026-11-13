
// ======================================
// 1. CHECK LOGIN STATUS
// ======================================

function checkLogin() {

    const token = sessionStorage.getItem("access_token");

    if (!token) {
        window.location.replace("login.html");
        return false;
    }

    return true;
}


// ======================================
// 2. LOGOUT FUNCTION
// ======================================

function logout() {

    sessionStorage.removeItem("access_token");

    window.location.replace("login.html");
}


// ======================================
// 3. GET AUTHORIZATION HEADERS
// ======================================

function getAuthHeaders() {

    const token = sessionStorage.getItem("access_token");

    if (!token) {
        window.location.replace("login.html");
        return {};
    }

    return {
        "Authorization": `Bearer ${token}`
    };
}
