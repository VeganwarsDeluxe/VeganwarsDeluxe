from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon, MeleeWeapon


class Police(MeleeWeapon):
    id = 'policebat'
    name = 'Полицейская дубинка'
    description = 'Ближний бой, урон 1-3, точность высокая. Каждая атака отнимает у цели 1 энергии.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0


@AttachedAction(Police)
class PoliceAttack(Attack):
    priority = -1

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        target.energy = max(target.energy - 1, 0)
        self.session.say(f'⚡️|{target.name} теряет 1 енергию!')
        return damage
