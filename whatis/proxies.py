from flask import current_app
from slack.web.client import WebClient
from sqlalchemy.orm.session import Session
from werkzeug.local import LocalProxy

__all__ = ["db_session", "slack_client"]

db_session: Session = LocalProxy(lambda: current_app.db.session)
slack_client: WebClient = LocalProxy(lambda: current_app.sc)
