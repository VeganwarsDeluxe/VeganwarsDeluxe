from core.Actions.Action import DecisiveAction
from core.Actions.ActionManager import action_manager
from core.Entities import Entity


@action_manager.register(Entity)
class ApproachAction(DecisiveAction):
    id = 'approach'
    name = 'Подойти'

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, self.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        self.session.say(f'👣|{source.name} подходит к противнику вплотную.')


@action_manager.register(Entity)
class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'

    def func(self, source, target):
        source.energy = source.max_energy
        self.session.say(source.weapon.reload_text(source))


@action_manager.register(Entity)
class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'

    def func(self, source, target):
        self.session.say(f"⬇|{source.name} пропускает ход.")
