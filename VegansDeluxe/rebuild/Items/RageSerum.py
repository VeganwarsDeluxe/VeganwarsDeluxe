import random

from VegansDeluxe.core import FreeItem
from VegansDeluxe.core import AttachedAction, RegisterItem
from VegansDeluxe.core import Nearest
from VegansDeluxe.core import EventContext
from VegansDeluxe.core import PostActionsGameEvent
from VegansDeluxe.core import Item
from VegansDeluxe.core import Everyone


@RegisterItem
class RageSerum(Item):
    id = 'rage-serum'
    name = 'Сыворотка бешенства'


@AttachedAction(RageSerum)
class RageSerumAction(FreeItem):
    id = 'rage-serum'
    name = 'Сыворотка бешенства'
    target_type = Everyone()

    def func(self, source, target):
        self.session.say(f"💉|{source.name} использует сыворотку бешенства на {target.name}!")

        @Nearest(self.session.id, event=PostActionsGameEvent)
        def serum_attack(context: EventContext[PostActionsGameEvent]):
            if target.dead:
                return
            attack = context.action_manager.get_action(self.session, target, 'attack')
            if not attack:
                self.session.say(f'💉|{target.name} чихает.')
                return
            attack.target = random.choice(attack.targets) if attack.targets else target
            attack()
