import logging
from flask import request, Blueprint
from whatis.utils.slack.interaction_handler import SlackInteractionHandler
from whatis.proxies import db_session

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

def add_whatis():
    pass


def delete_whatis():
    pass


def update_whatis():
    pass
