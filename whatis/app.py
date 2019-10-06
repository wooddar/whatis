import json
import logging
import os
import uuid
from hashlib import sha224
from pathlib import Path

from alembic import command
from alembic.migration import MigrationContext
from cachetools import cached, TTLCache
from flask import Flask
from flask_migrate import Migrate
from slack.errors import SlackApiError
from slack.web.client import WebClient

from .constants import WHATIS_FIELDS
from .models import db as sqlalchemy_db, WhatisPreloader, Whatis

logging.basicConfig(level=logging.DEBUG)


class WhatisApp(Flask):
    def __init__(self, db_uri=None, config=None, preload_path=None, **kwargs):
        Flask.__init__(self, __name__)

        # Preload default configuration
        self.config.from_object(config)
        self.config.from_mapping(kwargs)

        # Set the secret key for this instance (creating one if one does not exist already)
        self.config["SECRET_KEY"] = self.config["SECRET_KEY"] or str(uuid.uuid4())

        # Configure database
        if db_uri:
            self.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        if self.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:":
            self.logger.warning(
                "Using Sqlite in-memory database, all data will be lost when server shuts down!"
            )

        # DB dialect logic - used for lookup operations
        db_dialect = self.config["SQLALCHEMY_DATABASE_URI"].split(":")[0]
        self.logger.info(f"Attempting to use db dialect {db_dialect}")
        if self.config.get("DEBUG") is not True:
            self.logger.warning(
                "It is strongly recommended that you do not use Sqlite for production deployments!"
            )
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

        # Handle preloading an existing Terminology set
        self.handle_whatis_preload(preload_path)

        # Register Slack client on the current application instance
        if all(
            [
                self.config.get(i) is None
                for i in ["SLACK_SIGNING_SECRET", "SLACK_TOKEN"]
            ]
        ):
            raise RuntimeError(
                "Whatis must have both a slack signing secret and slack bot token set"
            )
        self.sc = WebClient(self.config.get("SLACK_TOKEN"), ssl=False)

        from whatis.routes.slack_route import slack_blueprint

        self.register_blueprint(slack_blueprint, url_prefix="/slack")

        if not all(
            [
                type(self.config[i]) == list
                for i in ["ADMIN_USER_IDS", "ADMIN_CHANNEL_IDS"]
            ]
        ):
            raise RuntimeError(
                "ADMIN_USER_IDS and ADMIN_CHANNEL_IDS must be lists of Admin user IDs or channel IDs"
            )

        try:
            au = self.admin_users
            self.logger.info(f"Initial Admin users set as {au}")
        except SlackApiError as s:
            raise RuntimeError(
                f"Failed to get Admin users from specified Admin channels - are you sure the whatis bot "
                f"is invited and has the necessary scopes {s}"
            )

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
        # This is terrible but seems to be needed for packaging
        migrations_path = (
            migrations_path
            if Path(migrations_path).exists() is True
            else os.path.join(os.path.dirname(__file__), "whatis/migrations")
        )
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

    @cached(TTLCache(ttl=3600, maxsize=2048))
    def _get_admin_users(self):
        channel_admin_members = []
        for channel in self.config["ADMIN_CHANNEL_IDS"]:
            try:
                channel_admin_members.extend(
                    self.sc.conversations_members(channel=channel)["members"]
                )
            except SlackApiError as s:
                self.logger.warning(
                    f"Could not get members from the specified Admin channel {channel} has the whatis "
                    f"bot been removed or scopes been changed? {s}"
                )
        return self.config["ADMIN_USER_IDS"] + channel_admin_members

    @property
    def admin_users(self):
        """
        Get all users approved as admins
        """
        return self._get_admin_users()

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

    def handle_whatis_preload(self, preload_path):
        with self.app_context():
            if preload_path is not None:
                filepath = Path(preload_path)
                if filepath.exists():
                    file_contents = open(filepath).read()
                    file_hash = sha224(file_contents.encode()).hexdigest()
                    existing_preload = (
                        self.db.session.query(WhatisPreloader)
                        .filter(WhatisPreloader.hash == file_hash)
                        .first()
                    )
                    if existing_preload is not None:
                        self.logger.info(
                            f"Existing whatis load found for the file {existing_preload}, skipping"
                        )
                    else:
                        raw = json.loads(file_contents)
                        self.logger.info(
                            f"Attempting to preload terminology from the file {filepath}, {len(raw)} records found"
                        )
                        for raw_whatis in raw:
                            if all(
                                [i in raw_whatis for i in ["terminology", "definition"]]
                            ) is False or not set(raw_whatis).issubset(
                                set(WHATIS_FIELDS)
                            ):
                                raise RuntimeError(
                                    f"Attempt to preload Terminology failed, Whatis {raw_whatis} has an unrecognised attribute or does not contain both of [terminology, definiton]"
                                )
                            wi = Whatis(
                                **{"version": 0, "added_by": "WHATIS BOT", **raw_whatis}
                            )
                            self.db.session.add(wi)
                            self.logger.debug(f"Added the Whatis {wi}")
                        # Now register the fact that we have loaded this file so it is ignored for future deployments
                        self.db.session.add(
                            WhatisPreloader(hash=file_hash, filename=str(filepath))
                        )
                        self.db.session.commit()

                else:
                    raise FileNotFoundError(
                        f"Preload filepath specified {preload_path} but no file found"
                    )
