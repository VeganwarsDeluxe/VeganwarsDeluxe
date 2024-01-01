from core.Context import StateContext, EventContext
from core.ContentManager import RegisterEvent
from core.Events.DamageEvents import AttackGameEvent
from core.ContentManager import RegisterState
from core.Events.Events import PreMoveGameEvent, AttachStateEvent, HPLossGameEvent
from core.Sessions import Session
from core.Skills.Skill import Skill


class Berserk(Skill):
    id = 'berserk'
    name = 'Берсерк'
    description = 'Вы начинаете матч с 3 энергии. За каждое потерянное хп вы получаете +1 к текущей и максимальной ' \
                  'энергии. Если у вас остался 1 хп, то ваш урон увеличивается на 2.'


@RegisterState(Berserk)
def register(root_context: StateContext[AttachStateEvent]):
    session: Session = root_context.session
    source = root_context.entity

    @RegisterEvent(session.id, PreMoveGameEvent, priority=1)
    def pre_actions(context: EventContext[PreMoveGameEvent]):
        source.max_energy = max(7 - source.hp, 2)
        if context.event.turn == 1:
            source.energy = source.max_energy

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    def hp_loss(context: EventContext[HPLossGameEvent]):
        if context.event.source != source:
            return
        source.energy = min(source.energy+context.event.hp_loss, source.max_energy)
        session.say(f"😡|Берсерк {source.name} получает {context.event.hp_loss} энергии.")
        if source.hp == 1:
            session.say(f"😡|Берсерк {source.name} входит в боевой транс!")

    @RegisterEvent(session.id, event=AttackGameEvent)
    def attack_handler(attack_context: EventContext[AttackGameEvent]):
        if attack_context.event.source != source:
            return
        if source.hp != 1:
            return
        if attack_context.event.damage:
            attack_context.event.damage += 2
