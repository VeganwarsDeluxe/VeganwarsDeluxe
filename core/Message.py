class Message:
    def __init__(self, session_id, turn):
        self.session_id = session_id
        self.turn = turn

    def __str__(self):
        return type(self).__name__


class PreMoveMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PreUpdatesMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PostUpdatesMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class HPLossMessage(Message):
    def __init__(self, session_id, turn, source, damage, hp_loss):
        super().__init__(session_id, turn)
        self.source = source
        self.damage = damage
        self.hp_loss = hp_loss


class PreActionsMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PostActionsMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PreDamagesMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PostDamagesMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PostTickMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class PostDeathsMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn)


class AttackMessage(Message):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PostAttackMessage(Message):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage
