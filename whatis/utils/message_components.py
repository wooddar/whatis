from typing import List, Union
from whatis.models import Whatis
from whatis import constants
from slack.web.classes import blocks, elements, messages, objects


def build_whatis_action_confirm(title: str, text: str) -> objects.ConfirmObject:
    return objects.ConfirmObject(
        title=title, text=text, confirm="Proceed", deny="Run Away!"
    )


def build_whatis_actions(whatis: Whatis, is_admin: bool = False) -> blocks.ActionsBlock:
    update_whatis_button = elements.ButtonElement(
        text="Update",
        style="primary",
        action_id=constants.UPDATE_WHATIS_ID,
        value=str(whatis.id),
        confirm=build_whatis_action_confirm(
            "Update Whatis",
            'Are you sure you want to update this Whatis? If you do, you will be listed under "Added by"',
        ),
    )
    rollback_whatis_button = elements.ButtonElement(
        text="Rollback",
        action_id=constants.ROLLBACK_WHATIS_ID,
        value=str(whatis.id),
        confirm=build_whatis_action_confirm(
            "Rollback Whatis",
            "Are you sure you would like to rollback this Whatis to its last version?",
        ),
    )
    delete_whatis_button = elements.ButtonElement(
        text="Delete",
        style="danger",
        action_id=constants.DELETE_WHATIS_ID,
        value=whatis.whatis_id,
        confirm=build_whatis_action_confirm(
            "Delete Whatis",
            "This will permanently delete this Whatis along with its whole version history, "
            "are you sure you want to do this?",
        ),
    )
    actions = [update_whatis_button]
    if is_admin is True:
        actions.extend([rollback_whatis_button, delete_whatis_button])
    return blocks.ActionsBlock(elements=actions)


def build_whatis_component(
    whatis: Whatis, is_admin: bool = False
) -> List[Union[blocks.DividerBlock, blocks.SectionBlock, blocks.ActionsBlock]]:
    """
    Build the component that will actually hold the whatis including actions relating to it
    :param whatis:
    :param is_admin:
    :return:
    """

    whatis_fields = []
    for field in [
        "terminology",
        "definition",
        "notes",
        "links",
        "point_of_contact",
        "added_by",
    ]:
        # My god I want walrus operators already
        value = getattr(whatis, field)
        if value is not None:
            if field == "links":
                value = "- " + "\n- ".join(value.split(","))
            elif field in ["added_by", "point_of_contact"]:
                mention_char = "@" if value.startswith("U") else "#"
                value = f"<{mention_char}{value}>"
            whatis_fields.append(f"*{field.capitalize().replace('_',' ')}*\n{value}\n")
    return [
        blocks.SectionBlock(fields=whatis_fields),
        # Add whatis action buttons
        build_whatis_actions(whatis, is_admin),
        # Add whatis contextual information
        blocks.ContextBlock(
            elements=[
                objects.MarkdownTextObject(
                    text=f"Last updated: {whatis.submitted_at.strftime('%Y-%m-%d')}"
                ),
                objects.MarkdownTextObject(text=f"{str(whatis.version)} revisions"),
            ]
        ),
        blocks.DividerBlock(),
    ]


def build_whatis_footer(is_admin: bool = False) -> blocks.ActionsBlock:
    # TODO: View all button
    add_new_button = elements.ButtonElement(
        text="Add a new Whatis!",
        style="primary",
        action_id=constants.CREATE_NEW_WHATIS_ID,
        value=constants.CREATE_NEW_WHATIS_ID,
    )
    return blocks.ActionsBlock(elements=[add_new_button])


def build_whatis_message(
    original_query: str, whatises: List[Whatis], is_admin: bool = False
) -> messages.Message:
    block_list = []
    if whatises:
        block_list.extend(
            [
                blocks.SectionBlock(
                    text=f"*The following result(s) best matched :* {original_query}"
                ),
                blocks.DividerBlock(),
            ]
        )
        for wi in whatises:
            block_list.extend(build_whatis_component(wi, is_admin=is_admin))
    else:
        block_list.append(
            blocks.SectionBlock(
                text=f"*No Whatis was found matching the query {original_query}* :shrug:"
                f"\nMaybe it's your time to shine by creating a Whatis of your own!"
            )
        )

    block_list.append(build_whatis_footer(is_admin=is_admin))
    return messages.Message(blocks=block_list, text="Whatis results!")
