import random

from VegansDeluxe import rebuild
from VegansDeluxe.core.Actions.Action import DecisiveAction
from VegansDeluxe.core import AttachedAction
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import RegisterEvent

from VegansDeluxe.core import PreDeathGameEvent

from VegansDeluxe.core import Session
from VegansDeluxe.core import OwnOnly
from .Dummy import Dummy
from ...startup import engine


class Elemental(Dummy):
    def __init__(self, session_id: str, name='Веган Елементаль|🌪'):
        super().__init__(session_id, name=name)

        self.hp = 9
        self.max_hp = 9
        self.energy = 7
        self.max_energy = 7

        self.items = [item() for item in rebuild.all_items]
        self.states.extend([skill() for skill in rebuild.all_skills])

        self.team = 'elemental'

        self.anger = False

        @RegisterEvent(self.session_id, event=PreDeathGameEvent, priority=5)
        def hp_loss(context: EventContext[PreDeathGameEvent]):
            if context.event.canceled:
                return
            session: Session = context.session
            if context.event.entity != self:
                return
            if self.anger:
                return
            self.hp = 5
            self.max_hp = 5
            self.anger = True
            session.say("🌪|Елементаль в ЯРОСТИ!")
            context.event.canceled = True

    def choose_act(self, session):
        super().choose_act(session)
        self.weapon = random.choice(rebuild.all_weapons)(session.id, self.id)
        engine.engine.action_manager.update_entity_actions(session, self)

        cost = False
        while not cost:
            if self.energy <= 0:
                action = engine.action_manager.get_action(session, self, "reload")
            else:
                action = random.choice(engine.action_manager.get_available_actions(session, self))
            if not action:
                action = random.choice(engine.action_manager.get_available_actions(session, self))
            if not action.targets:
                continue
            action.target = random.choice(action.targets)
            engine.action_manager.queue_action(session, self, action.id)
            if self.anger:
                cost = random.choice([True, False, False, False])
            else:
                cost = action.cost


@AttachedAction(Elemental)
class WarpReality(DecisiveAction):
    id = 'warp_reality'
    name = 'Искривить пространство'
    target_type = OwnOnly()

    def func(self, source, target):
        self.source.inbound_accuracy_bonus = -5
        self.session.say(f'🌌|{source.name} искривляет пространство.')


@AttachedAction(Elemental)
class Singularity(DecisiveAction):
    id = 'reload_singularity'
    name = 'Перезагрузить сингулярность'
    target_type = OwnOnly()

    def func(self, source, target):
        self.session.say(f'⚫️|{source.name} перезагружает сингулярность. Енергия восстановлена ({source.max_energy})!')
        source.energy = source.max_energy
