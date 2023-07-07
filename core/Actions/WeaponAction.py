import random

from core.Actions.Action import Action
from core.Entities import Entity
from core.Events.Events import PostAttackGameEvent, AttackGameEvent
from core.Sessions import Session
from core.TargetType import Enemies, Distance
from core.Weapons import Weapon


class WeaponAction(Action):
    def __init__(self, session: Session, source: Entity, weapon: Weapon):
        super().__init__(session, source)
        self.weapon = weapon


class FreeWeaponAction(WeaponAction):
    @property
    def cost(self):
        return False


class DecisiveWeaponAction(WeaponAction):
    @property
    def cost(self):
        return True


class Attack(DecisiveWeaponAction):
    id = 'attack'
    name = 'Атака'
    target_type = Enemies()

    def func(self, source, target):
        self.attack(source, target)

    def calculate_damage(self, source: Entity, target: Entity):
        """
        Mostly universal formulas for weapon damage.
        """
        damage = 0
        if source.energy <= 0:
            total_accuracy = 0
        else:
            total_accuracy = source.energy + self.weapon.accuracy_bonus \
                             + target.inbound_accuracy_bonus + source.outbound_accuracy_bonus
        for _ in range(self.weapon.cubes):
            dice_result = random.randint(1, 10)
            if dice_result <= total_accuracy:
                damage += 1
        if not damage:
            return 0  # You missed!
        damage += self.weapon.damage_bonus
        return damage

    def hit_chance(self, source):
        if source.energy <= 0:
            return 0
        total_accuracy = source.energy + self.weapon.accuracy_bonus + source.outbound_accuracy_bonus
        cubes = self.weapon.cubes
        return int(max((1 - ((1 - total_accuracy / 10) ** cubes)) * 100, 0))

    def attack(self, source, target):
        """
        Actually performs attack on target, dealing damage.
        """
        damage = self.calculate_damage(source, target)
        source.energy = max(source.energy - self.weapon.energy_cost, 0)

        message = AttackGameEvent(self.session.id, self.session.turn, source, target, damage)
        self.session.event_manager.publish(message)  # 7.1 Pre-Attack stage
        damage = message.damage

        self.attack_text(source, target, damage)

        message = PostAttackGameEvent(self.session.id, self.session.turn, source, target, damage)
        self.session.event_manager.publish(message)  # 7.2 Post-Attack stage
        damage = message.damage

        target.inbound_dmg.add(source, damage)
        source.outbound_dmg.add(target, damage)
        return damage

    def attack_text(self, source, target, damage):
        attack_text = 'стреляет в' if self.weapon.ranged else 'бьет'
        attack_emoji = '💥' if self.weapon.ranged else '👊'
        if damage:
            self.session.say(
                f'{attack_emoji}|{source.name} {attack_text} {target.name} используя {self.weapon.name}! '
                f'Нанесено {damage} урона.')
        else:
            self.session.say(f'💨|{source.name} {attack_text} {target.name} используя {self.weapon.name}, '
                             f'но не попадает.')

    def reload_text(self, source):
        if self.weapon.ranged:
            tts = f"🕓|{source.name} перезаряжается. " \
                  f"Энергия восстановлена до максимальной! ({source.max_energy})"
        else:
            tts = f"😤|{source.name}️ переводит дух. Энергия восстановлена до максимальной! ({source.max_energy})"
        return tts


class MeleeAttack(Attack):
    target_type = Enemies(distance=Distance.NEARBY_ONLY)


class RangedAttack(Attack):
    target_type = Enemies(distance=Distance.ANY)
