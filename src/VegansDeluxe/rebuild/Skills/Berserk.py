from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterEvent
from VegansDeluxe.core import AttackGameEvent
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import PreMoveGameEvent, HPLossGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Berserk(Skill):
    id = 'berserk'
    name = ls("skill_berserk_name")
    description = ls("skill_berserk_description")


@RegisterState(Berserk)
async def register(root_context: StateContext[Berserk]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, PreMoveGameEvent, priority=1)
    async def pre_actions(context: EventContext[PreMoveGameEvent]):
        source.max_energy = max(7 - source.hp, 2)
        if context.event.turn == 1:
            source.energy = source.max_energy

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    async def hp_loss(context: EventContext[HPLossGameEvent]):
        if context.event.source != source:
            return
        source.energy = min(source.energy+context.event.hp_loss, source.max_energy)
        session.say(f"😡|Берсерк {source.name} получает {context.event.hp_loss} энергии.")
        if source.hp == 1:
            session.say(f"😡|Берсерк {source.name} входит в боевой транс!")

    @RegisterEvent(session.id, event=AttackGameEvent)
    async def attack_handler(attack_context: EventContext[AttackGameEvent]):
        if attack_context.event.source != source:
            return
        if source.hp != 1:
            return
        if attack_context.event.damage:
            attack_context.event.damage += 2
