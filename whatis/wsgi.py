import os
from dotenv import load_dotenv, find_dotenv

from whatis.app import WhatisApp
from whatis.config import DevelopmentConfig, DockerDevelopmentConfig, ProductionConfig


load_dotenv(find_dotenv())

runtime_context = os.getenv("RUNTIME_CONTEXT")
config = {
    "local": DevelopmentConfig,
    "docker-local": DockerDevelopmentConfig,
    "production": ProductionConfig,
}.get(runtime_context)

app = WhatisApp(config=config)


if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")
