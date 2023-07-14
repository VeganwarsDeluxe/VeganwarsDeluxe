from core.Actions.ActionManager import AttachedAction
from core.Actions.ItemAction import DecisiveItem
from core.Events.DamageEvents import PostDamageGameEvent
from core.Events.EventManager import event_manager
from core.Items.Item import Item
from core.TargetType import Allies


class Shield(Item):
    id = 'shield'
    name = 'Щит'


@AttachedAction(Shield)
class ShieldAction(DecisiveItem):
    id = 'shield'
    name = 'Щит'
    target_type = Allies()
    priority = -2

    def func(self, source, target):
        if target == source:
            self.session.say(f"🔵|{source.name} использует щит. Урон отражен!")
        else:
            self.session.say(f"🔵|{source.name} использует щит на {target.name}. Урон отражен!")

        @event_manager.now(self.session.id, event=PostDamageGameEvent)
        def shield_block(event: PostDamageGameEvent):
            if event.target != target:
                return
            if not event.damage:
                return
            self.session.say(f"🔵|Щит {source.name} заблокировал весь урон!")
            event.damage = 0
