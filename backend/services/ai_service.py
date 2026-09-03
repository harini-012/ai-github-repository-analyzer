from groq import Groq
from config import Config


client = Groq(
    api_key=Config.GROQ_API_KEY
)


def generate_ai_analysis(repository):

    # --------------------------------------------------
    # Repository files
    # --------------------------------------------------

    files = repository.get("files") or []

    if not isinstance(files, list):
        files = [str(files)]

    file_structure = "\n".join(
        str(file)
        for file in files
    )

    # --------------------------------------------------
    # Source code
    # --------------------------------------------------

    source_files = repository.get("source_files") or []

    source_code = ""

    for file in source_files:

        path = file.get("path", "")
        content = file.get("content", "")

        source_code += f"""
==============================
FILE: {path}
==============================

{content}

"""

    # Keep prompt reasonably sized
    source_code = source_code[:60000]

    # --------------------------------------------------
    # AI prompt
    # --------------------------------------------------

    prompt = f"""
You are an expert software developer performing
a GitHub repository analysis.

Analyze ONLY the repository information and source
code provided below.

Do not browse the web.
Do not use tools.
Do not call functions.
Do not invent information.

If information cannot be determined from the
provided repository, clearly say so.

Keep the analysis beginner-friendly.

================================
REPOSITORY INFORMATION
================================

Repository Name:
{repository.get("name")}

Description:
{repository.get("description") or "No description available."}

Main Language:
{repository.get("language") or "Not specified"}

Stars:
{repository.get("stars", 0)}

Forks:
{repository.get("forks", 0)}

================================
PROJECT FILE STRUCTURE
================================

{file_structure}

================================
SOURCE CODE
================================

{source_code}

================================
ANALYSIS
================================

Analyze the repository using the following five
categories:

PROJECT SUMMARY
Explain what the project does.

TECHNOLOGIES
Identify programming languages, frameworks,
libraries, packages and technologies that have
evidence in the repository.

PROJECT ARCHITECTURE
Explain how the project is organized and how
the major components work together.

IMPORTANT FILES
Identify important files and explain their purpose
based on their actual contents.

GENERAL INSIGHTS

Provide useful general observations about the project
based only on the repository information and source code.

Discuss things such as:

- Overall strengths of the project
- Interesting or notable implementation choices
- The project's complexity and scope
- How the different components work together
- Good development practices that are visible
- Areas that could be improved
- Potential technical challenges
- Maintainability, scalability, security, or performance
  considerations when relevant
- Any other useful observations that help someone
  understand the project better

Do not make hiring or recruiter-related judgments.
Do not assign scores or ratings.
Do not invent information.
Only make observations supported by the repository.

Only make claims supported by the provided
repository information and source code.
"""

    # --------------------------------------------------
    # Groq request
    # --------------------------------------------------

    response = client.chat.completions.create(

        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        tool_choice="none",

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "github_repository_analysis",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "summary": {
                            "type": "string"
                        },
                        "technologies": {
                            "type": "string"
                        },
                        "architecture": {
                            "type": "string"
                        },
                        "important_files": {
                            "type": "string"
                        },
                        "general_insights": {
                            "type": "string"
                        }
                    },
                    "required": [
                        "summary",
                        "technologies",
                        "architecture",
                        "important_files",
                        "general_insights"
                    ],
                    "additionalProperties": False
                }
            }
        },

        temperature=0.2
    )

    return response.choices[0].message.content