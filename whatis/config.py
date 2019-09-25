import os
from dotenv import find_dotenv, load_dotenv
from whatis.default_config import DefaultWhatisConfig

load_dotenv(find_dotenv())


class DevelopmentConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres@localhost:5432/whatis"


class DockerDevelopmentConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@postgres:5432/whatis"


class StagingConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
