from flask import current_app
from slack.web.classes.interactions import MessageInteractiveEvent

from whatis.utils.interaction_handler import SlackInteractionHandler
from whatis.utils.dialog_components import LINKS_KEY, NOTES_KEY, TERMINOLOGY_KEY, DEFINITION_KEY
from whatis.routes.actions import create_whatis, update_whatis, send_create_form, send_update_form, delete_whatis, rollback_whatis
from whatis import constants


block_interactor = SlackInteractionHandler()


def handle_block_actions(data: dict):
    ah = MessageInteractiveEvent(data)

    return block_interactor.interact(ah.block_id, action=ah)



@block_interactor.interaction(constants.CREATE_NEW_WHATIS_ID)
def create_whatis_action(action: MessageInteractiveEvent):
    send_create_form(action.trigger_id)
    return '', 204


@block_interactor.interaction(constants.UPDATE_WHATIS_ID)
def update_whatis_action(action: MessageInteractiveEvent):
    send_update_form(action.trigger_id, action.value)
    return '', 204


@block_interactor.interaction(constants.ROLLBACK_WHATIS_ID)
def rollback_whatis_action(action: MessageInteractiveEvent):
    rollback_whatis(action.value)
    return '', 204


@block_interactor.interaction(constants.DELETE_WHATIS_ID)
def delete_whatis_action(action: MessageInteractiveEvent):
    delete_whatis(action.value)
    return '', 204