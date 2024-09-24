from VegansDeluxe.core import AttachedAction, RegisterWeapon
from VegansDeluxe.core import DecisiveWeaponAction, RangedAttack
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import Entity
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import PreMoveGameEvent
from VegansDeluxe.core import RegisterEvent
from VegansDeluxe.core import Session
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon


@RegisterWeapon
class Rifle(RangedWeapon):
    id = 'sniper_rifle'
    name = ls("rebuild.weapon.sniper_rifle.name")
    description = ls("rebuild.weapon.sniper_rifle.description")

    cubes = 1
    accuracy_bonus = -4
    energy_cost = 5
    damage_bonus = 7

    def __init__(self, session_id: str, entity_id: str):
        super().__init__(session_id, entity_id)
        self.main_target = None, 0

        @RegisterEvent(session_id=session_id, event=PreMoveGameEvent)
        async def pre_move(context: EventContext[PreMoveGameEvent]):
            entity = context.session.get_entity(entity_id)
            main_target, level = self.main_target
            if main_target:
                main_target: Entity

                chance = self.hit_chance(entity)
                if level == 1:
                    chance += 60
                elif level == 2:
                    chance += 90

                entity.notifications.append(
                    ls("rebuild.weapon.sniper_rifle.notification").format(main_target.name, chance)
                )


@AttachedAction(Rifle)
class RifleAttack(RangedAttack):
    def __init__(self, session: Session, source: Entity, weapon: Rifle):
        super().__init__(session, source, weapon)
        self.weapon: Rifle = weapon

    def calculate_damage(self, source, target):
        main_target, level = self.weapon.main_target
        if main_target == target:
            self.weapon.accuracy_bonus = 2 if level == 1 else 5
        else:
            self.weapon.accuracy_bonus = -4
        return super().calculate_damage(source, target)

    async def func(self, source, target):
        damage = (await super().attack(source, target)).dealt
        self.weapon.main_target = None, 0
        return damage


@AttachedAction(Rifle)
class AimRifle(DecisiveWeaponAction):
    id = 'aim_rifle'
    name = ls("rebuild.weapon.sniper_rifle.action.name")
    target_type = Enemies()

    def __init__(self, session: Session, source: Entity, weapon: Rifle):
        super().__init__(session, source, weapon)
        self.weapon: Rifle = weapon

    async def func(self, source, target):
        main_target, level = self.weapon.main_target
        self.weapon.main_target = target, min(2, level + 1)
        self.session.say(ls("rebuild.weapon.sniper_rifle.action.text").format(source.name))
