import os
import typing
from dotenv import find_dotenv, load_dotenv
from whatis.default_config import DefaultWhatisConfig
load_dotenv(find_dotenv())


class DevelopmentConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres@localhost:5432/whatis"
    ADMIN_USER_IDS: typing.List[str] = []
    ADMIN_CHANNEL_IDS: typing.List[str] = ["GNR4H7JG4"]


class DockerDevelopmentConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@postgres:5432/postgres"
    ADMIN_USER_IDS: typing.List[str] = ["U9KR5QZA5"]
    ADMIN_CHANNEL_IDS: typing.List[str] = ["C9Z2KJEVB"]


class StagingConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]


class ProductionConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]

