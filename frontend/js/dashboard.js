document.addEventListener(
    "DOMContentLoaded",
    loadDashboard
);


async function loadDashboard() {

    try {

        const response =
            await fetch("/api/auth/user");

        const user =
            await response.json();


        if (!user.logged_in) {

            window.location.href =
                "/login.html";

            return;
        }


        document.getElementById(
            "userName"
        ).textContent = user.name;


        document.getElementById(
            "welcomeName"
        ).textContent = user.name;


        await loadRepositories();


    } catch (error) {

        console.error(error);
    }
}


async function loadRepositories() {

    const response =
        await fetch("/api/repositories");


    const repositories =
        await response.json();


    const container =
        document.getElementById(
            "repositories"
        );


    container.innerHTML = "";


    if (!repositories.length) {

        container.innerHTML = `
            <div class="col-12">

                <div class="empty-state">

                    <h5>
                        No repositories analyzed yet
                    </h5>

                    <p>
                        Enter a GitHub repository above
                        to create your first analysis.
                    </p>

                </div>

            </div>
        `;

        return;
    }


    repositories.forEach(repository => {

        container.innerHTML += `

            <div class="col-md-6 col-lg-4">

                <div class="card repository-card h-100">

                    <div class="card-body">

                        <h5>
                            ${escapeHtml(repository.name)}
                        </h5>

                        <p class="text-muted">
                            ${
                                escapeHtml(
                                    repository.description || 
                                    "No description available."
                                )
                            }
                        </p>

                        <div class="small mb-3">

                            <span class="badge bg-secondary">
                                ${
                                    escapeHtml(
                                        repository.language ||
                                        "Unknown"
                                    )
                                }
                            </span>

                            <span class="ms-2">
                                ⭐ ${repository.stars}
                            </span>

                            <span class="ms-2">
                                🍴 ${repository.forks}
                            </span>

                        </div>


                        <a
                            href="/repository.html?id=${repository.id}"
                            class="btn btn-primary w-100"
                        >
                            View Analysis
                        </a>

                    </div>

                </div>

            </div>
        `;
    });
}


async function analyzeRepository() {

    const githubUrl =
        document.getElementById(
            "githubUrl"
        ).value.trim();


    const message =
        document.getElementById(
            "message"
        );


    if (!githubUrl) {

        message.innerHTML = `
            <div class="alert alert-danger">
                Please enter a GitHub repository URL.
            </div>
        `;

        return;
    }


    message.innerHTML = `
        <div class="alert alert-info">
            <strong>Step 1/2:</strong>
            Fetching repository from GitHub...
        </div>
    `;


    try {

        const response =
            await fetch(
                "/api/repositories/analyze",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        github_url: githubUrl
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            message.innerHTML = `
                <div class="alert alert-danger">
                    ${escapeHtml(data.error)}
                </div>
            `;

            return;
        }


        message.innerHTML = `
            <div class="alert alert-info">
                <strong>Step 2/2:</strong>
                Generating AI analysis with Groq...
            </div>
        `;


        const aiResponse =
            await fetch(
                `/api/ai/analyze/${data.repository_id}`,
                {
                    method: "POST"
                }
            );


        const aiData =
            await aiResponse.json();


        if (!aiResponse.ok) {

            message.innerHTML = `
                <div class="alert alert-danger">
                    ${escapeHtml(aiData.error)}
                </div>
            `;

            return;
        }


        window.location.href =
            `/repository.html?id=${data.repository_id}`;


    } catch (error) {

        console.error(error);

        message.innerHTML = `
            <div class="alert alert-danger">
                Something went wrong while analyzing
                the repository.
            </div>
        `;
    }
}


async function logout() {

    await fetch(
        "/api/auth/logout",
        {
            method: "POST"
        }
    );

    window.location.href =
        "/index.html";
}


function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}