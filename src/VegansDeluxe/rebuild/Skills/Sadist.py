from VegansDeluxe.core import HPLossGameEvent
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Sadist(Skill):
    id = 'sadist'
    name = ls("rebuild.skill.sadist.name")
    description = ls("rebuild.skill.sadist.description")


@RegisterState(Sadist)
async def register(root_context: StateContext[Sadist]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    async def func(context: EventContext[HPLossGameEvent]):
        if source in context.event.source.inbound_dmg.contributors():
            source.energy = min(source.energy + context.event.hp_loss, source.max_energy)
            session.say(ls("rebuild.skill.sadist.effect").format(source.name, context.event.hp_loss))
