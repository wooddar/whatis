import os
import pytest
from unittest.mock import MagicMock, patch
from json import loads, dumps
from whatis.app import WhatisApp
from whatis.models import Whatis
import json
from whatis.config import WhatisConfig
from whatis.utils.dialog_components import (
    TERMINOLOGY_KEY,
    DEFINITION_KEY,
    NOTES_KEY,
    LINKS_KEY,
    POINT_OF_CONTACT_KEY,
)

from whatis import constants

TEST_WHATIS = Whatis(
    id=2,
    whatis_id="sfCw",
    terminology="UDF",
    definition="User defined function",
    notes="A common feature to many SQL languages",
    links="google,facebook",
    version=0,
    added_by="UX8HGN",
    point_of_contact="C5TY9IL",
)


class TestingConfig(WhatisConfig):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SLACK_SIGNING_SECRET = 'secrety secret'
    SLACK_TOKEN = 'tokeny token'
    DEBUG = True


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
    return dict(
        payload=dumps(
            dict(
                user=dict(id="U9KR5QZA5", username="some dude"),
                response_url="https://slack.webhook.com/TN04R",
                channel=dict(id="CX6TY", name="some channel"),
                trigger_id="1032423.342",
                command="/whatis",
                team=dict(id="C4RRSV", domain="team mcteam"),
                type="block_actions",
                container=dict(message_ts="2242234.234"),
                actions=[
                    dict(action_id=action_id, block_id=block_id, value=action_value)
                ],
            )
        )
    )


def create_dialog_submit_action(callback_id):
    return dict(
        payload=dumps(
            dict(
                response_url="https://slack.webhook.com/TN04R",
                type="dialog_submission",
                user=dict(id="U9KR5QZA5", name="some dude"),
                channel=dict(id="CX6TY", name="some channel"),
                team=dict(id="C4RRSV", domain="team mcteam"),
                callback_id=callback_id,
                state="",
                submission={
                    POINT_OF_CONTACT_KEY: TEST_WHATIS.added_by,
                    LINKS_KEY: TEST_WHATIS.links,
                    NOTES_KEY: TEST_WHATIS.notes,
                    TERMINOLOGY_KEY: TEST_WHATIS.terminology,
                    DEFINITION_KEY: TEST_WHATIS.definition,
                },
            )
        )
    )


@pytest.fixture
def client():
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
                whatis_id="wE5Bn",
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
                whatis_id="wE5Bn",
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
    resp = client.post("/slack/whatis", data=create_slash_command_input(text="eod"))
    assert len(loads(resp.data)["blocks"]) == 7
    resp = client.post(
        "/slack/whatis", data=create_slash_command_input(text="Lost customer")
    )
    assert len(loads(resp.data)["blocks"]) == 7


@patch("requests.post")
def test_create_new(rp, client):
    # Press the Add new whatis button
    resp = client.post(
        "/slack/actions",
        data=create_block_action(
            action_id=constants.CREATE_NEW_WHATIS_ID,
            block_id="blocky",
            action_value=constants.CREATE_NEW_WHATIS_ID,
        ),
    )
    assert resp.data.decode() == ""

    # Now submit a dialog
    resp = client.post(
        "/slack/actions",
        data=create_dialog_submit_action(
            callback_id=constants.CREATE_NEW_WHATIS_ID_SUBMIT
        ),
        content_type="application/x-www-form-urlencoded",
    )
    assert resp.data.decode() == ""
    rp.assert_called()

    # Now query that same whatis we just created and ensure it returns result
    resp = client.post(
        "/slack/whatis", data=create_slash_command_input(text=TEST_WHATIS.terminology)
    )
    assert len(loads(resp.data)["blocks"]) == 7


def test_preload_whatises():
    fpath = '_testing_whatis_preload.json'
    with open(fpath, 'w') as file:
        file.write(json.dumps([
            dict(terminology='eod', definition='end of day'),
            dict(terminology='FBI', definition='Federal Bureau of Intelligence', links = 'https://www.jira.com/issues/DE-356'),
            dict(terminology='CSA', definition='Corporate Social allowance', notes = 'Here are some notes'),
        ]))

    client = WhatisApp(config=TestingConfig, preload_path=fpath)

    tc = client.test_client()
    resp = tc.post("/slack/whatis", data=create_slash_command_input(text="fbi"))
    assert len(loads(resp.data)["blocks"]) == 7

    client.handle_whatis_preload(fpath)

    # Check that loads don't happen again
    resp = tc.post("/slack/whatis", data=create_slash_command_input(text="fbi"))
    assert len(loads(resp.data)["blocks"]) == 7


    os.remove(fpath)

