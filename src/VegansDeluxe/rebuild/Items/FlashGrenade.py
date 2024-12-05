from VegansDeluxe.core import AttachedAction, RegisterItem, ActionTag, GameEvent
from VegansDeluxe.core import DecisiveItem
from VegansDeluxe.core import Enemies
from VegansDeluxe.core import Item
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class FlashGrenade(Item):
    id = 'flash_grenade'
    name = ls("rebuild.item.flash_grenade.name")


@AttachedAction(FlashGrenade)
class FlashGrenadeAction(DecisiveItem):
    id = 'flash_grenade'
    name = ls("rebuild.item.flash_grenade.name")
    target_type = Enemies()
    priority = -2

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.HARMFUL]

    async def func(self, source, target):
        flash_grenade_attempt = FlashGrenadeAttemptEvent(self.session.id, self.session.turn, target,
                                                         True, 8)
        await self.session.event_manager.publish(flash_grenade_attempt)

        target.energy = max(0, target.energy - flash_grenade_attempt.energy_lost)
        if flash_grenade_attempt.success:
            self.session.say(ls("rebuild.item.flash_grenade.text").format(self.source.name, target.name))
        else:
            self.session.say(ls("rebuild.item.flash_grenade.fail").format(
                self.source.name, target.name, flash_grenade_attempt.energy_lost))


class FlashGrenadeAttemptEvent(GameEvent):
    def __init__(self, session_id, turn, target, success, energy_lost):
        super().__init__(session_id, turn)
        self.target = target
        self.success = success
        self.energy_lost = energy_lost
