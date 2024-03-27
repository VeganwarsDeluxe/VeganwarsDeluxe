import random

from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import MeleeAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import MeleeWeapon


@RegisterWeapon
class Torch(MeleeWeapon):
    id = 'torch'
    name = ls("weapon_torch_name")
    description = ls("weapon_torch_description")

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.accuracy_bonus = 2
        self.cubes = 3


@AttachedAction(Torch)
class TorchAttack(MeleeAttack):
    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        if random.randint(0, 100) > 50:
            aflame = target.get_state('aflame')
            aflame.add_flame(self.session, target, source, 1)
        return damage
