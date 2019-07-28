import os


class BaseWhatisConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres@localhost:5432/whatis"


class DockerDevelopmentConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@postgres:5432/whatis"


class ProductionConfig(BaseWhatisConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
