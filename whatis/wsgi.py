import os
import logging

from whatis.app import WhatisApp
from whatis.config import DevelopmentConfig, DockerDevelopmentConfig, ProductionConfig

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

runtime_context = os.getenv("RUNTIME_CONTEXT")
config = {
    "local": DevelopmentConfig,
    "docker-local": DockerDevelopmentConfig,
    "production": ProductionConfig,
}.get(runtime_context)

app = WhatisApp(config=config)
