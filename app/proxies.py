from flask import current_app
from werkzeug.local import LocalProxy

__all__ = ['db_session']

db_session = LocalProxy(lambda: current_app.db.session)
