from core.ContentManager import AttachedAction
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon


class Fist(MeleeWeapon):
    id = 'fist'
    name = 'Кулаки'
    description = 'Ближний бой. Оружие для настоящих боев!'

    accuracy_bonus = 2


@AttachedAction(Fist)
class FistAttack(MeleeAttack):
    pass
