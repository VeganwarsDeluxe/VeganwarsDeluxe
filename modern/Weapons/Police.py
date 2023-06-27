from core.Weapons.Weapon import Weapon


class Police(Weapon):
    id = 'policebat'
    name = 'Полицейская дубинка'
    description = 'Ближний бой, урон 1-3, точность высокая. Каждая атака отнимает у цели 1 энергии.'

    def __init__(self, owner):
        super().__init__(owner)
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = 0

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        target.energy = max(target.energy-1, 0)
        source.session.say(f'⚡️|{target.name} теряет 1 енергию!')
        return damage

