from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Enemies
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Bow(RangedWeapon):
    id = 'bow'
    name = ls("weapon_bow_name")
    description = ls("weapon_bow_description")

    cubes = 3
    accuracy_bonus = 1
    energy_cost = 3
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0
        self.strike = False


@AttachedAction(Bow)
class BowAttack(RangedAttack):
    pass


@AttachedAction(Bow)
class FireArrow(RangedAttack):
    id = 'fire_arrow'
    name = ls("weapon_bow_fire_arrow_name")
    target_type = Enemies()

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        damage = self.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energy_cost, 0)
        if not damage:
            self.session.say(
                ls("weapon_bow_fire_arrow_miss")
                .format(source.name, target.name)
            )
            return
        self.session.say(
            ls("weapon_bow_fire_arrow_text")
            .format(source.name, target.name)
        )
        aflame = target.get_state('aflame')
        aflame.add_flame(self.session, target, source, 2)
