import typing
from slack.web.classes import dialog_elements, dialogs

from whatis import constants
from whatis.models import Whatis
from whatis.routes.actions import get_whatis

TERMINOLOGY_KEY = "terminology"
DEFINITION_KEY = "definition"
NOTES_KEY = "notes"
LINKS_KEY = "links"


def build_create_new_dialog(state: typing.Union[dict, str] = ""):
    d = (
        dialogs.DialogBuilder()
        .submit_label("Add")
        .notify_on_cancel(False)
        .callback_id(constants.CREATE_NEW_WHATIS_ID)
        .title("Create a new Whatis")
        .state(state)
        .text_field(
            name="Terminology",
            label=TERMINOLOGY_KEY,
            optional=False,
            hint="what are you defining",
            min_length=2,
        )
        .text_field(
            name="Definition",
            label=DEFINITION_KEY,
            optional=False,
            hint="What does it mean",
            min_length=8,
        )
        .text_area(
            name="Notes",
            label=NOTES_KEY,
            optional=True,
            hint="Other notes",
            min_length=8,
        )
        .text_area(
            name="Relevant Links",
            label=LINKS_KEY,
            optional=True,
            hint="Comma separated links to documentation",
            min_length=8,
        )
    )
    return d


def build_update_dialog(id, state: typing.Union[dict, str] = ""):
    whatis = get_whatis(id)
    d = (
        dialogs.DialogBuilder()
        .submit_label("Add")
        .notify_on_cancel(False)
        .callback_id(constants.UPDATE_WHATIS_ID)
        .title("Update Whatis")
        .state(state)
        .text_field(
            name="Terminology",
            label=TERMINOLOGY_KEY,
            optional=False,
            hint="what are you defining",
            min_length=2,
            value=whatis.terminology,
        )
        .text_field(
            name="Definition",
            label=DEFINITION_KEY,
            optional=False,
            hint="What does it mean",
            min_length=8,
            value=whatis.definition,
        )
        .text_area(
            name="Notes",
            label=NOTES_KEY,
            optional=True,
            hint="Other notes",
            min_length=8,
            value=whatis.notes,
        )
        .text_area(
            name="Relevant Links",
            label=LINKS_KEY,
            optional=True,
            hint="Comma separated links to documentation",
            min_length=8,
            value=whatis.links,
        )
    )
    return d
