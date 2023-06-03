from core.Weapons.Weapon import Weapon


class Knife(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 3
        self.name = 'Нож'
        self.accuracybonus = 2
        self.cubes = 3

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        bleeding = target.get_skill('bleeding')
        source.session.say(f'{target.name} истекает кровью!')
        bleeding.active = True
        return damage

