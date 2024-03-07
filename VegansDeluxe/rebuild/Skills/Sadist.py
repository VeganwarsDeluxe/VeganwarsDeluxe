from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import RegisterState, RegisterEvent
from VegansDeluxe.core import HPLossGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill


class Sadist(Skill):
    id = 'sadist'
    name = 'Садист'
    description = 'Отнимая ХП противнику, вы восстанавливаете 1 энергию.'


@RegisterState(Sadist)
def register(root_context: StateContext[Sadist]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    def func(context: EventContext[HPLossGameEvent]):
        if source in context.event.source.inbound_dmg.contributors():
            source.energy = min(source.energy + context.event.hp_loss, source.max_energy)
            session.say(f'😃|Садист {source.name} получает {context.event.hp_loss} энергии.')
