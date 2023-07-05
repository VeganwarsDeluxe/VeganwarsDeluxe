import random

import modern
from core.Events.EventManager import RegisterState
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Stockpile(Skill):
    id = 'stockpile'
    name = 'Запасливый'
    description = 'В начале матча вы получаете два дополнительных предмета.'


@RegisterState(Stockpile)
def register(event: AttachStateEvent[Stockpile]):
    session: Session = session_manager.get_session(event.session_id)
    source = session.get_entity(event.entity_id)

    given = []
    for _ in range(2):
        item = random.choice(modern.game_items_pool)(source)
        pool = list(filter(lambda i: i(source).id not in given, modern.game_items_pool))
        pool = list(filter(lambda i: i.id not in [playerItem.id for playerItem in self.source.items], pool))
        if pool:
            item = random.choice(pool)(source)
        else:
            random.choice(modern.game_items_pool)(source)
        given.append(item.id)
        source.items.append(item)
