from flask import current_app
from slack.web.classes.interactions import MessageInteractiveEvent

from whatis import constants
from whatis.routes.actions import (
    send_create_form,
    send_update_form,
    send_to_channel,
    delete_whatis,
    rollback_whatis,
    send_all_tsv,
)
from whatis.utils.interaction_handler import SlackInteractionHandler
from whatis.utils.responder import webhook_response, basic_responder_response

block_interactor = SlackInteractionHandler()


def handle_block_actions(data: dict):
    data["message"] = {"ts": data["container"]["message_ts"]}
    ah = MessageInteractiveEvent(data)
    result = block_interactor.interact(ah.action_id, action=ah)
    wr = None
    if result is not None:
        wr = webhook_response(ah.response_url, result)
    current_app.logger.info(
        f"Block action interaction for {ah.action_id} returning {result} - {wr}"
    )
    return "", 204


@block_interactor.interaction(constants.CREATE_NEW_WHATIS_ID)
def create_whatis_action(action: MessageInteractiveEvent):
    send_create_form(action.trigger_id)
    return


@block_interactor.interaction(constants.UPDATE_WHATIS_ID)
def update_whatis_action(action: MessageInteractiveEvent):
    send_update_form(action.trigger_id, action.value)
    return


@block_interactor.interaction(constants.WHATIS_SEND_CHANNEL_ID)
def send_to_channel_whatis_action(action: MessageInteractiveEvent):
    send_to_channel(action.channel.id, action.value, action.user.id)
    return


@block_interactor.interaction(constants.ROLLBACK_WHATIS_ID)
def rollback_whatis_action(action: MessageInteractiveEvent):
    rollback_whatis(action.value)
    return basic_responder_response(
        "Whatis successfully rolled back :rolled_up_newspaper:"
    ).to_dict()


@block_interactor.interaction(constants.DELETE_WHATIS_ID)
def delete_whatis_action(action: MessageInteractiveEvent):
    delete_whatis(action.value)
    return basic_responder_response("Whatis successfully deleted :skull:").to_dict()


@block_interactor.interaction(constants.WHATIS_ALL_ID)
def all_whatis_action(action: MessageInteractiveEvent):
    return send_all_tsv(action.user.id)
