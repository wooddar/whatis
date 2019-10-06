import typing

from slack.web.classes import dialogs

from whatis import constants
from whatis.models import Whatis

TERMINOLOGY_KEY = "terminology"
DEFINITION_KEY = "definition"
NOTES_KEY = "notes"
LINKS_KEY = "links"
POINT_OF_CONTACT_KEY = "pointofcontact"


def build_create_new_dialog(
    state: typing.Union[dict, str] = ""
) -> dialogs.DialogBuilder:
    d = (
        dialogs.DialogBuilder()
        .submit_label("Add")
        .notify_on_cancel(False)
        .callback_id(constants.CREATE_NEW_WHATIS_ID)
        .title("Create a new Whatis")
        .state(state)
        .text_field(
            label="Terminology",
            name=TERMINOLOGY_KEY,
            optional=False,
            hint="what are you defining",
            min_length=2,
        )
        .text_field(
            label="Definition",
            name=DEFINITION_KEY,
            optional=False,
            hint="What does it mean",
            min_length=8,
        )
        .text_area(
            label="Notes",
            name=NOTES_KEY,
            optional=True,
            hint="Other notes",
            placeholder="Is there anything else you think your teammates should know about this terminology?",
            min_length=8,
        )
        .text_area(
            label="Relevant Links",
            name=LINKS_KEY,
            optional=True,
            hint="Comma separated links to documentation",
            placeholder="Did you know that you can create hyperlinks by <www.thingtolinkto.com | "
            "writing it like this>! Useful for long links",
            min_length=8,
        )
        .conversation_selector(
            label="Point of Contact",
            name=POINT_OF_CONTACT_KEY,
            optional=True,
            placeholder="Where is the best place to ask about this",
        )
    )
    return d


def build_update_dialog(whatis: Whatis) -> dialogs.DialogBuilder:
    d = (
        dialogs.DialogBuilder()
        .submit_label("Add")
        .notify_on_cancel(False)
        .callback_id(constants.UPDATE_WHATIS_ID)
        .title("Update Whatis")
        .state({"id": whatis.id})
        .text_field(
            label="Terminology",
            name=TERMINOLOGY_KEY,
            optional=False,
            hint="what are you defining",
            min_length=2,
            value=whatis.terminology,
        )
        .text_field(
            label="Definition",
            name=DEFINITION_KEY,
            optional=False,
            hint="What does it mean",
            min_length=8,
            value=whatis.definition,
        )
        .text_area(
            label="Notes",
            name=NOTES_KEY,
            optional=True,
            hint="Other notes",
            min_length=8,
            value=whatis.notes,
        )
        .text_area(
            label="Relevant Links",
            name=LINKS_KEY,
            optional=True,
            hint="Comma separated links to documentation",
            min_length=8,
            value=whatis.links,
        )
        .conversation_selector(
            label="Point of Contact",
            name=POINT_OF_CONTACT_KEY,
            optional=True,
            value=whatis.point_of_contact,
            placeholder=whatis.added_by,
        )
    )
    return d
