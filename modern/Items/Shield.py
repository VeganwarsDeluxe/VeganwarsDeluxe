from core.Actions.ActionManager import AttachedAction
from core.Items.Item import Item
from core.Actions.ItemAction import DecisiveItem
from core.Events.Events import PostAttackGameEvent
from core.TargetType import Allies


class Shield(Item):
    id = 'shield'
    name = 'Щит'


@AttachedAction(Shield)
class ShieldAction(DecisiveItem):
    id = 'shield'
    name = 'Щит'
    target_type = Allies()

    def func(self, source, target):
        if target == source:
            self.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            self.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @self.session.event_manager.at(self.session.id, turn=self.session.turn, event=PostAttackGameEvent)
        def shield_block(event: PostAttackGameEvent):
            if event.target != target:
                return
            event.damage = 0
