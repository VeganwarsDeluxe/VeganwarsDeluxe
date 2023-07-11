from core.Events.EventManager import RegisterState, event_manager
from core.Events.Events import PreMoveGameEvent, AttachStateEvent, HPLossGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from modern.Items.RageSerum import RageSerum


class Sadist(Skill):
    id = 'sadist'
    name = 'Садист'
    description = 'Отнимая ХП противнику, вы восстанавливаете 1 энергию.'


@RegisterState(Sadist)
def register(event: AttachStateEvent):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    @event_manager.at_event(session.id, event=HPLossGameEvent, priority=2)
    def func(message: HPLossGameEvent):
        if source in message.source.inbound_dmg.contributors():
            source.energy += message.hp_loss
            session.say(f'😃|Садист {source.name} получает {message.hp_loss} энергии.')
