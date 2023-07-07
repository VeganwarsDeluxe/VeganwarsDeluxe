from core.Entities import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import PreMoveGameEvent
from core.Sessions import Session
from core.TargetType import TargetType, Own, Aliveness, Team, Distance


class Action:
    id = 'action'
    name = 'Action'
    priority = 0
    target_type = TargetType(0, 0, 0, 0)

    def __init__(self, session: Session, source: Entity):
        self.session: Session = session
        self.source: Entity = source
        self.target: Entity = source

        self.canceled = False
        self.type = 'action'
        self.removed = False

    def func(self, source, target):
        pass

    def __call__(self):  # Abstract "Run" method for overriding
        if self.canceled:
            return
        return self.func(self.source, self.target)

    @property
    def hidden(self) -> bool:
        return False

    @property
    def targets(self):
        return self.get_targets(self.source, self.target_type)

    def get_targets(self, source, target_type: TargetType):
        target_pool = self.session.entities
        if target_type.own == Own.SELF_ONLY:
            return [source]
        elif target_type.own == Own.SELF_EXCLUDED:
            target_pool = list(filter(lambda t: t != source, target_pool))

        if target_type.aliveness == Aliveness.ALIVE_ONLY:
            target_pool = list(filter(lambda t: not t.dead, target_pool))
        elif target_type.aliveness == Aliveness.DEAD_ONLY:
            target_pool = list(filter(lambda t: t.dead, target_pool))

        if target_type.team == Team.ALLIES_ONLY:  # Exclude enemies
            target_pool = list(filter(lambda t: source.is_ally(t), target_pool))
        elif target_type.team == Team.ENEMIES_ONLY:  # Exclude allies
            target_pool = list(filter(lambda t: not source.is_ally(t), target_pool))

        if target_type.distance == Distance.NEARBY_ONLY:  # Exclude distant
            target_pool = list(filter(lambda t: t in source.nearby_entities, target_pool))
        elif target_type.distance == Distance.DISTANT_ONLY:  # Exclude nearby
            target_pool = list(filter(lambda t: t not in source.nearby_entities, target_pool))

        return target_pool

    @property
    def blocked(self):
        return False

    @property
    def cost(self):
        return None


class DecisiveAction(Action):
    @property
    def cost(self):
        return True


class FreeAction(Action):
    @property
    def cost(self):
        return False
