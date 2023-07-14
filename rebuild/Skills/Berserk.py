from core.Events.DamageEvents import AttackGameEvent
from core.Events.EventManager import RegisterState, event_manager
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
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, PreMoveGameEvent, priority=1)
    def pre_actions(message: PreActionsGameEvent):
        source.max_energy = max(7 - source.hp, 2)
        if message.turn == 1:
            source.energy = source.max_energy

    @event_manager.at_event(session.id, event=HPLossGameEvent, priority=2)
    def hp_loss(message: HPLossGameEvent):
        if message.source != source:
            return
        source.energy = min(source.energy+message.hp_loss, source.max_energy)
        session.say(f"😡|Берсерк {source.name} получает {message.hp_loss} энергии.")
        if source.hp == 1:
            session.say(f"😡|Берсерк {source.name} входит в боевой транс!")

    @event_manager.at_event(session.id, event=AttackGameEvent)
    def attack_handler(attack_message: AttackGameEvent):
        if attack_message.source != source:
            return
        if source.hp != 1:
            return
        if attack_message.damage:
            attack_message.damage += 2
