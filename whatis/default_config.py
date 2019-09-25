import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class DefaultWhatisConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_USER_IDS = None
    ADMIN_CHANNEL_IDS = None
    SLACK_TOKEN = os.getenv("SLACK_TOKEN")
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
