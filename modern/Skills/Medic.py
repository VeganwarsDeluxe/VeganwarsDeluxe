from core.Events.EventManager import RegisterState
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill
from modern.Items.Stimulator import Stimulator


class Medic(Skill):
    id = 'medic'
    name = 'Медик'
    description = 'В начале боя вы получаете стимулятор, восстанавливающий 2 хп при использовании.'


@RegisterState(Medic)
def register(event: AttachStateEvent[Medic]):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    source.items.append(Stimulator())
