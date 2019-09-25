import os
import uuid
import logging

from slack.web.client import WebClient
from flask import Flask
from flask_migrate import Migrate
from .models import db as sqlalchemy_db
from alembic import command
from alembic.migration import MigrationContext

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class WhatisApp(Flask):
    def __init__(self, db_uri=None, debug=None, config=None, **kwargs):
        Flask.__init__(self, __name__)

        # Preload default configuration
        self.config.from_object(config)
        self.config.from_mapping(kwargs)

        # Set the secret key for this instance (creating one if one does not exist already)
        self.config["SECRET_KEY"] = self.config["SECRET_KEY"] or str(uuid.uuid4())

        # Configure database
        if db_uri:
            self.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        logger.debug(
            "Using database: {}".format(self.config["SQLALCHEMY_DATABASE_URI"])
        )

        # DB dialect logic - used for lookup operations
        db_dialect = self.config["SQLALCHEMY_DATABASE_URI"].split(":")[0]
        logger.info(f"Attempting to use db dialect {db_dialect}")
        if not any([i == db_dialect for i in ["postgres", "sqlite"]]):
            raise RuntimeError(
                f"Dialect {db_dialect} not supported - please use sqlite or postgres"
            )
        self.config["DB_DIALECT"] = db_dialect

        # Register database schema with flask app
        sqlalchemy_db.init_app(self)

        # Set up database migration information
        # Registers Migrate plugin in self.extensions['migrate']
        Migrate(self, self.db)

        # Try to create the database if it does not already exist
        # Existence is determined by whether there is an existing alembic migration revision
        db_auto_create = self.config.get("DB_AUTO_CREATE", True)
        db_auto_upgrade = self.config.get("DB_AUTO_UPGRADE", True)
        if db_auto_create and self.db_revision is None:
            self.db_init()
        elif db_auto_upgrade:
            self.db_upgrade()

        self.logger.setLevel(logging.DEBUG)

        # Install postgres fuzzystrmatch extension
        if db_dialect == "postgres":
            self.logger.info("Enabling Postgres fuzzy string matching")
            with self.app_context(), self.db.engine.connect() as conn:
                conn.execute("CREATE EXTENSION IF NOT EXISTS  fuzzystrmatch")

        # Register Slack client on the current application instance
        self.sc = WebClient(self.config.get("SLACK_TOKEN"), ssl=False)

        from routes.slack_route import slack_blueprint

        self.register_blueprint(slack_blueprint, url_prefix="/slack")

        # Register a basic route for healthchecking
        @self.route("/ping")
        def healthcheck():
            return "pong"

    @property
    def db(self):
        return sqlalchemy_db

    @property
    def _alembic_config(self):
        if not hasattr(self, "extensions") or "migrate" not in self.extensions:
            raise RuntimeError(
                "KnowledgeApp has not yet been configured. Please instantiate it via `get_app_for_repo`."
            )
        migrations_path = os.path.join(os.path.dirname(__file__), "migrations")
        return self.extensions["migrate"].migrate.get_config(migrations_path)

    def db_init(self):
        with self.app_context():
            # Create all tables
            sqlalchemy_db.create_all()

            # Stamp table as being current
            command.stamp(self._alembic_config, "head")
        return self

    @property
    def db_revision(self):
        with self.app_context():
            conn = self.db.engine.connect()

            context = MigrationContext.configure(conn)
            return context.get_current_revision()

    def db_upgrade(self):
        with self.app_context():
            command.upgrade(self._alembic_config, "head")
        return self

    def db_downgrade(self, revision):
        with self.app_context():
            command.downgrade(self._alembic_config, revision)
        return self

    def db_migrate(self, message, autogenerate=True):
        with self.app_context():
            command.revision(
                self._alembic_config, message=message, autogenerate=autogenerate
            )
        return self
