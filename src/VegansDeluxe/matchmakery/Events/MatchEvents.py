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


class DungeonMatchStartedEvent(GameEvent):
    """A Dungeon has initialized a child Match and made it active."""
    def __init__(self, session_id: str, turn: int, dungeon, previous_match, current_match):
        super().__init__(session_id, turn)
        self.dungeon = dungeon
        self.previous_match = previous_match
        self.current_match = current_match


class DungeonMatchFinishedEvent(GameEvent):
    """A child Match ended and is about to be replaced or finalized."""
    def __init__(self, session_id: str, turn: int, dungeon, completed_match):
        super().__init__(session_id, turn)
        self.dungeon = dungeon
        self.completed_match = completed_match


class DungeonFinishedEvent(GameEvent):
    """The final child Match ended and the Dungeon has no next level."""
    def __init__(self, session_id: str, turn: int, dungeon, final_match):
        super().__init__(session_id, turn)
        self.dungeon = dungeon
        self.final_match = final_match


class DungeonFailedEvent(GameEvent):
    """All players who joined a Dungeon died in one of its child Matches."""
    def __init__(self, session_id: str, turn: int, dungeon, failed_match):
        super().__init__(session_id, turn)
        self.dungeon = dungeon
        self.failed_match = failed_match
