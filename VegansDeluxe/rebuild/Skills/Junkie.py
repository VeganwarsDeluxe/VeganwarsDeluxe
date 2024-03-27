import random

from VegansDeluxe.core import RegisterEvent, RegisterState, At
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import AttackGameEvent
from VegansDeluxe.core import PreActionsGameEvent, PreDamagesGameEvent, PreMoveGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.Items.Adrenaline import Adrenaline
from VegansDeluxe.rebuild.Items.Chitin import Chitin
from VegansDeluxe.rebuild.Items.Jet import Jet
from VegansDeluxe.rebuild.Items.RageSerum import RageSerum
from VegansDeluxe.rebuild.Items.Stimulator import Stimulator


class Junkie(Skill):
    id = 'junkie'
    name = ls("skill_junkie_name")
    description = ls("skill_junkie_description")


@RegisterState(Junkie)
def register(root_context: StateContext[Junkie]):
    session: Session = root_context.session
    source = root_context.entity
    source.items.append(random.choice([Jet, Chitin, Adrenaline])())

    @RegisterEvent(session.id, event=PreMoveGameEvent)
    def func(context: EventContext[PreMoveGameEvent]):
        source.outbound_accuracy_bonus -= 1

    @RegisterEvent(session.id, PreActionsGameEvent)
    def pre_actions(context: EventContext[PreActionsGameEvent]):
        accuracy_bonus = 0
        damage_bonus = 0
        for action in context.action_manager.get_queued_session_actions(session):
            if action.id in [Jet.id, Chitin.id, Adrenaline.id, Stimulator.id, RageSerum.id]:
                if action.target == source and not action.canceled:
                    accuracy_bonus += 2
                    damage_bonus += 1

        if accuracy_bonus:
            @At(session.id, turn=session.turn, event=PreDamagesGameEvent)
            def post_actions(actions_context: EventContext[PreDamagesGameEvent]):
                session.say(ls("skill_junkie_effect").format(source.name))

            source.outbound_accuracy_bonus += accuracy_bonus

            @At(session.id, turn=session.turn, event=AttackGameEvent)
            def attack_handler(actions_context: EventContext[AttackGameEvent]):
                if actions_context.event.source != source:
                    return
                if actions_context.event.damage:
                    actions_context.event.damage += damage_bonus
