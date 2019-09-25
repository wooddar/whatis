import os
from dotenv import find_dotenv, load_dotenv
from whatis.default_config import DefaultWhatisConfig

load_dotenv(find_dotenv())


class DevelopmentConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres@localhost:5432/whatis"
    ADMIN_USER_IDS = []
    ADMIN_CHANNEL_IDS = ["GNR4H7JG4"]


class DockerDevelopmentConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@postgres:5432/whatis"
    ADMIN_USER_IDS = ["U9KR5QZA5"]
    ADMIN_CHANNEL_IDS = ["C9Z2KJEVB"]


class StagingConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


9
