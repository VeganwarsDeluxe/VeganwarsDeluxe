import random

import rebuild
from core.Actions.Action import Action, DecisiveAction
from core.Actions.ActionManager import action_manager, AttachedAction
from core.Actions.EntityActions import SkipActionGameEvent
from core.Events.EventManager import event_manager
from core.TargetType import Allies, Enemies, OwnOnly
from core.Weapons import Weapon
from core.utils import percentage_change
from deluxe.game.Entities.Dummy import Dummy


class Rat(Dummy):
    def __init__(self, session_id: str, name='Крыса|🐭'):
        super().__init__(session_id, name=name)

        self.hp = 4
        self.max_hp = 4
        self.energy = 5
        self.max_energy = 5

        self.items = []

        for _ in range(2):
            self.skills.append(random.choice(rebuild.all_skills)())

        self.weapon: Weapon = random.choice(rebuild.all_weapons)(session_id, self.id)

        self.team = None

    def choose_act(self, session):
        super().choose_act(session)
        if session.turn == 1:
            self.first_turn(session)
        else:
            session.say(f"🚬|{self.name} курит и не знает что делать.")

    def first_turn(self, session):
        base_action = Action(session, self)
        enemies = base_action.get_targets(self, Enemies())

        target = random.choice(enemies)

        if self.weapon.melee and target.weapon.melee:
            if percentage_change(40) and 'thief' in [s.id for s in self.skills]:
                self.use_thief(session, target)
            else:
                if percentage_change(50):
                    self.approach(session)
                else:
                    self.throw_something(session, target)

        elif self.weapon.ranged and target.weapon.melee:
            if percentage_change(80) or 'thief' not in [s.id for s in self.skills]:
                if percentage_change(50) and 'adrenaline' in [i.id for i in self.items]:
                    action = action_manager.get_action(session, self, "adrenaline")
                    action.target = self
                    action_manager.queue_action_instance(action)
                self.attack(session, target)
            else:
                self.use_thief(session, target)

        elif self.weapon.melee and target.weapon.ranged:
            if percentage_change(60):
                self.evade(self)
            else:
                self.approach(session)

        elif self.weapon.ranged and target.weapon.ranged:
            if percentage_change(80):
                self.attack(session, target)
            else:
                self.evade(self)

    def evade(self, session):
        if 'thief' not in [s.id for s in self.skills]:
            pass

    def throw_something(self, session, target):
        for item in self.items:
            if item.id in ['grenade', 'molotov', 'throwingknife']:
                action = action_manager.get_action(session, self, item.id)
                action.target = target
                action_manager.queue_action_instance(action)
                return True

    def approach(self, session):
        action = action_manager.get_action(session, self, "approach")
        action_manager.queue_action_instance(action)

    def attack(self, session, target):
        action = action_manager.get_action(session, self, "attack")
        action.target = target
        action_manager.queue_action_instance(action)

    def use_thief(self, session, target):
        action = action_manager.get_action(session, self, "steal")
        action.target = target
        action_manager.queue_action_instance(action)


@AttachedAction(Rat)
class ApproachAction(DecisiveAction):
    id = 'approach'
    name = 'Подойти'
    target_type = OwnOnly()

    @property
    def hidden(self) -> bool:
        return self.source.nearby_entities == list(filter(lambda t: t != self.source, self.session.entities))

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, self.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        self.session.say(f'👣|{source.name} подходит к противнику вплотную.')


@AttachedAction(Rat)
class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'
    target_type = OwnOnly()

    def func(self, source, target):
        source.energy = source.max_energy
        self.session.say(source.weapon.reload_text(source))


@AttachedAction(Rat)
class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'
    target_type = OwnOnly()
    priority = 2

    def func(self, source, target):
        message = event_manager.publish(SkipActionGameEvent(self.session.id, self.session.turn, source.id))
        if not message.no_text:
            self.session.say(f"⬇|{source.name} пропускает ход.")
