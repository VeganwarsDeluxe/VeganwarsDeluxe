from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon
from VegansDeluxe.rebuild import Aflame


@RegisterWeapon
class Bow(RangedWeapon):
    id = 'bow'
    name = ls("rebuild.weapon.bow.name")
    description = ls("rebuild.weapon.bow.description")

    cubes = 3
    accuracy_bonus = 1
    energy_cost = 3
    damage_bonus = 0

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.cooldown_turn = 0


@AttachedAction(Bow)
class BowAttack(RangedAttack):
    pass


@AttachedAction(Bow)
class FireArrow(RangedAttack):
    id = 'fire_arrow'
    name = ls("rebuild.weapon.bow.fire_arrow.name")
    target_type = Enemies()

    @property
    def hidden(self) -> bool:
        return self.session.turn < self.weapon.cooldown_turn

    async def func(self, source, target):
        self.weapon.cooldown_turn = self.session.turn + 5
        damage = self.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energy_cost, 0)
        if not damage:
            self.session.say(
                ls("rebuild.weapon.bow.fire_arrow_miss")
                .format(source.name, target.name)
            )
            return
        self.session.say(
            ls("rebuild.weapon.bow.fire_arrow.text")
            .format(source.name, target.name)
        )
        aflame = target.get_state(Aflame)
        aflame.add_flame(self.session, target, source, 2)
