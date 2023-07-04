import random

from core.Actions.ActionManager import AttachedAction
from core.Items.Item import Item
from core.Actions.ItemAction import FreeItem
from core.Events.Events import PostActionsGameEvent
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

        @self.session.event_manager.now(self.session.id, event=PostActionsGameEvent)
        def serum_attack(message: PostActionsGameEvent):
            if target.dead:
                return
            attack = target.get_action('attack', default=True)
            attack.target = random.choice(attack.targets) if attack.targets else target
            attack()
