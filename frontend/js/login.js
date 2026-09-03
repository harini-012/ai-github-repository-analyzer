async function loginUser() {

    const email =
        document.getElementById("email").value.trim();

    const password =
        document.getElementById("password").value;

    const message =
        document.getElementById("message");


    if (!email || !password) {

        message.innerHTML = `
            <div class="alert alert-danger">
                Please enter email and password.
            </div>
        `;

        return;
    }


    try {

        const response = await fetch(
            "/api/auth/login",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );


        const data = await response.json();


        if (!response.ok) {

            message.innerHTML = `
                <div class="alert alert-danger">
                    ${data.error}
                </div>
            `;

            return;
        }


        window.location.href =
            "/dashboard.html";


    } catch (error) {

        message.innerHTML = `
            <div class="alert alert-danger">
                Unable to connect to the server.
            </div>
        `;
    }
}