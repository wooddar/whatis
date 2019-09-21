import logging
from slack.web.client import WebClient
from slack.web.classes.interactions import SlashCommandInteractiveEvent
from flask import request, Blueprint, current_app
from utils.interaction_handler import SlackInteractionHandler
from whatis.proxies import db_session
from whatis.models import Whatis

logger = logging.getLogger(__name__)
slack_blueprint = Blueprint(__name__, "slack")

slinteract = SlackInteractionHandler()

sm = WebClient(current_app.config.get('SLACK_TOKEN'))

@slack_blueprint.route("/whatis", methods=["POST"])
def get_whatis():
    sc = SlashCommandInteractiveEvent(request.form.to_dict())

    terminology = sc.text
    if len(terminology) > 5:
        wi = db_session.query(Whatis).filter(Whatis.terminology.ilike(f'%{terminology}%')).all()
    else:
        wi = db_session.query(Whatis).filter(Whatis.terminology.ilike(f'{terminology}')).first()
    if wi is not None:
        return wi.definition
    else:
        return f"Nothing to see here for the query {terminology}"


@slack_blueprint.route("/actions")
def handle_action():

    # Handle message button actions


    # Handle dialog actions
    slinteract.handle_action()
    return "", 204


def send_create_form():
    pass


def send_update_form():
    pass


def create_whatis(terminology,whatis_id, definition, notes, links, version, owner, point_of_contact
):
    whatis = Whatis(
        terminology=terminology,
        definition=definition,
        whatis_id=whatis_id,
        notes=notes,
        version=version,
        links=links,
        owner=owner,
        point_of_contact=point_of_contact,
    )
    db_session.add(whatis)
    db_session.commit()


def update_whatis(id, definition, notes, links, owner, point_of_contact
):
    wi = db_session.query(Whatis).filter(Whatis.id == id).first()
    if wi is None:
        return "Tried to find a whatis that didn't exist"

    create_whatis(terminology=wi.terminology,
                  whatis_id=wi.whatis_id,
                  definition=definition,
                  notes=notes,
                  links=links,
                  version=wi.version+1,
                  owner= owner,
                  point_of_contact=point_of_contact)


def add_whatis_rule():
    pass


def delete_whatis():
    pass

def rollback_whatis():
    pass

