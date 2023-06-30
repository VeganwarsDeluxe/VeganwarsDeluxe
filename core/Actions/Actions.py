from core.Actions.Action import DecisiveAction
from core.TargetType import OwnOnly


class ApproachAction(DecisiveAction):
    id = 'approach'
    name = 'Подойти'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, source.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        source.session.say(f'👣|{source.name} подходит к противнику вплотную.')


class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.energy = source.max_energy
        source.session.say(source.weapon.reload_text(source))


class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'

    def __init__(self, source):
        super().__init__(source, OwnOnly())

    def func(self, source, target):
        source.session.say(f"⬇|{source.name} пропускает ход.")
