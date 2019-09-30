import os
from flask.cli import FlaskGroup
from whatis.config import DevelopmentConfig, DockerDevelopmentConfig, ProductionConfig
from whatis.app import WhatisApp
from whatis.models import Whatis
from functools import partial

runtime_context = os.getenv("RUNTIME_CONTEXT") or 'local'
config = {
    "local": DevelopmentConfig,
    "docker-local": DockerDevelopmentConfig,
    "production": ProductionConfig,
}[runtime_context]

app = WhatisApp(config=config, DB_AUTO_CREATE=False, DB_AUTO_UPGRADE=False)
cli = FlaskGroup(create_app=partial(WhatisApp, config=config))


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
        Whatis(
            terminology="whatis_a",
            definition="The definition of whatis A",
            notes="Some more notes about Whatis A",
            links="www.google.com",
            version=1,
            added_by=USER_ID,
            point_of_contact="U9KR5QZA5",
        ),
        Whatis(
            terminology="whatis_b",
            definition="The definition of whatis B",
            notes="Some more notes about Whatis B",
            links="www.facebook.com",
            version=1,
            added_by=USER_ID,
            point_of_contact="U9KR5QZA5",
        ),
    ]
    for m in models:
        app.db.session.add(m)
    app.db.session.commit()


if __name__ == "__main__":
    cli()
