from flask import Blueprint, jsonify, session
import json

from services.ai_service import generate_ai_analysis
from services.github_service import analyze_github_repository

from models.repository_model import get_repository
from models.analysis_model import save_analysis, get_analysis


ai_bp = Blueprint(
    "ai",
    __name__,
    url_prefix="/api/ai"
)


# ==========================================================
# GENERATE AI ANALYSIS
# ==========================================================

@ai_bp.route("/analyze/<int:repository_id>", methods=["POST"])
def analyze(repository_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    repository = get_repository(
        repository_id,
        session["user_id"]
    )

    if not repository:
        return jsonify({
            "error": "Repository not found"
        }), 404

    try:

        # Get latest GitHub information
        github_repository = analyze_github_repository(
            repository["github_url"]
        )

        # Add source code information
        repository["source_files"] = (
            github_repository.get("source_files", [])
        )

        # Generate AI response
        result = generate_ai_analysis(repository)

        print("\n")
        print("================================================")
        print("                 AI RESPONSE")
        print("================================================")
        print(result)
        print("================================================")
        print("\n")

        # Convert JSON string to Python dictionary
        try:

            sections = json.loads(result)

        except json.JSONDecodeError as error:

            print("JSON parsing error:")
            print(error)

            return jsonify({
                "error": "AI returned invalid JSON",
                "details": str(error),
                "raw_response": result
            }), 500

        print("\n")
        print("================================================")
        print("              PARSED AI RESULT")
        print("================================================")
        print(sections)
        print("================================================")
        print("\n")

        # --------------------------------------------------
        # Required AI fields
        # --------------------------------------------------

        required_fields = [
            "summary",
            "technologies",
            "architecture",
            "important_files",
            "general_insights"
        ]

        # --------------------------------------------------
        # Validate AI response
        # --------------------------------------------------

        for field in required_fields:

            if field not in sections:

                print(
                    f"AI response missing field: {field}"
                )

                return jsonify({
                    "error": (
                        f"AI response is missing field: {field}"
                    ),
                    "ai_response": sections
                }), 500

            if sections[field] is None:

                sections[field] = ""

            sections[field] = str(
                sections[field]
            ).strip()

            if not sections[field]:

                print(
                    f"AI returned empty value for: {field}"
                )

                return jsonify({
                    "error": (
                        f"AI returned an empty value for: {field}"
                    ),
                    "ai_response": sections
                }), 500

        # --------------------------------------------------
        # Save to Oracle
        #
        # IMPORTANT:
        # Oracle column is still called SUGGESTIONS.
        # We store GENERAL INSIGHTS inside that column.
        # --------------------------------------------------

        analysis_id = save_analysis(
            repository_id,
            sections["summary"],
            sections["technologies"],
            sections["architecture"],
            sections["important_files"],
            sections["general_insights"]
        )

        print("\n")
        print("================================================")
        print("       AI ANALYSIS SAVED SUCCESSFULLY")
        print("================================================")
        print("Analysis ID:", analysis_id)
        print("Repository ID:", repository_id)
        print("================================================")
        print("\n")

        # --------------------------------------------------
        # Return to frontend
        # --------------------------------------------------

        return jsonify({

            "analysis_id": analysis_id,

            "repository_id": repository_id,

            "summary": sections["summary"],

            "technologies": sections["technologies"],

            "architecture": sections["architecture"],

            "important_files": sections["important_files"],

            "general_insights": sections["general_insights"]

        }), 200

    except Exception as error:

        print("\n")
        print("================================================")
        print("             AI ANALYSIS ERROR")
        print("================================================")
        print(error)
        print("================================================")
        print("\n")

        return jsonify({
            "error": str(error)
        }), 500


# ==========================================================
# GET SAVED AI ANALYSIS
# ==========================================================

@ai_bp.route("/<int:repository_id>", methods=["GET"])
def get_saved_analysis(repository_id):

    if "user_id" not in session:

        return jsonify({
            "error": "Please login first"
        }), 401

    try:

        repository = get_repository(
            repository_id,
            session["user_id"]
        )

        if not repository:

            return jsonify({
                "error": "Repository not found"
            }), 404

        analysis = get_analysis(repository_id)

        if not analysis:

            return jsonify({}), 200

        # --------------------------------------------------
        # Database column is SUGGESTIONS.
        # Frontend will see it as GENERAL_INSIGHTS.
        # --------------------------------------------------

        return jsonify({

            "id": analysis["id"],

            "repository_id": analysis["repository_id"],

            "summary": analysis["summary"],

            "technologies": analysis["technologies"],

            "architecture": analysis["architecture"],

            "important_files": analysis["important_files"],

            "general_insights": analysis["suggestions"],

            "created_at": analysis["created_at"]

        }), 200

    except Exception as error:

        print("\n")
        print("================================================")
        print("          GET AI ANALYSIS ERROR")
        print("================================================")
        print(error)
        print("================================================")
        print("\n")

        return jsonify({
            "error": str(error)
        }), 500