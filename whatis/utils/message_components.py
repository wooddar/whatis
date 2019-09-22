from typing import List, Union
from whatis.models import Whatis
from slack.web.classes import blocks, elements, messages, objects


def build_whatis_component(
    whatis: Whatis
) -> List[Union[blocks.DividerBlock, blocks.SectionBlock, blocks.ActionsBlock]]:
    return [
        blocks.DividerBlock(),
        blocks.SectionBlock(
            fields=[
                whatis.terminology,
                whatis.definition,
                whatis.notes,
                whatis.links,
                whatis.point_of_contact,
            ]
        ),
        blocks.ContextBlock(
            elements=[
                objects.MarkdownTextObject(text=whatis.submitted_at),
                objects.MarkdownTextObject(text=whatis.version),
            ]
        ),
        blocks.DividerBlock(),
    ]


def build_whatis_footer(query: str) -> blocks.ActionsBlock:
    add_new_button = elements.ButtonElement()
    return blocks.ActionsBlock()


def build_whatis_message(original_query: str, whatises: List[Whatis]) -> messages.Message:
    blocks = []
    for wi in whatises:
        blocks.append(build_whatis_component(wi))
    blocks.append(build_whatis_footer(original_query))

    return messages.Message(
        text=f"*The following result(s) best matched the original_query: {original_query}",
        blocks=blocks,
    )
