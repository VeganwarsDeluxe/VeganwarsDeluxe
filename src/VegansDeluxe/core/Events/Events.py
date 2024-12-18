from VegansDeluxe.core.States import State


class Event:
    def __init__(self, unique_type=None):
        self.unique_type = unique_type
        self.canceled = False

    def __str__(self):
        return type(self).__name__


class AttachSessionEvent(Event):
    """
    Published by SessionManager after attaching a Session.
    Used by ContentManager to initialize it.
    """

    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id


class StartSessionEvent(Event):
    """
    Published by Session when it is started.
    """

    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id


class AttachStateEvent[T: State](Event):
    def __init__(self, session_id, entity_id, state: State):
        super().__init__(type(state))
        self.session_id = session_id
        self.entity_id = entity_id
        self.state: T = state


class GameEvent(Event):
    def __init__(self, session_id, turn):
        super().__init__()
        self.session_id = session_id
        self.turn = turn


class ActionGameEvent(GameEvent):
    def __init__(self, session_id, turn, source_id, target_id):
        super().__init__(session_id, turn)
        self.source_id = source_id
        self.target_id = target_id


class DeliveryRequestEvent(GameEvent):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class DeliveryPackageEvent(GameEvent):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class ExecuteActionEvent(GameEvent):
    def __init__(self, session_id, turn, action):
        super().__init__(session_id, turn)
        self.action = action


class PreDeathGameEvent(GameEvent):
    def __init__(self, session_id, turn, entity):
        super().__init__(session_id, turn)
        self.entity = entity


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


class SessionStopGameEvent(GameEvent):
    pass


class SessionFinishGameEvent(GameEvent):
    pass


class CallActionsGameEvent(GameEvent):
    pass


class PreMoveGameEvent(GameEvent):
    pass


# Action updating events start


class PreUpdatesGameEvent(GameEvent):
    pass


class PostUpdatesGameEvent(GameEvent):
    pass


class PreUpdateActionsGameEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id


class PostUpdateActionsGameEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id


# Action updating events end


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
