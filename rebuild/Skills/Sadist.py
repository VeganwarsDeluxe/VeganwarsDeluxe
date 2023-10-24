from core.Context import Context
from core.Decorators import RegisterState, RegisterEvent
from core.Events.Events import AttachStateEvent, HPLossGameEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Sadist(Skill):
    id = 'sadist'
    name = 'Садист'
    description = 'Отнимая ХП противнику, вы восстанавливаете 1 энергию.'


@RegisterState(Sadist)
def register(root_context: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_context.event.session_id)
    source = session.get_entity(root_context.event.entity_id)

    @RegisterEvent(session.id, event=HPLossGameEvent, priority=2)
    def func(context: Context[HPLossGameEvent]):
        if source in context.event.source.inbound_dmg.contributors():
            source.energy = min(source.energy + context.event.hp_loss, source.max_energy)
            session.say(f'😃|Садист {source.name} получает {context.event.hp_loss} энергии.')
