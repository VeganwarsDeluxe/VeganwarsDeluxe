from typing import Optional

from VegansDeluxe.core.Actions.Action import Action, FreeAction, DecisiveAction, InstantAction
from VegansDeluxe.core.Actions.ActionTags import ActionTag
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Events.DamageEvents import PostAttackGameEvent, AttackGameEvent
from VegansDeluxe.core.Events.Events import EnergyPaymentEvent
from VegansDeluxe.core.Session import Session
from VegansDeluxe.core.TargetType import Enemies, Distance
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons import Weapon
from VegansDeluxe.core.utils import per_cubes


class DamageData:
    def __init__(self, calculated: int, displayed: int, dealt: int):
        self.calculated = calculated
        self.displayed = displayed
        self.dealt = dealt

    def __int__(self):
        return self.dealt


class WeaponAction[T: Weapon](Action):
    def __init__(self, session: Session, source: Entity, weapon: T):
        super().__init__(session, source)
        self.weapon: T = weapon


class InstantWeaponAction(WeaponAction, InstantAction):
    pass

class FreeWeaponAction(WeaponAction, FreeAction):
    pass


class DecisiveWeaponAction(WeaponAction, DecisiveAction):
    pass


class Attack(DecisiveWeaponAction):
    id = 'attack'
    name = ls("core.base_attack.name")
    target_type = Enemies()
    priority = 0

    tags = DecisiveWeaponAction.tags + [ActionTag.HARMFUL, ActionTag.ATTACK]

    def __init__(self, *args):
        super().__init__(*args)

        self.ATTACK_TEXT = ls("core.base_attack.text_ranged") \
            if self.weapon.ranged else ls("core.base_attack.text_melee")
        self.ATTACK_EMOJI = ls("core.base_attack.emoji_ranged") \
            if self.weapon.ranged else ls("core.base_attack.emoji_melee")
        self.ATTACK_MESSAGE = ls("core.base_attack.hit")
        self.MISS_MESSAGE = ls("core.base_attack.miss")
        self.SELF_TARGET_NAME = ls("core.self_target_name")

    async def func(self, source, target):
        return await self.attack(source, target)

    def calculate_damage(self, source: Entity, target: Entity, energy: Optional[int] = None) -> int:
        """
        Calculate the damage based on weapon's damage bonus and accuracy.
        """
        if energy is None:
            energy = source.energy
        if energy <= 0:
            return 0
        damage = per_cubes(self.weapon.cubes, self.weapon.accuracy_bonus,
                           energy, target.inbound_accuracy_bonus + source.outbound_accuracy_bonus)
        return damage + self.weapon.damage_bonus if damage else 0

    async def attack(self, source, target, pay_energy=True,
                     bonus_damage: int = 0, send_message: bool = True) -> DamageData:
        """
        Actually performs attack on target, dealing damage. Bonus damage is added (and displayed) if there's no miss.
        """
        calculated_damage = self.calculate_damage(source, target)
        if calculated_damage:
            calculated_damage += bonus_damage
        if pay_energy:
            energy_payment_event = await self.publish_energy_payment_event(source, self.weapon.energy_cost)
            source.energy = max(source.energy - energy_payment_event.energy_payment, 0)

        displayed_damage_message = await self.publish_attack_event(source, target, calculated_damage)
        if send_message:
            self.send_attack_message(source, target, displayed_damage_message.damage)
        dealt_damage = await self.publish_post_attack_event(source, target, displayed_damage_message.damage)

        target.inbound_dmg.add(source, dealt_damage.damage, self.session.turn)
        source.outbound_dmg.add(target, dealt_damage.damage, self.session.turn)
        return DamageData(calculated_damage, displayed_damage_message.damage, dealt_damage.damage)

    async def publish_energy_payment_event(self, source, energy_cost) -> EnergyPaymentEvent:
        message = EnergyPaymentEvent(self.session.id, self.session.turn, source.id, energy_payment=energy_cost)
        await self.event_manager.publish(message)
        return message

    async def publish_attack_event(self, source, target, damage) -> AttackGameEvent:
        message = AttackGameEvent(self.session.id, self.session.turn, source, target, damage)
        await self.event_manager.publish(message)  # 7.1 Pre-Attack stage
        return message

    async def publish_post_attack_event(self, source, target, damage) -> PostAttackGameEvent:
        message = PostAttackGameEvent(self.session.id, self.session.turn, source, target, damage)
        await self.event_manager.publish(message)  # 7.2 Post-Attack stage
        return message

    def send_attack_message(self, source: Entity, target: Entity, damage: int):
        target_name = self.SELF_TARGET_NAME if source == target else target.name
        if damage:
            message = self.ATTACK_MESSAGE.format(attack_emoji=self.ATTACK_EMOJI, source_name=source.name,
                                                 attack_text=self.ATTACK_TEXT,
                                                 target_name=target_name, weapon_name=self.weapon.name, damage=damage)
        else:
            message = self.MISS_MESSAGE.format(source_name=source.name, attack_text=self.ATTACK_TEXT,
                                               target_name=target_name,
                                               weapon_name=self.weapon.name)
        self.session.say(message)


class MeleeAttack(Attack):
    target_type = Enemies(distance=Distance.NEARBY_ONLY)


class RangedAttack(MeleeAttack):
    target_type = Enemies(distance=Distance.ANY)
