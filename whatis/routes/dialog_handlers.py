from flask import current_app
from slack.web.classes.interactions import DialogInteractiveEvent

from whatis import constants
from whatis.routes.actions import create_whatis, update_whatis
from whatis.utils.dialog_components import (
    LINKS_KEY,
    NOTES_KEY,
    TERMINOLOGY_KEY,
    DEFINITION_KEY,
    POINT_OF_CONTACT_KEY,
)
from whatis.utils.interaction_handler import SlackInteractionHandler
from whatis.utils.responder import webhook_response, basic_responder_response

dialog_interactor = SlackInteractionHandler()


def handle_dialog_submission(data: dict):
    ds = DialogInteractiveEvent(data)
    result = dialog_interactor.interact(ds.callback_id, data=ds)
    wr = webhook_response(ds.response_url, result)
    current_app.logger.info(
        f"Dialog sumbit interaction for {ds.callback_id} returning {result} - {wr}"
    )
    return "", 204


@dialog_interactor.interaction(constants.CREATE_NEW_WHATIS_ID_SUBMIT)
def create_dialog_sumbit_action(data: DialogInteractiveEvent):
    submission = data.submission
    whatis = create_whatis(
        terminology=submission.get(TERMINOLOGY_KEY),
        definition=submission.get(DEFINITION_KEY),
        notes=submission.get(NOTES_KEY),
        links=submission.get(LINKS_KEY),
        version=1,
        added_by=data.user.id,
        point_of_contact=submission.get(POINT_OF_CONTACT_KEY),
    )
    return basic_responder_response(
        f"Successfully created the Whatis {whatis.terminology} :tada:"
    ).to_dict()


@dialog_interactor.interaction(constants.UPDATE_WHATIS_ID_SUBMIT)
def update_dialog_sumbit_action(data: DialogInteractiveEvent):
    submission = data.submission
    id = data.state["id"]
    whatis = update_whatis(
        id=int(id),
        definition=submission.get(DEFINITION_KEY),
        notes=submission.get(NOTES_KEY),
        links=submission.get(LINKS_KEY),
        added_by=data.user.id,
        point_of_contact=submission.get(POINT_OF_CONTACT_KEY),
    )
    return basic_responder_response(
        f"Successfully updated the Whatis {whatis.terminology} :tada:"
    ).to_dict()
