from VegansDeluxe.core import Allies, PreDamagesGameEvent
from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Item
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class Stimulator(Item):
    id = 'stimulator'
    name = ls("rebuild.item.stimulator.name")


@AttachedAction(Stimulator)
class StimulatorAction(DecisiveItem):
    id = 'stimulator'
    name = ls("rebuild.item.stimulator.name")
    target_type = Allies()
    priority = -2

    tags = DecisiveItem.tags + [ActionTag.MEDICINE]

    async def func(self, source, target):
        target.hp = min(target.hp + 2, target.max_hp)
        message = "rebuild.item.stimulator.text_self" if source.id == target.id \
            else "rebuild.item.stimulator.text"
        self.session.say(ls(message).format(source.name, target.name),
                         source_id=source.id, target_id=target.id)
        self.session.say(ls("rebuild.item.stimulator.effect").format(target.hearts, target.name, target.hp),
                         source_id=source.id, target_id=target.id, at_next_event=PreDamagesGameEvent)
