from VegansDeluxe.core.Events.Events import GameEvent


class ChooseActionEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id
