from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import Attack
from core.Weapons.Weapon import Weapon


class Fist(Weapon):
    id = 'fist'
    name = 'Кулаки'
    description = 'Ближний бой. Оружие для настоящих боев!'

    def __init__(self):
        super().__init__()
        self.accuracy_bonus = 2


@AttachedAction(Fist)
class FistAttack(Attack):
    pass
