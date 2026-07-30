from VegansDeluxe.core import AttachedAction, RegisterWeapon, DamageData
from VegansDeluxe.core import RangedAttack
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.core.Weapons.Weapon import RangedWeapon
from VegansDeluxe.rebuild import Aflame


@RegisterWeapon
class Flamethrower(RangedWeapon):
    id = 'flamethrower'
    name = ls("rebuild.weapon.flamethrower.name")
    description = ls("rebuild.weapon.flamethrower.description")

    energy_cost = 3
    cubes = 2
    accuracy_bonus = 2


@AttachedAction(Flamethrower)
class FlamethrowerAttack(RangedAttack):
    def calculate_damage(self, *args):
        damage = super().calculate_damage(*args)
        if damage:
            return 1

    async def attack(self, source, target, pay_energy=True,
                     bonus_damage: int = 0, send_message: bool = True) -> DamageData:
        """
        Actually performs attack on target, dealing damage. Bonus damage is added (and displayed) if there's no miss.
        """
        calculated_damage = self.calculate_damage(source, target)
        if calculated_damage:
            calculated_damage += bonus_damage

            aflame = target.get_state(Aflame)
            aflame.add_flame(self.session, target, source, 1)

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
