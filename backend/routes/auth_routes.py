from flask import Blueprint, request, jsonify, session

from models.user_model import (
    create_user,
    get_user_by_email,
    verify_password
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "error": "All fields are required"
        }), 400

    existing_user = get_user_by_email(email)

    if existing_user:
        return jsonify({
            "error": "Email already registered"
        }), 409

    user_id = create_user(
        name,
        email,
        password
    )

    session["user_id"] = user_id
    session["user_name"] = name

    return jsonify({
        "message": "Registration successful"
    })


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = get_user_by_email(email)

    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    if not verify_password(
        password,
        user["password"]
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    return jsonify({
        "message": "Login successful"
    })


@auth_bp.route("/logout", methods=["POST"])
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out successfully"
    })


@auth_bp.route("/user", methods=["GET"])
def current_user():

    if "user_id" not in session:
        return jsonify({
            "logged_in": False
        })

    return jsonify({
        "logged_in": True,
        "id": session["user_id"],
        "name": session["user_name"]
    })