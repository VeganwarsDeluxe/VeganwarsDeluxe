class Message:
    def __init__(self, session_id, turn, current_event):
        self.session_id = session_id
        self.turn = turn
        self.current_event = current_event


class PreMoveMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'pre-move')


class PreUpdateMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'pre-update')


class PostUpdateMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'post-update')


class HPLossMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'hp-loss')


class PreActionMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'pre-action')


class PostActionMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'post-action')


class PreDamagesMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'pre-damages')


class PostDamagesMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'post-damages')


class PostTickMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'post-tick')


class PostDeathMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'post-death')


class AttackMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'attack')


class PostAttackMessage(Message):
    def __init__(self, session_id, turn):
        super().__init__(session_id, turn, 'post-attack')
