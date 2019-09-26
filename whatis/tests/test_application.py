import os
import pytest
from unittest.mock import MagicMock
from json import loads, dumps
from unittest import TestCase
from whatis.app import WhatisApp
from whatis.models import Whatis
from whatis.default_config import DefaultWhatisConfig
from whatis import constants


class TestingConfig(DefaultWhatisConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True


def create_slash_command_input(text, user_id="U9KR5QZA5"):
    return dict(
        text=text,
        response_url="https://slack.webhook.com/TN04R",
        user_id=user_id,
        user_name="Steff Nezos",
        channel_id="C9Z2KJTTB",
        channel_name="cat-factoids",
        trigger_id="1032423.342",
        command="/whatis",
        team_id="C4RRSV",
        team_domain="parragon",
    )


def create_block_action(action_id, block_id, action_value, user_id="U9KR5QZA5"):
    return dict(payload=dumps(dict(
        user=dict(id="U9KR5QZA5", username="some dude"),
        response_url="https://slack.webhook.com/TN04R",
        channel=dict(id="CX6TY", name="some channel"),
        trigger_id="1032423.342",
        command="/whatis",
        team=dict(id="C4RRSV", domain="team mcteam"),
        type="block_actions",
        container=dict(message_ts='2242234.234'),
        actions=[dict(action_id=action_id, block_id=block_id, value=action_value)],
    )))


def create_dialog_submit_action(text, user_id="U9KR5QZA5"):
    return dict(
        text=text,
        response_url="https://slack.webhook.com/TN04R",
        user_id=user_id,
        user_name="Steff Nezos",
        channel_id="C9Z2KJTTB",
        channel_name="cat-factoids",
        trigger_id="1032423.342",
        command="/whatis",
        team_id="C4RRSV",
        team_domain="parragon",
    )


@pytest.fixture
def client():
    os.environ["RUNTIME_CONTEXT"] = "local"
    client = WhatisApp(config=TestingConfig)
    client.sc = MagicMock()
    with client.app_context():
        client.db.session.add(
            Whatis(
                terminology="eod",
                definition="End of Day",
                notes="Used when you dont have time to say end of day",
                links="google,facebook",
                point_of_contact="C9Z2KJEVB",
                version=0,
                added_by="U9KR5QZA5",
            )
        )
        client.db.session.add(
            Whatis(
                terminology="Lost customer",
                definition="When a customer does not make any repeat transactions for > 20 days",
                notes="Decided on by Data science team",
                links=None,
                point_of_contact=None,
                version=0,
                added_by="U9KR5QZB4",
            )
        )
        client.db.session.add(
            Whatis(
                terminology="Lost customer",
                definition="When a customer does not make any repeat transactions for > 20 days",
                notes="Decided on by Data science team and CIO",
                links="jira",
                point_of_contact=None,
                version=1,
                added_by="U9KR5QZA5",
            )
        )
        client.db.session.commit()
    return client.test_client()


def test_client_dialect(client):
    assert client.application.config["DB_DIALECT"] == "sqlite"


def test_get_whatis(client):
    resp = client.post("/slack/whatis", query_string=create_slash_command_input(text="eod"))
    assert len(loads(resp.data)["blocks"]) == 7


def test_action_handlers(client):
    resp = client.post(
        "/slack/actions",
        data=create_block_action(
            action_id=constants.CREATE_NEW_WHATIS_ID,
            block_id="blocky",
            action_value=constants.CREATE_NEW_WHATIS_ID,
        ),
    )
    assert resp.data.decode() == ''
