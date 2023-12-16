from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.WeaponAction import MeleeAttack
from core.Context import EventContext
from core.Decorators import Nearest
from core.Events.EventManager import event_manager
from core.Events.Events import PreDamagesGameEvent
from core.Weapons.Weapon import MeleeWeapon


class Knuckles(MeleeWeapon):
    id = 'knuckles'
    name = 'Кастет'
    description = 'Ближний бой, урон 1-3, точность высокая. Атакуя перезаряжающегося врага, вы снимаете ему 4 энергии.'

    cubes = 3
    accuracy_bonus = 2
    energy_cost = 2
    damage_bonus = 0


@AttachedAction(Knuckles)
class KnucklesAttack(MeleeAttack):
    priority = -1

    def func(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        for action in action_manager.get_queued_entity_actions(self.session, target):
            if action.id == 'reload':
                @Nearest(self.session.id, event=PreDamagesGameEvent)
                def pre_damages(context: EventContext[PreDamagesGameEvent]):
                    self.session.say(f'⚡️|{target.name} теряет 4 енергии!')
                    target.energy = max(target.energy - 4, 0)

        return damage
