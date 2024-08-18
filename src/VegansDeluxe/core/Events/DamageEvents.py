from .Events import GameEvent


class DamageGameEvent(GameEvent):
    """
    Published when damage is going to be dealt.
    Generally occurs twice, before and after the corresponding log message.
    Metaclass for damage - should not be used.
    """

    def __init__(self, session_id, turn, source, target, damage):
        super().__init__(session_id, turn)

        self.source = source
        self.target = target
        self.damage = damage


class PreDamageGameEvent(DamageGameEvent):
    """
    Published when damage is going to be dealt.
    Occurs BEFORE the corresponding log message.
    Can be used to alter the damage before it is displayed.
    """

    pass


class PostDamageGameEvent(DamageGameEvent):
    """
    Published when damage is going to be dealt.
    Occurs AFTER the corresponding log message.
    Can be used to alter the damage after it is displayed.
    """

    pass


class AttackGameEvent(PreDamageGameEvent):
    """
    Published when damage is going to be dealt by attacks (usually by weapons).
    Event, that generally occurs BEFORE the corresponding log message.
    Can be used to alter the damage before it is displayed.
    """

    pass


class PostAttackGameEvent(PostDamageGameEvent):
    """
    Published when damage is going to be dealt by attacks (usually by weapons).
    Event, that generally occurs AFTER the corresponding log message.
    Can be used to alter the damage after it is displayed.
    """

    pass
