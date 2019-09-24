from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import partial
from secrets import token_urlsafe

db = SQLAlchemy()

# whatis_id generator
widgen = partial(token_urlsafe, 5)


class Whatis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    whatis_id = db.Column(db.String, nullable=False, default=widgen)
    terminology = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True)
    links = db.Column(db.String, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.String, nullable=False)
    point_of_contact = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Whatis {self.terminology} - {self.id}>"
