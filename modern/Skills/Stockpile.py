import random

import modern
from core.Skills.Skill import Skill


class Stockpile(Skill):
    def __init__(self, source):
        super().__init__(source, id='stockpile', name='Запасливый', stage='pre-move')

    def __call__(self):
        if self.source.session.turn == 1:
            given = []
            for _ in range(2):
                item = random.choice(modern.game_items_pool)(self.source)
                pool = list(filter(lambda i: i(self.source).id not in given, modern.game_items_pool))
                if pool:
                    item = random.choice(pool)(self.source)
                given.append(item.id)
                self.source.items.append(item)
