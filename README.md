# AI-Powered GitHub Repository Analyzer

An AI-powered full-stack web application that analyzes GitHub repositories and generates structured technical insights using Generative AI.

The application retrieves repository metadata, explores its file structure, fetches selected source-code files, and uses a Large Language Model (LLM) to explain the project's functionality, technologies, architecture, important files, and general insights.

## Project Overview

Understanding an unfamiliar GitHub repository can be time-consuming, especially when it contains multiple files, frameworks, and components.

The AI GitHub Repository Analyzer simplifies this process by automating repository exploration and generating beginner-friendly explanations using Generative AI.

## Features

- **User Authentication:** Registration, login, and session-based authentication.
- **GitHub Integration:** Retrieve repository metadata and file structures using the GitHub REST API.
- **Source Code Analysis:** Fetch and process selected source-code files.
- **AI-Powered Analysis:** Use Groq LLM to generate technical insights.
- **Project Summary:** Understand the purpose and functionality of a repository.
- **Technology Identification:** Identify programming languages, frameworks, libraries, and tools based on available repository evidence.
- **Architecture Explanation:** Understand the organization and interaction of project components.
- **Important File Identification:** Discover important files and their purposes.
- **General Insights:** Generate observations about project strengths, maintainability, performance, and possible improvements.
- **Database Persistence:** Store repository information and AI-generated analysis in PostgreSQL.

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Backend | Python, Flask |
| Database | PostgreSQL |
| AI / LLM | Groq API, `openai/gpt-oss-20b` |
| External API | GitHub REST API |
| Authentication | Flask Sessions |
| Deployment | Render |

## System Architecture

```text
              USER
                |
                v
       FRONTEND APPLICATION
       HTML, CSS, Bootstrap, JS
                |
                v
          FLASK BACKEND
                |
       +--------+---------+
       |        |         |
       v        v         v
  PostgreSQL  GitHub    Groq API
  Database    REST API   LLM
       |        |         |
       |        v         |
       |   Repository     |
       |   Metadata &     |
       |   Source Code    |
       |        |         |
       |        v         |
       |   Source Code    |
       |   Processing     |
       |        |         |
       |        v         |
       |   AI Analysis    |
       |        |         |
       |        v         |
       |   Structured     |
       |   JSON Response  |
       |        |         |
       +--------+---------+
                |
                v
       DISPLAY AI INSIGHTS
          TO THE USER
```

## How It Works

1. **Repository Input:** The user enters a GitHub repository URL.
2. **Repository Metadata Retrieval:** The Flask backend communicates with the GitHub REST API to retrieve repository details such as name, description, language, stars, forks, and default branch.
3. **File Structure Retrieval:** The application retrieves the repository's file tree using the GitHub Git Trees API.
4. **Source Code Collection:** Relevant text and source-code files are selected, and their contents are retrieved.
5. **AI Processing:** The collected repository information and source code are passed to the Groq LLM with a structured prompt.
6. **Structured Response:** The LLM generates a JSON response containing five analysis categories.
7. **Database Storage:** The backend validates the response and stores the generated analysis in PostgreSQL.
8. **Frontend Display:** JavaScript retrieves the analysis and displays the results in the web interface.

## AI Analysis Categories

The application generates insights in five categories:

| Category | Description |
|---|---|
| Project Summary | Explains the purpose and functionality of the repository. |
| Technologies | Identifies technologies supported by repository evidence. |
| Project Architecture | Explains the organization of the project and its components. |
| Important Files | Identifies important files and describes their roles. |
| General Insights | Provides observations, strengths, challenges, and potential improvements. |

## Database Design

The application uses PostgreSQL with three main tables.

**1. Users**
- Stores user registration and authentication information.
- Uses a unique user ID as the primary key.

**2. Repositories**
- Stores repository URLs, metadata, and file structures.
- Uses `user_id` as a foreign key referencing the Users table.

**3. Analyses**
- Stores AI-generated summaries, technologies, architecture explanations, important files, and general insights.
- Uses `repository_id` as a foreign key referencing the Repositories table.

### Database Relationships

```text
USERS
  |
  | One-to-Many
  |
REPOSITORIES
  |
  | One-to-Many
  |
ANALYSES
```

## Project Structure

```text
ai-github-repository-analyzer/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── repository_model.py
│   │   └── analysis_model.py
│   │
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── repository_routes.py
│   │   └── ai_routes.py
│   │
│   ├── services/
│   │   ├── github_service.py
│   │   └── ai_service.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── repository.html
│   │
│   ├── css/
│   │   ├── style.css
│   │   ├── auth.css
│   │   └── dashboard.css
│   │
│   └── js/
│       ├── login.js
│       ├── register.js
│       ├── dashboard.js
│       └── repository.js
│
├── database/
│   └── schema.sql
│
├── .gitignore
└── README.md
```

## Installation and Local Setup

### Prerequisites

- Python 3.10 or a compatible version
- PostgreSQL
- Git
- GitHub Personal Access Token
- Groq API Key

### 1. Clone the Repository

```bash
git clone https://github.com/harini-012/ai-github-repository-analyzer.git
```

```bash
cd ai-github-repository-analyzer
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install Flask Flask-Cors psycopg2-binary python-dotenv requests groq gunicorn
```

Install any additional packages listed in `backend/requirements.txt` if required.

### 4. Create the PostgreSQL Database

Create a database named:

```sql
CREATE DATABASE github_analyzer;
```

The application initializes the required database tables when Flask starts.

### 5. Configure Environment Variables

Create a `.env` file inside the `backend` directory.

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=github_analyzer
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password

GITHUB_TOKEN=your_github_token
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_secret_key
```

Replace the placeholder values with your actual credentials.

**Important:** Never commit your `.env` file or expose your API keys publicly.

### 6. Run the Application

Navigate to the backend directory:

```bash
cd backend
```

Start the Flask application:

```bash
python app.py
```

### 7. Open the Application

Visit:

```text
http://127.0.0.1:5000
```

Register an account, log in, and submit a GitHub repository URL to generate an AI-powered analysis.

## Limitations

- Large repositories may exceed the LLM's input-token limits.
- The application analyzes selected source files rather than every file in a repository.
- AI-generated insights depend on the quality and completeness of the provided source code.
- GitHub API rate limits may affect repository retrieval.
- Private repository access requires a GitHub token with appropriate permissions.
- The current implementation depends on external GitHub and Groq API availability.

## Future Improvements

- Implement intelligent source-code selection and token-aware processing.
- Introduce code chunking and multi-stage summarization for large repositories.
- Add caching to reduce repeated GitHub API requests.
- Integrate GitHub OAuth or GitHub Apps for individual users' private repositories.
- Improve automated testing and error handling.
- Add analysis quality evaluation and more detailed technical insights.
- Improve scalability and performance for larger repositories.

## Learning Outcomes

Through this project, I gained practical experience in:

- Building a full-stack application using Python and Flask.
- Integrating external REST APIs.
- Working with Generative AI and Large Language Models.
- Designing structured prompts and JSON-based AI responses.
- Processing repository source code.
- Designing relational databases using PostgreSQL.
- Implementing authentication and session management.
- Handling API errors and LLM input-token constraints.
- Deploying a full-stack application using Render.

## Author

**Harini**



---

**Built with Python, Flask, PostgreSQL, GitHub REST API, and Generative AI.**
