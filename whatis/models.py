from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# TODO: Ensure length rules for all IDs in models

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String)
    team_id = db.Column(db.String, unique=True, nullable=False)
    whatises = db.relationship('Whatis', backref='team', lazy=True)
    teamadmins = db.relationship('TeamAdmin', backref='team', lazy=True)

    def __repr__(self):
        return f"<Team {self.team_id}>"


class Whatis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String, db.ForeignKey('team.team_id'), nullable=False,)
    terminology = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    notes = db.Column(db.String, nullable=True)
    links = db.Column(db.ARRAY(db.String), nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    version = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.String, nullable=False)
    point_of_contact = db.Column(db.String, nullable=True)


    def __repr__(self):
        return f"<Whatis {self.id} for {self.team_id}>"

class TeamAdmin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.String, db.ForeignKey('team.team_id'), nullable=False)
    admin_id = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<TeamAdmin {self.id} for {self.team_id}>"