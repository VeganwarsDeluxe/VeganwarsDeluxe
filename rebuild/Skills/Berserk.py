from core.Context import Context
from core.Decorators import RegisterEvent
from core.Events.DamageEvents import AttackGameEvent
from core.Decorators import RegisterState
from core.Events.Events import PreMoveGameEvent, AttachStateEvent, PreActionsGameEvent, HPLossGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Berserk(Skill):
    id = 'berserk'
    name = 'Берсерк'
    description = 'Вы начинаете матч с 3 энергии. За каждое потерянное хп вы получаете +1 к текущей и максимальной ' \
                  'энергии. Если у вас остался 1 хп, то ваш урон увеличивается на 2.'


@RegisterState(Berserk)
def register(root_context: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_context.event.session_id)
    source = session.get_entity(root_context.event.entity_id)

    @RegisterEvent(session.id, PreMoveGameEvent, priority=1)
    def pre_actions(context: Context[PreMoveGameEvent]):
        source.max_energy = max(7 - source.hp, 2)
        if context.event.turn == 1:
            source.energy = source.max_energy

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    def hp_loss(context: Context[HPLossGameEvent]):
        if context.event.source != source:
            return
        source.energy = min(source.energy+context.event.hp_loss, source.max_energy)
        session.say(f"😡|Берсерк {source.name} получает {context.event.hp_loss} энергии.")
        if source.hp == 1:
            session.say(f"😡|Берсерк {source.name} входит в боевой транс!")

    @RegisterEvent(session.id, event=AttackGameEvent)
    def attack_handler(attack_context: Context[AttackGameEvent]):
        if attack_context.event.source != source:
            return
        if source.hp != 1:
            return
        if attack_context.event.damage:
            attack_context.event.damage += 2
