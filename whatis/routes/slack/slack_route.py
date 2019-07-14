import logging
from flask import request, Blueprint
from whatis.utils.slack.interaction_handler import SlackInteractionHandler
from whatis.proxies import db_session
from whatis.models import Whatis

logger = logging.getLogger(__name__)
slack_blueprint = Blueprint(__name__, 'slack')

slinteract = SlackInteractionHandler()


@slack_blueprint.route('/whatis', methods=['POST'])
def get_whatis():
    pass



@slack_blueprint.route('/actions')
def handle_action():
    slinteract.handle_action()
    return '', 204


def send_create_form():
    pass


def send_update_form():
    pass


def create_whatis(team_id, terminology, definition, notes, links, version, owner, point_of_contact):
    whatis = Whatis(
        team_id=team_id,
        terminology=terminology,
        definition=definition,
        notes=notes,
        version=version,
        links=links,
        owner=owner,
        point_of_contact=point_of_contact
    )
    db_session.add(whatis)
    db_session.commit()

def add_whatis_rule():
    pass


def delete_whatis():
    pass


def update_whatis():
    pass
