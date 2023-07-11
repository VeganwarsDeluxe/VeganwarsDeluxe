from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon, MeleeWeapon


class Knife(MeleeWeapon):
    id = 'knife'
    name = 'Нож'
    description = 'Ближний бой, урон 1-3, точность высокая. Каждый удар накладывает кровотечение на цель.'

    def __init__(self):
        super().__init__()
        self.accuracy_bonus = 2
        self.cubes = 3


@AttachedAction(Knife)
class KnifeAttack(Attack):
    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        bleeding = target.get_skill('bleeding')
        self.session.say(f'{target.name} истекает кровью!')
        bleeding.active = True
        return damage
