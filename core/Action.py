from core.TargetType import TargetType


class Action:
    id = 'action'
    name = 'Action'

    def __init__(self, source, target_type, priority=0):
        self.priority: int = priority  # TODO: Revise priorities of all actions
        self.data = dict()

        self.target_type: TargetType = target_type

        self.source = source
        self.target = None

        self.canceled = False
        self.type = 'action'

    def func(self, source, target):
        pass

    def __call__(self):  # Abstract "Run" method for overriding
        if self.canceled:
            return
        self.source.session.event.action = self
        return self.func(self.source, self.target)

    @property
    def targets(self):
        return self.get_targets(self.source, self.target_type)

    def get_targets(self, source, target_type: TargetType):
        target_pool = source.session.entities
        if target_type.own == 1:    # Self only
            return [source]
        elif target_type.own == 2:  # Exclude self
            target_pool = list(filter(lambda t: t != source, target_pool))

        if target_type.aliveness == 1:   # Exclude dead
            target_pool = list(filter(lambda t: not t.dead, target_pool))
        elif target_type.aliveness == 2: # Exclude alive
            target_pool = list(filter(lambda t: t.dead, target_pool))

        if target_type.team == 1:  # Exclude enemies
            target_pool = list(filter(lambda t: source.is_ally(t), target_pool))
        elif target_type.team == 2:  # Exclude allies
            target_pool = list(filter(lambda t: not source.is_ally(t), target_pool))

        if target_type.distance == 1:   # Exclude distant
            target_pool = list(filter(lambda t: t in source.nearby_entities, target_pool))
        elif target_type.distance == 2:  # Exclude nearby
            target_pool = list(filter(lambda t: t not in source.nearby_entities, target_pool))

        return target_pool

    @property
    def cost(self):
        return False

    @property
    def blocked(self):
        return False


class DecisiveAction(Action):
    def __init__(self, source, target_type, priority=0):
        super().__init__(source, target_type=target_type, priority=priority)

    @property
    def cost(self):
        return 1


class FreeAction(Action):
    def __init__(self, source, target_type, priority=0):
        super().__init__(source, target_type=target_type, priority=priority)

    @property
    def cost(self):
        return 0


class ImmediateAction(Action):
    def __init__(self, source, target_type, priority=0):
        super().__init__(source, target_type=target_type, priority=priority)

    @property
    def cost(self):
        return -1
