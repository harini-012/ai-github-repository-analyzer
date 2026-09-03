from flask import Flask, send_from_directory
from config import Config

from routes.auth_routes import auth_bp
from routes.repository_routes import repository_bp
from routes.ai_routes import ai_bp

import os


app = Flask(
    __name__,
    static_folder="../frontend",
    static_url_path=""
)

app.config.from_object(Config)

app.secret_key = Config.SECRET_KEY

app.register_blueprint(auth_bp)
app.register_blueprint(repository_bp)
app.register_blueprint(ai_bp)


@app.route("/")
def home():

    return send_from_directory(
        "../frontend",
        "index.html"
    )


@app.route("/<path:path>")
def frontend(path):

    file_path = os.path.join(
        "../frontend",
        path
    )

    if os.path.isfile(file_path):

        return send_from_directory(
            "../frontend",
            path
        )

    return send_from_directory(
        "../frontend",
        "index.html"
    )

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )