from .Events import GameEvent


class DamageGameEvent(GameEvent):
    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PreDamageGameEvent(DamageGameEvent):
    pass


class PostDamageGameEvent(DamageGameEvent):
    pass


class AttackGameEvent(PreDamageGameEvent):
    pass


class PostAttackGameEvent(PostDamageGameEvent):
    pass
