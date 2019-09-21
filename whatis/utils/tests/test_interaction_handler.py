import pytest
from utils.interaction_handler import (
    SlackInteractionHandler,
    SlackInteractionNotRegistered,
)


@pytest.fixture
def interaction_handler():
    return SlackInteractionHandler()


def test_add_interaction(interaction_handler):
    @interaction_handler.interaction("SOME_ID")
    def my_interaction():
        pass

    with pytest.raises(SlackInteractionNotRegistered):
        interaction_handler.interact("nothing here")
    assert interaction_handler.interact("SOME_ID") == my_interaction
