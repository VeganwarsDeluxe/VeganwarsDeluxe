class Event:
    def __str__(self):
        return type(self).__name__


class AttachSessionEvent(Event):
    def __init__(self, session_id):
        self.session_id = session_id


class GameEvent(Event):
    def __init__(self, session_id, turn):
        self.session_id = session_id
        self.turn = turn


class ActionGameEvent(GameEvent):
    def __init__(self, session_id, turn, source_id, target_id):
        super().__init__(session_id, turn)
        self.source_id = source_id
        self.target_id = target_id


class AddAction(GameEvent):
    pass


class RemoveAction(GameEvent):
    pass


class CallActionsGameEvent(GameEvent):
    pass


class DeathGameEvent(GameEvent):
    def __init__(self, session_id, turn, entity):
        super().__init__(session_id, turn)
        self.entity = entity


class HPLossGameEvent(GameEvent):
    def __init__(self, session_id, turn, source, damage, hp_loss):
        super().__init__(session_id, turn)
        self.source = source
        self.damage = damage
        self.hp_loss = hp_loss


class AttackGameEvent(GameEvent):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PostAttackGameEvent(GameEvent):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PreMoveGameEvent(GameEvent):
    pass


class PreUpdatesGameEvent(GameEvent):
    pass


class PostUpdatesGameEvent(GameEvent):
    pass


class PreActionsGameEvent(GameEvent):
    pass


class PostActionsGameEvent(GameEvent):
    pass


class PreDamagesGameEvent(GameEvent):
    pass


class PostDamagesGameEvent(GameEvent):
    pass


class PostTickGameEvent(GameEvent):
    pass


class PostDeathsGameEvent(GameEvent):
    pass
