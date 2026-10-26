const loginForm = document.getElementById("login-form");
const loginMessage = document.getElementById("login-message");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();


    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });


    const data = await response.json();

    if (response.ok) {
    localStorage.setItem("access_token", data.access_token);

    const token = localStorage.getItem("access_token");
    console.log("Token exists:", token !== null);

    const meResponse = await fetch("http://127.0.0.1:8000/auth/me", {
    method: "GET",
    headers: {
        "Authorization": "Bearer " + token
    }
});

    console.log("ME status:", meResponse.status);

    const meData = await meResponse.json();
    console.log("Current user:", meData);

    loginMessage.textContent = "Anmeldung erfolgreich!";

}

});