import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class BaseWhatisConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_IDS = None
    ADMIN_CHANNEL = None
    SLACK_TOKEN = os.getenv("SLACK_TOKEN")


class DevelopmentConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class DockerDevelopmentConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@postgres:5432/whatis"


class StagingConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
