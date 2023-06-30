from core.Items.ItemAction import DecisiveItem
import random

from core.TargetType import Enemies


class Molotov(DecisiveItem):
    id = 'molotov'
    name = 'Коктейль Молотова'

    def __init__(self, source):
        super().__init__(source, target_type=Enemies())

        self.range = 2

    def use(self):
        targets = []
        for _ in range(self.range):
            target_pool = list(filter(lambda t: t not in targets,
                                      self.get_targets(self.source, Enemies())
                                      ))
            if not target_pool:
                continue
            target = random.choice(target_pool)
            aflame = target.get_skill('aflame')
            aflame.add_flame(self.source, 1)
            targets.append(target)
        self.source.energy = max(self.source.energy - 2, 0)
        self.source.session.say(f'🍸|{self.source.name} кидает коктейль молотова! '
                                f'{",".join([t.name for t in targets])} в огне!')

    @property
    def blocked(self):
        return self.source.energy < 2
