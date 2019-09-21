import os
from slack.web.client import WebClient
from flask import request
from functools import partial
from slack.web.classes.blocks import SectionBlock, DividerBlock, ActionsBlock
from slack.web.classes.elements import ButtonElement


WebClient.validate_slack_signature()

def verify_slack_request(request) -> bool:
    ...

