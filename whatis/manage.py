import os
from flask.cli import FlaskGroup
from config import DevelopmentConfig, DockerDevelopmentConfig, ProductionConfig
from app import create_app
from models import Whatis, Team, TeamAdmin
from functools import partial

runtime_context = os.getenv("RUNTIME_CONTEXT")
config = {
    "local": DevelopmentConfig,
    "docker-local": DockerDevelopmentConfig,
    "production": ProductionConfig,
}[runtime_context]

app = create_app(config)
cli = FlaskGroup(create_app=partial(create_app, config))


@cli.command("recreate_db")
def recreate_db():
    app.db.drop_all()
    app.db.create_all()
    app.db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    TEAM_ID = "CCX3T"
    USER_ID = "UX8FHM5"
    models = [
        Team(team_name="Wooddarteam", team_id=TEAM_ID),
        TeamAdmin(team_id=TEAM_ID, admin_id=USER_ID),
        Whatis(
            team_id=TEAM_ID,
            terminology="whatis_a",
            definition="The definition of whatis A",
            notes="Some more notes about Whatis A",
            links="www.google.com",
            version=1,
            owner=USER_ID,
        ),
        Whatis(
            team_id=TEAM_ID,
            terminology="whatis_b",
            definition="The definition of whatis B",
            notes="Some more notes about Whatis B",
            links="www.facebook.com",
            version=1,
            owner=USER_ID,
        ),
    ]
    for m in models:
        app.db.session.add(m)
    app.db.session.commit()


if __name__ == "__main__":
    cli()
