from typing import List, Union
from whatis.models import Whatis
from whatis import constants
from slack.web.classes import blocks, elements, messages, objects


def build_whatis_actions(whatis: Whatis) -> blocks.ActionsBlock:
    # TODO: Add in confirmations
    update_whatis_button = elements.ButtonElement(
        text="Update",
        style="primary",
        action_id=constants.UPDATE_WHATIS_ID,
        value=str(whatis.id),
    )
    rollback_whatis_button = elements.ButtonElement(
        text="Rollback", action_id=constants.ROLLBACK_WHATIS_ID, value=str(whatis.id)
    )
    delete_whatis_button = elements.ButtonElement(
        text="Delete",
        style="danger",
        action_id=constants.DELETE_WHATIS_ID,
        value=whatis.whatis_id,
    )

    return blocks.ActionsBlock(
        elements=[update_whatis_button, rollback_whatis_button, delete_whatis_button]
    )


def build_whatis_component(
    whatis: Whatis
) -> List[Union[blocks.DividerBlock, blocks.SectionBlock, blocks.ActionsBlock]]:

    whatis_fields = []
    for field in ["terminology", "definition", "notes", "links", "point_of_contact"]:
        # My god I want walrus operators already
        value = getattr(whatis, field)
        if value is not None:
            if field == "links":
                value = "-" + "\n- ".join(value.split(","))
            elif field == "point_of_contact":
                value = f"<@{value}>"
            whatis_fields.append(f"*{field.capitalize().replace('_',' ')}*\n{value}\n")
    return [
        blocks.SectionBlock(fields=whatis_fields),
        # Add whatis action buttons
        build_whatis_actions(whatis),
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


def build_whatis_footer(query: str) -> blocks.ActionsBlock:
    add_new_button = elements.ButtonElement(
        text="Add a new Whatis!",
        style="primary",
        action_id=constants.CREATE_NEW_WHATIS_ID,
        value=constants.CREATE_NEW_WHATIS_ID,
    )
    return blocks.ActionsBlock(elements=[add_new_button])


def build_whatis_message(
    original_query: str, whatises: List[Whatis]
) -> messages.Message:
    block_list = []
    if whatises:
        block_list.append(
            blocks.SectionBlock(
                text=f"*The following result(s) best matched the original_query:* "
                f"{original_query}"
            )
        )
        for wi in whatises:
            block_list.extend(build_whatis_component(wi))
    else:
        block_list.append(
            blocks.SectionBlock(
                text=f"*No Whatis was found matching the query {original_query}* :shrug:"
                f"\nMaybe it's your time to shine by creating a Whatis of your own!"
            )
        )

    block_list.append(build_whatis_footer(original_query))
    return messages.Message(blocks=block_list, text="Whatis results!")
