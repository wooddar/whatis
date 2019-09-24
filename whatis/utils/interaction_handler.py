from collections import defaultdict


class SlackInteractionNotRegistered(Exception):
    ...


class SlackInteractionHandler:
    def __init__(self):
        self._interactions = defaultdict(dict)

    def add_interaction(self, interaction_id, f):

        self._interactions[interaction_id] = f

    def interaction(self, interaction_id):
        def wrap(f):
            self.add_interaction(interaction_id, f)
            return f

        return wrap

    def interact(self, interaction_id, **kwargs):
        r = self._interactions.get(interaction_id)

        if r is None:
            raise SlackInteractionNotRegistered(
                f"No function registered for the interaction ID {interaction_id}"
            )
        else:
            return r(**kwargs)
