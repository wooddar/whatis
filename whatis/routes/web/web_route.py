from flask import Blueprint

web_blueprint = Blueprint(__name__, "web")


@web_blueprint.route("/ping", methods=["GET"])
def health_check():
    return "pong"
