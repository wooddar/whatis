from flask import current_app
from slack.web.classes.interactions import DialogInteractiveEvent

from whatis.utils.interaction_handler import SlackInteractionHandler
from whatis.utils.dialog_components import LINKS_KEY, NOTES_KEY, TERMINOLOGY_KEY, DEFINITION_KEY
from whatis.routes.actions import create_whatis, update_whatis
from whatis import constants

dialog_interactor = SlackInteractionHandler()


def handle_dialog_submission(data: dict):
    ds = DialogInteractiveEvent(data)
    return dialog_interactor.interact(ds.callback_id, data=ds)


@dialog_interactor.interaction(constants.CREATE_NEW_WHATIS_ID_SUBMIT)
def create_dialog_sumbit_action(data: DialogInteractiveEvent):
    submission = data.submission
    whatis=create_whatis(
        terminology=submission.get(TERMINOLOGY_KEY),
        definition=submission.get(DEFINITION_KEY),
        notes=submission.get(NOTES_KEY),
        links=submission.get(LINKS_KEY),
        version=1,
        owner=data.user,
        point_of_contact=data.user,
    )
    return f"Successfully created the Whatis {whatis.terminology} :party:"


@dialog_interactor.interaction(constants.UPDATE_WHATIS_ID_SUBMIT)
def update_dialog_sumbit_action(data: DialogInteractiveEvent):
    submission = data.submission
    id = data.state['id']
    whatis = update_whatis(
        id=id,
        definition=submission.get(DEFINITION_KEY),
        notes=submission.get(NOTES_KEY),
        links=submission.get(LINKS_KEY),
        owner=data.user,
        point_of_contact=data.user,
    )
    return f"Successfully updated the Whatis {whatis.terminology} :party:"
