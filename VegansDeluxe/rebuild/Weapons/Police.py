from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Police(MeleeWeapon):
    id = 'policebat'
    name = 'Полицейская дубинка'
    description = 'Ближний бой, урон 1-3, точность высокая. Каждая атака отнимает у цели 1 энергии.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Police)
class PoliceAttack(MeleeAttack):
    priority = -1

    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        target.energy = max(target.energy - 1, 0)
        self.session.say(f'⚡️|{target.name} теряет 1 енергию!')
        return damage
