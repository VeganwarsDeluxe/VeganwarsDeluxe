from VegansDeluxe.core.Actions.Action import DecisiveAction, FreeAction
from VegansDeluxe.core.Actions.ActionTags import ActionTag
from VegansDeluxe.core.ContentManager import AttachedAction
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Events.Events import GameEvent
from VegansDeluxe.core.TargetType import OwnOnly
from VegansDeluxe.core.Translator.LocalizedString import ls


@AttachedAction(Entity)
class InfoAction(FreeAction):
    id = 'info_action'
    name = ls("core.action.info.name")
    target_type = OwnOnly()

    async def func(self, source, target):
        pass


@AttachedAction(Entity)
class ApproachAction(DecisiveAction):
    id = 'approach'
    name = ls("core.action.approach.name")
    target_type = OwnOnly()

    @property
    def hidden(self) -> bool:
        return self.source.nearby_entities == list(filter(lambda t: t != self.source, self.session.entities))

    async def func(self, source, target):
        source.nearby_entities = list(filter(lambda t: t != source, self.session.entities))
        for entity in source.nearby_entities:
            entity.nearby_entities.append(source) if source not in entity.nearby_entities else None
        self.session.say(ls("core.action.approach.text").format(source.name))


@AttachedAction(Entity)
class ReloadAction(DecisiveAction):
    id = 'reload'
    name = ls("core.action.reload.name")
    target_type = OwnOnly()

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.RELOAD]

    async def func(self, source, target):
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
    name = ls("core.action.skip.name")
    target_type = OwnOnly()
    priority = 2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.SKIP]

    async def func(self, source, target):
        message = SkipActionGameEvent(self.session.id, self.session.turn, source.id)
        await self.event_manager.publish(message)
        if not message.no_text:
            self.session.say(ls("core.action.skip.text").format(source.name))
