from core.ContentManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon


class Knife(MeleeWeapon):
    id = 'knife'
    name = 'Нож'
    description = 'Ближний бой, урон 1-3, точность высокая. Каждый удар накладывает кровотечение на цель.'

    accuracy_bonus = 2
    cubes = 3


@AttachedAction(Knife)
class KnifeAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        bleeding = target.get_skill('bleeding')
        if bleeding.active:
            bleeding.bleeding -= 1
            self.session.say(f"🩸|Кровотечение усиливается!")
        else:
            self.session.say(f'🩸|{target.name} истекает кровью!')
        bleeding.active = True
        return damage
