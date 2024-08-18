from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Fist(MeleeWeapon):
    id = 'fist'
    name = ls("weapon_fist_name")
    description = ls("weapon_fist_description")

    accuracy_bonus = 2


@AttachedAction(Fist)
class FistAttack(MeleeAttack):
    pass
