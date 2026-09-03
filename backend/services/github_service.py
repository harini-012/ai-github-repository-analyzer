import requests
import base64
from urllib.parse import urlparse

from config import Config


# File extensions that are useful for AI analysis
TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".html",
    ".css",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".php",
    ".rb",
    ".rs",
    ".swift",
    ".kt",
    ".kts",
    ".sql",
    ".json",
    ".xml",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".sh",
    ".bat",
    ".dockerfile"
}


# Files that usually contain useful project information
IMPORTANT_FILE_NAMES = {
    "requirements.txt",
    "package.json",
    "README.md",
    "runtime.txt",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".env.example"
}


def is_text_file(path):
    """
    Check whether a GitHub file is suitable for AI analysis.
    """

    path_lower = path.lower()

    # Special files
    file_name = path.split("/")[-1]

    if file_name in IMPORTANT_FILE_NAMES:
        return True

    # Extension-based check
    for extension in TEXT_EXTENSIONS:
        if path_lower.endswith(extension):
            return True

    return False


def get_file_content(owner, repo, path, headers):
    """
    Read a file from GitHub.

    This uses GET only.
    It does NOT modify the GitHub repository.
    """

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents/{path}"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("type") != "file":
        return None

    content = data.get("content")

    if not content:
        return None

    try:
        decoded = base64.b64decode(content).decode(
            "utf-8",
            errors="ignore"
        )

        return decoded

    except Exception:
        return None


def analyze_github_repository(github_url):

    parsed = urlparse(github_url)

    if parsed.netloc.lower() not in [
        "github.com",
        "www.github.com"
    ]:
        raise ValueError(
            "Please enter a valid GitHub repository URL"
        )

    parts = parsed.path.strip("/").split("/")

    if len(parts) < 2:
        raise ValueError(
            "Invalid GitHub repository URL"
        )

    owner = parts[0]
    repo = parts[1]

    if repo.endswith(".git"):
        repo = repo[:-4]

    headers = {
        "Accept": "application/vnd.github+json"
    }

    if Config.GITHUB_TOKEN:
        headers["Authorization"] = (
            f"Bearer {Config.GITHUB_TOKEN}"
        )

    # --------------------------------------------------
    # 1. Get repository information
    # --------------------------------------------------

    repository_api = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}"
    )

    response = requests.get(
        repository_api,
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:
        raise ValueError(
            "GitHub repository not found or inaccessible"
        )

    data = response.json()

    branch = data["default_branch"]

    # --------------------------------------------------
    # 2. Get repository file tree
    # --------------------------------------------------

    tree_api = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/"
        f"{branch}?recursive=1"
    )

    tree_response = requests.get(
        tree_api,
        headers=headers,
        timeout=20
    )

    if tree_response.status_code != 200:
        raise ValueError(
            "Unable to retrieve repository files"
        )

    tree_data = tree_response.json()

    files = []

    for item in tree_data.get("tree", []):

        if item.get("type") == "blob":
            files.append(item["path"])

    # --------------------------------------------------
    # 3. Retrieve useful source files
    # --------------------------------------------------

    source_files = []

    # Limit the number of files sent to GitHub/Groq
    # to keep the analysis manageable.
    candidate_files = [
        file for file in files
        if is_text_file(file)
    ]

    candidate_files = candidate_files[:20]

    for file_path in candidate_files:

        content = get_file_content(
            owner,
            repo,
            file_path,
            headers
        )

        if content is None:
            continue

        # Prevent very large files from consuming
        # the AI context.
        content = content[:12000]

        source_files.append({
            "path": file_path,
            "content": content
        })

    # --------------------------------------------------
    # 4. Return repository information
    # --------------------------------------------------

    return {
        "name": data["name"],
        "description": data["description"],
        "language": data["language"],
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "files": files[:100],
        "source_files": source_files
    }