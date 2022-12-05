import os

from flask import Flask, request
from . import webhook


def create_app(test_config=None):
    """
    To initialize the flask app.

    :param test_config: Config file
    :return: Returns the flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    webhook_obj = webhook.Webhook()

    @app.route("/webhook", methods=["POST"])
    def webhook_endpoint():
        if request.method == "POST":
            webhook_obj.is_command(request.json)
            return f"Webhook: {request.json}"

    from . import db
    db.init_app(app)

    @app.route("/initdb", methods=["GET"])
    def init_db():
        db.init_db()

    return app



