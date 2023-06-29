class Event:
    def __init__(self, session_id, turn):
        self.session_id = session_id
        self.turn = turn

    def __str__(self):
        return type(self).__name__


class DeathEvent(Event):
    def __init__(self, session_id, turn, entity):
        super().__init__(session_id, turn)
        self.entity = entity


class HPLossEvent(Event):
    def __init__(self, session_id, turn, source, damage, hp_loss):
        super().__init__(session_id, turn)
        self.source = source
        self.damage = damage
        self.hp_loss = hp_loss


class AttackEvent(Event):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PostAttackEvent(Event):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PreMoveEvent(Event):
    pass


class PreUpdatesEvent(Event):
    pass


class PostUpdatesEvent(Event):
    pass


class PreActionsEvent(Event):
    pass


class PostActionsEvent(Event):
    pass


class PreDamagesEvent(Event):
    pass


class PostDamagesEvent(Event):
    pass


class PostTickEvent(Event):
    pass


class PostDeathsEvent(Event):
    pass
