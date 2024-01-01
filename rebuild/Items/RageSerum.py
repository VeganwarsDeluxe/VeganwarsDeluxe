import random

from core.ContentManager import AttachedAction, content_manager
from core.Actions.ItemAction import DecisiveItem, FreeItem
from core.Context import EventContext
from core.ContentManager import Nearest

from core.Events.Events import PostActionsGameEvent
from core.Items.Item import Item
from core.TargetType import Everyone


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
            attack = action_manager.get_action(self.session, target, 'attack')
            if not attack:
                self.session.say(f'💉|{target.name} чихает.')
                return
            attack.target = random.choice(attack.targets) if attack.targets else target
            attack()
