import random

from core.Actions.ActionManager import AttachedAction
from core.Actions.StateAction import DecisiveStateAction
from core.Entities import Entity
from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import AttachStateEvent, PreDeathGameEvent, PostDamagesGameEvent
from core.SessionManager import session_manager
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
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)
    state: Inquisitor = event.state

    @event_manager.at_event(session.id, event=PreDeathGameEvent, priority=2)
    def hp_loss(message: PreDeathGameEvent):
        if message.canceled:
            return
        if message.entity != source:
            return
        if random.randint(0, 100) > 30:
            return
        if state.random_activated:
            return
        if source.hp <= 0:
            source.hp = 1
            session.say(f'😇|Высшие силы решили спасти {source.name}!')
            state.random_activated = True
            message.canceled = True


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

            @event_manager.at(self.session.id, turn=self.session.turn, event=PreDeathGameEvent)
            def hp_loss(message: PreDeathGameEvent):
                if message.entity != source:
                    return
                if source.hp <= 0:
                    source.hp = 1
                    self.session.say(f'😇|Высшие силы спасли {source.name}!')
                    message.canceled = True

            return

        if not target.outbound_dmg.contributors():
            self.session.say(f"💨|{source.name} молится, но с {target.name} ничего не происходит.")
            return

        self.session.say(f'🙏|{source.name} молится. Над {target.name} собираются тучи!')

        @event_manager.after(self.session.id, turns=0, repeats=2, event=PostDamagesGameEvent)
        def post_actions(actions_message: PostDamagesGameEvent):
            self.session.say(f"☁️|Над {target.name} собираются тучи. ({self.get_timer()})")

        @event_manager.after(self.session.id, turns=3, repeats=1, event=PostDamagesGameEvent)
        def post_actions(actions_message: PostDamagesGameEvent):
            self.session.say(f"🌩|Гнев небес обрушивается на {target.name} в виде молнии!")
            self.session.say(f"🌀|{target.name} оглушен!")

            target.get_skill("stun").stun += 1

    def get_timer(self):
        self._timer -= 1
        return self._timer


