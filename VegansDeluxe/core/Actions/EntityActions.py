from VegansDeluxe.core.Actions.Action import DecisiveAction
from VegansDeluxe.core.ContentManager import AttachedAction
from VegansDeluxe.core.Entities import Entity

from VegansDeluxe.core.Events.Events import GameEvent
from VegansDeluxe.core.TargetType import OwnOnly


@AttachedAction(Entity)
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


@AttachedAction(Entity)
class ReloadAction(DecisiveAction):
    id = 'reload'
    name = 'Перезарядка'
    target_type = OwnOnly()

    def func(self, source, target):
        source.energy = source.max_energy
        self.session.say(source.weapon.reload_text(source))


class SkipActionGameEvent(GameEvent):
    def __init__(self, session_id, turn, entity_id):
        super().__init__(session_id, turn)
        self.entity_id = entity_id
        self.no_text = False


@AttachedAction(Entity)
class SkipTurnAction(DecisiveAction):
    id = 'skip'
    name = 'Пропустить'
    target_type = OwnOnly()
    priority = 2

    def func(self, source, target):
        message = self.event_manager.publish(SkipActionGameEvent(self.session.id, self.session.turn, source.id))
        if not message.no_text:
            self.session.say(f"⬇|{source.name} пропускает ход.")
