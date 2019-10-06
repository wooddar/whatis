import logging
import os
import typing

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
logger = logging.getLogger(__name__)


class WhatisConfig:

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    ADMIN_USER_IDS: typing.List[str] = []
    ADMIN_CHANNEL_IDS: typing.List[str] = []
    SLACK_TOKEN: typing.Optional[str] = os.environ.get("SLACK_TOKEN")
    SLACK_SIGNING_SECRET: typing.Optional[str] = os.environ.get("SLACK_SIGNING_SECRET")
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

    @classmethod
    def from_args(cls, args):

        if args.db is not None:
            cls.SQLALCHEMY_DATABASE_URI = args.db

        if args.debug is not None:
            cls.DEBUG = args.debug

        if args.admin_user_ids is not None:
            cls.ADMIN_USER_IDS = args.admin_user_ids.split(",")

        if args.admin_channel_ids is not None:
            cls.ADMIN_CHANNEL_IDS = args.admin_channel_ids.split(",")

        if args.slack_token is not None:
            cls.SLACK_TOKEN = args.slack_token

        if args.slack_signing_secret is not None:
            cls.SLACK_SIGNING_SECRET = args.slack_signing_secret

        return cls()
