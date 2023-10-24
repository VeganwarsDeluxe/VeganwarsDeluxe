import random

import rebuild
from core.Context import Context
from core.Decorators import RegisterState
from core.Events.Events import AttachStateEvent
from core.SessionManager import session_manager
from core.Sessions import Session
from core.Skills.Skill import Skill


class Stockpile(Skill):
    id = 'stockpile'
    name = 'Запасливый'
    description = 'В начале матча вы получаете два дополнительных предмета.'


@RegisterState(Stockpile)
def register(root_context: Context[AttachStateEvent]):
    session: Session = session_manager.get_session(root_context.event.session_id)
    source = session.get_entity(root_context.event.entity_id)

    given = []
    for _ in range(2):
        item = random.choice(rebuild.game_items_pool)()
        pool = list(filter(lambda i: i().id not in given, rebuild.game_items_pool))
        pool = list(filter(lambda i: i.id not in [playerItem.id for playerItem in source.items], pool))
        if pool:
            item = random.choice(pool)()
        else:
            random.choice(rebuild.game_items_pool)()
        given.append(item.id)
        source.items.append(item)
