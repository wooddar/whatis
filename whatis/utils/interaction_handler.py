class SlackInteractionNotRegistered(Exception):
    ...


class SlackInteractionHandler:
    _interactions = {}

    def add_interaction(self, interaction_id, f):
        self._interactions[interaction_id] = f

    def interaction(self, interaction_id):
        def wrap(f):
            self.add_interaction(interaction_id, f)
            return f

        return wrap

    def interact(self, interaction_id):
        r = self._interactions.get(interaction_id)
        if r is None:
            raise SlackInteractionNotRegistered(
                f"No function registered fro the interaction ID {interaction_id}"
            )
        else:
            return r
