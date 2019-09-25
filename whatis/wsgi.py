import os
from dotenv import load_dotenv, find_dotenv

from whatis.app import WhatisApp
from whatis.config import DevelopmentConfig, DockerDevelopmentConfig, ProductionConfig, StagingConfig
from whatis.constants import RUNTIME_CONTEXTS

load_dotenv(find_dotenv())

runtime_context = os.getenv("RUNTIME_CONTEXT")

if runtime_context is None:
    raise RuntimeError("RUNTIME_CONTEXT environment variable cannot be None")
elif runtime_context not in RUNTIME_CONTEXTS:
    raise RuntimeError(f"RUNTIME_CONTEXT environment variable {runtime_context} must be in {RUNTIME_CONTEXTS}")

config = {
    "local": DevelopmentConfig,
    "docker-local": DockerDevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
}.get(runtime_context)

app = WhatisApp(config=config)


if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")
