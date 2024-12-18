import random

from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import Everyone
from VegansDeluxe.core import FreeItem, ActionTag
from VegansDeluxe.core import Item
from VegansDeluxe.core import Next
from VegansDeluxe.core import PostActionsGameEvent
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class RageSerum(Item):
    id = 'rage-serum'
    name = ls("rebuild.item.rage_serum.name")


@AttachedAction(RageSerum)
class RageSerumAction(FreeItem):
    id = 'rage-serum'
    name = ls("rebuild.item.rage_serum.name")
    target_type = Everyone()

    def __init__(self, *args):
        super().__init__(*args)

        self.tags += [ActionTag.MEDICINE]

    async def func(self, source, target):
        self.session.say(
            ls("rebuild.item.rage_serum.text").format(source.name, target.name)
        )

        @Next(self.session.id, event=PostActionsGameEvent)
        async def serum_attack(context: EventContext[PostActionsGameEvent]):
            if target.dead:
                return

            attack = None

            for action in context.action_manager.get_actions(self.session, target):
                if ActionTag.ATTACK in action.tags:
                    attack = action
                    break

            if not attack:
                self.session.say(ls("rebuild.item.rage_serum.sneeze").format(target.name))
                return
            attack.target = random.choice(attack.targets) if attack.targets else target
            await attack.execute()
