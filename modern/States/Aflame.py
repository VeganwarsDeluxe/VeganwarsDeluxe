from core.Action import DecisiveAction
from core.Events.Events import PostActionsEvent, PostUpdatesEvent, PreDamagesEvent, AttackEvent, \
    PostAttackEvent
from core.States.State import State
from core.TargetType import OwnOnly


class Aflame(State):
    id = 'aflame'

    def __init__(self, source):
        super().__init__(source)
        self.flame = 0
        self.dealer = self.source
        self.extinguished = False

        self.timer = 0

    def register(self, session_id):
        source = self.source

        @self.event_manager.at_event(session_id, event=PostActionsEvent)
        def func(message: PostActionsEvent):
            if self.source.action.id == 'skip' and self.flame:
                self.source.session.say(f'💨|{self.source.name} потушил себя.')
                self.timer = 0
                self.flame = 0
                self.extinguished = False

        @self.event_manager.at_event(session_id, event=PostUpdatesEvent)
        def func(message: PostUpdatesEvent):
            if not self.flame:
                return
            self.source.remove_action('skip')

        @self.event_manager.at_event(session_id, event=PreDamagesEvent)
        def func(message: PreDamagesEvent):
            if not self.flame:
                return
            if self.extinguished:
                self.flame = 0
                self.extinguished = False
                self.timer = 0
                source.session.say(f'🔥|Огонь на {source.name} потух!')
                return
            else:
                self.extinguished = False
            damage = self.flame

            message = AttackEvent(message.session_id, message.turn, self.dealer, self.source, damage)
            self.source.session.event_manager.publish(message)
            damage = message.damage

            source.session.say(f'🔥|{source.name} горит. Получает {damage} урона.')

            message = PostAttackEvent(message.session_id, self.source.session.turn, self.dealer, self.source, damage)
            self.source.session.event_manager.publish(message)
            damage = message.damage

            source.inbound_dmg.add(self.dealer, damage)
            source.outbound_dmg.add(self.dealer, damage)
            if self.flame > 1:
                source.session.say(f'🔥|{source.name} горит. Теряет {self.flame - 1} энергии.')
                source.energy -= self.flame - 1
            if self.timer <= 1:
                self.extinguished = True
            else:
                self.timer -= 1

    def add_flame(self, source, flame):
        self.timer = 2
        if self.flame == 0:
            source.session.say(f'🔥|{self.source.name} загорелся!')
        else:
            source.session.say(f'🔥|Огонь {self.source.name} усиливается!')
        self.flame += flame
        self.dealer = source

    @property
    def actions(self):
        if not self.flame:
            return []
        return [
            Extinguish(self.source, self)
        ]


class Extinguish(DecisiveAction):
    id = 'extinguish'
    name = 'Потушится'

    def __init__(self, source, state):
        super().__init__(source, OwnOnly())
        self.state = state

    def func(self, source, target):
        self.state.flame = 0
        self.state.extinguished = False
        source.session.say(f'💨|{source.name} тушит себя.')
