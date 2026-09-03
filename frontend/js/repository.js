document.addEventListener(
    "DOMContentLoaded",
    loadRepository
);


async function loadRepository() {

    const params =
        new URLSearchParams(
            window.location.search
        );

    const id =
        params.get("id");


    if (!id) {

        window.location.href =
            "/dashboard.html";

        return;
    }


    try {

        const response =
            await fetch(
                `/api/repositories/${id}`
            );


        const repository =
            await response.json();


        if (!response.ok) {

            window.location.href =
                "/dashboard.html";

            return;
        }


        displayRepository(repository);

        await loadAnalysis(id);


    } catch (error) {

        console.error(
            "Repository loading error:",
            error
        );

        window.location.href =
            "/dashboard.html";
    }
}


function displayRepository(repository) {

    document.getElementById(
        "repositoryInfo"
    ).innerHTML = `

        <div class="card">

            <div class="card-body p-4">

                <h1>
                    ${escapeHtml(repository.name)}
                </h1>

                <p class="text-muted">
                    ${
                        escapeHtml(
                            repository.description ||
                            "No description available."
                        )
                    }
                </p>


                <div class="row text-center mt-4">

                    <div class="col-md-4">

                        <strong>
                            Language
                        </strong>

                        <p class="mt-2">
                            ${
                                escapeHtml(
                                    repository.language ||
                                    "Unknown"
                                )
                            }
                        </p>

                    </div>


                    <div class="col-md-4">

                        <strong>
                            Stars
                        </strong>

                        <p class="mt-2">
                            ⭐ ${repository.stars || 0}
                        </p>

                    </div>


                    <div class="col-md-4">

                        <strong>
                            Forks
                        </strong>

                        <p class="mt-2">
                            🍴 ${repository.forks || 0}
                        </p>

                    </div>

                </div>


                <a
                    href="${escapeHtml(repository.github_url)}"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="btn btn-dark"
                >
                    Open GitHub
                </a>

            </div>

        </div>
    `;


    let files = repository.files || [];


    if (typeof files === "string") {

        try {

            files = JSON.parse(files);

        } catch (error) {

            console.error(
                "Unable to parse repository files:",
                error
            );

            files = [];
        }
    }


    if (!Array.isArray(files)) {
        files = [];
    }


    document.getElementById(
        "fileTree"
    ).textContent =
        files.join("\n");
}


async function loadAnalysis(id) {

    const analysisContainer =
        document.getElementById(
            "analysis"
        );


    // Show loading message first
    analysisContainer.innerHTML = `

        <div class="card">

            <div class="card-body p-4">

                <h3>
                    🤖 AI Analysis
                </h3>

                <p class="text-muted">
                    Loading AI analysis...
                </p>

            </div>

        </div>
    `;


    try {

        const response =
            await fetch(
                `/api/ai/${id}`
            );


        const analysis =
            await response.json();


        console.log(
            "AI analysis response:",
            analysis
        );


        if (!response.ok) {

            analysisContainer.innerHTML = `

                <div class="card">

                    <div class="card-body p-4">

                        <h3>
                            🤖 AI Analysis
                        </h3>

                        <p class="text-danger">
                            Unable to load AI analysis.
                        </p>

                        <p class="text-muted">
                            ${
                                escapeHtml(
                                    analysis.error ||
                                    "Unknown server error."
                                )
                            }
                        </p>

                    </div>

                </div>
            `;

            return;
        }


        /*
         * The backend returns an empty object
         * when no analysis exists.
         */

        if (
            !analysis ||
            typeof analysis !== "object" ||
            !analysis.summary ||
            !analysis.summary.trim()
        ) {

            analysisContainer.innerHTML = `

                <div class="card">

                    <div class="card-body p-4">

                        <h3>
                            🤖 AI Analysis
                        </h3>

                        <p class="text-muted">
                            No AI analysis is available yet.
                        </p>

                    </div>

                </div>
            `;

            return;
        }


        /*
         * Analysis exists.
         */

        analysisContainer.innerHTML = `

            <div class="card">

                <div class="card-body p-4">

                    <h3>
                        🤖 AI Analysis
                    </h3>

                    <hr>


                    <h4>
                        Project Summary
                    </h4>

                    <div class="analysis-text">
                        ${formatText(
                            analysis.summary
                        )}
                    </div>


                    <h4 class="mt-4">
                        Technologies
                    </h4>

                    <div class="analysis-text">
                        ${formatText(
                            analysis.technologies
                        )}
                    </div>


                    <h4 class="mt-4">
                        Project Architecture
                    </h4>

                    <div class="analysis-text">
                        ${formatText(
                            analysis.architecture
                        )}
                    </div>


                    <h4 class="mt-4">
                        Important Files
                    </h4>

                    <div class="analysis-text">
                        ${formatText(
                            analysis.important_files
                        )}
                    </div>


                    <h4 class="mt-4">
                        General Insights
                    </h4>

                    <div class="analysis-text">
                        ${formatText(
                            analysis.general_insights
                        )}
                    </div>

                </div>

            </div>
        `;


    } catch (error) {

        console.error(
            "AI analysis loading error:",
            error
        );


        analysisContainer.innerHTML = `

            <div class="card">

                <div class="card-body p-4">

                    <h3>
                        🤖 AI Analysis
                    </h3>

                    <p class="text-danger">
                        Error loading AI analysis.
                    </p>

                </div>

            </div>
        `;
    }
}


function formatText(text) {

    if (!text) {
        return "No information available.";
    }


    return escapeHtml(
        String(text)
    ).replace(
        /\n/g,
        "<br>"
    );
}


function escapeHtml(value) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


async function logout() {

    try {

        await fetch(
            "/api/auth/logout",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error(
            "Logout error:",
            error
        );
    }


    window.location.href =
        "/index.html";
}