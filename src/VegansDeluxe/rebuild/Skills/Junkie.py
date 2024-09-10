import random

from VegansDeluxe.core import AttackGameEvent
from VegansDeluxe.core import PreActionsGameEvent, PreDamagesGameEvent, PreMoveGameEvent
from VegansDeluxe.core import RegisterEvent, RegisterState, At, ActionTag
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.Items.Adrenaline import Adrenaline
from VegansDeluxe.rebuild.Items.Chitin import Chitin
from VegansDeluxe.rebuild.Items.Jet import Jet


class Junkie(Skill):
    id = 'junkie'
    name = ls("skill_junkie_name")
    description = ls("skill_junkie_description")

    item_pool = [Jet, Chitin, Adrenaline]


@RegisterState(Junkie)
async def register(root_context: StateContext[Junkie]):
    session: Session = root_context.session
    source = root_context.entity
    source.items.append(random.choice(Junkie.item_pool)())

    @RegisterEvent(session.id, event=PreMoveGameEvent)
    async def func(context: EventContext[PreMoveGameEvent]):
        source.outbound_accuracy_bonus -= 1

    @RegisterEvent(session.id, PreActionsGameEvent)
    async def pre_actions(context: EventContext[PreActionsGameEvent]):
        accuracy_bonus = 0
        damage_bonus = 0
        for action in context.action_manager.get_queued_session_actions(session):
            if ActionTag.MEDICINE in action.tags:
                if action.target == source and not action.canceled:
                    accuracy_bonus += 2
                    damage_bonus += 1

        if accuracy_bonus:
            @At(session.id, turn=session.turn, event=PreDamagesGameEvent)
            async def post_actions(actions_context: EventContext[PreDamagesGameEvent]):
                session.say(ls("skill_junkie_effect").format(source.name))

            source.outbound_accuracy_bonus += accuracy_bonus

            @At(session.id, turn=session.turn, event=AttackGameEvent)
            async def attack_handler(actions_context: EventContext[AttackGameEvent]):
                if actions_context.event.source != source:
                    return
                if actions_context.event.damage:
                    actions_context.event.damage += damage_bonus
