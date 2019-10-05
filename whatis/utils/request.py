import logging

from flask import request, abort, current_app
from slack.web.client import WebClient

logger = logging.getLogger(__name__)


def verify_slack_request() -> None:
    """
    This verification function is designed to be placed in a flask before_request handler
    """
    request_data = request.get_data().decode()
    current_app.logger.debug(request.headers)
    current_app.logger.debug(request_data)
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    slack_sig = request.headers.get("X-Slack-Signature", "")
    request_verified = False
    verify_message = ""

    if any([timestamp == "", slack_sig == ""]):
        verify_message += "Slack request missing timestamp or signature headers"
    else:
        request_verified = WebClient.validate_slack_signature(
            signing_secret=current_app.config["SLACK_SIGNING_SECRET"],
            timestamp=timestamp,
            signature=slack_sig,
            data=request_data,
        )

    if request_verified is False:
        if current_app.config["DEBUG"] is True:
            current_app.logger.info(
                f"Request verification: {request_verified}, msg: {verify_message}"
            )
        else:
            verify_message = "Request signature verification failed"
            abort(403, verify_message)
