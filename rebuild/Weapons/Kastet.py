from core.Actions.ActionManager import AttachedAction, action_manager
from core.Actions.WeaponAction import MeleeAttack
from core.Events.EventManager import event_manager
from core.Events.Events import PreDamagesGameEvent
from core.Weapons.Weapon import MeleeWeapon


class Kastet(MeleeWeapon):
    id = 'kastet'
    name = 'Кастет'
    description = 'Ближний бой, урон 1-3, точность высокая. Атакуя перезаряжающегося врага, вы снимаете ему 4 энергии.'

    def __init__(self):
        super().__init__()
        self.cubes = 3
        self.accuracy_bonus = 2
        self.energy_cost = 2
        self.damage_bonus = 0


@AttachedAction(Kastet)
class KastetAttack(MeleeAttack):
    priority = -1

    def attack(self, source, target):
        damage = super().attack(source, target)
        if not damage:
            return damage
        for action in action_manager.get_queued_entity_actions(self.session, target):
            if action.id == 'reload':
                @event_manager.nearest(self.session.id, event=PreDamagesGameEvent)
                def pre_damages(event):
                    self.session.say(f'⚡️|{target.name} теряет 4 енергии!')
                    target.energy = max(target.energy - 4, 0)

        return damage
