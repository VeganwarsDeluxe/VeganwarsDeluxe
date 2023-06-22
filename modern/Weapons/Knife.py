from core.Weapons.Weapon import Weapon


class Knife(Weapon):
    id = 3
    description = 'Ближний бой, урон 1-3, точность высокая. Каждый удар накладывает кровотечение на цель.'

    def __init__(self, owner):
        super().__init__(owner)
        self.accuracybonus = 2
        self.cubes = 3

        self.name = 'Нож'

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        bleeding = target.get_skill('bleeding')
        source.session.say(f'{target.name} истекает кровью!')
        bleeding.active = True
        return damage

