from core.ContentManager import AttachedAction, RegisterWeapon
from core.Actions.WeaponAction import MeleeAttack
from core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Fist(MeleeWeapon):
    id = 'fist'
    name = 'Кулаки'
    description = 'Ближний бой. Оружие для настоящих боев!'

    accuracy_bonus = 2


@AttachedAction(Fist)
class FistAttack(MeleeAttack):
    pass
