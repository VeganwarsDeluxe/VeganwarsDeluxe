import random
from core.Weapons.Weapon import Weapon


class Kastet(Weapon):
    id = 'kastet'
    name = 'Кастет'
    description = 'Ближний бой, урон 1-3, точность высокая. Атакуя перезаряжающегося врага, вы снимаете ему 4 энергии.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

    def attack(self, source, target):
        damage = super().attack(source, target)
        if target.action.id == 'reloading':
            source.session.say(f'⚡️|{target.name} теряет 4 енергии!')
            target.energy = max(target.energy-4, 0)
        return damage
