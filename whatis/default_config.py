import os
import typing
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class DefaultWhatisConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    ADMIN_USER_IDS: typing.List[str] = []
    ADMIN_CHANNEL_IDS: typing.List[str] = []
    SLACK_TOKEN: str = os.environ["SLACK_TOKEN"]
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
