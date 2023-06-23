from core.Items.Item import DecisiveItem
import random

from core.TargetType import Enemies


class Grenade(DecisiveItem):
    def __init__(self, source):
        super().__init__(source, name='Граната', id='grenade', target_type=Enemies())

        self.damage = 3
        self.range = 2

    def use(self):
        damage = self.damage
        targets = []
        for _ in range(self.range):
            target_pool = list(filter(lambda t: t not in targets,
                                      self.get_targets(self.source, Enemies())
                                      ))
            if not target_pool:
                continue
            target = random.choice(target_pool)
            target.inbound_dmg.add(self.source, damage)
            self.source.outbound_dmg.add(self.source, damage)
            targets.append(target)
        self.source.energy = max(self.source.energy - 2, 0)
        self.source.session.say(f'💣|{self.source.name} кидает гранату! Нанесено {damage} урона следующим целям: '
                                f'{",".join([t.name for t in targets])}.')

    @property
    def blocked(self):
        return self.source.energy < 2
