from core.Weapons.Weapon import Weapon


class Police(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 29
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

        self.name = 'Полицейская дубинка'
        self.description = 'Ближний бой, урон 1-3, точность высокая. Каждая атака отнимает у цели 1 энергии.'

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        target.energy = max(target.energy-1, 0)
        source.session.say(f'⚡️|{target.name} теряет 1 енергию!')
        return damage

