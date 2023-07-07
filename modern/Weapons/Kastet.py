from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon, MeleeWeapon


class Kastet(MeleeWeapon):
    id = 'kastet'
    name = 'Кастет'
    description = 'Ближний бой, урон 1-3, точность высокая. Атакуя перезаряжающегося врага, вы снимаете ему 4 энергии.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0


@AttachedAction(Kastet)
class KastetAttack(Attack):
    priority = -1

    def attack(self, source, target):
        damage = super().attack(source, target)
        if target.action.id == 'reloading':
            self.session.say(f'⚡️|{target.name} теряет 4 енергии!')
            target.energy = max(target.energy - 4, 0)
        return damage
