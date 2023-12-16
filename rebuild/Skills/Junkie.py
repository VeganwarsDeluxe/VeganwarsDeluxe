import random

from core.Context import StateContext, EventContext
from core.Decorators import RegisterEvent, RegisterState, Nearest, At
from core.Actions.ActionManager import action_manager
from core.Events.DamageEvents import AttackGameEvent
from core.Events.EventManager import event_manager
from core.Events.Events import AttachStateEvent, PreActionsGameEvent, PreDamagesGameEvent, PreMoveGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.Items.Adrenaline import Adrenaline
from rebuild.Items.Hitin import Hitin
from rebuild.Items.Jet import Jet
from rebuild.Items.RageSerum import RageSerum
from rebuild.Items.Stimulator import Stimulator


class Junkie(Skill):
    id = 'junkie'
    name = 'Наркоман'
    description = 'Ваша точность понижена на 1. Каждый раз, когда вы применяете 💉медикамент, ' \
                  'ваша точность на этом ходу увеличивается на 2, а урон на 1.'


@RegisterState(Junkie)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity
    source.items.append(random.choice([Jet, Hitin, Adrenaline])())

    @RegisterEvent(session.id, event=PreMoveGameEvent)
    def func(context: EventContext[PreMoveGameEvent]):
        source.outbound_accuracy_bonus -= 1

    @RegisterEvent(session.id, PreActionsGameEvent)
    def pre_actions(context: EventContext[PreActionsGameEvent]):
        accuracy_bonus = 0
        damage_bonus = 0
        for action in action_manager.get_queued_session_actions(session):
            if action.id in [Jet.id, Hitin.id, Adrenaline.id, Stimulator.id, RageSerum.id]:
                if action.target == source and not action.canceled:
                    accuracy_bonus += 2
                    damage_bonus += 1

        if accuracy_bonus:
            @At(session.id, turn=session.turn, event=PreDamagesGameEvent)
            def post_actions(actions_context: EventContext[PreDamagesGameEvent]):
                session.say(f"🙃|{source.name} получает бонусную точность и урон!")

            source.outbound_accuracy_bonus += accuracy_bonus

            @At(session.id, turn=session.turn, event=AttackGameEvent)
            def attack_handler(actions_context: EventContext[AttackGameEvent]):
                if actions_context.event.source != source:
                    return
                if actions_context.event.damage:
                    actions_context.event.damage += damage_bonus
