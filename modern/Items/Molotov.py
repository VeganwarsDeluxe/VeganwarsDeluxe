from core.Items.Item import DecisiveItem
import random

from core.TargetType import Enemies


class Molotov(DecisiveItem):
    def __init__(self):
        super().__init__(name='Коктейль Молотова', id='molotov')

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
            aflame.flame += 1
            targets.append(target)

        self.source.session.say(f'🍸|{self.source.name} кидает коктейль молотова! '
                                f'{",".join([t.name for t in targets])} в огне!')
