const registerForm = document.getElementById("register-form");
const registerMessage = document.getElementById("register-message");

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;

    const response = await fetch("http://127.0.0.1:8000/auth/register", {
        method: "POST",
        headers: {
    "Content-Type": "application/json"
        },
        body: JSON.stringify({
    email: email,
    password: password
        })
    });


    console.log("Status:", response.status);

    const data = await response.json();

    console.log("Response:", data);

    if (response.ok) {
    registerMessage.textContent = "Konto erfolgreich erstellt!";
    }
    else {
    registerMessage.textContent = data.detail;
    }

});


