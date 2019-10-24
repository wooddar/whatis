"""
Defines the different methods that build the Whatis component visible in Slack
"""
from typing import List, Union

from slack.web.classes import blocks, elements, messages, objects

from whatis import constants
from whatis.models import Whatis


def build_whatis_action_confirm(title: str, text: str) -> objects.ConfirmObject:
    return objects.ConfirmObject(
        title=title, text=text, confirm="`Accept`", deny="Cancel"
    )


def build_whatis_actions(whatis: Whatis, is_admin: bool = False) -> blocks.ActionsBlock:
    """
    Adds the message button components to The Whatis message
    Args:
        whatis: A whatis model object
        is_admin: Is the user this component is being built for a workspace whatis admin

    Returns:

    """
    update_whatis_button = elements.ButtonElement(
        text="Update",
        style="primary",
        action_id=constants.UPDATE_WHATIS_ID,
        value=str(whatis.id),
        confirm=build_whatis_action_confirm(
            "Update Whatis",
            'Are you sure you want to update this Whatis? If you do, you will be listed under "Added by" and the '
            "previous updater will be notified!",
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
    channel_whatis_button = elements.ButtonElement(
        text="Send to Channel",
        action_id=constants.WHATIS_SEND_CHANNEL_ID,
        value=str(whatis.id),
        confirm=build_whatis_action_confirm(
            "Send Whatis to channel?",
            "This Action will post this Whatis as visible to everyone in the current channel!",
        ),
    )
    actions = [update_whatis_button, channel_whatis_button]
    if is_admin is True:
        actions.extend([rollback_whatis_button, delete_whatis_button])
    return blocks.ActionsBlock(elements=actions)


def build_whatis_component(
    whatis: Whatis, is_admin: bool = False, include_buttons: bool = True
) -> List[Union[blocks.DividerBlock, blocks.SectionBlock, blocks.ActionsBlock]]:
    """
    Build the component that will actually hold the whatis including actions relating to it

    Args:
        whatis: A whatis model object
        is_admin: Is the user this component is being built for a workspace whatis admin
        include_buttons: Should action buttons be included - used for channel messages

    Returns: The component for each Whatis

    """
    whatis_fields = []
    for field in constants.WHATIS_FIELDS:
        # My god I want walrus operators already
        value = getattr(whatis, field)
        if value is not None:
            if field == "links":
                value = "- " + "\n- ".join(value.split(","))
            elif field in ["added_by", "point_of_contact"]:
                mention_char = "@" if value.startswith("U") else "#"
                value = f"<{mention_char}{value}>"
            whatis_fields.append(f"*{field.capitalize().replace('_',' ')}*\n{value}\n")
    component_blocks = [blocks.SectionBlock(fields=whatis_fields)]

    # Add whatis action buttons
    if include_buttons is True:
        component_blocks.append(build_whatis_actions(whatis, is_admin))

    # Add the rest of the block content
    component_blocks.extend(
        [
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
    )
    return component_blocks


def build_whatis_footer(is_admin: bool = False) -> blocks.ActionsBlock:
    """
    Builds the footer to attach to all whatis requests

    Args:
        is_admin: Is the user this component is being built for a workspace whatis admin

    Returns:

    """
    add_new_button = elements.ButtonElement(
        text="Add a new Whatis!",
        style="primary",
        action_id=constants.CREATE_NEW_WHATIS_ID,
        value=constants.CREATE_NEW_WHATIS_ID,
    )
    send_all_button = elements.ButtonElement(
        text="See all Whatises",
        action_id=constants.WHATIS_ALL_ID,
        value=constants.WHATIS_ALL_ID,
        confirm=build_whatis_action_confirm(
            "Get all Whatises?",
            "This action will cause me to send you a TSV of all "
            "your organisation's terminology, this may cause "
            "things to break or take some time.",
        ),
    )
    return blocks.ActionsBlock(elements=[add_new_button, send_all_button])


def build_whatis_message(
    original_query: str, whatises: List[Whatis], is_admin: bool = False
) -> messages.Message:
    block_list = []
    if whatises:
        block_list.extend(
            [
                blocks.SectionBlock(
                    text=f"*{'I found some terminology' if len(whatises) > 1 else 'I found a whatis'} matching :* {original_query} :muscle:"
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


def build_channel_whatis(triggering_user: str, whatis: Whatis) -> messages.Message:
    """
    Builds a single whatis message to send to channel

    Args:
        triggering_user: The Slack ID of the user who triggered the send to channel action
        whatis: A whatis model object

    Returns: An in-channel whatis message

    """
    channel_blocks = build_whatis_component(whatis, include_buttons=False)
    channel_blocks.insert(
        0,
        blocks.SectionBlock(
            text=f"The user <@{triggering_user}> wants everyone to know about this whatis:"
        ),
    )
    message = messages.Message(text="Whatis channel message", blocks=channel_blocks)
    return message
