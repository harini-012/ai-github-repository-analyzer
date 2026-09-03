from flask import Blueprint, request, jsonify, session

from services.github_service import analyze_github_repository

from models.repository_model import (
    save_repository,
    get_user_repositories,
    get_repository,
    delete_repository
)


repository_bp = Blueprint(
    "repository",
    __name__,
    url_prefix="/api/repositories"
)


@repository_bp.route("/analyze", methods=["POST"])
def analyze():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    data = request.get_json()

    github_url = data.get("github_url")

    if not github_url:
        return jsonify({
            "error": "GitHub URL is required"
        }), 400

    try:

        repository = analyze_github_repository(
            github_url
        )

        repository_id = save_repository(

            session["user_id"],

            github_url,

            repository["name"],

            repository["description"],

            repository["language"],

            repository["stars"],

            repository["forks"],

            repository["files"]
        )

        return jsonify({

            "repository_id": repository_id,

            "repository": repository

        })

    except Exception as error:

        print(
            "Repository analysis error:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


@repository_bp.route("", methods=["GET"])
def repositories():

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    repositories = get_user_repositories(
        session["user_id"]
    )

    return jsonify(repositories)


@repository_bp.route(
    "/<int:repository_id>",
    methods=["GET"]
)
def repository(repository_id):

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

    return jsonify(repository)


@repository_bp.route(
    "/<int:repository_id>",
    methods=["DELETE"]
)
def delete(repository_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Please login first"
        }), 401

    delete_repository(
        repository_id,
        session["user_id"]
    )

    return jsonify({
        "message": "Repository deleted"
    })