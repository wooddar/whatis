import os
import logging

from app import create_app
from config import DevelopmentConfig, DockerDevelopmentConfig, ProductionConfig

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

runtime_context = os.getenv("RUNTIME_CONTEXT")
config = {
    "local": DevelopmentConfig,
    "docker-local": DockerDevelopmentConfig,
    "production": ProductionConfig,
}.get(runtime_context)

app = create_app(config)
