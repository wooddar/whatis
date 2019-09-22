from flask import current_app
from werkzeug.local import LocalProxy
from sqlalchemy.orm.session import Session
from slack.web.client import WebClient

__all__ = ["db_session", "slack_client"]

db_session: Session = LocalProxy(lambda: current_app.db.session)
slack_client: WebClient = LocalProxy(lambda: current_app.sc)
