from flask import current_app
from sqlalchemy import desc
from io import StringIO

from whatis.models import Whatis
from whatis.proxies import db_session, slack_client
from whatis.utils import dialog_components, responder
from whatis.utils.message_components import build_channel_whatis
from whatis.utils.lookups import get_all_whatises
from whatis import constants


def send_create_form(trigger_id):
    slack_client.dialog_open(
        trigger_id=trigger_id,
        dialog=dialog_components.build_create_new_dialog().to_dict(),
    )
    return "", 204


def send_update_form(trigger_id, whatis_id: int):
    slack_client.dialog_open(
        trigger_id=trigger_id,
        dialog=dialog_components.build_update_dialog(
            whatis=get_whatis(whatis_id)
        ).to_dict(),
    )
    return "", 204


def create_whatis(
    terminology,
    definition,
    whatis_id=None,
    notes=None,
    links=None,
    version=None,
    added_by=None,
    point_of_contact=None,
) -> Whatis:
    whatis = Whatis(
        terminology=terminology,
        definition=definition,
        whatis_id=whatis_id,
        notes=notes,
        version=version,
        links=links,
        added_by=added_by,
        point_of_contact=point_of_contact,
    )
    db_session.add(whatis)
    db_session.commit()
    current_app.logger.info(f"Created the Whatis: {whatis}")
    return whatis


def update_whatis(id, definition, notes, links, added_by, point_of_contact) -> Whatis:
    wi: Whatis = db_session.query(Whatis).filter(Whatis.id == id).first()
    # Check to see if a different user updated your terminology
    if added_by != wi.added_by:
        slack_client.chat_postMessage(
            channel=wi.added_by,
            text=f"Hey  <@{wi.added_by}>, the user <@{added_by}> has updated your Whatis for *{wi.terminology}*, "
            f"try searching for it again to see what they changed!",
        )
    create_whatis(
        terminology=wi.terminology,
        whatis_id=wi.whatis_id,
        definition=definition,
        notes=notes,
        links=links,
        version=wi.version + 1,
        added_by=added_by,
        point_of_contact=point_of_contact,
    )
    return wi


def delete_whatis(whatis_id):
    wi = db_session.query(Whatis).filter(Whatis.whatis_id == whatis_id).all()
    for w in wi:
        db_session.delete(w)
    db_session.commit()


def rollback_whatis(id):
    wi = (
        db_session.query(Whatis)
        .filter(Whatis.id == id)
        .order_by(desc(Whatis.version))
        .first()
    )
    db_session.delete(wi)
    db_session.commit()


def get_whatis(id: int) -> Whatis:
    wi = db_session.query(Whatis).filter(Whatis.id == id).first()
    return wi


def send_all_tsv(user_id: str):
    all_whatis = get_all_whatises()
    whatis_tsv = "\t".join([i.capitalize() for i in constants.WHATIS_FIELDS])
    for wi in all_whatis:
        whatis_tsv += "\n" + "\t".join(
            getattr(wi, a) or "" for a in constants.WHATIS_FIELDS
        )
    slack_client.files_upload(
        content=whatis_tsv, channels=user_id, filename="all_company_terminology.tsv"
    )
    return "A list of all Whatises for your company is on its way to you :fire_engine:"


def send_to_channel(channel_id: str, id: int, user: str):
    wi = get_whatis(id)
    message = build_channel_whatis(triggering_user=user, whatis=wi)
    slack_client.chat_postMessage(
        channel=channel_id,
        blocks=[i.to_dict() for i in message.blocks],
        text=message.text,
    )
