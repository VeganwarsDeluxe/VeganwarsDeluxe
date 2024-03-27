import random

from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import Nearest
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import PostActionsGameEvent
from VegansDeluxe.core import Item
from VegansDeluxe.core import Everyone
from VegansDeluxe.core.Translator.LocalizedString import ls


@RegisterItem
class RageSerum(Item):
    id = 'rage-serum'
    name = ls("item_rage_serum_name")


@AttachedAction(RageSerum)
class RageSerumAction(FreeItem):
    id = 'rage-serum'
    name = ls("item_rage_serum_name")
    target_type = Everyone()

    def func(self, source, target):
        self.session.say(
            ls("item_rage_serum_text").format(source.name, target.name)
        )

        @Nearest(self.session.id, event=PostActionsGameEvent)
        def serum_attack(context: EventContext[PostActionsGameEvent]):
            if target.dead:
                return

            attack = context.action_manager.get_action(self.session, target, 'attack')
            # TODO: Wrong way to do it. Add types for actions.

            if not attack:
                self.session.say(ls("item_rage_serum_sneeze").format(target.name))
                return
            attack.target = random.choice(attack.targets) if attack.targets else target
            attack()
