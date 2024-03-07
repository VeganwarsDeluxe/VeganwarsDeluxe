from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
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
        bleeding = target.get_state('bleeding')
        if bleeding.active:
            bleeding.bleeding -= 1
            self.session.say(f"🩸|Кровотечение усиливается!")
        else:
            self.session.say(f'🩸|{target.name} истекает кровью!')
        bleeding.active = True
        return damage
