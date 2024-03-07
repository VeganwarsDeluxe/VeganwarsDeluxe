from VegansDeluxe.core import RegisterEvent
from VegansDeluxe.core import StateContext, EventContext
from VegansDeluxe.core import HPLossGameEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Skills.Skill import Skill


class Pyromaniac(Skill):
    id = 'pyromaniac'
    name = 'Пиромант'
    description = 'За каждого горящего соперника вы получаете бонус к урону.'


# @RegisterState(Pyromaniac)
def register(root_context: StateContext[Pyromaniac]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, event=HPLossGameEvent)
    def func(context: EventContext[HPLossGameEvent]):
        if source in context.event.source.inbound_dmg.contributors():
            source.energy += context.event.hp_loss
            session.say(f'😃|Садист {source.name} получает {context.event.hp_loss} энергии.')


def get_bonus(session: Session):
    bonus = 0
    for entity in session.entities:
        aflame = entity.get_state('aflame')
        if aflame.flame:
            bonus += 1
    return bonus
