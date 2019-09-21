from whatis.app import create_app
from flask_testing import TestCase
from whatis.models import db, Team
from routes.slack_route import create_whatis


class TestDbModels(TestCase):
    SQLALCHEMY_DATABASE_URI = "postgresql:///hugodarwood"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def test_add_whatis(self):
        team = Team(team_name="Deliveroo", team_id=2)
        self.db.session.add(team)
        self.db.session.commit()
        create_whatis(2, "eod", "end of day", "", ["www.google.com"], 0, "UX8HGM", "")

    def setUp(self):
        self.db = self.app.db
        self.db.Model.metadata = db.metadata
        self.db.create_all()

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
