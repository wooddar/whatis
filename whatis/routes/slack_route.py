import logging
import json

from flask import request, Blueprint, current_app, abort, jsonify
from slack.web.classes.interactions import SlashCommandInteractiveEvent
from sqlalchemy import func

from whatis.utils.request import verify_slack_request
from whatis.utils.message_components import build_whatis_message
from whatis.utils.lookups import lookup_whatis
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
def get_whatis_rule():
    sc = SlashCommandInteractiveEvent(request.form.to_dict())

    terminology = sc.text
    # Shortcut command to create new terminology
    if terminology == "create":
        return send_create_form(sc.trigger_id)

    elif terminology == "":
        return "Oops! you need to give me something to search - try /whatis eod"

    # TODO: only max version for each `whatis_id` to be returned
    # TODO: Different point of contact to owner changes
    wi = lookup_whatis(terminology)
    current_app.logger.info(f"Whatis query result for {terminology}: {wi}")
    message = build_whatis_message(terminology, wi)
    return jsonify(message.to_dict())


@slack_blueprint.route("/actions", methods=["POST"])
def handle_action():
    request_data = request.form.to_dict()
    current_app.logger.info(request_data)

    action_payload = json.loads(request_data.get("payload"))
    action_type = action_payload.get("type")

    if action_type == "dialog_submission":
        return handle_dialog_submission(action_payload)
    elif action_type == "block_actions":
        return handle_block_actions(action_payload)
    else:
        abort(400, f"Unknown action type {action_type}")
    return "", 204
