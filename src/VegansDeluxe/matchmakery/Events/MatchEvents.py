from VegansDeluxe.core.Events.Events import GameEvent


class RequestActionChoiceEvent(GameEvent):
    """
    Published at the start of each move. The UI requests a choice from players, and NPCs decide on their own.
    """
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id

class RequestTeamChoiceEvent(GameEvent):
    """
    Published at the start of the lobby phase. The UI requests a choice from players.
    NPCs are set up by the Match itself.
    """
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id

class PlayerReadyEvent(GameEvent):
    """
    Published when player selected a Decisive Action. When all players (and NPCs) are ready, Match advances.
    """

    def __init__(self, session_id: str, turn: int, entity_id: str):
        super().__init__(session_id, turn)
        self.entity_id: str = entity_id


class BroadcastLogsEvent(GameEvent):
    """
    Published when sessions is requesting to post per-turn logs.
    """

    def __init__(self, session_id: str, turn: int):
        super().__init__(session_id, turn)


class BroadcastEndMessagesEvent(GameEvent):
    """
    Published when sessions is requesting to post ending logs.
    """

    def __init__(self, session_id: str, turn: int):
        super().__init__(session_id, turn)


class DisplayItemChoiceEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id


class DisplayActionSelectionMenuEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id

class DisplayWeaponSelectionMenuEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id

class DisplaySkillSelectionMenuEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id

class DisplayQuestionChoiceMenuEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id, question_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id
        self.question_id = question_id

class WeaponsChosenEvent(GameEvent):
    def __init__(self, session_id: str, turn: int):
        super().__init__(session_id, turn)

class SkillsChosenEvent(GameEvent):
    def __init__(self, session_id: str, turn: int):
        super().__init__(session_id, turn)