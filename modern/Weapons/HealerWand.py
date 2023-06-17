from core.Action import DecisiveAction
from core.TargetType import TargetType
from core.Weapons.Weapon import Weapon


class HealerWand(Weapon):
    def __init__(self, owner):
        super().__init__(owner)
        self.id = 145
        self.cubes = 3
        self.accuracybonus = 2
        self.energycost = 2
        self.dmgbonus = -7
        self.ranged = True

        self.name = "Исцелитель"
        self.description = 'Дальний бой. Исцеляющий лазер!'

    @property
    def actions(self):
        return [
            DecisiveAction(self.attack, self.owner,
                           target_type=TargetType(own=0), name='Атака', id='attack')
        ]

    def attack_text(self, source, target, damage):
        attack_text = 'стреляет в'
        attack_emoji = '🟢'
        if damage:
            source.session.say(f'{attack_emoji}|{source.name} {attack_text} {target.name} используя {self.name}! '
                               f'Нанесено {damage} урона.')
        else:
            source.session.say(f'💨|{source.name} {attack_text} {target.name} используя {self.name}, но не попадает.')