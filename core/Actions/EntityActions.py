from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import action_manager, AttachedAction
from core.Entities import Entity
from core.TargetType import OwnOnly


@AttachedAction(Entity)
class ApproachAction(DecisiveAction):
    id = 'approach'
    name = 'Подойти'
    target_type = OwnOnly()

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, self.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        self.session.say(f'👣|{source.name} подходит к противнику вплотную.')


@AttachedAction(Entity)
class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'
    target_type = OwnOnly()

    def func(self, source, target):
        source.energy = source.max_energy
        self.session.say(source.weapon.reload_text(source))


@AttachedAction(Entity)
class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'
    target_type = OwnOnly()
    priority = 2

    def func(self, source, target):
        self.session.say(f"⬇|{source.name} пропускает ход.")
