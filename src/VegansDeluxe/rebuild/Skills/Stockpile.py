import random

from VegansDeluxe import rebuild
from VegansDeluxe.core import RegisterState
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext
from VegansDeluxe.core.Skills.Skill import Skill
from VegansDeluxe.core.Translator.LocalizedString import ls


class Stockpile(Skill):
    id = 'stockpile'
    name = ls("rebuild.skill.stockpile.name")
    description = ls("rebuild.skill.stockpile.description")


@RegisterState(Stockpile)
async def register(root_context: StateContext[Stockpile]):
    session: Session = root_context.session
    source = root_context.entity

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
