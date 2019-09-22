import logging

from sqlalchemy import desc
from flask import request, Blueprint, current_app, abort, jsonify
from slack.web.classes.interactions import SlashCommandInteractiveEvent

from whatis.utils.interaction_handler import SlackInteractionHandler
from whatis.utils.request import verify_slack_request
from whatis.utils.message_components import build_whatis_message
from whatis.proxies import db_session
from whatis.models import Whatis
from whatis.routes.actions import send_create_form
from whatis.routes.block_action_handlers import handle_block_actions
from whatis.routes.dialog_handlers import handle_dialog_submission

slack_blueprint = Blueprint(__name__, "slack")

logger = logging.getLogger(__name__)


@slack_blueprint.before_request
def verify_request():
    verify_slack_request()


@slack_blueprint.route("/whatis", methods=["POST"])
def get_whatis():
    sc = SlashCommandInteractiveEvent(request.form.to_dict())

    terminology = sc.text
    # Shortcut command to create new terminology
    if terminology == "create":
        return send_create_form(sc.trigger_id)

    if len(terminology) > 5:
        wi = (
            db_session.query(Whatis)
            .filter(Whatis.terminology.ilike(f"%{terminology}%"))
            .all()
        )
    else:
        wi = (
            db_session.query(Whatis)
            .filter(Whatis.terminology.ilike(f"{terminology}"))
            .first()
        )
    if wi is not None:
        return jsonify(build_whatis_message(terminology, wi).to_dict())
    else:
        return f"Nothing to see here for the query {terminology}"


@slack_blueprint.route("/actions", methods=["POST"])
def handle_action():
    request_data = request.form.to_dict()
    current_app.logger.info(request_data)

    action_type = request_data.get("type")

    if action_type == "dialog_submission":
        return handle_dialog_submission(request_data)
    elif action_type == "block_actions":
        return handle_block_actions(request_data)
    else:
        abort(400, f"Unknown action type {action_type}")
    return "", 204
