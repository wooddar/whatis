from flask import current_app
from sqlalchemy import desc

from whatis.models import Whatis
from whatis.proxies import db_session, slack_client
from whatis.utils import dialog_components


def send_create_form(trigger_id):
    slack_client.dialog_open(
        trigger_id=trigger_id,
        dialog=dialog_components.build_create_new_dialog().to_dict(),
    )
    return "", 204


def send_update_form(trigger_id, whatis_id: int):
    slack_client.dialog_open(
        # TODO: this needs to be whatis numerical ID
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
    wi = db_session.query(Whatis).filter(Whatis.id == id).first()

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


def send_all_rule():
    # TODO: Rule to send all terminology to a user as a CSV
    ...
