import random

from core.Actions.StateAction import DecisiveStateAction
from core.ContentManager import AttachedAction
from core.ContentManager import RegisterEvent, RegisterState, After, At
from core.Context import StateContext, EventContext
from core.Entities import Entity
from core.Events.Events import PreDeathGameEvent, PostDamagesGameEvent
from core.Sessions import Session
from core.Skills.Skill import Skill
from core.TargetType import Everyone


class Inquisitor(Skill):
    id = 'inquisitor'
    name = 'Инквизитор'
    description = 'Вы можете направить гнев небес на соперника. Если в этот ход соперник делает действие, ' \
                  'наносящее вред, то через 2 хода он будет оглушен. Если применить на союзника, то в этот ход он ' \
                  'не может умереть.'

    def __init__(self):
        super().__init__()
        self.cooldown_turn = 0

        self.random_activated = False


@RegisterState(Inquisitor)
def register(root_context: StateContext[Inquisitor]):
    session: Session = root_context.session
    source = root_context.entity
    state: Inquisitor = root_context.state

    @RegisterEvent(session.id, event=PreDeathGameEvent, priority=2)
    def hp_loss(context: EventContext[PreDeathGameEvent]):
        if context.event.canceled:
            return
        if context.event.entity != source:
            return
        if random.randint(0, 100) > 30:
            return
        if state.random_activated:
            return
        if source.hp <= 0:
            source.hp = 1
            session.say(f'😇|Высшие силы решили спасти {source.name}!')
            state.random_activated = True
            context.event.canceled = True


@AttachedAction(Inquisitor)
class Pray(DecisiveStateAction):
    id = 'pray'
    name = 'Направить взор небес'
    priority = 2
    target_type = Everyone()

    def __init__(self, session: Session, source: Entity, skill: Inquisitor):
        super().__init__(session, source, skill)
        self.state = skill

        self._timer = 3

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.state.cooldown_turn

    def func(self, source: Entity, target: Entity):
        self.state.cooldown_turn = self.session.turn + 3
        if source.is_ally(target):
            self.session.say(f"🙏|{source.name} молится за {target.name}!")

            @At(self.session.id, turn=self.session.turn, event=PreDeathGameEvent)
            def hp_loss(context: EventContext[PreDeathGameEvent]):
                if context.event.entity != source:
                    return
                if source.hp <= 0:
                    source.hp = 1
                    self.session.say(f'😇|Высшие силы спасли {source.name}!')
                    context.event.canceled = True

            return

        if not target.outbound_dmg.contributors():
            self.session.say(f"💨|{source.name} молится, но с {target.name} ничего не происходит.")
            return

        self.session.say(f'🙏|{source.name} молится. Над {target.name} собираются тучи!')

        @After(self.session.id, turns=0, repeats=2, event=PostDamagesGameEvent)
        def post_actions(actions_context: EventContext[PostDamagesGameEvent]):
            self.session.say(f"☁️|Над {target.name} собираются тучи. ({self.get_timer()})")

        @After(self.session.id, turns=3, repeats=1, event=PostDamagesGameEvent)
        def post_actions(actions_context: EventContext[PostDamagesGameEvent]):
            self.session.say(f"🌩|Гнев небес обрушивается на {target.name} в виде молнии!")
            self.session.say(f"🌀|{target.name} оглушен!")

            target.get_skill("stun").stun += 1

    def get_timer(self):
        self._timer -= 1
        return self._timer


