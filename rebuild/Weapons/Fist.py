from core.Actions.ActionManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon


class Fist(MeleeWeapon):
    id = 'fist'
    name = 'Кулаки'
    description = 'Ближний бой. Оружие для настоящих боев!'

    def __init__(self):
        super().__init__()
        self.accuracy_bonus = 2


@AttachedAction(Fist)
class FistAttack(MeleeAttack):
    pass
