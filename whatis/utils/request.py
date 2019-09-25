import os
import logging
from typing import List
from slack.web.client import WebClient
from flask import request, abort, current_app
from functools import partial

import constants

logger = logging.getLogger(__name__)

runtime_context = os.getenv("RUNTIME_CONTEXT")
if runtime_context is None or runtime_context not in constants.RUNTIME_CONTEXTS:
    raise RuntimeError(
        "Cannot validate signatures without a valid RUNTIME_CONTEXT environment variable set. Must be "
        f"in {constants.RUNTIME_CONTEXTS}"
    )


def get_env_secrets() -> List[str]:
    return [v for k, v in os.environ.items() if k.startswith("SLACK_SIGNING_SECRET")]


validators = [
    partial(WebClient.validate_slack_signature, signing_secret=i)
    for i in get_env_secrets()
]


def verify_slack_request() -> None:
    """
    This verification function is designed to be placed in a flask before_request handler
    """
    request_data = request.get_data()
    current_app.logger.info(request.headers)
    current_app.logger.info(request_data)
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    slack_sig = request.headers.get("X-Slack-Signature", "")
    request_verified = False
    verify_message = ""

    if any([timestamp == "", slack_sig == ""]):
        if runtime_context not in constants.LOCAL_RUNTIME_CONTEXTS:
            verify_message = "Incorrect verification headers"
        else:
            current_app.logger.info(
                "Slack request missing timestamp or signature headers"
            )
    else:
        request_verified = any(
            [
                v(timestamp=timestamp, signature=slack_sig, data=request_data)
                for v in validators
            ]
        )

    if request_verified is False:
        if runtime_context not in constants.LOCAL_RUNTIME_CONTEXTS:
            verify_message = "Request signature verification failed"
            abort(403, verify_message)
        else:
            current_app.logger.info(
                f"Request verification: {request_verified}, msg: {verify_message}"
            )
